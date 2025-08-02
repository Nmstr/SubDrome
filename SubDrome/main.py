from SubDrome import resource_rc  # noqa: F401
from config_handler import ConfigHandler
from login_handler import LoginHandler
from api_handler import ApiHandler
from playback_handler import PlaybackHandler
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QDir
import sys

def main() -> None:
    """
    Main function to start SubDrome
    :return: None
    """
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)

    config_handler = ConfigHandler()
    login_handler = LoginHandler(config_handler)
    engine.rootContext().setContextProperty("loginHandler", login_handler)
    api_handler = ApiHandler(config_handler)
    engine.rootContext().setContextProperty("apiHandler", api_handler)
    playback_handler = PlaybackHandler(api_handler, config_handler)
    engine.rootContext().setContextProperty("playbackHandler", playback_handler)
    engine.addImportPath(QDir.currentPath() + "/SubDrome")
    engine.load("SubDrome/main.qml")

    # Try to log in with saved credentials
    login_handler.handle_login(url=config_handler.server_address,
                               username=config_handler.username,
                               password="",
                               salt=config_handler.salt,
                               token=config_handler.token,
                               write=False)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
