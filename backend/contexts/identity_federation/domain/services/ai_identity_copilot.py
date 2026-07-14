"""Identity Copilot — explainable assistant for admins (platform AI ACL-ready)."""
from __future__ import annotations


def explain_authentication_decision(*, decision: dict) -> dict:
    action = decision.get("action") or decision.get("recommendation") or "unknown"
    return {
        "topic": "authentication_decision",
        "explanation": (
            f"The federation decision was '{action}' based on risk={decision.get('risk_score', 'n/a')} "
            f"and trust={decision.get('trust_score', 'n/a')}."
        ),
        "factors": decision.get("explanation", {}).get("contributions")
        or decision.get("checks")
        or decision.get("failed_dimensions")
        or [],
        "suggest_next": _next_for_action(str(action)),
    }


def explain_trust_score(*, trust: dict) -> dict:
    return {
        "topic": "trust_score",
        "explanation": (
            f"Composite trust score is {trust.get('trust_score')} ({trust.get('trust_level')}). "
            f"Weakest link: {trust.get('weakest_link', 'n/a')}."
        ),
        "dimensions": trust.get("dimensions") or trust.get("hierarchy") or {},
        "suggest_next": ["Review weakest trust dimension", "Re-evaluate partner certificates"],
    }


def explain_federation_error(*, error_code: str, context: dict | None = None) -> dict:
    catalog = {
        "federation.errors.disabled": "Federation is policy-disabled for this tenant.",
        "federation.errors.no_provider_routed": "No IdP matched email domain or hint.",
        "federation.errors.provider_not_found": "Referenced provider_ref is missing.",
        "pkce_required": "OAuth client requires PKCE; supply code_challenge.",
        "invalid_grant": "Authorization code or refresh token is invalid/expired.",
    }
    return {
        "topic": "federation_error",
        "error_code": error_code,
        "explanation": catalog.get(error_code, f"Federation error: {error_code}"),
        "context": context or {},
        "suggest_next": ["Check provider config", "Validate policy flags", "Inspect audit trail"],
    }


def suggest_policy_improvements(*, analytics: dict) -> list[dict]:
    suggestions = []
    if analytics.get("failed_logins", 0) > 5:
        suggestions.append({
            "policy_key": "federation.risk.step_up.threshold",
            "suggestion": "Lower step-up threshold temporarily during incident spike",
            "priority": "high",
        })
    if analytics.get("federation_trends", {}).get("enabled_providers", 0) > 3:
        suggestions.append({
            "policy_key": "federation.broker.enabled",
            "suggestion": "Enable identity discovery to improve IdP routing accuracy",
            "priority": "medium",
        })
    if not suggestions:
        suggestions.append({
            "policy_key": "federation.zero_trust.enabled",
            "suggestion": "Keep Zero Trust enabled; schedule quarterly trust recalibration",
            "priority": "low",
        })
    return suggestions


def detect_configuration_problems(*, providers: list[dict], mappings_count: int) -> list[dict]:
    problems = []
    for p in providers:
        if p.get("enabled") and not (p.get("config") or {}):
            problems.append({
                "severity": "medium",
                "provider_ref": p.get("provider_ref"),
                "issue": "enabled_without_config",
                "recommendation": "Add issuer/domains metadata",
            })
        if p.get("protocol") in ("oidc", "saml") and mappings_count == 0:
            problems.append({
                "severity": "low",
                "provider_ref": p.get("provider_ref"),
                "issue": "missing_claims_mappings",
                "recommendation": "Create claims mappings for email/sub",
            })
            break
    return problems


def generate_security_recommendations(*, analytics: dict, intelligence: dict | None = None) -> list[dict]:
    recs = []
    if intelligence and intelligence.get("dormant_account"):
        recs.append({"title": "Disable dormant account", "priority": "high"})
    if intelligence and intelligence.get("privilege_escalation_flag"):
        recs.append({"title": "Review privilege escalation", "priority": "critical"})
    if analytics.get("policy_violations", 0) > 0:
        recs.append({"title": "Export policy violation audit", "priority": "medium"})
    if not recs:
        recs.append({"title": "Rotate federation certificates on schedule", "priority": "low"})
    return recs


def summarize_audit_events(*, entries: list[dict], limit: int = 10) -> dict:
    recent = entries[:limit]
    by_type: dict[str, int] = {}
    for e in recent:
        t = str(e.get("event_type", "unknown"))
        by_type[t] = by_type.get(t, 0) + 1
    return {
        "count": len(recent),
        "by_type": by_type,
        "summary": f"Summarized {len(recent)} federation audit events across {len(by_type)} types.",
        "highlights": [
            e.get("event_type") for e in recent if e.get("decision") in ("deny", "step_up", "rejected")
        ][:5],
    }


def assist_administrator(*, question: str, context: dict | None = None) -> dict:
    q = question.lower()
    context = context or {}
    if "trust" in q:
        return explain_trust_score(trust=context.get("trust") or {"trust_score": 50, "trust_level": "medium"})
    if "error" in q or "fail" in q:
        return explain_federation_error(
            error_code=str(context.get("error_code") or "federation.errors.no_provider_routed"),
            context=context,
        )
    if "policy" in q:
        return {
            "topic": "policy",
            "explanation": "Federation policies are evaluated via Policy Engine; never hardcode thresholds.",
            "suggest_next": suggest_policy_improvements(analytics=context.get("analytics") or {}),
        }
    if "audit" in q:
        return summarize_audit_events(entries=context.get("audit") or [])
    return {
        "topic": "general",
        "explanation": (
            "I can explain trust scores, authentication decisions, federation errors, "
            "suggest policy improvements, detect misconfigurations, and summarize audit events."
        ),
        "capabilities": [
            "explain_authentication_decisions",
            "explain_trust_score",
            "explain_federation_errors",
            "suggest_policy_improvements",
            "detect_configuration_problems",
            "generate_security_recommendations",
            "summarize_audit_events",
            "assist_administrators",
        ],
    }


def _next_for_action(action: str) -> list[str]:
    if action in ("deny", "deny_and_investigate"):
        return ["Open security dashboard", "Review user devices", "Trigger incident workflow"]
    if action in ("step_up", "require_mfa", "step_up_and_notify"):
        return ["Complete MFA challenge", "Re-evaluate session trust"]
    return ["Continue federated session", "Monitor continuous verification"]
