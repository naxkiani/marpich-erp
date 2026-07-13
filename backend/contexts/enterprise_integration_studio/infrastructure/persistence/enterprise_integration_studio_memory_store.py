"""In-memory Enterprise Integration Studio persistence."""
from __future__ import annotations

from contexts.enterprise_integration_studio.domain.aggregates.enterprise_integration_studio_platform import (
    MarketplaceListing,
    StudioArtifact,
    StudioDeployment,
    StudioProfile,
    StudioProject,
    StudioTestRun,
    StudioVersion,
)
from contexts.enterprise_integration_studio.domain.ports.enterprise_integration_studio_repositories import (
    IMarketplaceListingRepository,
    IStudioArtifactRepository,
    IStudioDeploymentRepository,
    IStudioProfileRepository,
    IStudioProjectRepository,
    IStudioTestRunRepository,
    IStudioVersionRepository,
)


class _RefCounter:
    _counters: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls._counters = {}

    @classmethod
    def next(cls, tenant_id: str, prefix: str) -> str:
        key = f"{tenant_id}:{prefix}"
        n = cls._counters.get(key, 0) + 1
        cls._counters[key] = n
        return f"{prefix}-{tenant_id[:4].upper()}-{n:05d}"


class InMemoryStudioProfileRepository(IStudioProfileRepository):
    _store: dict[str, StudioProfile] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, profile: StudioProfile) -> None:
        self._store[str(profile.id)] = profile

    async def find_by_tenant(self, tenant_id: str) -> StudioProfile | None:
        for p in self._store.values():
            if p.tenant_id == tenant_id:
                return p
        return None

    def next_profile_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-EIS-PRF")


class InMemoryStudioProjectRepository(IStudioProjectRepository):
    _store: dict[str, StudioProject] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, project: StudioProject) -> None:
        self._store[str(project.id)] = project

    async def list_by_tenant(self, tenant_id: str) -> list[StudioProject]:
        return [p for p in self._store.values() if p.tenant_id == tenant_id]

    async def find_by_ref(self, tenant_id: str, project_ref: str) -> StudioProject | None:
        for p in self._store.values():
            if p.tenant_id == tenant_id and p.project_ref == project_ref:
                return p
        return None

    def next_project_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-EIS-PRJ")


class InMemoryStudioArtifactRepository(IStudioArtifactRepository):
    _store: dict[str, StudioArtifact] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, artifact: StudioArtifact) -> None:
        self._store[str(artifact.id)] = artifact

    async def list_by_tenant(self, tenant_id: str) -> list[StudioArtifact]:
        return [a for a in self._store.values() if a.tenant_id == tenant_id]

    async def find_by_ref(self, tenant_id: str, artifact_ref: str) -> StudioArtifact | None:
        for a in self._store.values():
            if a.tenant_id == tenant_id and a.artifact_ref == artifact_ref:
                return a
        return None

    def next_artifact_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-EIS-ART")


class InMemoryStudioVersionRepository(IStudioVersionRepository):
    _store: dict[str, StudioVersion] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, version: StudioVersion) -> None:
        self._store[str(version.id)] = version

    async def list_by_tenant(self, tenant_id: str) -> list[StudioVersion]:
        return [v for v in self._store.values() if v.tenant_id == tenant_id]

    def next_version_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-EIS-VER")


class InMemoryStudioDeploymentRepository(IStudioDeploymentRepository):
    _store: dict[str, StudioDeployment] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, deployment: StudioDeployment) -> None:
        self._store[str(deployment.id)] = deployment

    async def list_by_tenant(self, tenant_id: str) -> list[StudioDeployment]:
        return [d for d in self._store.values() if d.tenant_id == tenant_id]

    def next_deployment_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-EIS-DEP")


class InMemoryStudioTestRunRepository(IStudioTestRunRepository):
    _store: dict[str, StudioTestRun] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, test_run: StudioTestRun) -> None:
        self._store[str(test_run.id)] = test_run

    async def list_by_tenant(self, tenant_id: str) -> list[StudioTestRun]:
        return sorted(
            [t for t in self._store.values() if t.tenant_id == tenant_id],
            key=lambda t: t.created_at,
            reverse=True,
        )

    def next_test_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-EIS-TST")


class InMemoryMarketplaceListingRepository(IMarketplaceListingRepository):
    _store: dict[str, MarketplaceListing] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, listing: MarketplaceListing) -> None:
        self._store[str(listing.id)] = listing

    async def list_by_tenant(self, tenant_id: str) -> list[MarketplaceListing]:
        return [l for l in self._store.values() if l.tenant_id == tenant_id]

    def next_listing_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-EIS-MKT")
