from PySide6.QtCore import QObject, Slot

class PlaybackHandler(QObject):
    def __init__(self, api_handler) -> None:
        super().__init__()
        self.api_handler = api_handler

    @Slot(str)
    def play_song(self, song_id: str) -> None:
        """
        Play a song by its ID.
        :param song_id: The ID of the song to play.
        """
        print(f"Playing song with ID: {song_id}")
