"""
xval - Xval's Python SDK and CLI
"""

__version__ = "0.0.2"



from typing import Literal
import xval.api as api

api_endpoints = {
    "env": {"list": "users/environment/", "create": "users/environment/"},
    "data": {"list": "data/", "create": "data/", "delete": "data/{uuid}/"},
    "run": {
      "list": "run/", "create": "run/", "delete": "run/{uuid}/", "clone": "run/{uuid}/clone/",
    },
}

def find_object(
    kind: Literal["env", "data", "run"],
    name: str,
):
    """Find an object by name."""
    objects = list(kind)
    for obj in objects:
        if obj['name'] == name:
            return obj
    return None

def list(
    kind: Literal["env", "data", "run"],
):
    """List objects."""

    if kind in api_endpoints and "list" in api_endpoints[kind]:
        return(api.get(api_endpoints[kind]["list"]))

    else:
        raise ValueError("Invalid kind.")
    
def delete(
  kind: Literal["env", "data", "run"],
  uuid: str,	
):
    """Delete an object."""
    if kind in api_endpoints and "delete" in api_endpoints[kind]:
        return api.delete(api_endpoints[kind]["delete"].format(uuid=uuid))

    else:
        raise ValueError("Invalid kind.")

def clone(
    kind: Literal["env", "data", "run"],
    uuid: str,
    new_name: str,
):
    """Clone an object."""
    if kind in api_endpoints and "clone" in api_endpoints[kind]:
        return api.post(api_endpoints[kind]["clone"].format(uuid=uuid), {"name": new_name})
    else:
        raise ValueError("Invalid kind.")


def run(
    uuid: str
):
	"""Start a run."""
	return api.post(f"run/{uuid}/start/")

def init(
    uuid: str
):
    """Initialize a run."""
    return api.post(f"run/{uuid}/init/")

def audit(
    uuid: str
):
    """Audit a run_element."""
    return api.post(f"run-element/{uuid}/audit/")

