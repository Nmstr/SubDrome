use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct Envelope<T> {
    #[serde(rename = "subsonic-response")]
    pub subsonic_response: ResponseBody<T>,
}

#[derive(Debug, Deserialize)]
pub struct ResponseBody<T> {
    pub status: String,
    #[serde(default)]
    pub error: Option<ApiError>,
    #[serde(flatten)]
    pub data: T,
}

#[derive(Debug, Deserialize)]
pub struct Empty {}

#[derive(Debug, Deserialize)]
pub struct ApiError {
    pub code: u32,
    pub message: String,
}
