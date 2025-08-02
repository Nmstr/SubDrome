from SubDrome.config_handler import ConfigHandler
import pytest

@pytest.fixture
def config_handler(tmp_path, monkeypatch):
    """
    Fixture to create a ConfigHandler instance with a mocked keyring and config directory.
    :param tmp_path: Temporary path for the config directory.
    :param monkeypatch: Monkeypatching to mock keyring functions and config directory.
    :return: ConfigHandler instance
    """
    config_dir = tmp_path / ".config" / "SubDrome"
    config_dir.mkdir(parents=True)

    mock_keyring_storage = {}

    def mock_get_password(service, username):
        return mock_keyring_storage.get((service, username), None)

    def mock_set_password(service, username, password):
        key = f"{service}:{username}"
        mock_keyring_storage[key] = password

    def mock_delete_password(service, username):
        key = f"{service}:{username}"
        if key in mock_keyring_storage:
            del mock_keyring_storage[key]

    monkeypatch.setattr("keyring.get_password", mock_get_password)
    monkeypatch.setattr("keyring.set_password", mock_set_password)
    monkeypatch.setattr("keyring.delete_password", mock_delete_password)

    monkeypatch.setattr("os.path.expanduser", lambda path: str(tmp_path) + path[1:] if path.startswith("~") else path)

    return ConfigHandler()

def test_username_default_value_is_empty(config_handler):
    assert config_handler.username == ""

def test_username_setter_stores_value(config_handler):
    config_handler.username = "test_user"
    assert config_handler.username == "test_user"

def test_server_address_default_value_is_empty(config_handler):
    assert config_handler.server_address == ""

def test_server_address_setter_stores_value(config_handler):
    config_handler.server_address = "http://example.com"
    assert config_handler.server_address == "http://example.com"

def test_token_default_value_is_empty(config_handler):
    assert config_handler.token == ""

def test_token_setter_stores_value(config_handler):
    config_handler.token = "test_token"
    assert config_handler.token == "test_token"

def test_token_deleter_clears_value(config_handler):
    del config_handler.token
    assert config_handler.token == ""

def test_salt_default_value_is_empty(config_handler):
    assert config_handler.salt == ""

def test_salt_setter_stores_value(config_handler):
    config_handler.salt = "test_salt"
    assert config_handler.salt == "test_salt"

def test_salt_deleter_clears_value(config_handler):
    del config_handler.salt
    assert config_handler.salt == ""

def test_volume_default_value_is_05(config_handler):
    assert config_handler.volume == 0.5

def test_volume_setter_stores_value(config_handler):
    config_handler.volume = 0.8
    assert config_handler.volume == 0.8
