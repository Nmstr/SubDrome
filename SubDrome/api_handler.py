from PySide6.QtCore import QObject, Slot, Signal
import requests
import os

class ApiHandler(QObject):
    albumsUpdated = Signal("QVariant")

    def __init__(self, config_handler):
        super().__init__()
        self.config_handler = config_handler

    def get_cover_art(self, cover_id: str) -> str:
        """
        Fetch cover art from the server.
        :param cover_id: The ID of the cover art to fetch.
        :return: The path to the cover art
        """
        cache_dir = os.path.expanduser(os.path.join("~", ".cache", "SubDrome"))
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        cover_file_path = os.path.join(cache_dir, f"{cover_id}.jpg")
        if os.path.exists(cover_file_path):
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
                    return cover_file_path
        except requests.RequestException:
            pass
        return ""

    @Slot()
    def get_random_albums(self):
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
            "type": "random",
            "size": 15
        }
        try:
            response = requests.get(f"{self.config_handler.server_address}/rest/getAlbumList2", params=params)
            if response.status_code == 200 and response.json().get("subsonic-response", {}).get("status") == "ok":
                albums = []
                for album in response.json().get("subsonic-response", {}).get("albumList2", {}).get("album", []):
                    cover_art_path = self.get_cover_art(album.get("coverArt", ""))
                    albums.append([
                        album.get("id"),
                        album.get("name"),
                        album.get("artist"),
                        cover_art_path
                    ])
                self.albumsUpdated.emit(albums)
        except requests.RequestException:
            pass
