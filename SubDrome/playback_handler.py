from PySide6.QtCore import QObject, Slot, Signal, QTimer
import PySoundSphere

class PlaybackHandler(QObject):
    newSong = Signal(str, str, int, str)
    positionChanged = Signal(int)
    isPlaying = Signal(bool)
    queueUpdated = Signal(str, str, str, "QVariant")

    def __init__(self, api_handler, config_handler) -> None:
        super().__init__()
        self.api_handler = api_handler
        self.config_handler = config_handler
        self.audio_player = PySoundSphere.AudioPlayer("pygame")
        self.audio_player.set_callback_function(lambda: self.skip_song(1))
        self.audio_player.volume = self.config_handler.volume

        self.current_album_id = ""
        self.current_song_id = ""
        self.is_playing_playlist = False

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

    @Slot(int)
    def skip_song(self, amount: int) -> None:
        """
        Skip around in the queue.
        If the song is not available, playback will stop.
        :param amount: The number of songs to skip (-1 = previous song, 1 = next song).
        """
        if not self.current_album_id or not self.current_song_id:
            return
        if self.is_playing_playlist:
            playlist_details = self.api_handler.get_playlist_details(self.current_album_id)
            song_list = playlist_details.get("entry", [])
        else:
            album_details = self.api_handler.get_album_details(self.current_album_id)
            song_list = album_details.get("song", [])
        if not song_list:
            return

        current_index = next((i for i, song in enumerate(song_list) if song.get("id") == self.current_song_id), -1)
        if (current_index == -1) or (current_index + amount >= len(song_list)) or (current_index + amount < 0):
            self.audio_player.pause()
            self.isPlaying.emit(False)
            return
        next_song = song_list[current_index + amount]
        self.play_song(self.current_album_id, next_song.get("id", ""), self.is_playing_playlist)

    @Slot(str, str)
    @Slot(str, str, str)
    def play_song(self, album_id: str, song_id: str, is_playlist = False) -> None:
        """
        Play a song by its ID.
        :param album_id: The ID of the album containing the song.
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

        self.current_song_id = song_id
        self.current_album_id = album_id
        self.is_playing_playlist = is_playlist

        if is_playlist:
            songs = self.api_handler.get_playlist_details(self.current_album_id).get("entry", [])
        else:
            songs = self.api_handler.get_album_details(album_id).get("song", [])
        add_songs = False
        current_song_art_path = ""
        song_list = []
        for song in songs:
            if not add_songs:  # Make sure to add songs only after the current song
                if song.get("id") == song_id:
                    current_song_art_path = self.api_handler.get_cover_art(song.get("coverArt", ""))
                    add_songs = True
                    continue
                else:
                    continue
            art_path = self.api_handler.get_cover_art(song["coverArt"])
            song_list.append([
                song.get("title", ""),
                song.get("artist", ""),
                art_path,
            ])
        self.queueUpdated.emit(song_details.get("title", ""), song_details.get("artist", ""),
                               current_song_art_path, song_list)

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
