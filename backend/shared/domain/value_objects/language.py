"""BCP 47 language tag (simplified)."""
from __future__ import annotations

import re
from dataclasses import dataclass

_LANGUAGE_PATTERN = re.compile(r"^[a-z]{2}(-[A-Z]{2})?$")


@dataclass(frozen=True, slots=True)
class Language:
    tag: str

    def __post_init__(self) -> None:
        normalized = self.tag.strip().replace("_", "-")
        parts = normalized.split("-")
        if len(parts) == 2:
            normalized = f"{parts[0].lower()}-{parts[1].upper()}"
        else:
            normalized = parts[0].lower()
        if not _LANGUAGE_PATTERN.match(normalized):
            raise ValueError(f"Invalid language tag: {self.tag}")
        object.__setattr__(self, "tag", normalized)

    @property
    def code(self) -> str:
        return self.tag.split("-")[0]

    def __str__(self) -> str:
        return self.tag
