import typer
from ..config import config as _config

def set_(
    slug: str = typer.Option(None, "--slug", help="The slug to use for the app."),
    email: str = typer.Option(None, "--email", help="The user's email."),
    env: str = typer.Option(None, "--env", help="The xval environment to switch to."),
    api_url: str = typer.Option(None, "--api-url", help="The API URL to use for the app."),
):
    """Set config items."""
    if slug:
        _config.set_api_url(slug)
        typer.echo(f"API URL set to: {_config.get_api_url()}")
    if email:
        _config.user_email = email
        _config._save_config()
        typer.echo(f"User email set to: {email}")
    if api_url:
        _config.api_url = api_url
        typer.echo(f"API URL set to: {_config.get_api_url()}")
        
def status():
    """Display all configuration settings."""
    typer.echo("Current configuration:")
    for key in _config.attributes:
        if key == 'session_token':
            auth_info = _config.current_user()
            if auth_info:
                typer.echo(f"logged_in_as: {auth_info['email']}")
                typer.echo(f"environment: {auth_info['current_environment']['name']}")
            else:
                typer.echo("logged_in_as: None")
        else:
            typer.echo(f"{key}: {getattr(_config, key)}")

def login(
    email: str = typer.Option(None, prompt=not _config.user_email, help="The email to use for login."),
    password: str = typer.Option(None, prompt=True, hide_input=True, help="The password to use for login.")
):
    """Login to Xval."""
    typer.echo(_config.login(email, password))
    

def logout():
    """Logout from Xval."""
    typer.echo(_config.logout())