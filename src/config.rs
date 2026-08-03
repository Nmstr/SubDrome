use serde::{Deserialize, Serialize};
use std::path::PathBuf;

const KEYRING_SERVICE: &str = "SubDrome";

#[derive(Debug, Default, Serialize, Deserialize)]
pub struct Config {
    pub server_url: Option<String>,
    pub active_username: Option<String>,
    pub active_salt: Option<String>,
}

impl Config {
    pub fn load() -> Result<Self, std::io::Error> {
        let path = Self::path()?;
        if !path.exists() {
            return Ok(Self::default());
        }
        Ok(serde_json::from_str(&std::fs::read_to_string(path)?)?)
    }

    pub fn save(&self) -> Result<(), std::io::Error> {
        let path = Self::path()?;
        if let Some(parent) = path.parent() {
            std::fs::create_dir_all(parent)?;
        }
        std::fs::write(path, serde_json::to_string_pretty(self)?)?;
        Ok(())
    }

    pub fn path() -> Result<PathBuf, std::io::Error> {
        let dirs = directories::ProjectDirs::from("org", "LightDrive", "SubDrome")
            .ok_or(std::io::ErrorKind::NotFound)?;
        Ok(dirs.config_dir().join("config.json"))
    }
}

pub fn save_credentials(
    username: &str,
    token: &str,
) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let entry = keyring::Entry::new(KEYRING_SERVICE, username);
    entry?.set_password(token)?;
    Ok(())
}

pub fn load_credentials(username: &str) -> Result<String, keyring::Error> {
    let entry = keyring::Entry::new(KEYRING_SERVICE, username);
    entry?.get_password()
}
