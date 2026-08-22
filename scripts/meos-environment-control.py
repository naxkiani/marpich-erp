#!/usr/bin/env python3
"""P394 environment control plane. Orchestrates existing factories. No production unlock."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_p394 import COMMANDS, control, evaluate  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="status", choices=COMMANDS)
    parser.add_argument("--provider", default="")
    parser.add_argument("--environment", default="LOCAL")
    parser.add_argument("--profile", default="")
    parser.add_argument("--size", default="SMALL")
    parser.add_argument("--authorize", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.command == "status":
        data = evaluate()
    else:
        data = control(
            args.command,
            provider_name=args.provider or None,
            environment=args.environment,
            profile=args.profile or None,
            size=args.size,
            authorize=args.authorize,
        )
    _ = args.dry_run
    print(json.dumps(data, indent=2, sort_keys=True, default=str))
    print(f"P394_STATUS={data.get('P394_STATUS', 'SELF_SERVICE_ENVIRONMENT_PLATFORM_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED')}")
    print(f"executed={data.get('executed', False)}")
    print("G26_READY=FALSE")
    print("PRODUCTION_READY=False")
    return 2


if __name__ == "__main__":
    sys.exit(main())
