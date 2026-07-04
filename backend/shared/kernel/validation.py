"""Format validators — no business rules."""
from __future__ import annotations

import re

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$")


def is_valid_email(value: str) -> bool:
    return bool(_EMAIL_PATTERN.match(value.strip()))


def is_valid_slug(value: str) -> bool:
    return bool(_SLUG_PATTERN.match(value.strip().lower()))


def normalize_slug(value: str) -> str:
    slug = value.strip().lower()
    if not is_valid_slug(slug):
        raise ValueError(f"Invalid slug: {value}")
    return slug
