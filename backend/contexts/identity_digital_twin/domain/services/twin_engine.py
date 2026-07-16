"""Pure projection and dashboard rules for identity twins."""
def normalize_projection(projection: dict) -> dict:
    return {"attributes": dict(projection.get("attributes") or {}), "role_refs": sorted(set(projection.get("role_refs") or [])), "session_refs": sorted(set(projection.get("session_refs") or [])), "federation_link_refs": sorted(set(projection.get("federation_link_refs") or [])), "lifecycle_state": projection.get("lifecycle_state"), "source_version": str(projection.get("source_version") or "")}
def dashboard(twins: list[dict], alerts: list[dict]) -> dict:
    return {"twins_count": len(twins), "active_sessions_referenced": sum(len(t["session_refs"]) for t in twins), "open_drift_alerts": sum(a["status"] == "open" for a in alerts), "critical_drift_alerts": sum(a["severity"] == "critical" and a["status"] == "open" for a in alerts)}
