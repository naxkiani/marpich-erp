#!/usr/bin/env python3
"""P364 environment factory. Reference-only. Never mints credentials."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_env_classify import classify  # noqa: E402

ENVS = ("LOCAL", "DEMO", "STAGING", "PRE_PRODUCTION", "PRODUCTION")


def profile(env_id: str) -> dict:
    classify(env_id)
    production = False
    refs = "REFERENCE_ONLY" if env_id in {"STAGING", "PRE_PRODUCTION", "PRODUCTION"} else "LOCAL_OPTIONAL"
    return {
        "ENVIRONMENT_ID": env_id,
        "identity": "NON_PRODUCTION" if env_id != "PRODUCTION" else "REQUIRES_G26_EVIDENCE",
        "production": production,
        "APP_ENV": env_id.lower(),
        "DEPLOYMENT_MODE": "PLAN_ONLY" if env_id == "PRODUCTION" else env_id,
        "DATABASE_URL_REFERENCE": refs,
        "REDIS_URL_REFERENCE": refs,
        "SECRET_PROVIDER": "NOT_STORED",
        "SECRET_REFERENCE": "READY_FOR_CREDENTIALS" if refs == "REFERENCE_ONLY" else "optional_env",
        "APP_DOMAIN": "app.example.com",
        "API_DOMAIN": "api.example.com",
        "AUTH_DOMAIN": "auth.example.com",
        "ADMIN_DOMAIN": "admin.example.com",
        "STORAGE_PROVIDER": "READY_FOR_CREDENTIALS" if env_id != "LOCAL" else "optional_minio",
        "TLS_PROVIDER": "PUBLIC_CA_REQUIRED" if env_id in {"PRE_PRODUCTION", "PRODUCTION"} else "NOT_APPLICABLE",
        "IMAGE": "ghcr.io/marpich/marpich-backend",
        "IMAGE_DIGEST": "NOT_AVAILABLE",
        "LOG_LEVEL": "INFO",
        "OBSERVABILITY_PROVIDER": "G23_CONFIGURED",
        "resource_profile": "local" if env_id in {"LOCAL", "DEMO"} else "READY_FOR_CREDENTIALS",
        "equals_production": False,
        "g26_ready": False,
    }


def evaluate() -> dict:
    return {
        "factory": "REFERENCE_ONLY",
        "mints_credentials": False,
        "environments": {env: profile(env) for env in ENVS},
        "promotion": ["LOCAL", "DEMO", "STAGING", "PRE_PRODUCTION", "PRODUCTION"],
        "same_immutable_artifact": True,
        "rebuild_between_environments": False,
        "g26_ready": False,
        "localhost_is_production": False,
        "compose_is_production": False,
    }


def main() -> int:
    if len(sys.argv) == 1:
        data = evaluate()
        print(json.dumps(data, indent=2, sort_keys=True))
        print("ENVIRONMENT_FACTORY=REFERENCE_ONLY")
        print("FAKE_PRODUCTION_CREDENTIALS=FALSE")
        print("G26_READY=FALSE")
        return 0
    import argparse

    from meos_p398 import factory  # noqa: E402

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("status", "inspect", "plan", "validate", "bootstrap", "verify", "drift", "destroy-plan"),
    )
    parser.add_argument("--environment", default="LOCAL")
    parser.add_argument("--provider", default="")
    parser.add_argument("--authorize", action="store_true")
    args = parser.parse_args()
    data = factory(
        args.command,
        environment=args.environment,
        provider_name=args.provider or None,
        authorize=args.authorize,
    )
    print(json.dumps(data, indent=2, sort_keys=True, default=str))
    if args.command == "status":
        print(f"P398_STATUS={data.get('P398_STATUS')}")
        print("G26_READY=FALSE")
        print("PRODUCTION_READY=False")
    else:
        print(f"executed={data.get('executed')}")
        status = data.get("STATUS")
        if status is None and isinstance(data.get("environment"), dict):
            status = data["environment"].get("STATUS")
        print(f"STATUS={status}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
