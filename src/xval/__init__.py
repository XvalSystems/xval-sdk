"""
xval - Xval's Python SDK and CLI
"""

import importlib.metadata

__version__ = importlib.metadata.version("xval")

from typing import Literal
import xval.api as api

api_endpoints = {
    "env": {
        "list": "/users/environment/", 
        "create": "/users/environment/",
        "retrieve": "/users/environment/{uuid}/"
    },
    "data": {
        "list": "/data/", 
        "create": "/data/", 
        "delete": "/data/{uuid}/",
        "retrieve": "/data/{uuid}/"
    },
    "run": {
      "list": "/run/", 
      "create": "/run/", 
      "delete": "/run/{uuid}/", 
      "clone": "/run/{uuid}/clone/",
      "retrieve": "/run/{uuid}/",
    #   "results": "/run/{uuid}/results_detail/",
      "audits": "/run/{uuid}/audits/",
    },
    "run_element": {
        "update": "/run-element/{uuid}/",
        "retrieve": "/run-element/{uuid}/"
    },
}

def find_object(
    kind: Literal["env", "data", "run"],
    name: str,
):
    """Find an object by name."""
    objects = list_(kind)
    for obj in objects:
        if obj['name'] == name:
            return obj
    return None

def retrieve(
    kind: Literal["env", "data", "run", "run_element"],
    uuid: str,
):
    """Retrieve an object by uuid."""
    return api.get(api_endpoints[kind]["retrieve"].format(uuid=uuid))

def list_(
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
	return api.post(f"/run/{uuid}/start/")

def init(
    uuid: str
):
    """Initialize a run."""
    return api.post(f"/run/{uuid}/init/")

def audit(
    uuid: str
):
    """Audit a run_element."""
    return api.post(f"/run-element/{uuid}/audit/")

def list_audits(
    kind: Literal["run", "run_element"],
    uuid: str
):
    """Get results for a run."""
    return api.get(api_endpoints[kind]["audits"].format(uuid=uuid))


def switch_to_env(
    uuid: str
):
    """Switch to an environment."""
    return api.post(f"/users/environment/{uuid}/switch/")


def update(
    kind: Literal["run_element"], 
    uuid: str, 
    data: dict
) -> None:
    """Update an object."""
    return api.patch(api_endpoints[kind]['update'].format(uuid=uuid), data)

 