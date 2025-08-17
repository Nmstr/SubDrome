from PySide6.QtCore import QObject, Slot, Signal, QThreadPool
import requests
import time
import os

class ApiHandler(QObject):
    albumsUpdated = Signal("QVariant")
    coverReady = Signal(str, str)
    albumDetailsReceived = Signal(str, str, str, str, int, str, bool, int, "QVariant")
    playlistListChanged = Signal("QVariant")
    playlistDetailsReceived = Signal(str, str, str, str, int, str, bool, "QVariant")

    def __init__(self, config_handler):
        super().__init__()
        self.config_handler = config_handler
        self.thread_manager = QThreadPool()

    def _send_request(self, endpoint: str, extra_params: dict = None) -> dict:
        """
        Helper method to send a request to the Subsonic server.
        :param endpoint: The API endpoint to call.
        :param extra_params: (optional) Additional parameters for the request.
        :return: The JSON response from the server.
        """
        params = {
            "u": self.config_handler.username,
            "t": self.config_handler.token,
            "s": self.config_handler.salt,
            "c": "SubDromeClient",
            "v": "1.0",
            "f": "json"
        }
        if extra_params:
            params.update(extra_params)
        try:
            response = requests.get(f"{self.config_handler.server_address}/rest/{endpoint}", params=params)
            if response.status_code == 200:
                return response.json().get("subsonic-response", {})
        except requests.RequestException:
            pass
        return {}

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

        # This doesn't use _send_request because the endpoint does not return JSON data
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

    @Slot(str, int)
    def get_albums(self, album_type: str, page: int) -> None:
        """
        Fetch random albums from the server.
        :param album_type: The type of albums to fetch (e.g., "random", "favourite").
        :param page: The page number.
        :return: A list of random albums or an empty list if the request fails.
        """
        extra_params = {
            "type": album_type,
            "size": 20,
            "offset": page * 20 - 20
        }
        response = self._send_request("getAlbumList2", extra_params)
        if response.get("status") == "ok":
            albums = []
            for album in response.get("albumList2", {}).get("album", []):
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

    @Slot(str)
    def get_album_details(self, album_id: str) -> dict:
        """
        Fetch details of a specific album from the server.
        :param album_id: The ID of the album to fetch details for.
        :return: A dictionary containing album details or an empty dictionary if the request fails.
        """
        extra_params = {
            "id": album_id
        }
        response = self._send_request("getAlbum", extra_params)
        if response.get("status") == "ok":
            album_details = response.get("album", {})

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
                album_details.get("id", ""),
                album_details.get("name"),
                album_details.get("artist"),
                cover_art_path,
                album_details.get("songCount", 0),
                time.strftime("%H:%M:%S", time.gmtime(album_details.get("duration", 0))),
                True if album_details.get("starred", False) else False,
                album_details.get("userRating", 0),
                song_list
            )
            return album_details
        return {}

    def get_song_details(self, song_id: str) -> dict:
        """
        Fetch details of a specific song from the server.
        :param song_id: The ID of the song to fetch details for.
        :return: A dictionary containing song details or an empty dictionary if the request fails.
        """
        extra_params = {
            "id": song_id
        }
        response = self._send_request("getSong", extra_params)
        if response.get("status") == "ok":
            return response.get("song", {})
        return {}

    def download_song(self, song_id: str) -> str:
        """
        Download a song by its ID.
        :param song_id: The ID of the song to download.
        :return: The path to the downloaded song file.
        """
        # This doesn't use _send_request because the endpoint does not return JSON data
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

    @Slot(str, int)
    def search_albums(self, query: str, page: int) -> None:
        """
        Search for albums
        :param query: The search query.
        :param page: The page number.
        """
        extra_params = {
            "query": query,
            "albumCount": 20,
            "albumOffset": page * 20 - 20
        }
        response = self._send_request("search2", extra_params)
        if response.get("status") == "ok":
            albums = []
            for album in response.get("searchResult2", {}).get("album", []):
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

    @Slot()
    def update_playlist_list(self) -> None:
        """
        Fetch the list of playlists from the server.
        """
        response = self._send_request("getPlaylists")
        if response.get("status") == "ok":
            playlists = []
            for playlist in response.get("playlists", {}).get("playlist", []):
                cover_art_path = self.get_cover_art(playlist.get("coverArt", ""))
                playlists.append([
                    playlist.get("id", ""),
                    playlist.get("name", ""),
                    cover_art_path
                ])
            self.playlistListChanged.emit(playlists)

    @Slot(str)
    def get_playlist_details(self, playlist_id: str) -> dict:
        """
        Fetch details of a specific playlist from the server.
        :param playlist_id: The ID of the playlist to fetch details for.
        """
        extra_params = {
            "id": playlist_id
        }
        response = self._send_request("getPlaylist", extra_params)
        if response.get("status") == "ok":
            playlist_details = response.get("playlist", {})
            song_list = []
            for song in playlist_details.get("entry", []):
                song_list.append([
                    song.get("id", ""),
                    song.get("title", ""),
                    song.get("artist", ""),
                    song.get("duration", 0),
                ])
            cover_art_path = self.get_cover_art(playlist_details.get("coverArt", ""))
            self.playlistDetailsReceived.emit(
                playlist_details.get("id", ""),
                playlist_details.get("name"),
                playlist_details.get("owner", ""),
                cover_art_path,
                playlist_details.get("songCount", 0),
                time.strftime("%H:%M:%S", time.gmtime(playlist_details.get("duration", 0))),
                playlist_details.get("public", False),
                song_list
            )
            return playlist_details
        return {}

    @Slot(str, bool)
    def set_favourite_status(self, id: str, status: bool) -> None:
        """
        Set the favourite status of an album, song or artist.
        :param id: The ID of the album, song or artist.
        :param status: True to favourite, False to unfavourite.
        """
        extra_params = {
            "id": id,
        }
        # favourites are stars on the Subsonic server
        # Here we use a heart (favourite) because stars are used for ratings
        if status:
            endpoint = "star"
        else:
            endpoint = "unstar"
        self._send_request(endpoint, extra_params)

    @Slot(str, int)
    def set_rating(self, target_id: str, rating: int) -> None:
        """
        Set the rating of an album, song or artist.
        :param target_id: The ID of the album, song or artist.
        :param rating: The rating to set (0-5; 0 removes the rating).
        """
        if rating < 0 or rating > 5:
            return
        extra_params = {
            "id": target_id,
            "rating": rating
        }
        self._send_request("setRating", extra_params)

    @Slot(result="QVariant")
    def get_artists(self):
        response = self._send_request("getArtists")
        if response.get("status") == "ok":
            artists = []
            for indices in response.get("artists", {}).get("index", []):
                for artist in indices.get("artist", []):
                    artists.append([
                        artist.get("id", ""),
                        artist.get("name", ""),
                        artist.get("albumCount", 0)
                    ])
            return artists
        return [[]]
