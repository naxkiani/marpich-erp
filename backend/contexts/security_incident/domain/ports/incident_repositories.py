"""Enterprise Security Incident Platform repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.security_incident.domain.aggregates.incident_platform import (
    IncidentEvidence,
    IncidentLessonLearned,
    IncidentNotification,
    IncidentTenantProfile,
    SecurityIncident,
)


class IIncidentTenantProfileRepository(ABC):
    @abstractmethod
    async def save(self, profile: IncidentTenantProfile) -> None: ...

    @abstractmethod
    async def find_by_tenant(self, tenant_id: str) -> IncidentTenantProfile | None: ...

    @abstractmethod
    def next_profile_ref(self, tenant_id: str) -> str: ...


class ISecurityIncidentRepository(ABC):
    @abstractmethod
    async def save(self, incident: SecurityIncident) -> None: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, incident_ref: str) -> SecurityIncident | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[SecurityIncident]: ...

    @abstractmethod
    def next_incident_ref(self, tenant_id: str) -> str: ...


class IIncidentEvidenceRepository(ABC):
    @abstractmethod
    async def save(self, evidence: IncidentEvidence) -> None: ...

    @abstractmethod
    async def list_by_incident(self, tenant_id: str, incident_ref: str) -> list[IncidentEvidence]: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[IncidentEvidence]: ...

    @abstractmethod
    def next_evidence_ref(self, tenant_id: str) -> str: ...


class IIncidentNotificationRepository(ABC):
    @abstractmethod
    async def save(self, notification: IncidentNotification) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[IncidentNotification]: ...

    @abstractmethod
    def next_notification_ref(self, tenant_id: str) -> str: ...


class IIncidentLessonLearnedRepository(ABC):
    @abstractmethod
    async def save(self, lesson: IncidentLessonLearned) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[IncidentLessonLearned]: ...

    @abstractmethod
    def next_lesson_ref(self, tenant_id: str) -> str: ...
