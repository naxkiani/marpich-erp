"""Enterprise Identity Analytics — trends, distributions, executive insights."""
from __future__ import annotations

from datetime import UTC, datetime


def build_identity_analytics(
    *,
    providers: list[dict],
    partners: list[dict],
    trusts: list[dict],
    sessions: list[dict] | None = None,
    audit_entries: list[dict] | None = None,
    risk_scores: list[int] | None = None,
    trust_scores: list[int] | None = None,
) -> dict:
    sessions = sessions or []
    audit = audit_entries or []
    risks = risk_scores or []
    trusts_scores = trust_scores or [int(t.get("trust_score", 50)) for t in trusts]

    failed = [a for a in audit if a.get("decision") in ("deny", "failed", "rejected")]
    policy_violations = [a for a in audit if a.get("event_type", "").startswith("policy")]

    return {
        "authentication_trends": {
            "total_sessions": len(sessions),
            "active_sessions": sum(1 for s in sessions if s.get("status") == "active"),
            "failed_logins": len(failed),
        },
        "federation_trends": {
            "providers": len(providers),
            "enabled_providers": sum(1 for p in providers if p.get("enabled", True)),
            "partners": len(partners),
            "protocols": _count_by(providers, "protocol"),
        },
        "identity_lifecycle": {
            "trust_relationships": len(trusts),
            "audit_events": len(audit),
        },
        "provisioning_statistics": {
            "jit_events": sum(1 for a in audit if "provision" in str(a.get("event_type", ""))),
        },
        "synchronization_statistics": {
            "sync_events": sum(1 for a in audit if "sync" in str(a.get("event_type", ""))),
        },
        "failed_logins": len(failed),
        "risk_distribution": _bucket(risks),
        "trust_distribution": _bucket(trusts_scores),
        "policy_violations": len(policy_violations),
        "certificate_status": {"healthy": True, "rotation_due": False},
        "generated_at": datetime.now(UTC).isoformat(),
    }


def _count_by(items: list[dict], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for item in items:
        k = str(item.get(key, "unknown"))
        out[k] = out.get(k, 0) + 1
    return out


def _bucket(scores: list[int]) -> dict[str, int]:
    buckets = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    for s in scores:
        if s >= 85:
            buckets["critical"] += 1
        elif s >= 70:
            buckets["high"] += 1
        elif s >= 40:
            buckets["medium"] += 1
        else:
            buckets["low"] += 1
    return buckets


def executive_report(analytics: dict, *, insights: list[dict] | None = None) -> dict:
    return {
        "report_type": "executive",
        "summary": {
            "federation_health": analytics["federation_trends"],
            "risk_distribution": analytics["risk_distribution"],
            "trust_distribution": analytics["trust_distribution"],
            "failed_logins": analytics["failed_logins"],
            "policy_violations": analytics["policy_violations"],
        },
        "ai_insights": insights or [],
        "kpis": {
            "sso_adoption_proxy": analytics["authentication_trends"]["active_sessions"],
            "provider_coverage": analytics["federation_trends"]["enabled_providers"],
        },
        "generated_at": datetime.now(UTC).isoformat(),
    }


def operational_report(analytics: dict) -> dict:
    return {
        "report_type": "operational",
        "queues": {
            "failed_logins": analytics["failed_logins"],
            "policy_violations": analytics["policy_violations"],
            "sync_events": analytics["synchronization_statistics"]["sync_events"],
            "provision_events": analytics["provisioning_statistics"]["jit_events"],
        },
        "certificate_status": analytics["certificate_status"],
        "generated_at": datetime.now(UTC).isoformat(),
    }


def synthesize_ai_insights(analytics: dict) -> list[dict]:
    insights = []
    if analytics["failed_logins"] > 10:
        insights.append({
            "type": "anomaly",
            "severity": "high",
            "message": "Elevated failed login volume in federation audit trail",
            "recommendation": "Review IdP health and enable step-up for high-risk routes",
        })
    high_risk = analytics["risk_distribution"].get("high", 0) + analytics["risk_distribution"].get("critical", 0)
    if high_risk > 0:
        insights.append({
            "type": "risk",
            "severity": "medium",
            "message": f"{high_risk} identities in high/critical risk bands",
            "recommendation": "Run identity health scoring and privilege review",
        })
    if analytics["federation_trends"]["enabled_providers"] == 0:
        insights.append({
            "type": "configuration",
            "severity": "high",
            "message": "No enabled identity providers",
            "recommendation": "Register and activate at least one IdP via admin portal",
        })
    if not insights:
        insights.append({
            "type": "health",
            "severity": "low",
            "message": "Federation analytics within normal operating range",
            "recommendation": "Continue monitoring trust and certificate rotation",
        })
    return insights
