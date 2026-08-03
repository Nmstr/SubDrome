use crate::config;
use crate::config::Config;
use slint::ComponentHandle;
use std::error::Error;
use std::sync::{Arc, Mutex};
use rand::distr::{Alphanumeric, SampleString};

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
                    cfg.active_salt = Some(Alphanumeric.sample_string(&mut rand::rng(), 16));

                    let digest = md5::compute(
                        password.clone() + cfg.active_salt.as_deref().unwrap_or_default(),
                    );

                    if let Err(err) = config::save_credentials(&username, &format!("{:x}", digest))
                    {
                        let _ = weak.upgrade_in_event_loop(move |window| {
                            let session = window.global::<Session>();
                            session.set_status("Failed to save credentials.".into());
                        });

                        return;
                    }

                    if let Err(err) = cfg.save() {
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

        self.window.run().map_err(Into::into)
    }
}
