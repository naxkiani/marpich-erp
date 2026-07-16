"""Enterprise Integration Studio aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class StudioCapability(StrEnum):
    VISUAL_API_BUILDER = "visual_api_builder"
    VISUAL_CONNECTOR_BUILDER = "visual_connector_builder"
    VISUAL_WORKFLOW_BUILDER = "visual_workflow_builder"
    VISUAL_EVENT_DESIGNER = "visual_event_designer"
    DATA_MAPPING = "data_mapping"
    TRANSFORMATION = "transformation"
    TESTING = "testing"
    MOCK_SERVICES = "mock_services"
    API_DOCUMENTATION = "api_documentation"
    CONNECTOR_MARKETPLACE = "connector_marketplace"
    VERSIONING = "versioning"
    DEPLOYMENT = "deployment"
    DEVELOPER_PORTAL = "developer_portal"
    CITIZEN_DEVELOPER_WORKSPACE = "citizen_developer_workspace"


class ArtifactType(StrEnum):
    API = "api"
    CONNECTOR = "connector"
    WORKFLOW = "workflow"
    EVENT = "event"
    MAPPING = "mapping"
    MOCK = "mock"


class ArtifactStatus(StrEnum):
    DRAFT = "draft"
    TESTED = "tested"
    PUBLISHED = "published"
    DEPLOYED = "deployed"
    ARCHIVED = "archived"


class DeploymentStatus(StrEnum):
    PENDING = "pending"
    DEPLOYING = "deploying"
    LIVE = "live"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass(eq=False, kw_only=True)
class StudioProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    api_builder_enabled: bool = True
    connector_builder_enabled: bool = True
    workflow_builder_enabled: bool = True
    event_designer_enabled: bool = True
    testing_enabled: bool = True
    mock_services_enabled: bool = True
    marketplace_enabled: bool = True
    citizen_workspace_enabled: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, profile_ref: str) -> StudioProfile:
        return cls(id=UniqueId.generate(), tenant_id=tenant_id, profile_ref=profile_ref)

    def to_dict(self) -> dict:
        return {
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "api_builder_enabled": self.api_builder_enabled,
            "connector_builder_enabled": self.connector_builder_enabled,
            "workflow_builder_enabled": self.workflow_builder_enabled,
            "event_designer_enabled": self.event_designer_enabled,
            "testing_enabled": self.testing_enabled,
            "mock_services_enabled": self.mock_services_enabled,
            "marketplace_enabled": self.marketplace_enabled,
            "citizen_workspace_enabled": self.citizen_workspace_enabled,
        }


@dataclass(eq=False, kw_only=True)
class StudioProject(AggregateRoot):
    tenant_id: str
    project_ref: str
    name: str
    workspace_type: str
    description: str = ""
    artifact_count: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        project_ref: str,
        name: str,
        workspace_type: str = "developer",
        description: str = "",
    ) -> StudioProject:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            project_ref=project_ref,
            name=name,
            workspace_type=workspace_type,
            description=description,
        )

    def to_dict(self) -> dict:
        return {
            "project_ref": self.project_ref,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "workspace_type": self.workspace_type,
            "description": self.description,
            "artifact_count": self.artifact_count,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class StudioArtifact(AggregateRoot):
    tenant_id: str
    artifact_ref: str
    project_ref: str
    name: str
    artifact_type: str
    status: str
    version: str = "1.0.0"
    designer_graph: dict = field(default_factory=dict)
    mapping: dict = field(default_factory=dict)
    transformation: dict = field(default_factory=dict)
    openapi: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        artifact_ref: str,
        project_ref: str,
        name: str,
        artifact_type: str,
        designer_graph: dict | None = None,
        mapping: dict | None = None,
        transformation: dict | None = None,
        openapi: dict | None = None,
        metadata: dict | None = None,
    ) -> StudioArtifact:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            artifact_ref=artifact_ref,
            project_ref=project_ref,
            name=name,
            artifact_type=artifact_type,
            status=ArtifactStatus.DRAFT.value,
            designer_graph=designer_graph or {},
            mapping=mapping or {},
            transformation=transformation or {},
            openapi=openapi or {},
            metadata=metadata or {},
        )

    def to_dict(self) -> dict:
        return {
            "artifact_ref": self.artifact_ref,
            "project_ref": self.project_ref,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "artifact_type": self.artifact_type,
            "status": self.status,
            "version": self.version,
            "designer_graph": self.designer_graph,
            "mapping": self.mapping,
            "transformation": self.transformation,
            "openapi": self.openapi,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class StudioVersion(AggregateRoot):
    tenant_id: str
    version_ref: str
    artifact_ref: str
    version: str
    changelog: str = ""
    published_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls,
        *,
        tenant_id: str,
        version_ref: str,
        artifact_ref: str,
        version: str,
        changelog: str = "",
    ) -> StudioVersion:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            version_ref=version_ref,
            artifact_ref=artifact_ref,
            version=version,
            changelog=changelog,
        )

    def to_dict(self) -> dict:
        return {
            "version_ref": self.version_ref,
            "artifact_ref": self.artifact_ref,
            "version": self.version,
            "changelog": self.changelog,
            "published_at": self.published_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class StudioDeployment(AggregateRoot):
    tenant_id: str
    deployment_ref: str
    artifact_ref: str
    version: str
    environment: str
    status: str
    deployed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        deployment_ref: str,
        artifact_ref: str,
        version: str,
        environment: str = "sandbox",
    ) -> StudioDeployment:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            deployment_ref=deployment_ref,
            artifact_ref=artifact_ref,
            version=version,
            environment=environment,
            status=DeploymentStatus.PENDING.value,
        )

    def mark_live(self) -> None:
        self.status = DeploymentStatus.LIVE.value
        self.deployed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "deployment_ref": self.deployment_ref,
            "artifact_ref": self.artifact_ref,
            "version": self.version,
            "environment": self.environment,
            "status": self.status,
            "deployed_at": self.deployed_at.isoformat() if self.deployed_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class StudioTestRun(AggregateRoot):
    tenant_id: str
    test_ref: str
    artifact_ref: str
    status: str
    assertions_passed: int = 0
    assertions_failed: int = 0
    duration_ms: float = 0.0
    mock_used: bool = False
    report: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def run(
        cls,
        *,
        tenant_id: str,
        test_ref: str,
        artifact_ref: str,
        status: str,
        assertions_passed: int,
        assertions_failed: int,
        duration_ms: float,
        mock_used: bool = False,
        report: dict | None = None,
    ) -> StudioTestRun:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            test_ref=test_ref,
            artifact_ref=artifact_ref,
            status=status,
            assertions_passed=assertions_passed,
            assertions_failed=assertions_failed,
            duration_ms=duration_ms,
            mock_used=mock_used,
            report=report or {},
        )

    def to_dict(self) -> dict:
        return {
            "test_ref": self.test_ref,
            "artifact_ref": self.artifact_ref,
            "status": self.status,
            "assertions_passed": self.assertions_passed,
            "assertions_failed": self.assertions_failed,
            "duration_ms": self.duration_ms,
            "mock_used": self.mock_used,
            "report": self.report,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class MarketplaceListing(AggregateRoot):
    tenant_id: str
    listing_ref: str
    connector_type: str
    name: str
    publisher: str
    version: str
    installs: int = 0
    rating: float = 5.0
    certified: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def list_connector(
        cls,
        *,
        tenant_id: str,
        listing_ref: str,
        connector_type: str,
        name: str,
        publisher: str,
        version: str,
        certified: bool = True,
    ) -> MarketplaceListing:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            listing_ref=listing_ref,
            connector_type=connector_type,
            name=name,
            publisher=publisher,
            version=version,
            certified=certified,
        )

    def to_dict(self) -> dict:
        return {
            "listing_ref": self.listing_ref,
            "connector_type": self.connector_type,
            "name": self.name,
            "publisher": self.publisher,
            "version": self.version,
            "installs": self.installs,
            "rating": self.rating,
            "certified": self.certified,
            "created_at": self.created_at.isoformat(),
        }
