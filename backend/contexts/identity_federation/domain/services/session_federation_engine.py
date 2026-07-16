"""Session federation — cross-app/tenant sessions, SLO, revocation, transfer."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta


def create_federated_session(
    *,
    session_ref: str,
    user_id: str,
    provider_ref: str,
    protocol: str,
    apps: list[str] | None = None,
    tenant_scope: list[str] | None = None,
    ttl_hours: int = 8,
) -> dict:
    now = datetime.now(UTC)
    return {
        "session_ref": session_ref,
        "user_id": user_id,
        "provider_ref": provider_ref,
        "protocol": protocol,
        "apps": apps or [],
        "tenant_scope": tenant_scope or [],
        "status": "active",
        "created_at": now.isoformat(),
        "expires_at": (now + timedelta(hours=ttl_hours)).isoformat(),
        "revocable": True,
        "slo_capable": True,
    }


def attach_app_session(session: dict, *, app_id: str) -> dict:
    apps = list(session.get("apps") or [])
    if app_id not in apps:
        apps.append(app_id)
    session = {**session, "apps": apps}
    return session


def global_logout(sessions: list[dict], *, user_id: str) -> dict:
    revoked = []
    for s in sessions:
        if s.get("user_id") == user_id and s.get("status") == "active":
            s["status"] = "revoked"
            revoked.append(s.get("session_ref"))
    return {
        "user_id": user_id,
        "revoked_sessions": revoked,
        "mode": "global_logout",
        "synchronized": True,
    }


def transfer_session(session: dict, *, target_app: str, target_tenant: str | None = None) -> dict:
    if session.get("status") != "active":
        return {"transferred": False, "reason": "session_not_active"}
    result = attach_app_session(session, app_id=target_app)
    if target_tenant:
        scope = list(result.get("tenant_scope") or [])
        if target_tenant not in scope:
            scope.append(target_tenant)
        result["tenant_scope"] = scope
    return {"transferred": True, "session": result}


def session_audit_entry(*, session_ref: str, action: str, actor: str, detail: dict | None = None) -> dict:
    return {
        "session_ref": session_ref,
        "action": action,
        "actor": actor,
        "detail": detail or {},
        "at": datetime.now(UTC).isoformat(),
    }
