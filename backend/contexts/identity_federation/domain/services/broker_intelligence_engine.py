"""Broker intelligence — conflict resolution, merge, duplicate detection, dynamic routing."""
from __future__ import annotations


def detect_duplicates(*, candidates: list[dict], email: str | None = None, external_subject: str | None = None) -> dict:
    matches = []
    for c in candidates:
        score = 0
        reasons = []
        if email and c.get("email") and c["email"].lower() == email.lower():
            score += 80
            reasons.append("email_match")
        if external_subject and c.get("external_subject") == external_subject:
            score += 90
            reasons.append("subject_match")
        if score >= 80:
            matches.append({"candidate": c, "confidence": min(100, score), "reasons": reasons})
    return {"duplicates": matches, "count": len(matches)}


def resolve_identity_conflict(*, primary: dict, secondary: dict, strategy: str = "prefer_verified") -> dict:
    strategies = {
        "prefer_verified": lambda a, b: a if a.get("verified") else b if b.get("verified") else a,
        "prefer_newest": lambda a, b: a if (a.get("updated_at") or "") >= (b.get("updated_at") or "") else b,
        "merge_attributes": lambda a, b: {**b, **{k: v for k, v in a.items() if v}},
    }
    resolver = strategies.get(strategy, strategies["prefer_verified"])
    resolved = resolver(primary, secondary)
    return {
        "strategy": strategy,
        "resolved": resolved,
        "conflict": True,
    }


def merge_identities(*, left: dict, right: dict) -> dict:
    merged = {**right, **left}
    merged["merged_from"] = [left.get("id"), right.get("id")]
    merged["merge_status"] = "merged"
    return merged


def dynamic_route(
    *,
    email: str | None,
    risk_score: int,
    trust_score: int,
    providers: list[dict],
    prefer_mfa: bool = True,
) -> dict:
    """Policy-aware dynamic routing — high risk → stronger IdP / step-up path."""
    enabled = [p for p in providers if p.get("enabled", True)]
    if not enabled:
        return {"routed": False, "reason": "no_providers"}
    if risk_score >= 70:
        mfa_capable = [p for p in enabled if (p.get("config") or {}).get("mfa_required") or prefer_mfa]
        target = mfa_capable[0] if mfa_capable else enabled[0]
        return {
            "routed": True,
            "provider": target,
            "method": "risk_elevated",
            "requires_step_up": True,
            "trust_score": trust_score,
            "risk_score": risk_score,
        }
    if email and "@" in email:
        domain = email.split("@", 1)[1].lower()
        for p in enabled:
            domains = (p.get("config") or {}).get("domains") or []
            if domain in [d.lower() for d in domains]:
                return {
                    "routed": True,
                    "provider": p,
                    "method": "domain_policy",
                    "requires_step_up": False,
                    "trust_score": trust_score,
                    "risk_score": risk_score,
                }
    return {
        "routed": True,
        "provider": enabled[0],
        "method": "default",
        "requires_step_up": trust_score < 40,
        "trust_score": trust_score,
        "risk_score": risk_score,
    }
