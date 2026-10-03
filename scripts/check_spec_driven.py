#!/usr/bin/env python3
"""Run bundle validation and isolated tests from any working directory."""
from pathlib import Path
import os
import subprocess
import sys
root=Path(__file__).resolve().parents[1]/'plugins/spec-driven-development'
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
for command in ([sys.executable,'scripts/validate_package.py'],[sys.executable,'-m','unittest','discover','-s','tests','-v']):
    result=subprocess.run(command,cwd=root,env=env)
    if result.returncode:sys.exit(result.returncode)
