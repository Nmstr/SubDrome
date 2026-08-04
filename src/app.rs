use crate::config;
use crate::config::Config;
use crate::subsonic::{SubsonicClient, SubsonicError};
use rand::distr::{Alphanumeric, SampleString};
use slint::ComponentHandle;
use std::error::Error;
use std::sync::{Arc, Mutex};

slint::include_modules!();

pub struct App {
    window: MainWindow,
    config: Arc<Mutex<Config>>,
}

impl App {
    pub fn new() -> Result<Self, Box<dyn Error>> {
        let window = MainWindow::new()?;
        let config = Arc::new(Mutex::new(Config::load()?));
        slint::set_xdg_app_id("SubDrome")?;

        let app = Self { window, config };
        app.wire_session();
        Ok(app)
    }

    fn wire_session(&self) {
        let session = self.window.global::<Session>();
        let weak = self.window.as_weak();
        let config = self.config.clone();

        session.on_login(move |url, username, password| {
            let weak = weak.clone();
            let config = config.clone();
            let url = url.to_string();
            let username = username.to_string();
            let password = password.to_string();

            tokio::spawn(async move {
                let salt = Alphanumeric.sample_string(&mut rand::rng(), 16);
                let token = format!("{:x}", md5::compute(format!("{password}{salt}")));

                let client = SubsonicClient::new(&url);
                if let Err(err) = client.ping(&username, &token, &salt).await {
                    let message = match err {
                        SubsonicError::Api { message, .. } => message,
                        SubsonicError::Network(e) => format!("Could not reach server: {e}"),
                    };
                    let _ = weak.upgrade_in_event_loop(move |window| {
                        window.global::<Session>().set_status(message.into());
                    });
                    return;
                }

                {
                    let mut cfg = match config.lock() {
                        Ok(cfg) => cfg,
                        Err(e) => {
                            eprintln!("Error locking config: {}", e);
                            return;
                        }
                    };

                    cfg.server_url = Some(url.clone());
                    cfg.active_username = Some(username.clone());
                    cfg.active_salt = Some(salt);

                    if let Err(_err) = config::save_credentials(&username, &token) {
                        let _ = weak.upgrade_in_event_loop(move |window| {
                            let session = window.global::<Session>();
                            session.set_status("Failed to save credentials.".into());
                        });

                        return;
                    }

                    if let Err(_err) = cfg.save() {
                        let _ = weak.upgrade_in_event_loop(move |window| {
                            let session = window.global::<Session>();
                            session.set_status("Failed to save configuration.".into());
                        });

                        return;
                    }
                }

                weak.upgrade_in_event_loop(move |window| {
                    let session = window.global::<Session>();
                    session.set_logged_in(true);
                    session.set_status("".into());
                })
                .ok();
            });
        });
    }

    pub fn run(&mut self) -> Result<(), slint::PlatformError> {
        println!("{:?}", config::load_credentials("test"));

        self.window.run()
    }
}
