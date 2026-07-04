"""Feature flag integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class FlagCreatedIntegration(IntegrationEvent):
    flag_key: str

    @property
    def event_name(self) -> str:
        return "feature_flag.created"

    @property
    def source_context(self) -> str:
        return "feature_flags"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"flag_key": self.flag_key}


@dataclass(frozen=True, kw_only=True)
class FlagUpdatedIntegration(IntegrationEvent):
    flag_key: str
    version: int

    @property
    def event_name(self) -> str:
        return "feature_flag.updated"

    @property
    def source_context(self) -> str:
        return "feature_flags"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"flag_key": self.flag_key, "version": self.version}


@dataclass(frozen=True, kw_only=True)
class RolloutUpdatedIntegration(IntegrationEvent):
    flag_key: str
    percentage: int
    stage: str

    @property
    def event_name(self) -> str:
        return "feature_flag.rollout.updated"

    @property
    def source_context(self) -> str:
        return "feature_flags"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"flag_key": self.flag_key, "percentage": self.percentage, "stage": self.stage}


@dataclass(frozen=True, kw_only=True)
class EmergencyDisabledIntegration(IntegrationEvent):
    flag_key: str
    reason: str

    @property
    def event_name(self) -> str:
        return "feature_flag.emergency_disabled"

    @property
    def source_context(self) -> str:
        return "feature_flags"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"flag_key": self.flag_key, "reason": self.reason}


@dataclass(frozen=True, kw_only=True)
class RollbackAppliedIntegration(IntegrationEvent):
    flag_key: str
    target_version: int

    @property
    def event_name(self) -> str:
        return "feature_flag.rollback.applied"

    @property
    def source_context(self) -> str:
        return "feature_flags"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"flag_key": self.flag_key, "target_version": self.target_version}
