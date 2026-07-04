"""Write command — one per use case."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateExampleCommand:
    tenant_id: str
    name: str
    correlation_id: str
