use crate::config;
use crate::config::Config;
use slint::ComponentHandle;
use std::error::Error;

slint::include_modules!();

pub struct App {
    window: MainWindow,
    config: Config,
}

impl App {
    pub fn new() -> Result<Self, Box<dyn Error>> {
        let window = MainWindow::new()?;
        let config = Config::load()?;
        slint::set_xdg_app_id("SubDrome")?;

        let app = Self { window, config };
        Ok(app)
    }

    pub fn run(&mut self) -> Result<(), slint::PlatformError> {
        self.config.active_username = Some(String::from("test"));
        self.config.active_salt = Some(String::from("test-salt"));
        self.config.save().expect("Failed to save config");

        let digest = md5::compute(
            self.config.active_username.clone().unwrap_or_default()
                + &self.config.active_salt.clone().unwrap_or_default(),
        );
        config::save_credentials("test", &format!("{:x}", digest))
            .expect("Failed to save credentials");
        println!("{:?}", config::load_credentials("test"));

        self.window.run().map_err(Into::into)
    }
}
