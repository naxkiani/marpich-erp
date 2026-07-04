from __future__ import annotations

DEFAULT_METRICS: tuple[tuple[str, str, str], ...] = (
    ("events.total", "Total Events", "*"),
    ("users.created", "Users Created", "identity.user.created"),
    ("users.logged_in", "User Logins", "identity.user.logged_in"),
    ("encounters.completed", "Encounters Completed", "hospital.encounter.completed"),
    ("workflows.completed", "Workflows Completed", "workflow.process.completed"),
    ("documents.uploaded", "Documents Uploaded", "documents.document.uploaded"),
)

DEFAULT_WIDGETS: list[dict] = [
    {"type": "metric", "metric_key": "events.total", "title": "Total Events"},
    {"type": "metric", "metric_key": "users.created", "title": "New Users"},
    {"type": "metric", "metric_key": "users.logged_in", "title": "Logins"},
    {"type": "metric", "metric_key": "encounters.completed", "title": "Encounters"},
]
