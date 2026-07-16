"""LMS sync integration events — published by ECF after connector execute."""
from __future__ import annotations

from dataclasses import dataclass, field

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class LmsBatchSyncedIntegration(IntegrationEvent):
    """Normalized LMS batch for university/school ACL consumers."""

    provider: str
    operation: str
    instance_ref: str
    execution_ref: str
    courses: list[dict] = field(default_factory=list)
    enrollments: list[dict] = field(default_factory=list)
    grades: list[dict] = field(default_factory=list)

    @property
    def event_name(self) -> str:
        return f"integration.{self.provider}.batch.synced"

    @property
    def source_context(self) -> str:
        return "enterprise_connector_framework"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "provider": self.provider,
            "operation": self.operation,
            "instance_ref": self.instance_ref,
            "execution_ref": self.execution_ref,
            "courses": self.courses,
            "enrollments": self.enrollments,
            "grades": self.grades,
        }
