#!/usr/bin/env python3
"""Read-only Git inventory. Caller verifies ownership, fetch freshness and authority."""
import argparse
import json
import sys
from workflow import inspect
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',required=True)
a=p.parse_args()
try:print(json.dumps(inspect(a.repo),indent=2))
except (ValueError,OSError) as e:print(str(e),file=sys.stderr);sys.exit(1)
