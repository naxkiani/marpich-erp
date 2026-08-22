#!/usr/bin/env python3
"""P397 Release Factory CLI. Coordinates existing meos-release.py / P385 / P386. No second CI."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_p397 import factory  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        nargs="?",
        default="status",
        choices=("status", "validate", "plan", "build", "inspect", "promote", "verify", "history", "revoke"),
    )
    parser.add_argument("--from", dest="source", default="DEV")
    parser.add_argument("--to", dest="target", default="TEST")
    parser.add_argument("--release", default="")
    args = parser.parse_args()
    data = factory(args.command, source=args.source, target=args.target, release_id=args.release or None)
    print(json.dumps(data, indent=2, sort_keys=True, default=str))
    if args.command == "status":
        print(f"P397_STATUS={data.get('P397_STATUS')}")
        print(f"VERSION={data.get('VERSION')}")
        print(f"IMAGE_DIGEST={data.get('IMAGE_DIGEST')}")
        print("G26_READY=FALSE")
        print("PRODUCTION_READY=False")
    else:
        print(f"executed={data.get('executed')}")
        print(f"STATUS={data.get('STATUS')}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
