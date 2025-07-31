from PySide6.QtCore import QObject, Slot, Signal, QThreadPool
import requests
import os

class ApiHandler(QObject):
    albumsUpdated = Signal("QVariant")
    coverReady = Signal(str, str)
    albumDetailsReceived = Signal(str, str, str, "QVariant")

    def __init__(self, config_handler):
        super().__init__()
        self.config_handler = config_handler
        self.thread_manager = QThreadPool()

    def get_cover_art(self, cover_id: str, album_id: str = None) -> str:
        """
        Fetch cover art from the server.
        :param cover_id: The ID of the cover art to fetch.
        :param album_id: The ID of the album (optional, required for signal to emit).
        :return: The path to the cover art
        """
        cache_dir = os.path.expanduser(os.path.join("~", ".cache", "SubDrome", "covers"))
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        cover_file_path = os.path.join(cache_dir, f"{cover_id}.jpg")
        if os.path.exists(cover_file_path):
            if album_id:
                self.coverReady.emit(album_id, cover_file_path)
            return cover_file_path

        params = {
            "u": self.config_handler.username,
            "t": self.config_handler.token,
            "s": self.config_handler.salt,
            "c": "SubDromeClient",
            "v": "1.0",
            "f": "json",
            "id": cover_id
        }
        try:
            response = requests.get(f"{self.config_handler.server_address}/rest/getCoverArt", params=params)
            if response.status_code == 200:
                try:
                    response.json()  # If this does not raise an exception, the response is valid JSON
                    return ""  # This is not what we want, as it means the cover art was not found
                except ValueError:  # Invalid JSON means we got the image data - this is cursed
                    with open(cover_file_path, "wb") as cover:
                        cover.write(response.content)
                    if album_id:
                        self.coverReady.emit(album_id, cover_file_path)
                    return cover_file_path
        except requests.RequestException:
            pass
        return ""

    @Slot(str)
    def get_albums(self, album_type: str) -> None:
        """
        Fetch random albums from the server.
        :return: A list of random albums or an empty list if the request fails.
        """
        params = {
            "u": self.config_handler.username,
            "t": self.config_handler.token,
            "s": self.config_handler.salt,
            "c": "SubDromeClient",
            "v": "1.0",
            "f": "json",
            "type": album_type,
            "size": 20
        }
        try:
            response = requests.get(f"{self.config_handler.server_address}/rest/getAlbumList2", params=params)
            if response.status_code == 200 and response.json().get("subsonic-response", {}).get("status") == "ok":
                albums = []
                for album in response.json().get("subsonic-response", {}).get("albumList2", {}).get("album", []):
                    cover_id = album.get("coverArt", "")
                    album_id = album.get("id", "")
                    self.thread_manager.start(lambda cid=cover_id, aid=album_id: self.get_cover_art(cid, aid))
                    albums.append([
                        album_id,
                        album.get("name"),
                        album.get("artist"),
                        f"{os.getcwd()}/assets/icons/material/album.svg"
                    ])
                self.albumsUpdated.emit(albums)
        except requests.RequestException:
            pass

    @Slot(str)
    def get_album_details(self, album_id: str) -> dict:
        """
        Fetch details of a specific album from the server.
        :param album_id: The ID of the album to fetch details for.
        :return: A dictionary containing album details or an empty dictionary if the request fails.
        """
        params = {
            "u": self.config_handler.username,
            "t": self.config_handler.token,
            "s": self.config_handler.salt,
            "c": "SubDromeClient",
            "v": "1.0",
            "f": "json",
            "id": album_id
        }
        try:
            response = requests.get(f"{self.config_handler.server_address}/rest/getAlbum", params=params)
            if response.status_code == 200 and response.json().get("subsonic-response", {}).get("status") == "ok":
                album_details = response.json().get("subsonic-response", {}).get("album", {})

                song_list = []
                for song in album_details.get("song", []):
                    song_list.append([
                        song.get("id", ""),
                        song.get("title", ""),
                        song.get("artist", ""),
                        song.get("duration", 0),
                    ])

                cover_art_path = self.get_cover_art(album_details.get("coverArt", ""))
                self.albumDetailsReceived.emit(
                    album_details.get("name"),
                    album_details.get("artist"),
                    cover_art_path,
                    song_list
                )
                return response.json().get("subsonic-response", {}).get("album", {})
        except requests.RequestException:
            pass
        return {}

    def get_song_details(self, song_id: str) -> dict:
        """
        Fetch details of a specific song from the server.
        :param song_id: The ID of the song to fetch details for.
        :return: A dictionary containing song details or an empty dictionary if the request fails.
        """
        params = {
            "u": self.config_handler.username,
            "t": self.config_handler.token,
            "s": self.config_handler.salt,
            "c": "SubDromeClient",
            "v": "1.0",
            "f": "json",
            "id": song_id
        }
        try:
            response = requests.get(f"{self.config_handler.server_address}/rest/getSong", params=params)
            if response.status_code == 200 and response.json().get("subsonic-response", {}).get("status") == "ok":
                return response.json().get("subsonic-response", {}).get("song", {})
        except requests.RequestException:
            pass
        return {}

    def download_song(self, song_id: str) -> str:
        """
        Download a song by its ID.
        :param song_id: The ID of the song to download.
        :return: The path to the downloaded song file.
        """
        params = {
            "u": self.config_handler.username,
            "t": self.config_handler.token,
            "s": self.config_handler.salt,
            "c": "SubDromeClient",
            "v": "1.0",
            "f": "json",
            "id": song_id
        }
        try:
            response = requests.get(f"{self.config_handler.server_address}/rest/download", params=params)
            if response.status_code == 200:
                cache_dir = os.path.expanduser(os.path.join("~", ".cache", "SubDrome", "songs"))
                if not os.path.exists(cache_dir):
                    os.makedirs(cache_dir)
                song_file_path = os.path.join(cache_dir, f"{song_id}.mp3")
                with open(song_file_path, "wb") as song_file:
                    song_file.write(response.content)
                return song_file_path
        except requests.RequestException:
            pass
        return ""
