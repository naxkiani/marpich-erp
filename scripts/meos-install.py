#!/usr/bin/env python3
"""MEOS one-command installer (P354). Default PLAN_ONLY. Does not print secrets."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_release_engine import PLATFORMS, installation_plan  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="MEOS installer — PLAN_ONLY unless --execute")
    parser.add_argument("--platform", default="LOCAL", choices=list(PLATFORMS))
    parser.add_argument("--execute", action="store_true", help="Declare execution intent; still plan unless --apply")
    parser.add_argument("--apply", action="store_true", help="LOCAL/DEMO only; never production")
    parser.add_argument("--production", action="store_true", help="Claim production (still requires EXT-G26 evidence)")
    parser.add_argument("--authorize-migrate", action="store_true")
    parser.add_argument("--authorize-destructive", action="store_true")
    parser.add_argument("--db-host", default="")
    parser.add_argument("--db-port", default="")
    args = parser.parse_args()
    plan = installation_plan(
        args.platform,
        execute=args.execute,
        apply=args.apply,
        claim_production=args.production,
        authorize_migrate=args.authorize_migrate,
        authorize_destructive=args.authorize_destructive,
        db_host=args.db_host,
        db_port=args.db_port,
    )
    print(json.dumps(plan, indent=2, sort_keys=True))
    print("INSTALLATION_PLAN=TRUE")
    print(f"MODE={plan['mode']}")
    print(f"PLATFORM={plan['platform']}")
    print(f"STATUS={plan['status']}")
    print("SECRETS_IN_OUTPUT=FALSE")
    print("PROCESS_HEALTH=/api/v1/health")
    print("APPLICATION_READINESS=/api/v1/ready")
    print("PRODUCTION_READINESS=python3 scripts/meos-ext-g26-readiness.py")
    if plan["blocked"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
