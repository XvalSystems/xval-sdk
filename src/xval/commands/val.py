import typer
import questionary
from ..api import post
from .. import (
    api_endpoints,
    find_object,
    list as list_ctrl,
    delete as delete_ctrl,
    clone as clone_ctrl,
    run as run_ctrl,
    init as init_ctrl,
    audit as audit_ctrl,
)

def list(
    kind: str = typer.Argument(None, help="The kind of objects to list."),
    attr: list[str] = typer.Option([], "--attr", help="The attributes to list."),
):
    """List objects."""
    typer.echo(f"Retrieving {kind} objects...")

    attr = ['name'] + attr

    if kind in api_endpoints and "list" in api_endpoints[kind]:
        objects = list_ctrl(kind)
        for obj in objects:
            typer.echo(' '.join([str(obj.get(a, '')) for a in attr]))
    else:
        raise typer.Abort("Invalid kind.")

def create(
    kind: str = typer.Argument(None, help="The kind of objects to create."),
    name: str|None = typer.Option(None, "--name", help="The name of the object to create."),
):
    """List objects."""
    if name is None:
        name = typer.prompt("Enter the name of the object to create.")

    typer.echo(f"Creating {kind} object...")
    if kind == "run":
        typer.echo(post('run/', {'name': name}))
    else:
        raise typer.Abort("Invalid kind.")

def delete(
    kind: str = typer.Argument(None, help="The kind of objects to delete."),
    name: str|None = typer.Option(None, "--name", help="The name of the object to delete."),
):
    """Delete an object."""
    if name is None:
        name = typer.prompt("Enter the name of the object to delete.")

    if kind not in api_endpoints or 'list' not in api_endpoints[kind] or 'delete' not in api_endpoints[kind]:
        raise typer.Abort("Invalid kind.")


    obj = find_object(kind, name)

    if obj is None:
        raise typer.Abort("Invalid object.")

    typer.echo(f"Deleting {kind} object {name}...")
    if kind == "run":
        typer.echo(delete_ctrl(kind, obj['uuid']))
    else:
        raise typer.Abort("Invalid kind.")
            
def clone(
    kind: str = typer.Argument(None, help="The kind of objects to clone."),
    name: str|None = typer.Option(None, "--name", help="The name of the object to clone."),
    new_name: str|None = typer.Option(None, "--new-name", help="The name of the new object."),
):
    """Clone an object."""
    if name is None:
        name = typer.prompt("Enter the name of the object to clone.")

    if new_name is None:
        new_name = typer.prompt("Enter the name of the new object.")

    if kind not in api_endpoints or 'list' not in api_endpoints[kind] or 'clone' not in api_endpoints[kind]:
        raise typer.Abort("Invalid kind.")



    obj = find_object(kind, name)

    if obj is None:
        raise typer.Abort("Invalid object.")

    typer.echo(f"Cloning {kind} object...")
    if kind in ["env", "data", "run"]:
        typer.echo(clone_ctrl(kind, obj['uuid'], new_name))
    else:
        raise typer.Abort("Invalid kind.")
            
def init(
    name: str|None = typer.Option(None, "--name", help="The name of the object to run."),
):
    """Clone an object."""
    if name is None:
        name = typer.prompt("Enter the name of the run to start.")

    obj = find_object("run", name)

    if obj is None:
        raise typer.Abort("Invalid object.")

    typer.echo(f"Initializing run...")
    typer.echo(init_ctrl(obj['uuid']))

def run(
    name: str|None = typer.Argument(None, help="The name of the object to run."),
):
    """Start a run."""
    if name is None:
        name = typer.prompt("Enter the name of the run to start.")

    obj = find_object("run", name)

    if obj is None:
        raise typer.Abort("Invalid name.")

    typer.echo(f"Starting run...")
    typer.echo(run_ctrl(obj['uuid']))
    typer.Exit()

def audit(
    name: str|None = typer.Argument(None, help="The name of the run to audit."),
):
    """Audit a run."""
    if name is None:
        name = typer.prompt("Enter the name of the run to audit.")

    choices = [
        {'value':run_element['uuid'], 'name': run_element['name']} 
        for run_element in find_object("run", name)['run_elements']
    ]

    if len(choices) == 0:
        raise typer.Abort("No run elements found.")
    elif len(choices) == 1:
        choice = choices[0]['value']
    else:
        choice = questionary.select(
            "Select a run element to audit.",
            choices=choices
        ).ask()

    typer.echo(audit_ctrl(choice))