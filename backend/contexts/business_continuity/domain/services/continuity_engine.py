"""Enterprise Business Continuity Platform engine."""
from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime

from contexts.business_continuity.domain.aggregates.continuity_platform import (
    ContinuityCapability,
    CriticalityTier,
    FailoverStatus,
    PlanStatus,
    PlanType,
    TestStatus,
)

PLATFORM_CATALOG: dict[str, dict] = {
    ContinuityCapability.DISASTER_RECOVERY.value: {"label": "Disaster Recovery", "plan_type": PlanType.DR.value},
    ContinuityCapability.BUSINESS_CONTINUITY_PLAN.value: {
        "label": "Business Continuity Plan",
        "plan_type": PlanType.BCP.value,
    },
    ContinuityCapability.BACKUP_STRATEGY.value: {
        "label": "Backup Strategy",
        "delegates_to": "data_protection",
        "no_duplication": True,
    },
    ContinuityCapability.RECOVERY_POINT_OBJECTIVE.value: {"label": "Recovery Point Objective (RPO)", "metric": "hours"},
    ContinuityCapability.RECOVERY_TIME_OBJECTIVE.value: {"label": "Recovery Time Objective (RTO)", "metric": "hours"},
    ContinuityCapability.FAILOVER.value: {"label": "Failover", "automated": False},
    ContinuityCapability.HIGH_AVAILABILITY.value: {"label": "High Availability", "ha": True},
    ContinuityCapability.REPLICATION.value: {"label": "Replication", "sync": True},
    ContinuityCapability.EMERGENCY_OPERATIONS.value: {
        "label": "Emergency Operations",
        "delegates_to": "security_incident",
        "no_duplication": True,
    },
    ContinuityCapability.RECOVERY_TESTING.value: {"label": "Recovery Testing", "audit_trail": True},
    ContinuityCapability.CONTINUITY_DASHBOARD.value: {"label": "Continuity Dashboard"},
}

POLICY_KEYS = [
    "continuity.rpo.default_hours",
    "continuity.rto.default_hours",
    "continuity.failover.auto_trigger_threshold",
    "continuity.testing.frequency_days",
    "continuity.ha.replication_lag_threshold",
]

DEFAULT_SEED_PLANS: list[dict] = [
    {
        "title": "Core ERP Disaster Recovery Plan",
        "plan_type": PlanType.DR.value,
        "criticality_tier": CriticalityTier.TIER_1.value,
        "rpo_hours": 1,
        "rto_hours": 4,
        "recovery_steps": ["Activate DR site", "Restore database from backup", "Validate services"],
    },
    {
        "title": "Finance Business Continuity Plan",
        "plan_type": PlanType.BCP.value,
        "criticality_tier": CriticalityTier.TIER_1.value,
        "rpo_hours": 4,
        "rto_hours": 8,
        "recovery_steps": ["Notify finance leadership", "Switch to manual processing", "Reconcile transactions"],
    },
    {
        "title": "Treasury Operations Continuity",
        "plan_type": PlanType.BCP.value,
        "criticality_tier": CriticalityTier.TIER_2.value,
        "rpo_hours": 2,
        "rto_hours": 6,
        "recovery_steps": ["Activate treasury backup site", "Verify liquidity positions"],
        "delegated_to": "treasury",
    },
    {
        "title": "Emergency Operations Center Plan",
        "plan_type": PlanType.EMERGENCY_OPS.value,
        "criticality_tier": CriticalityTier.TIER_1.value,
        "rpo_hours": 0,
        "rto_hours": 1,
        "recovery_steps": ["Activate EOC", "Establish communication channels", "Assign incident roles"],
        "delegated_to": "security_incident",
    },
]

DEFAULT_SEED_BACKUPS: list[dict] = [
    {
        "name": "Database Full Backup",
        "backup_type": "full",
        "frequency_hours": 6,
        "retention_days": 30,
        "rpo_hours": 6,
    },
    {
        "name": "Transaction Log Incremental",
        "backup_type": "incremental",
        "frequency_hours": 1,
        "retention_days": 14,
        "rpo_hours": 1,
    },
    {
        "name": "Configuration Snapshot",
        "backup_type": "snapshot",
        "frequency_hours": 24,
        "retention_days": 90,
        "rpo_hours": 24,
    },
]


def list_capability_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in PLATFORM_CATALOG.items()]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def list_criticality_tiers() -> list[dict]:
    return [
        {"tier": t.value, "label": t.value.replace("_", " ").title()}
        for t in CriticalityTier
    ]


def dependency_map() -> dict:
    nodes = [{"id": "business_continuity", "type": "platform", "label": "Business Continuity Platform"}]
    edges = []
    for mod in ("data_protection", "security_incident", "workflow", "treasury", "audit"):
        nodes.append({"id": mod, "type": "module", "label": mod})
        edges.append({"from": mod, "to": "business_continuity", "type": "supports_continuity"})
    for svc in ("policy",):
        nodes.append({"id": svc, "type": "shared_service", "label": svc})
        edges.append({"from": "business_continuity", "to": svc, "type": "delegates"})
    return {"nodes": nodes, "edges": edges, "no_continuity_duplication": True}


def compute_ha_status(*, profile: dict | None, failovers: list[dict]) -> dict:
    active_failovers = [f for f in failovers if f.get("status") in (
        FailoverStatus.INITIATED.value,
        FailoverStatus.IN_PROGRESS.value,
    )]
    return {
        "ha_enabled": profile.get("ha_enabled", True) if profile else True,
        "replication_enabled": profile.get("replication_enabled", True) if profile else True,
        "active_failovers": len(active_failovers),
        "availability_status": "degraded" if active_failovers else "healthy",
        "uptime_target_pct": 99.9,
    }


def compute_replication_status(*, strategies: list[dict], lag_threshold_seconds: int = 30) -> dict:
    encrypted = len([s for s in strategies if s.get("encrypted")])
    return {
        "strategies_count": len(strategies),
        "encrypted_backups": encrypted,
        "replication_lag_threshold_seconds": lag_threshold_seconds,
        "estimated_lag_seconds": 12,
        "lag_within_threshold": True,
        "delegates_encryption_to": "data_protection",
    }


def build_rpo_rto_summary(*, plans: list[dict], backups: list[dict], profile: dict | None) -> dict:
    active_plans = [p for p in plans if p.get("status") == PlanStatus.ACTIVE.value]
    rpo_values = [p.get("rpo_hours", 0) for p in active_plans]
    rto_values = [p.get("rto_hours", 0) for p in active_plans]
    backup_rpo = [b.get("rpo_hours", 0) for b in backups]

    return {
        "rpo": {
            "default_hours": profile.get("default_rpo_hours", 4) if profile else 4,
            "min_plan_hours": min(rpo_values) if rpo_values else None,
            "max_plan_hours": max(rpo_values) if rpo_values else None,
            "min_backup_hours": min(backup_rpo) if backup_rpo else None,
            "plans_count": len(active_plans),
        },
        "rto": {
            "default_hours": profile.get("default_rto_hours", 8) if profile else 8,
            "min_plan_hours": min(rto_values) if rto_values else None,
            "max_plan_hours": max(rto_values) if rto_values else None,
            "plans_count": len(active_plans),
        },
    }


def build_dashboard(
    *,
    profile: dict | None,
    plans: list[dict],
    backups: list[dict],
    failovers: list[dict],
    tests: list[dict],
    lag_threshold: int = 30,
) -> dict:
    active_plans = [p for p in plans if p.get("status") == PlanStatus.ACTIVE.value]
    by_type: dict[str, int] = defaultdict(int)
    by_tier: dict[str, int] = defaultdict(int)
    for plan in active_plans:
        by_type[plan.get("plan_type", "unknown")] += 1
        by_tier[plan.get("criticality_tier", "unknown")] += 1

    passed_tests = [t for t in tests if t.get("status") == TestStatus.PASSED.value]
    failed_tests = [t for t in tests if t.get("status") == TestStatus.FAILED.value]
    completed_failovers = [f for f in failovers if f.get("status") == FailoverStatus.COMPLETED.value]

    return {
        "summary": {
            "capabilities": len(PLATFORM_CATALOG),
            "active_plans": len(active_plans),
            "backup_strategies": len(backups),
            "failover_events": len(failovers),
            "recovery_tests": len(tests),
            "tests_passed": len(passed_tests),
            "tests_failed": len(failed_tests),
            "failovers_completed": len(completed_failovers),
            "enabled_tiers": profile.get("enabled_tiers", []) if profile else [],
        },
        "by_plan_type": dict(by_type),
        "by_criticality_tier": dict(by_tier),
        "rpo_rto": build_rpo_rto_summary(plans=plans, backups=backups, profile=profile),
        "high_availability": compute_ha_status(profile=profile, failovers=failovers),
        "replication": compute_replication_status(strategies=backups, lag_threshold_seconds=lag_threshold),
        "recent_tests": sorted(tests, key=lambda t: t.get("created_at", ""), reverse=True)[:5],
        "recent_failovers": sorted(failovers, key=lambda f: f.get("created_at", ""), reverse=True)[:5],
        "delegation": {
            "data_protection_backup_encryption": True,
            "security_incident_emergency_ops": True,
            "workflow_emergency_lock": True,
            "local_continuity_duplication": False,
        },
        "generated_at": datetime.now(UTC).isoformat(),
    }


def simulate_recovery_test(
    *,
    plan: dict,
    test_type: str = "full",
) -> dict:
    rto_target = plan.get("rto_hours", 8)
    rpo_target = plan.get("rpo_hours", 4)
    tier_factor = {"tier_1": 0.85, "tier_2": 0.95, "tier_3": 1.05}.get(
        plan.get("criticality_tier", "tier_2"), 0.95
    )
    rto_achieved = round(rto_target * tier_factor, 1)
    rpo_achieved = round(rpo_target * tier_factor * 0.9, 1)
    passed = rto_achieved <= rto_target and rpo_achieved <= rpo_target

    return {
        "test_type": test_type,
        "rto_target_hours": rto_target,
        "rpo_target_hours": rpo_target,
        "rto_achieved_hours": rto_achieved,
        "rpo_achieved_hours": rpo_achieved,
        "passed": passed,
        "findings": [] if passed else [
            f"RTO: {rto_achieved}h vs target {rto_target}h",
            f"RPO: {rpo_achieved}h vs target {rpo_target}h",
        ],
    }
