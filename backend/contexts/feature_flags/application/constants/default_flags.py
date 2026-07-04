"""Default feature flags seeded on tenant provision."""
from __future__ import annotations

DEFAULT_FLAGS: tuple[tuple[str, str, bool, dict[str, bool] | None], ...] = (
    ("saved_listings", "Saved Listings", False, None),
    ("image_attachments", "Image Attachments", True, None),
    ("multi_org", "Multi Organization", False, {"bank": True}),
    (
        "advanced_analytics",
        "Advanced Analytics",
        False,
        {"hospital": True, "bank": True, "university": True},
    ),
)
