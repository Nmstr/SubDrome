from PySide6.QtCore import QObject, Slot, Signal
import validators
import requests
import hashlib
import os

class LoginHandler(QObject):
    loginFailed = Signal(str)
    loginSuccess = Signal()
    loggedOut = Signal()
    loginFilled = Signal(str, str)

    def __init__(self, config_handler):
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
            self.config_handler.token = token
            self.config_handler.salt = salt
            self.config_handler.server_address = url
            self.config_handler.username = username
        self.loginSuccess.emit()
        return True

    @Slot()
    def request_login_fill(self) -> None:
        """
        Tries to automatically fill in the login fields with server address and username.
        This method exists since there is no way to access the config handler directly from QML.
        """
        self.loginFilled.emit(self.config_handler.server_address, self.config_handler.username)

    @Slot()
    def logout(self):
        """
        Handle the logout process by clearing the saved credentials.
        """
        del self.config_handler.token
        del self.config_handler.salt
        self.loggedOut.emit()
