#!/usr/bin/env python3
"""MEOS DEMO helpers (P355). Isolated, not production. No production secrets."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSE = ROOT / "infrastructure" / "docker" / "compose" / "docker-compose.dev.yml"


def main() -> int:
    parser = argparse.ArgumentParser(description="DEMO reset/seed/health — NON_PRODUCTION")
    parser.add_argument("command", choices=["reset", "seed", "health", "readiness"])
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    print("CLASS=DEMO")
    print("PRODUCTION=FALSE")
    print("SECRETS=none")
    if args.command == "reset":
        cmd = ["docker", "compose", "-f", str(COMPOSE), "down"]
        print("RESET_COMMAND=" + " ".join(cmd))
        print("NOTE=does not use -v unless operator adds it; data wipe is explicit")
        if args.apply:
            return subprocess.run(cmd, cwd=ROOT, check=False).returncode
        print("MODE=PLAN_ONLY")
        return 0
    if args.command == "seed":
        print("SEED=scripts/dev-up.sh + documented demo credentials in .env.example only")
        print("MODE=PLAN_ONLY" if not args.apply else "APPLY_DEV_UP")
        if args.apply:
            return subprocess.run([str(ROOT / "scripts" / "dev-up.sh")], cwd=ROOT, check=False).returncode
        return 0
    if args.command == "health":
        print("PROCESS_HEALTH=/api/v1/health")
        return 0
    print("APPLICATION_READINESS=/api/v1/ready")
    print("PRODUCTION_READINESS=python3 scripts/meos-ext-g26-readiness.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
