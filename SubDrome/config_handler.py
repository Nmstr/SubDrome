import configparser
import keyring
import os

class ConfigHandler:
    def __init__(self):
        self.config_dir = os.path.expanduser(os.path.join("~", ".config", "SubDrome"))
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        self.config_file = os.path.join(self.config_dir, "config.ini")
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

        self.cached_token = keyring.get_password("SubDrome", "token") or ""
        self.cached_salt = keyring.get_password("SubDrome", "salt") or ""

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
        return self.cached_token

    @token.setter
    def token(self, value):
        self.cached_token = value
        keyring.set_password("SubDrome", "token", value)

    @token.deleter
    def token(self):
        self.cached_token = ""
        keyring.delete_password("SubDrome", "token")

    @property
    def salt(self):
        return self.cached_salt

    @salt.setter
    def salt(self, value):
        self.cached_salt = value
        keyring.set_password("SubDrome", "salt", value)

    @salt.deleter
    def salt(self):
        self.cached_salt = ""
        keyring.delete_password("SubDrome", "salt")

    @property
    def volume(self):
        if not self.config.has_section("Playback"):
            self.config.add_section("Playback")
        if not self.config.has_option("Playback", "volume"):
            return 0.5
        return self.config.getfloat("Playback", "volume")

    @volume.setter
    def volume(self, value):
        if not self.config.has_section("Playback"):
            self.config.add_section("Playback")
        self.config.set("Playback", "volume", str(value))
        with open(self.config_file, "w") as f:
            self.config.write(f)
