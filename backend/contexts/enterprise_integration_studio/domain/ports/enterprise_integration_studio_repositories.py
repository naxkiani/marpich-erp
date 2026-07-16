"""Enterprise Integration Studio repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.enterprise_integration_studio.domain.aggregates.enterprise_integration_studio_platform import (
    MarketplaceListing,
    StudioArtifact,
    StudioDeployment,
    StudioProfile,
    StudioProject,
    StudioTestRun,
    StudioVersion,
)


class IStudioProfileRepository(ABC):
    @abstractmethod
    async def save(self, profile: StudioProfile) -> None: ...
    @abstractmethod
    async def find_by_tenant(self, tenant_id: str) -> StudioProfile | None: ...
    @abstractmethod
    def next_profile_ref(self, tenant_id: str) -> str: ...


class IStudioProjectRepository(ABC):
    @abstractmethod
    async def save(self, project: StudioProject) -> None: ...
    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[StudioProject]: ...
    @abstractmethod
    async def find_by_ref(self, tenant_id: str, project_ref: str) -> StudioProject | None: ...
    @abstractmethod
    def next_project_ref(self, tenant_id: str) -> str: ...


class IStudioArtifactRepository(ABC):
    @abstractmethod
    async def save(self, artifact: StudioArtifact) -> None: ...
    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[StudioArtifact]: ...
    @abstractmethod
    async def find_by_ref(self, tenant_id: str, artifact_ref: str) -> StudioArtifact | None: ...
    @abstractmethod
    def next_artifact_ref(self, tenant_id: str) -> str: ...


class IStudioVersionRepository(ABC):
    @abstractmethod
    async def save(self, version: StudioVersion) -> None: ...
    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[StudioVersion]: ...
    @abstractmethod
    def next_version_ref(self, tenant_id: str) -> str: ...


class IStudioDeploymentRepository(ABC):
    @abstractmethod
    async def save(self, deployment: StudioDeployment) -> None: ...
    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[StudioDeployment]: ...
    @abstractmethod
    def next_deployment_ref(self, tenant_id: str) -> str: ...


class IStudioTestRunRepository(ABC):
    @abstractmethod
    async def save(self, test_run: StudioTestRun) -> None: ...
    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[StudioTestRun]: ...
    @abstractmethod
    def next_test_ref(self, tenant_id: str) -> str: ...


class IMarketplaceListingRepository(ABC):
    @abstractmethod
    async def save(self, listing: MarketplaceListing) -> None: ...
    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[MarketplaceListing]: ...
    @abstractmethod
    def next_listing_ref(self, tenant_id: str) -> str: ...
