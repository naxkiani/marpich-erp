"""Tenant identifier — mandatory on every aggregate and event."""
from __future__ import annotations

import re
from dataclasses import dataclass

_TENANT_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$")


@dataclass(frozen=True, slots=True)
class TenantId:
    value: str

    @classmethod
    def create(cls, value: str) -> TenantId:
        normalized = value.strip().lower()
        if not _TENANT_PATTERN.match(normalized):
            raise ValueError(f"Invalid tenant ID: {value}")
        return cls(normalized)

    def __str__(self) -> str:
        return self.value
