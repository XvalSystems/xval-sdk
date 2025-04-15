import typer
import questionary
import xval.api as api
from .. import (
    retrieve as retrieve_ctrl,
    list_ as list_ctrl,
    delete as delete_ctrl,
    clone as clone_ctrl,
    start as run_ctrl,
    init as init_ctrl,
    audit as audit_ctrl,
    update as update_ctrl,
)

from . import views 

def do_retrieve(
    kind: str,
    name: str|None = None,
    uuid: str|None = None,
):
    """Retrieve an object."""
    if name is None and uuid is None:
        name = typer.prompt("Enter the name or uuid of the object.")

    if uuid is not None:
        return retrieve_ctrl(kind, uuid)
    else:
        return retrieve_ctrl(kind, name)

def create(
    kind: str = typer.Argument(None, help="The kind of objects to create."),
    name: str|None = typer.Option(None, "--name", help="The name of the object to create."),
):
    """List objects."""
    if name is None:
        name = typer.prompt("Enter the name of the object to create.")

    typer.echo(f"Creating {kind} object...")
    if kind == "run":
        typer.echo(api.post('/run/', {'name': name}))
    else:
        raise typer.Abort("Invalid kind.")

def list_(
    kind: str = typer.Argument(None, help="The kind of objects to list."),
    attr: list[str] = typer.Option([], "--attr", help="The attributes to list."),
):
    """List objects."""
    typer.echo(f"Retrieving {kind} objects...")

    attr = ['name'] + attr

    if kind in api.endpoints and "list" in api.endpoints[kind]:
        objects = list_ctrl(kind)
        for obj in objects:
            typer.echo(' '.join([str(obj.get(a, '')) for a in attr]))
    else:
        raise typer.Abort("Invalid kind.")


def view(
    kind: str = typer.Argument(None, help="The kind of objects to view."),
    name: str|None = typer.Option(None, "--name", help="The name of the object to view."),
    uuid: str|None = typer.Option(None, "--uuid", help="The uuid of the object to view."),
    attr: list[str]|None = typer.Option(None, "--attr", help="The attributes to view."),
):
    """View an object."""
    obj = do_retrieve(kind, name, uuid)
    if attr is None:
        views.handlers[kind](obj['uuid'])
    else:
        print(' '.join([str(obj.get(a, '')) for a in attr]))


def delete(
    kind: str = typer.Argument(None, help="The kind of objects to delete."),
    name: str|None = typer.Option(None, "--name", help="The name of the object to delete."),
    uuid: str|None = typer.Option(None, "--uuid", help="The uuid of the object to delete."),
):
    """Delete an object."""

    if kind not in api.endpoints or 'list' not in api.endpoints[kind] or 'delete' not in api.endpoints[kind]:
        raise typer.Abort("Invalid kind.")

    obj = do_retrieve(kind, name, uuid)

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
    uuid: str|None = typer.Option(None, "--uuid", help="The uuid of the object to clone."),
    new_name: str|None = typer.Option(None, "--new-name", help="The name of the new object."),
):
    """Clone an object."""
    if kind not in api.endpoints or 'list' not in api.endpoints[kind] or 'clone' not in api.endpoints[kind]:
        raise typer.Abort("Invalid kind.")
    
    obj = do_retrieve(kind, name, uuid)

    if obj is None:
        raise typer.Abort("Invalid object.")

    if new_name is None:
        new_name = typer.prompt("Enter the name of the new object.")

    typer.echo(f"Cloning {kind} object...")
    if kind in ["env", "data", "run"]:
        typer.echo(clone_ctrl(kind, obj['uuid'], new_name))
    else:
        raise typer.Abort("Invalid kind.")
            
def init(
    name: str|None = typer.Option(None, "--name", help="The name of the object to run."),
    uuid: str|None = typer.Option(None, "--uuid", help="The uuid of the object to clone."),
):
    """Clone an object."""

    obj = do_retrieve("run", name, uuid)

    if obj is None:
        raise typer.Abort("Invalid object.")

    typer.echo(f"Initializing run...")
    typer.echo(init_ctrl(obj['uuid']))

def run(
    name: str|None = typer.Argument(None, help="The name of the object to run."),
    uuid: str|None = typer.Option(None, "--uuid", help="The uuid of the object to run."),
):
    """Start a run."""

    obj = do_retrieve("run", name, uuid)

    if obj is None:
        raise typer.Abort("Invalid name.")

    typer.echo(f"Starting run...")
    typer.echo(run_ctrl(obj['uuid']))
    typer.Exit()

def audit(
    name: str|None = typer.Argument(None, help="The name of the run to audit."),
    uuid: str|None = typer.Option(None, "--uuid", help="The uuid of the object to audit."),
    no_config: bool = typer.Option(False, "--no-config", help="Do not offer config options."),
):
    """Audit a run."""
    obj = do_retrieve("run", name, uuid)

    if obj is None:
        raise typer.Abort("Invalid object.")

    choices = [
        {'value':run_element['uuid'], 'name': run_element['name']} 
        for run_element in obj['run_elements']
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
    
    if not no_config:
        audit_config_prompts(choice)

    typer.echo(audit_ctrl(choice))

def audit_config_prompts(run_element_uuid: str):
    run_element = api.get(f'/run-element/{run_element_uuid}/')
    keep_inputs = run_element['audit_config']['keep_inputs']
    keep_vtables = run_element['audit_config']['keep_vtables']
    for tbl in keep_inputs:
        tbl['indices'] = prompt_for_list_of_indices(
            tbl['indices'], 
            f"Enter indices for {tbl['name']} (comma separated integers, or leave blank to keep current value: {tbl.get('indices', [])})"
        )

    for vtbl in keep_vtables:
        vtbl['values'] = prompt_for_list_of_indices(
            vtbl['values'], 
            f"Enter indices for {vtbl['name']} (comma separated integers, or leave blank to keep current value: {vtbl.get('values', [])})"
        )

    update_ctrl(
        kind = "run_element",
        uuid = run_element_uuid,
        data = {
            'audit_config': {
                'keep_inputs': keep_inputs,
                'keep_vtables': keep_vtables
            }
        }
    )


def prompt_for_list_of_indices(value_list: list[int], prompt_text: str, ):
    indices_input = questionary.text(prompt_text).ask()
    if indices_input:
        return [int(idx.strip()) for idx in indices_input.split(',') if idx.strip()]
    else:
        return value_list
