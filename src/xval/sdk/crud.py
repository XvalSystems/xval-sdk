from typing import Literal
from .. import api
from .. import config
import re

def is_uuid(s: str) -> bool:
	uuid_pattern = re.compile(
		r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', 
		re.IGNORECASE
  )
	return bool(uuid_pattern.match(s))


def retrieve(
    kind: Literal["env", "data", "run", "run_element"],
    name_or_uuid: str,
) -> dict:
    """
    Retrieve an object by name or uuid.Using uuid is faster than name lookup.
    
    Args:
        kind: The kind of object to retrieve.
        name_or_uuid: The name or uuid of the object to retrieve.
        
    Returns:
        dict: The object.
        
    """

    if is_uuid(name_or_uuid):
      return api.get(api.endpoints[kind]["retrieve"].format(uuid=name_or_uuid))

    return _find_object(kind, name_or_uuid)

def list_(
    kind: Literal["env", "data", "run"],
):
    """List objects."""
    if kind in api.endpoints and "list" in api.endpoints[kind]:
        return api.get(api.endpoints[kind]["list"])
    else:
        raise ValueError("Invalid kind.")
    
def _find_object(
    kind: Literal["env", "data", "run"],
    name: str,
):
    """Find an object by name."""
    objects = list_(kind)
    for obj in objects:
        if obj['name'] == name:
            return obj
    raise ValueError(f"No {kind} found with name '{name}' in Environment '{config.config.current_environment}'")

def update(
    kind: Literal["run_element"], 
    name_or_uuid: str, 
    data: dict
) -> None:
    """Update an object."""
    if is_uuid(name_or_uuid):
      return api.patch(
        api.endpoints[kind]['update'].format(uuid=name_or_uuid), 
        data
      )

    obj = _find_object(kind, name_or_uuid)

def clone(
    kind: Literal["env", "data", "run"],
    uuid: str,
    new_name: str,
):
    """Clone an object."""
    if kind in api.endpoints and "clone" in api.endpoints[kind]:
        return api.post(api.endpoints[kind]["clone"].format(uuid=uuid), {"name": new_name})
    else:
        raise ValueError("Invalid kind.")
    
def delete(
    kind: Literal["env", "data", "run"],
    uuid: str,    
):
    """Delete an object."""
    if kind in api.endpoints and "delete" in api.endpoints[kind]:
        return api.delete(api.endpoints[kind]["delete"].format(uuid=uuid))
    else:
        raise ValueError("Invalid kind.")