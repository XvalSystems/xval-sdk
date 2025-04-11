import typer
from .. import __version__
from .users import (
    set_, 
    status,
    login,
    logout,
)

from .val import (
    list,
    create,
    delete,
    clone,
    run,
    init,
    audit,
)
# Dictionary mapping command names to functions
COMMANDS = {
    "set": set_,
    'status': status,
    'login': login,
    'logout': logout,
    'list': list,
    'create': create,
    'delete': delete,
    'clone': clone,
    'run': run,
    'init': init,
    'audit': audit,
}

def register_commands(app):
    """Register all commands to the provided Typer app."""
    for name, func in COMMANDS.items():
        app.command(name=name)(func)

app = typer.Typer(help="Xval CLI commands")

register_commands(app)

@app.callback()
def callback():
    """Xval CLI commands."""

@app.command()
def hello():
    """Print Hello World!"""
    typer.echo("Hello World!")

@app.command()
def version():
    """Show the application version."""
    print(f"xval-cli v{__version__}")
    



