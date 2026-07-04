"""Application DTO — not HTTP schema, not domain entity."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExampleDto:
    id: str
    name: str
    tenant_id: str
