"""Localization helpers — not the Localization bounded context."""
from __future__ import annotations

_RTL_LANGUAGES = frozenset({"ar", "fa", "he", "ur"})


def normalize_locale_tag(tag: str) -> str:
    tag = tag.strip().replace("_", "-")
    parts = tag.split("-")
    if len(parts) >= 2:
        return f"{parts[0].lower()}-{parts[1].upper()}"
    return parts[0].lower()


def text_direction(locale_tag: str) -> str:
    code = normalize_locale_tag(locale_tag).split("-")[0]
    return "rtl" if code in _RTL_LANGUAGES else "ltr"
