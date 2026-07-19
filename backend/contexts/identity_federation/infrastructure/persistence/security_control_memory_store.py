"""In-memory security control plane store (P200-B9)."""
from __future__ import annotations

from contexts.identity_federation.domain.aggregates.security_control_platform import (
    CompliancePostureSnapshot,
    RiskAssessment,
    SecurityControl,
    SecurityException,
    ThreatEvent,
)


class SecurityControlMemoryStore:
    controls: dict[str, SecurityControl] = {}
    risks: dict[str, RiskAssessment] = {}
    threats: dict[str, ThreatEvent] = {}
    compliance: dict[str, CompliancePostureSnapshot] = {}
    exceptions: dict[str, SecurityException] = {}
    events: list[dict] = []
    last_zt: dict[str, dict] = {}
    counters: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls.controls.clear()
        cls.risks.clear()
        cls.threats.clear()
        cls.compliance.clear()
        cls.exceptions.clear()
        cls.events.clear()
        cls.last_zt.clear()
        cls.counters.clear()

    @classmethod
    def _next(cls, tenant_id: str, prefix: str) -> str:
        key = f"{tenant_id}:{prefix}"
        cls.counters[key] = cls.counters.get(key, 0) + 1
        return f"{prefix}-{cls.counters[key]:04d}"

    @classmethod
    def append_event(cls, event: dict) -> None:
        cls.events.append(event)
        cls.events = cls.events[-500:]


def get_security_control_store() -> type[SecurityControlMemoryStore]:
    return SecurityControlMemoryStore


def reset_security_control_store() -> None:
    SecurityControlMemoryStore.reset()
