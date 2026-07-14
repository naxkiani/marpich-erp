"""Deterministic what-if simulation; authoritative changes remain in source contexts."""
def simulate(twin: dict, scenario_type: str, proposed_change: dict) -> dict:
    if scenario_type == "access_change":
        before, after = set(twin["role_refs"]), set(proposed_change.get("role_refs", []))
        return {"would_allow_access": bool(after), "roles_added": sorted(after - before), "roles_removed": sorted(before - after), "mutation_applied": False}
    if scenario_type == "lifecycle_transition":
        return {"from_state": twin.get("lifecycle_state"), "to_state": proposed_change.get("lifecycle_state"), "would_disable_sessions": proposed_change.get("lifecycle_state") in {"suspended", "deprovisioned", "deleted"}, "mutation_applied": False}
    if scenario_type == "federation_disable":
        return {"federation_links_affected": len(twin["federation_link_refs"]), "would_require_local_auth": True, "mutation_applied": False}
    raise ValueError("unsupported_scenario_type")
