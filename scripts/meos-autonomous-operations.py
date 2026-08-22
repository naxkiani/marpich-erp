#!/usr/bin/env python3
"""P400 Autonomous Platform Operations CLI. Policy-governed. No blind execution."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_p400 import COMMANDS, dispatch, evaluate  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="status", choices=COMMANDS)
    parser.add_argument("--environment", default="LOCAL")
    parser.add_argument("--action", default="BACKUP_RETRY")
    parser.add_argument("--fixture", default="")
    parser.add_argument("--plan-id", default="")
    parser.add_argument("--role", default="VIEWER")
    parser.add_argument("--tenant", default="platform")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--authorize", action="store_true")
    parser.add_argument("--pause", action="store_true")
    args = parser.parse_args()
    data = dispatch(
        args.command,
        environment=args.environment,
        action=args.action,
        fixture=args.fixture or None,
        plan_id=args.plan_id or None,
        role=args.role,
        authorize=args.authorize,
        dry_run=args.dry_run or args.command != "execute",
        tenant_id=args.tenant,
        pause=True if args.pause else None,
    )
    if args.command == "status":
        data = evaluate()
    print(json.dumps(data, indent=2, sort_keys=True, default=str))
    if args.command == "status":
        print(f"P400_STATUS={data.get('P400_STATUS')}")
        print("G26_READY=FALSE")
        print("PRODUCTION_READY=False")
    else:
        print(f"executed={data.get('executed', False)}")
        print(f"STATUS={data.get('STATUS')}")
        if data.get("SIMULATION"):
            print("SIMULATION=true")
    return 2


if __name__ == "__main__":
    sys.exit(main())
