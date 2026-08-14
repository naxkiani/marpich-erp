"""ReBAC engine — relation-tuple checks (Zanzibar-style, AuthZ-owned)."""
from __future__ import annotations

# Default action → relation mapping when context.relation is omitted.
ACTION_RELATION_MAP: dict[str, str] = {
    "read": "viewer",
    "view": "viewer",
    "list": "viewer",
    "write": "editor",
    "update": "editor",
    "create": "editor",
    "delete": "owner",
    "admin": "owner",
    "manage": "owner",
}


def parse_resource_uri(resource: str) -> tuple[str, str] | None:
    """Parse marpich://{type}/{id}[/{...}] → (object_type, object_id)."""
    if not resource.startswith("marpich://"):
        return None
    parts = resource.replace("marpich://", "").split("/")
    if len(parts) < 2:
        return None
    return parts[0].lower(), parts[1]


def resolve_required_relation(*, action: str, facts: dict) -> str | None:
    if facts.get("relation"):
        return str(facts["relation"]).strip().lower()
    if facts.get("required_relation"):
        return str(facts["required_relation"]).strip().lower()
    action_key = (action or "").strip().lower().split(".")[-1]
    return ACTION_RELATION_MAP.get(action_key)


def evaluate_rebac(
    *,
    tuples: list[dict],
    subject_id: str,
    object_type: str,
    object_id: str,
    relation: str,
    subject_type: str = "user",
) -> tuple[str | None, list[str]]:
    """Return allow/None and reason codes. Missing match → None (defer to other models)."""
    ot = object_type.lower()
    oid = object_id
    rel = relation.lower()
    st = subject_type.lower()
    sid = subject_id

    for t in tuples:
        if not t.get("active", True):
            continue
        if (
            t.get("object_type") == ot
            and t.get("object_id") == oid
            and t.get("relation") == rel
            and t.get("subject_type") == st
            and t.get("subject_id") == sid
        ):
            return "allow", [f"rebac.allow.{rel}.{ot}/{oid}"]
        # owner implies editor/viewer
        if (
            rel in {"viewer", "editor"}
            and t.get("object_type") == ot
            and t.get("object_id") == oid
            and t.get("relation") == "owner"
            and t.get("subject_type") == st
            and t.get("subject_id") == sid
        ):
            return "allow", [f"rebac.allow.owner_implies_{rel}.{ot}/{oid}"]
        if (
            rel == "viewer"
            and t.get("object_type") == ot
            and t.get("object_id") == oid
            and t.get("relation") == "editor"
            and t.get("subject_type") == st
            and t.get("subject_id") == sid
        ):
            return "allow", [f"rebac.allow.editor_implies_viewer.{ot}/{oid}"]

    return None, [f"rebac.no_match.{rel}.{ot}/{oid}"]
