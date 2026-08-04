use crate::subsonic::models::{Empty, Envelope};
use reqwest::Client;
use serde::de::DeserializeOwned;

const API_VERSION: &str = "1.16.1";
const CLIENT_NAME: &str = "SubDrome";

pub struct SubsonicClient {
    http: Client,
    base_url: String,
}

#[derive(Debug)]
pub enum SubsonicError {
    Network(reqwest::Error),
    Api { code: u32, message: String },
}

impl std::fmt::Display for SubsonicError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Network(err) => write!(f, "Network error: {}", err),
            Self::Api { code, message } => write!(f, "subsonic error ({}: {})", code, message),
        }
    }
}

impl std::error::Error for SubsonicError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Network(err) => Some(err),
            Self::Api { .. } => None,
        }
    }
}

impl From<reqwest::Error> for SubsonicError {
    fn from(err: reqwest::Error) -> Self {
        Self::Network(err)
    }
}

impl SubsonicClient {
    pub fn new(base_url: impl Into<String>) -> Self {
        Self {
            http: Client::new(),
            base_url: base_url.into(),
        }
    }

    pub async fn ping(&self, username: &str, token: &str, salt: &str) -> Result<(), SubsonicError> {
        self.request::<Empty>("ping", username, token, salt, &[])
            .await?;
        Ok(())
    }

    async fn request<T: DeserializeOwned>(
        &self,
        endpoint: &str,
        username: &str,
        token: &str,
        salt: &str,
        extra_params: &[(&str, &str)],
    ) -> Result<T, SubsonicError> {
        let url = format!(
            "{}/rest/{}.view",
            self.base_url.trim_end_matches('/'),
            endpoint
        );

        let mut params = vec![
            ("u", username),
            ("t", token),
            ("s", salt),
            ("v", API_VERSION),
            ("c", CLIENT_NAME),
            ("f", "json"),
        ];
        params.extend_from_slice(extra_params);

        let response = self.http.get(&url).query(&params).send().await?;
        let envelope: Envelope<T> = response.json().await?;
        let body = envelope.subsonic_response;

        if body.status == "ok" {
            Ok(body.data)
        } else {
            let err = body.error.unwrap_or(super::models::ApiError {
                code: 0,
                message: "unknown error".into(),
            });
            Err(SubsonicError::Api {
                code: err.code,
                message: err.message,
            })
        }
    }
}
