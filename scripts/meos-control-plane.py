#!/usr/bin/env python3
"""P399 Universal Control Plane CLI. Orchestrates existing factories. No blind execution."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_p399 import COMMANDS, dispatch, evaluate  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="status", choices=COMMANDS)
    parser.add_argument("--environment", default="LOCAL")
    parser.add_argument("--provider", default="")
    parser.add_argument("--operation", default="INSPECT")
    parser.add_argument("--role", default="VIEWER")
    parser.add_argument("--query", default="")
    parser.add_argument("--tenant", default="platform")
    parser.add_argument("--idempotency-key", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--authorize", action="store_true")
    args = parser.parse_args()
    data = dispatch(
        args.command,
        environment=args.environment,
        provider_name=args.provider or None,
        operation=args.operation,
        role=args.role,
        dry_run=args.dry_run or args.command != "execute",
        authorize=args.authorize,
        tenant_id=args.tenant,
        query=args.query,
        idempotency_key=args.idempotency_key,
    )
    if args.command == "status":
        data = evaluate()
    print(json.dumps(data, indent=2, sort_keys=True, default=str))
    if args.command == "status":
        print(f"P399_STATUS={data.get('P399_STATUS')}")
        print("G26_READY=FALSE")
        print("PRODUCTION_READY=False")
    else:
        print(f"executed={data.get('executed', False)}")
        status = data.get("STATUS")
        if status is None and isinstance(data.get("dashboard"), dict):
            status = data["dashboard"].get("status")
        print(f"STATUS={status}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
