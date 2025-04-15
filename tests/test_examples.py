import sys
from pathlib import Path

import random
import string

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from xval.examples import (
	clone_run_and_audit,
)

import xval as xv

def test_clone_run_and_start_audit():
	run_name = "Clone Test " + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
	clone_run_and_audit.main(run_name)
	run = xv.retrieve("run", run_name)
	audits = xv.list_audits("run", run["uuid"])

	assert len(audits) > 0

	xv.delete("run", run["uuid"])
