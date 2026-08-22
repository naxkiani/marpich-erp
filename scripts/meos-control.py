#!/usr/bin/env python3
"""P389/P390 operator control plane. Reuses existing promote/deploy/G26. No bypass."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_p389 import COMMANDS, dispatch, evaluate  # noqa: E402
from meos_p390 import INFRA_COMMANDS, dispatch_infra, evaluate as p390_evaluate  # noqa: E402
from meos_p392 import FABRIC_COMMANDS, dispatch_fabric, evaluate as p392_evaluate  # noqa: E402

ALL = tuple(dict.fromkeys([*COMMANDS, *INFRA_COMMANDS, *FABRIC_COMMANDS]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="status", choices=ALL)
    parser.add_argument("--target", default="")
    parser.add_argument("--environment", default="LOCAL")
    parser.add_argument("--release", dest="release_id", default="")
    parser.add_argument("--previous-digest", default="")
    parser.add_argument("--deploy", action="store_true")
    parser.add_argument("--authorize", action="store_true")
    args = parser.parse_args()
    if args.command in FABRIC_COMMANDS:
        data = dispatch_fabric(
            args.command,
            release_id=args.release_id or None,
            environment=args.environment,
            previous_digest=args.previous_digest or None,
        )
        if args.command == "fabric-status":
            data = p392_evaluate()
        print(json.dumps(data, indent=2, sort_keys=True, default=str))
        print(f"P392_STATUS={data.get('P392_STATUS', 'DEPLOYMENT_FABRIC_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED')}")
        print(f"executed={data.get('executed', False)}")
        print("PRODUCTION_READY=False")
        return 2
    if args.command in INFRA_COMMANDS:
        data = dispatch_infra(
            args.command,
            target=args.target or None,
            environment=args.environment,
            authorize=args.authorize,
        )
        if args.command == "infra-status":
            data = p390_evaluate()
        print(json.dumps(data, indent=2, sort_keys=True, default=str))
        print(f"P390_STATUS={data.get('P390_STATUS', 'INFRASTRUCTURE_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED')}")
        print(f"PROVISIONED={data.get('PROVISIONED', data.get('provisioned', False))}")
        print("PRODUCTION_READY=False")
        return 2
    data = dispatch(args.command, target=args.target or None, environment=args.environment, deploy=args.deploy)
    if args.command == "status":
        data = evaluate()
    print(json.dumps(data, indent=2, sort_keys=True, default=str))
    if args.command == "status":
        print(f"P389_STATUS={data['P389_STATUS']}")
        print(f"P390_STATUS=INFRASTRUCTURE_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED")
        print("P391_STATUS=MULTI_PLATFORM_LAUNCH_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED")
        print("P392_STATUS=DEPLOYMENT_FABRIC_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED")
        print("P393_STATUS=UNIVERSAL_LAUNCH_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED")
        print("P394_STATUS=SELF_SERVICE_ENVIRONMENT_PLATFORM_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED")
        print("P395_STATUS=LAUNCH_CENTER_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED")
        print("P396_STATUS=DEPLOYMENT_ORCHESTRATION_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED")
        print("P397_STATUS=RELEASE_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED")
        print("P398_STATUS=ENVIRONMENT_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED")
        print("P399_STATUS=CONTROL_PLANE_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED")
        print("P400_STATUS=AUTONOMOUS_PLATFORM_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED")
        print(f"RELEASE={data['RELEASE']}")
        print(f"TARGET={data['TARGET_STATUS']}")
        print(f"ENVIRONMENT={args.environment}")
        print(f"IMAGE={data['IMAGE']}")
        print(f"DIGEST={data['DIGEST']}")
        print(f"DATABASE={data['DATABASE']}")
        print(f"TLS={data['TLS']}")
        print(f"DNS={data['DNS']}")
        print(f"SECRETS={data['SECRET_MANAGER']}")
        print(f"OBSERVABILITY={data['OBSERVABILITY']}")
        print(f"BACKUP={data['BACKUP']}")
        print(f"ROLLBACK={data['ROLLBACK']}")
        print(f"G26={data['G26_STATUS']}")
        print(f"P313={data['P313']}")
        print(f"P0={data['P0']}")
        print(f"GO-LIVE={data['GO_LIVE_AUTHORIZATION']}")
    print(f"PRODUCTION_DEPLOYMENT_LOCKED={data.get('PRODUCTION_DEPLOYMENT_LOCKED', True)}")
    print("PRODUCTION_READY=False")
    if args.command == "g26":
        return 0 if data.get("G26_READY") is True else 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
