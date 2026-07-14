def detect(expected: dict, observed: dict, threshold: int = 1) -> dict:
    fields = [key for key in ("attributes", "role_refs", "session_refs", "federation_link_refs", "lifecycle_state") if expected.get(key) != observed.get(key)]
    severity = "critical" if len(fields) >= max(3, threshold + 2) else "high" if len(fields) >= threshold else "none"
    return {"drift_fields": fields, "severity": severity, "detected": bool(fields)}
