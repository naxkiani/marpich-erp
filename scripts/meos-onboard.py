#!/usr/bin/env python3
"""MEOS tenant onboarding planner (P355). PLAN_ONLY. No production tenants."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_product_engine import onboarding_plan  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="MEOS onboarding — does not create production tenants")
    parser.add_argument("--authorize-create-tenant", action="store_true")
    parser.add_argument("--production", action="store_true")
    args = parser.parse_args()
    plan = onboarding_plan(
        authorize_create_tenant=args.authorize_create_tenant,
        production=args.production,
    )
    print(json.dumps(plan, indent=2, sort_keys=True))
    print("PRODUCTION_TENANT_CREATED=FALSE")
    print("FAKE_CUSTOMER=FALSE")
    if plan["blocked"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
