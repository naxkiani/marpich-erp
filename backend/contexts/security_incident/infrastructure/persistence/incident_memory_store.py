"""In-memory Enterprise Security Incident Platform persistence."""
from __future__ import annotations

from contexts.security_incident.domain.aggregates.incident_platform import (
    IncidentEvidence,
    IncidentLessonLearned,
    IncidentNotification,
    IncidentTenantProfile,
    SecurityIncident,
)
from contexts.security_incident.domain.ports.incident_repositories import (
    IIncidentEvidenceRepository,
    IIncidentLessonLearnedRepository,
    IIncidentNotificationRepository,
    IIncidentTenantProfileRepository,
    ISecurityIncidentRepository,
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


class InMemoryIncidentTenantProfileRepository(IIncidentTenantProfileRepository):
    _store: dict[str, IncidentTenantProfile] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, profile: IncidentTenantProfile) -> None:
        self._store[str(profile.id)] = profile

    async def find_by_tenant(self, tenant_id: str) -> IncidentTenantProfile | None:
        for p in self._store.values():
            if p.tenant_id == tenant_id:
                return p
        return None

    def next_profile_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-INC-PRF")


class InMemorySecurityIncidentRepository(ISecurityIncidentRepository):
    _store: dict[str, SecurityIncident] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, incident: SecurityIncident) -> None:
        self._store[str(incident.id)] = incident

    async def find_by_ref(self, tenant_id: str, incident_ref: str) -> SecurityIncident | None:
        for item in self._store.values():
            if item.tenant_id == tenant_id and item.incident_ref == incident_ref:
                return item
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[SecurityIncident]:
        items = [i for i in self._store.values() if i.tenant_id == tenant_id]
        return sorted(items, key=lambda i: i.created_at)

    def next_incident_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-INC")


class InMemoryIncidentEvidenceRepository(IIncidentEvidenceRepository):
    _store: dict[str, IncidentEvidence] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, evidence: IncidentEvidence) -> None:
        self._store[str(evidence.id)] = evidence

    async def list_by_incident(self, tenant_id: str, incident_ref: str) -> list[IncidentEvidence]:
        items = [
            e for e in self._store.values()
            if e.tenant_id == tenant_id and e.incident_ref == incident_ref
        ]
        return sorted(items, key=lambda e: e.created_at)

    async def list_by_tenant(self, tenant_id: str) -> list[IncidentEvidence]:
        items = [e for e in self._store.values() if e.tenant_id == tenant_id]
        return sorted(items, key=lambda e: e.created_at)

    def next_evidence_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-EVD")


class InMemoryIncidentNotificationRepository(IIncidentNotificationRepository):
    _store: dict[str, IncidentNotification] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, notification: IncidentNotification) -> None:
        self._store[str(notification.id)] = notification

    async def list_by_tenant(self, tenant_id: str) -> list[IncidentNotification]:
        items = [n for n in self._store.values() if n.tenant_id == tenant_id]
        return sorted(items, key=lambda n: n.sent_at, reverse=True)

    def next_notification_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-NOT")


class InMemoryIncidentLessonLearnedRepository(IIncidentLessonLearnedRepository):
    _store: dict[str, IncidentLessonLearned] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, lesson: IncidentLessonLearned) -> None:
        self._store[str(lesson.id)] = lesson

    async def list_by_tenant(self, tenant_id: str) -> list[IncidentLessonLearned]:
        items = [l for l in self._store.values() if l.tenant_id == tenant_id]
        return sorted(items, key=lambda l: l.created_at, reverse=True)

    def next_lesson_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-LSN")
