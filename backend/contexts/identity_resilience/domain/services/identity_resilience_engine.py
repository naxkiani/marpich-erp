"""Identity resilience engine — multi-region HA helpers."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from contexts.identity_resilience.domain.aggregates.identity_resilience_platform import (
    ResilienceCapability,
    WorkerRole,
    WorkerStatus,
    WorkerType,
)

POLICY_KEYS = [
    "identity_resilience.multi_region.enabled",
    "identity_resilience.failover.auto_trigger",
    "identity_resilience.worker.heartbeat_timeout_seconds",
    "identity_resilience.replication.lag_threshold_seconds",
]

CAPABILITY_LABELS = {
    ResilienceCapability.REGION_CATALOG.value: "Region Catalog",
    ResilienceCapability.WORKER_REGISTRY.value: "Worker Registry",
    ResilienceCapability.DIRECTORY_SYNC_WORKER_HA.value: "Directory Sync Worker HA",
    ResilienceCapability.RISK_SCORING_WORKER_HA.value: "Risk Scoring Worker HA",
    ResilienceCapability.LEADER_ELECTION.value: "Leader Election",
    ResilienceCapability.FAILOVER_ORCHESTRATION.value: "Failover Orchestration",
    ResilienceCapability.REPLICATION_HEALTH.value: "Replication Health",
    ResilienceCapability.POLICY_DRIVEN_RESILIENCE.value: "Policy-Driven Resilience",
    ResilienceCapability.RESILIENCE_DASHBOARD.value: "Resilience Dashboard",
    ResilienceCapability.IDENTITY_RESILIENCE_API.value: "Identity Resilience API",
}

DEFAULT_REGIONS = [
    {"region_id": "eu-west-1", "display_name": "EU West", "is_primary": True},
    {"region_id": "us-east-1", "display_name": "US East", "is_primary": False},
]

WORKER_TYPES = [
    {"worker_type": WorkerType.DIRECTORY_SYNC.value, "label": "Directory Sync Worker"},
    {"worker_type": WorkerType.RISK_SCORING.value, "label": "Risk Scoring Worker"},
]


def list_capability_catalog() -> list[dict]:
    return [
        {"capability": c.value, "label": CAPABILITY_LABELS.get(c.value, c.name.replace("_", " ").title())}
        for c in ResilienceCapability
    ]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def list_default_regions() -> list[dict]:
    return list(DEFAULT_REGIONS)


def list_worker_types() -> list[dict]:
    return list(WORKER_TYPES)


def dependency_map() -> dict:
    return {
        "nodes": [
            {"id": "identity_resilience", "type": "platform", "label": "Identity Resilience"},
            {"id": "directory", "type": "platform", "label": "Directory"},
            {"id": "identity_risk", "type": "platform", "label": "Identity Risk"},
        ],
        "edges": [
            {"from": "identity_resilience", "to": "directory", "type": "worker_ha"},
            {"from": "identity_resilience", "to": "identity_risk", "type": "worker_ha"},
        ],
    }


def is_heartbeat_stale(
    last_heartbeat_at: datetime | None,
    *,
    timeout_seconds: int,
    now: datetime | None = None,
) -> bool:
    if last_heartbeat_at is None:
        return True
    reference = now or datetime.now(UTC)
    return reference - last_heartbeat_at > timedelta(seconds=timeout_seconds)


def select_failover_target(
    workers: list[dict],
    *,
    worker_type: str,
    exclude_region_id: str,
) -> dict | None:
    candidates = [
        w
        for w in workers
        if w.get("worker_type") == worker_type
        and w.get("region_id") != exclude_region_id
        and w.get("status") != WorkerStatus.OFFLINE.value
    ]
    if not candidates:
        return None
    standbys = [w for w in candidates if w.get("role") == WorkerRole.STANDBY.value]
    pool = standbys or candidates
    return sorted(pool, key=lambda w: w.get("region_id", ""))[0]


def build_dashboard(
    *,
    profile: dict | None,
    regions: list[dict],
    workers: list[dict],
    failovers: list[dict],
) -> dict:
    leaders = [w for w in workers if w.get("role") == WorkerRole.LEADER.value]
    offline = [w for w in workers if w.get("status") == WorkerStatus.OFFLINE.value]
    degraded_regions = [r for r in regions if r.get("health") != "healthy"]
    return {
        "summary": {
            "capabilities": len(list_capability_catalog()),
            "regions": len(regions),
            "workers": len(workers),
            "leaders": len(leaders),
            "offline_workers": len(offline),
            "degraded_regions": len(degraded_regions),
            "failover_events": len(failovers),
        },
        "profile": profile,
        "region_health": {r["region_id"]: r["health"] for r in regions},
    }
