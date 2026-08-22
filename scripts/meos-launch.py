#!/usr/bin/env python3
"""MEOS unified launch CLI (P354). Orchestration only. Does not print secrets."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_launch_engine import (  # noqa: E402
    deploy,
    list_environments,
    normalize_env,
    plan,
    preflight,
    refuse_overrides,
    rollback,
    status,
    verify,
)


def _print(data: dict) -> None:
    print(json.dumps(data, indent=2, sort_keys=True, default=str))


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    refused = refuse_overrides(argv)
    if refused:
        _print(refused)
        print("DEPLOYMENT=BLOCKED")
        print("FORBIDDEN_OVERRIDE=TRUE")
        print("G26_READY=FALSE")
        return 2

    parser = argparse.ArgumentParser(description="MEOS launch control — existing mechanisms only")
    parser.add_argument(
        "command",
        choices=["list", "preflight", "plan", "deploy", "verify", "status", "rollback"],
    )
    parser.add_argument("--env", default=None, help="local|demo|vps|hostinger-vps|aws|azure|gcp|kubernetes|production")
    parser.add_argument("--confirm", default="", help="Must be 'yes' to execute deploy/rollback")
    args = parser.parse_args(argv)

    if args.command == "list":
        data = list_environments()
        _print(data)
        print("ORCHESTRATION_ONLY=TRUE")
        return 0

    env = args.env or ("local" if args.command != "status" else None)
    if env:
        try:
            normalize_env(env)
        except ValueError as exc:
            print(json.dumps({"status": "DEPLOYMENT_BLOCKED", "error": str(exc)}))
            return 2

    if args.command == "preflight":
        data = preflight(env)
    elif args.command == "plan":
        data = plan(env)
    elif args.command == "deploy":
        data = deploy(env, confirm=args.confirm)
    elif args.command == "verify":
        data = verify(env)
    elif args.command == "rollback":
        data = rollback(env, confirm=args.confirm)
    else:
        data = status(env)

    _print(data)
    print(f"COMMAND={args.command.upper()}")
    print(f"ENVIRONMENT={data.get('environment') or data.get('TARGET') or data.get('ENVIRONMENT') or data.get('DEPLOY_TARGET')}")
    print(f"STATUS={data.get('status')}")
    print("G26_READY=FALSE")
    print("P313=NOT_CERTIFIED")
    print("GO_LIVE_AUTHORIZATION=NOT_APPROVED")
    print("LOCALHOST_IS_PRODUCTION=FALSE")
    print("COMPOSE_IS_PRODUCTION=FALSE")
    if args.command == "plan":
        print("DEPLOYMENT_OCCURS=FALSE")
    executed = data.get("executed")
    if executed is False and args.command in {"deploy", "rollback"}:
        return 2
    if data.get("status") in {"DEPLOYMENT_BLOCKED"}:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
