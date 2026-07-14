"""Federation engine — lifecycle, SSO, logout orchestration."""
from __future__ import annotations

FEDERATION_LIFECYCLE = (
    "registration", "verification", "activation", "federation",
    "provisioning", "synchronization", "update", "suspension",
    "recovery", "reactivation", "deprovisioning", "archiving", "deletion",
)

LIFECYCLE_TRANSITIONS = {
    "registered": {"verify": "verified", "suspend": "suspended"},
    "verified": {"activate": "active", "federate": "federated"},
    "active": {"federate": "federated", "suspend": "suspended", "update": "active"},
    "federated": {"suspend": "suspended", "deprovision": "deprovisioned"},
    "suspended": {"recover": "recovering", "reactivate": "active", "deprovision": "deprovisioned"},
    "recovering": {"reactivate": "active", "verify": "verified"},
    "deprovisioned": {"archive": "archived"},
    "archived": {"delete": "deleted"},
}


def transition_lifecycle(current_state: str, event: str) -> str | None:
    return LIFECYCLE_TRANSITIONS.get(current_state, {}).get(event)


def build_federation_catalog() -> dict:
    return {
        "capabilities": [
            "identity_federation", "enterprise_sso", "identity_broker",
            "identity_translation", "identity_synchronization", "cross_tenant_federation",
            "cross_organization_trust", "identity_delegation", "jit_provisioning",
            "federated_logout", "single_logout", "identity_discovery", "dynamic_trust",
        ],
        "protocols": ["oidc", "saml", "ldap", "scim"],
        "lifecycle_states": list(FEDERATION_LIFECYCLE),
        "standards": [
            "OIDC 1.0", "SAML 2.0", "SCIM 2.0", "OAuth 2.0", "OpenID Connect Federation",
            "NIST SP 800-63", "ISO/IEC 29146", "Zero Trust Architecture",
        ],
        "industry_packs": [
            "banking", "government", "healthcare", "education", "taxation",
            "erp", "saas", "construction", "retail", "manufacturing", "ngo",
        ],
    }


def orchestrate_federated_logout(
    *,
    session_ref: str,
    provider_protocol: str,
    single_logout_enabled: bool,
) -> dict:
    if not single_logout_enabled:
        return {"logout_type": "local", "session_ref": session_ref, "idp_logout": False}
    idp_logout_urls = {
        "oidc": "/protocol/openid-connect/logout",
        "saml": "/saml/logout",
    }
    return {
        "logout_type": "federated" if provider_protocol in idp_logout_urls else "local",
        "session_ref": session_ref,
        "idp_logout": provider_protocol in idp_logout_urls,
        "idp_logout_path": idp_logout_urls.get(provider_protocol),
    }


def resolve_identity(
    *,
    external_subject: str,
    email: str | None,
    existing_links: list[dict],
) -> dict:
    """Identity resolution — match external identity to internal user."""
    for link in existing_links:
        if link.get("external_subject") == external_subject:
            return {"resolved": True, "user_id": link.get("user_id"), "method": "existing_link"}
    if email:
        for link in existing_links:
            if link.get("email") == email:
                return {"resolved": True, "user_id": link.get("user_id"), "method": "email_match"}
    return {"resolved": False, "method": "jit_required", "external_subject": external_subject}
