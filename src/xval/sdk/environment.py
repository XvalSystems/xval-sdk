from typing import Literal
from .. import api

def switch_to_env(
    uuid: str
):
    """Switch to an environment."""
    return api.post(f"/users/environment/{uuid}/switch/") 