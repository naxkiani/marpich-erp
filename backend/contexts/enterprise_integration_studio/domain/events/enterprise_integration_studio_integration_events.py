"""Enterprise Integration Studio integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class ArtifactCreatedIntegration(IntegrationEvent):
    artifact_ref: str
    artifact_type: str
    project_ref: str

    @property
    def event_name(self) -> str:
        return "enterprise_integration_studio.artifact.created"

    @property
    def source_context(self) -> str:
        return "enterprise_integration_studio"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "artifact_ref": self.artifact_ref,
            "artifact_type": self.artifact_type,
            "project_ref": self.project_ref,
        }


@dataclass(frozen=True, kw_only=True)
class TestCompletedIntegration(IntegrationEvent):
    artifact_ref: str
    test_ref: str
    status: str

    @property
    def event_name(self) -> str:
        return "enterprise_integration_studio.test.completed"

    @property
    def source_context(self) -> str:
        return "enterprise_integration_studio"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"artifact_ref": self.artifact_ref, "test_ref": self.test_ref, "status": self.status}


@dataclass(frozen=True, kw_only=True)
class VersionPublishedIntegration(IntegrationEvent):
    artifact_ref: str
    version: str

    @property
    def event_name(self) -> str:
        return "enterprise_integration_studio.version.published"

    @property
    def source_context(self) -> str:
        return "enterprise_integration_studio"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"artifact_ref": self.artifact_ref, "version": self.version}


@dataclass(frozen=True, kw_only=True)
class DeploymentCompletedIntegration(IntegrationEvent):
    deployment_ref: str
    artifact_ref: str
    environment: str

    @property
    def event_name(self) -> str:
        return "enterprise_integration_studio.deployment.completed"

    @property
    def source_context(self) -> str:
        return "enterprise_integration_studio"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "deployment_ref": self.deployment_ref,
            "artifact_ref": self.artifact_ref,
            "environment": self.environment,
        }


@dataclass(frozen=True, kw_only=True)
class StudioDashboardGeneratedIntegration(IntegrationEvent):
    projects_total: int
    artifacts_total: int
    deployments_live: int

    @property
    def event_name(self) -> str:
        return "enterprise_integration_studio.dashboard.generated"

    @property
    def source_context(self) -> str:
        return "enterprise_integration_studio"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "projects_total": self.projects_total,
            "artifacts_total": self.artifacts_total,
            "deployments_live": self.deployments_live,
        }
