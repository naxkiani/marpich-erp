from __future__ import annotations
from dataclasses import dataclass
from shared.domain.events.integration_event import IntegrationEvent
class _TwinEvent(IntegrationEvent):
    @property
    def source_context(self) -> str: return "identity_digital_twin"
    @property
    def event_version(self) -> int: return 1
@dataclass(frozen=True, kw_only=True)
class TwinCreatedIntegration(_TwinEvent):
    twin_ref: str
    identity_ref: str
    @property
    def event_name(self) -> str: return "identity_twin.created"
    def to_payload(self) -> dict: return {"twin_ref": self.twin_ref, "identity_ref": self.identity_ref}
@dataclass(frozen=True, kw_only=True)
class TwinSynchronizedIntegration(_TwinEvent):
    twin_ref: str
    source_event: str
    @property
    def event_name(self) -> str: return "identity_twin.synchronized"
    def to_payload(self) -> dict: return {"twin_ref": self.twin_ref, "source_event": self.source_event}
@dataclass(frozen=True, kw_only=True)
class TwinSimulationCompletedIntegration(_TwinEvent):
    simulation_ref: str
    twin_ref: str
    scenario_type: str
    @property
    def event_name(self) -> str: return "identity_twin.simulation.completed"
    def to_payload(self) -> dict: return {"simulation_ref": self.simulation_ref, "twin_ref": self.twin_ref, "scenario_type": self.scenario_type}
@dataclass(frozen=True, kw_only=True)
class TwinDriftDetectedIntegration(_TwinEvent):
    alert_ref: str
    twin_ref: str
    severity: str
    @property
    def event_name(self) -> str: return "identity_twin.drift.detected"
    def to_payload(self) -> dict: return {"alert_ref": self.alert_ref, "twin_ref": self.twin_ref, "severity": self.severity}
