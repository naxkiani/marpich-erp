"""Identity broker engine — routing, discovery, federation orchestration."""
from __future__ import annotations

from typing import Any


def route_authentication(
    *,
    tenant_id: str,
    email: str | None = None,
    domain: str | None = None,
    hint: str | None = None,
    providers: list[dict],
) -> dict:
    """Identity routing — select IdP based on hints, domain, or discovery."""
    enabled = [p for p in providers if p.get("enabled", True)]
    if not enabled:
        return {"routed": False, "reason": "no_providers", "provider": None}

    if hint:
        for p in enabled:
            if p.get("provider_ref") == hint or p.get("name", "").lower() == hint.lower():
                return {"routed": True, "provider": p, "routing_method": "hint"}

    if domain:
        for p in enabled:
            domains = (p.get("config") or {}).get("domains", [])
            if domain.lower() in [d.lower() for d in domains]:
                return {"routed": True, "provider": p, "routing_method": "domain"}

    if email and "@" in email:
        email_domain = email.split("@", 1)[1].lower()
        for p in enabled:
            domains = (p.get("config") or {}).get("domains", [])
            if email_domain in [d.lower() for d in domains]:
                return {"routed": True, "provider": p, "routing_method": "email_domain"}

    default = next((p for p in enabled if (p.get("config") or {}).get("default")), None)
    if default:
        return {"routed": True, "provider": default, "routing_method": "default"}

    if len(enabled) == 1:
        return {"routed": True, "provider": enabled[0], "routing_method": "single_provider"}

    return {"routed": False, "reason": "discovery_required", "providers": [p.get("provider_ref") for p in enabled]}


def discover_identity_providers(
    *,
    email: str | None = None,
    tenant_id: str | None = None,
    providers: list[dict],
) -> dict:
    """Identity discovery — return available IdPs for user."""
    route = route_authentication(
        tenant_id=tenant_id or "",
        email=email,
        domain=email.split("@")[1] if email and "@" in email else None,
        providers=providers,
    )
    if route.get("routed"):
        return {
            "discovery_method": route["routing_method"],
            "recommended_provider": route["provider"],
            "available_providers": [route["provider"]],
        }
    return {
        "discovery_method": "manual_selection",
        "recommended_provider": None,
        "available_providers": [p for p in providers if p.get("enabled", True)],
    }


def broker_federation_flow(
    *,
    provider: dict,
    raw_claims: dict[str, Any],
    transformed_claims: dict[str, Any],
) -> dict:
    """Broker flow result — normalized federation response."""
    return {
        "brokered": True,
        "provider_ref": provider.get("provider_ref"),
        "protocol": provider.get("protocol"),
        "external_subject": transformed_claims.get("sub") or raw_claims.get("sub"),
        "email": transformed_claims.get("email") or raw_claims.get("email"),
        "display_name": transformed_claims.get("name") or raw_claims.get("name"),
        "claims": transformed_claims,
    }
