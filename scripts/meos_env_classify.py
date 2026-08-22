"""Shared environment classification — localhost/compose ≠ PRODUCTION."""
from __future__ import annotations

import os

LOCAL_HOSTS = frozenset({"127.0.0.1", "localhost", "::1", "0.0.0.0"})
NON_PROD_PORTS = frozenset({"5433", "5444", "8000", "8080"})
ALLOWED = frozenset({"LOCAL", "DEMO", "STAGING", "PRE_PRODUCTION", "PRODUCTION"})


def classify(
    claimed: str | None = None,
    *,
    host: str | None = None,
    port: str | None = None,
) -> dict:
    claimed_env = (claimed or os.environ.get("MEOS_ENVIRONMENT") or "LOCAL").strip().upper()
    if claimed_env not in ALLOWED:
        claimed_env = "LOCAL"
    pghost = (host or os.environ.get("PGHOST") or os.environ.get("MEOS_PRODUCTION_PGHOST") or "127.0.0.1").strip()
    pgport = str(port or os.environ.get("PGPORT") or os.environ.get("MEOS_PRODUCTION_PGPORT") or "5433").strip()
    local_marker = pghost.lower() in LOCAL_HOSTS or pgport in NON_PROD_PORTS
    compose_marker = os.environ.get("COMPOSE_PROJECT_NAME", "").lower() in {"meosprod", "marpich"}
    if claimed_env == "PRODUCTION" and (local_marker or compose_marker):
        return {
            "claimed": claimed_env,
            "resolved": "LOCAL",
            "production": False,
            "localhost_is_production": False,
            "compose_is_production": False,
            "database_class": "NON_PRODUCTION",
            "pghost": pghost,
            "pgport": pgport,
            "ambiguity": "DANGEROUS_AMBIGUITY",
            "blocked": True,
            "reason": "localhost/compose/dev ports cannot be PRODUCTION",
            "g26_ready": False,
        }
    resolved = "DEMO" if local_marker and (pgport == "5444" or compose_marker) else (
        "LOCAL" if local_marker else claimed_env
    )
    return {
        "claimed": claimed_env,
        "resolved": resolved,
        "production": False,
        "localhost_is_production": False,
        "compose_is_production": False,
        "database_class": "NON_PRODUCTION" if local_marker else "UNKNOWN",
        "pghost": pghost,
        "pgport": pgport,
        "ambiguity": "NONE",
        "blocked": False,
        "reason": "NON_PRODUCTION" if local_marker else "CLAIMED_PRODUCTION_NOT_CERTIFIED"
        if claimed_env == "PRODUCTION"
        else "host_not_local",
        "g26_ready": False,
    }
