from PySide6.QtCore import QObject, Slot, Signal, QTimer
import PySoundSphere

class PlaybackHandler(QObject):
    newSong = Signal(str, str, int, str)
    positionChanged = Signal(int)
    isPlaying = Signal(bool)

    def __init__(self, api_handler, config_handler) -> None:
        super().__init__()
        self.api_handler = api_handler
        self.config_handler = config_handler
        self.audio_player = PySoundSphere.AudioPlayer("pygame")
        self.audio_player.volume = self.config_handler.volume

        self.position_timer = QTimer(self)
        self.position_timer.setInterval(1000)
        self.position_timer.timeout.connect(self.update_position)
        self.position_timer.start()

    @Slot(float)
    def set_volume(self, volume: float) -> None:
        """
        Set the volume of the audio player.
        :param volume: Volume level (0 - 1).
        """
        self.audio_player.volume = volume
        self.config_handler.volume = volume

    @Slot(result=float)
    def get_volume(self) -> float:
        """
        Get the current volume of the audio player.
        :return: Volume level (0 - 1).
        """
        return self.audio_player.volume

    def update_position(self) -> None:
        """
        Updates the current playback position.
        Called once per second.
        """
        position = self.audio_player.position
        self.positionChanged.emit(position)

    @Slot(float)
    def set_position(self, position: float) -> None:
        """
        Set the playback position of the audio player.
        :param position: Position in seconds.
        """
        self.audio_player.position = position
        self.positionChanged.emit(position)

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
        song_details = self.api_handler.get_song_details(song_id)
        art_path = self.api_handler.get_cover_art(song_details.get("coverArt", ""))
        self.newSong.emit(song_details.get("title", "Unknown Title"), song_details.get("artist", "Unknown Artist"), song_details.get("duration", 0), art_path)
        self.isPlaying.emit(True)

    @Slot()
    def pause(self) -> None:
        """
        Pause the currently playing song.
        """
        self.audio_player.pause()
        self.isPlaying.emit(False)

    @Slot()
    def play(self) -> None:
        """
        Resume the currently paused song.
        """
        try:
            self.audio_player.play()
            self.isPlaying.emit(True)
        except ValueError:
            pass  # No song is loaded
