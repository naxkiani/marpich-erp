"""Integration event — versioned, published via messaging adapter."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExampleCreatedIntegrationEvent:
    event_type: str = "module_id.example.created"
    version: int = 1
    tenant_id: str = ""
    example_id: str = ""
    name: str = ""
