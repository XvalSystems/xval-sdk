import pytest
import sys
import os

sys.path.append(os.path.abspath("xval-sdk"))

if __name__ == "__main__":
    pytest.main([
        "-v", "tests/test_examples.py::test_clone_run_and_start_audit",
    ])
    