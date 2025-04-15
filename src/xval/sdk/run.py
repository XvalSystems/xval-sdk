from typing import Literal
from .. import api

def start(uuid: str):
    """Start a run."""
    return api.post(f"/run/{uuid}/start/")

def init(uuid: str):
    """Initialize a run."""
    return api.post(f"/run/{uuid}/init/")

def audit(uuid: str):
    """Audit a run_element."""
    return api.post(f"/run-element/{uuid}/audit/")

def list_audits(
    kind: Literal["run", "run_element"],
    uuid: str
):
    """Get results for a run."""
    return api.get(api.endpoints[kind]["audits"].format(uuid=uuid))

