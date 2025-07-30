from PySide6.QtCore import QObject, Slot
import PySoundSphere

class PlaybackHandler(QObject):
    def __init__(self, api_handler) -> None:
        super().__init__()
        self.api_handler = api_handler
        self.audio_player = PySoundSphere.AudioPlayer("pygame")

    @Slot(float)
    def set_volume(self, volume: float) -> None:
        """
        Set the volume of the audio player.
        :param volume: Volume level (0 - 1).
        """
        self.audio_player.volume = volume

    @Slot(str)
    def play_song(self, song_id: str) -> None:
        """
        Play a song by its ID.
        :param song_id: The ID of the song to play.
        """
        path = self.api_handler.download_song(song_id)
        if not path:
            return  # If the path is empty, the song could not be downloaded
        self.audio_player.stop()  # No effect if not playing
        self.audio_player.load(path)
        self.audio_player.play()
