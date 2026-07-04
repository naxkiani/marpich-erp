"""Default locales seeded for new tenants."""
from __future__ import annotations

DEFAULT_LOCALES: list[tuple[str, str, str, bool]] = [
    ("en", "English", "ltr", True),
    ("fa", "فارسی", "rtl", False),
]
