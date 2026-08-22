#!/usr/bin/env python3
"""P396 deployment orchestrator CLI. Coordinates existing factories. Does not deploy production."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_p396 import orchestrate  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        nargs="?",
        default="status",
        choices=("status", "plan", "validate", "deploy", "verify", "rollback", "history", "approve"),
    )
    parser.add_argument("--release", default="")
    parser.add_argument("--provider", default="")
    parser.add_argument("--environment", default="staging")
    parser.add_argument("--authorize", action="store_true")
    args = parser.parse_args()
    data = orchestrate(
        args.command,
        release=args.release or None,
        provider_name=args.provider or None,
        environment=args.environment,
        authorize=args.authorize,
    )
    print(json.dumps(data, indent=2, sort_keys=True, default=str))
    if args.command == "status":
        print(f"P396_STATUS={data.get('P396_STATUS')}")
        print("G26_READY=FALSE")
        print("PRODUCTION_READY=False")
    else:
        print(f"executed={data.get('executed')}")
        print(f"STATUS={data.get('STATUS')}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
