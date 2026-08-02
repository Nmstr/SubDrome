mod app;
mod config;

use app::App;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let runtime = tokio::runtime::Runtime::new()?;
    let _guard = runtime.enter();
    App::new()?.run()?;
    Ok(())
}
