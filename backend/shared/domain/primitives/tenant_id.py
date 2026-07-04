from __future__ import annotations

from dataclasses import dataclass

from .value_object import ValueObject


@dataclass(frozen=True)
class TenantId(ValueObject):
    value: str

    def __post_init__(self) -> None:
        import re

        normalized = self.value.strip().lower()
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,62}[a-z0-9]", normalized):
            raise ValueError(f"Invalid tenant_id: {self.value}")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value
