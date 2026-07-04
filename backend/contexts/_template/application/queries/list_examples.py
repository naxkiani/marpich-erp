"""Read query — no side effects."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ListExamplesQuery:
    tenant_id: str
    limit: int = 50
    offset: int = 0
