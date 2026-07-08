"""Enterprise Regulatory Reporting Platform repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.regulatory_reporting.domain.aggregates.regulatory_reporting_platform import (
    CountryAdapter,
    DigitalSubmission,
    RegulatoryTenantProfile,
)


class IRegulatoryTenantProfileRepository(ABC):
    @abstractmethod
    async def save(self, profile: RegulatoryTenantProfile) -> None: ...

    @abstractmethod
    async def find_by_tenant(self, tenant_id: str) -> RegulatoryTenantProfile | None: ...

    @abstractmethod
    def next_profile_ref(self, tenant_id: str) -> str: ...


class ICountryAdapterRepository(ABC):
    @abstractmethod
    async def save(self, adapter: CountryAdapter) -> None: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, adapter_ref: str) -> CountryAdapter | None: ...

    @abstractmethod
    async def find_by_country(self, tenant_id: str, country_code: str) -> CountryAdapter | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[CountryAdapter]: ...

    @abstractmethod
    def next_adapter_ref(self, tenant_id: str) -> str: ...


class IDigitalSubmissionRepository(ABC):
    @abstractmethod
    async def save(self, submission: DigitalSubmission) -> None: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, submission_ref: str) -> DigitalSubmission | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[DigitalSubmission]: ...

    @abstractmethod
    def next_submission_ref(self, tenant_id: str) -> str: ...
