from SubDrome import resource_rc  # noqa: F401
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal
import configparser
import validators
import requests
import keyring
import hashlib
import sys
import os

class ConfigHandler:
    def __init__(self):
        self.config_dir = os.path.expanduser(os.path.join("~", ".config", "SubDrome"))
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        self.config_file = os.path.join(self.config_dir, "config.ini")
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    @property
    def username(self):
        if not self.config.has_section("Server"):
            self.config.add_section("Server")
        if not self.config.has_option("Server", "username"):
            return ""
        return self.config.get("Server", "username")

    @username.setter
    def username(self, value):
        if not self.config.has_section("Server"):
            self.config.add_section("Server")
        self.config.set("Server", "username", value)
        with open(self.config_file, "w") as f:
            self.config.write(f)

    @property
    def server_address(self):
        if not self.config.has_section("Server"):
            self.config.add_section("Server")
        if not self.config.has_option("Server", "address"):
            return ""
        return self.config.get("Server", "address")

    @server_address.setter
    def server_address(self, value):
        if not self.config.has_section("Server"):
            self.config.add_section("Server")
        self.config.set("Server", "address", value)
        with open(self.config_file, "w") as f:
            self.config.write(f)

    @property
    def token(self):
        return keyring.get_password("SubDrome", "token") or ""

    @token.setter
    def token(self, value):
        keyring.set_password("SubDrome", "token", value)

    @property
    def salt(self):
        return keyring.get_password("SubDrome", "salt") or ""

    @salt.setter
    def salt(self, value):
        keyring.set_password("SubDrome", "salt", value)

class LoginHandler(QObject):
    loginFailed = Signal(str)
    loginSuccess = Signal(str)

    def __init__(self, config_handler: ConfigHandler):
        super().__init__()
        self.config_handler = config_handler

    def is_online(self, url: str) -> bool:
        """
        Check if the server is online by making a request to the server.
        :param url: The base URL of the server.
        :return: Whether the server is online or not.
        """
        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def is_user_valid(self, url: str, username: str, token: str, salt: str) -> bool:
        """
        Check if the user is valid by making a request to the server.
        :param url: The base URL of the server.
        :param username: The username of the user.
        :param token: The token of the user.
        :param salt: The salt to use for hashing the password.
        :return: Whether the user is valid or not.
        """
        params = {
            "u": username,
            "t": token,
            "s": salt,
            "c": "SubDromeClient",
            "v": "1.0",
            "f": "json",
            "username": username,
        }
        try:
            response = requests.get(f"{url}/rest/getUser", params=params)
            if response.status_code == 200:
                if response.json().get("subsonic-response", {}).get("status") == "ok":
                    return True
            return False
        except requests.RequestException:
            return False

    @Slot(str, str, str)
    def handle_login(self, url: str, username: str, password: str, salt: str = os.urandom(64).hex(), token: str = None, write: bool = True) -> bool:
        """
        Handle the login process by checking if the server is online and if the user is valid.
        :param url: The base URL of the server.
        :param username: The username of the user.
        :param password: The password of the user.
        :param salt: The salt to use for hashing the password (optional, defaults to a random value).
        :param token: The token to use for authentication (optional, defaults to None).
        :param write: Whether to write the credentials to the config file (default is True).
        :return: Whether the login was successful or not.
        """
        if not validators.url(url):
            self.loginFailed.emit("Invalid URL")
            return False
        if not self.is_online(url):
            self.loginFailed.emit("Cannot connect to the server")
            return False
        if not token:
            token = hashlib.md5((password + salt).encode("utf-8")).hexdigest()
        if not self.is_user_valid(url, username, token, salt):
            self.loginFailed.emit("Invalid username or password")
            return False

        if write:
            keyring.set_password("SubDrome", "salt", salt)
            keyring.set_password("SubDrome", "token", token)
            self.config_handler.server_address = url
            self.config_handler.username = username
        self.loginSuccess.emit("Logged in")
        return True

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)

    config_handler = ConfigHandler()
    login_handler = LoginHandler(config_handler)
    engine.rootContext().setContextProperty("loginHandler", login_handler)
    engine.load("SubDrome/main.qml")

    # Try to log in with saved credentials
    login_handler.handle_login(url=config_handler.server_address,
                               username=config_handler.username,
                               password="",
                               salt=config_handler.salt,
                               token=config_handler.token,
                               write=False)

    sys.exit(app.exec())
