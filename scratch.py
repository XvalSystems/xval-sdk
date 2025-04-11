import sys
from pathlib import Path

base_path = Path(__file__).parent
src_path = Path(__file__).resolve().parent / 'src'
sys.path.append(str(src_path))

from src.xval import commands as cmd

def do():
    cmd.audit("FDA STAT 2", no_config=False)

if __name__ == "__main__":
    do()
