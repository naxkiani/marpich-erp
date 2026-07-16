"""In-memory Banking Security Platform repositories."""
from __future__ import annotations

from contexts.banking.domain.aggregates.banking_security_engine import (
    EmergencyFreeze,
    FreezeStatus,
    LimitUsageTracker,
    SecurityApprovalRequest,
    SecurityAuditEntry,
    SecurityDevice,
    SecuritySession,
    TransactionMonitorAlert,
)


class InMemorySecurityApprovalRepository:
    _store: dict[str, SecurityApprovalRequest] = {}
    _counter: dict[str, int] = {}

    async def save(self, request: SecurityApprovalRequest) -> None:
        self._store[str(request.id)] = request

    async def find_by_id(self, request_id: str) -> SecurityApprovalRequest | None:
        return self._store.get(request_id)

    async def list_by_tenant(self, tenant_id: str) -> list[SecurityApprovalRequest]:
        return [r for r in self._store.values() if r.tenant_id == tenant_id]

    def next_request_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"APR{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemorySecurityDeviceRepository:
    _store: dict[str, SecurityDevice] = {}
    _counter: dict[str, int] = {}

    async def save(self, device: SecurityDevice) -> None:
        self._store[str(device.id)] = device

    async def find_by_fingerprint(
        self, tenant_id: str, user_id: str, fingerprint: str
    ) -> SecurityDevice | None:
        return next(
            (
                d
                for d in self._store.values()
                if d.tenant_id == tenant_id
                and d.user_id == user_id
                and d.device_fingerprint == fingerprint
            ),
            None,
        )

    async def list_by_user(self, tenant_id: str, user_id: str) -> list[SecurityDevice]:
        return [d for d in self._store.values() if d.tenant_id == tenant_id and d.user_id == user_id]

    def next_device_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"DEV{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemorySecuritySessionRepository:
    _store: dict[str, SecuritySession] = {}
    _counter: dict[str, int] = {}

    async def save(self, session: SecuritySession) -> None:
        self._store[str(session.id)] = session

    async def find_by_id(self, session_id: str) -> SecuritySession | None:
        return self._store.get(session_id)

    async def list_by_tenant(self, tenant_id: str) -> list[SecuritySession]:
        return [s for s in self._store.values() if s.tenant_id == tenant_id]

    def next_session_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"SES{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryTransactionMonitorRepository:
    _store: dict[str, TransactionMonitorAlert] = {}
    _counter: dict[str, int] = {}

    async def save(self, alert: TransactionMonitorAlert) -> None:
        self._store[str(alert.id)] = alert

    async def list_by_tenant(self, tenant_id: str) -> list[TransactionMonitorAlert]:
        return [a for a in self._store.values() if a.tenant_id == tenant_id]

    def next_alert_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"ALT{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryEmergencyFreezeRepository:
    _store: dict[str, EmergencyFreeze] = {}
    _counter: dict[str, int] = {}

    async def save(self, freeze: EmergencyFreeze) -> None:
        self._store[str(freeze.id)] = freeze

    async def find_active(self, tenant_id: str) -> EmergencyFreeze | None:
        return next(
            (
                f
                for f in self._store.values()
                if f.tenant_id == tenant_id and f.status == FreezeStatus.ACTIVE.value
            ),
            None,
        )

    async def list_by_tenant(self, tenant_id: str) -> list[EmergencyFreeze]:
        return [f for f in self._store.values() if f.tenant_id == tenant_id]

    def next_freeze_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"FRZ{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemorySecurityAuditRepository:
    _store: dict[str, SecurityAuditEntry] = {}
    _counter: dict[str, int] = {}

    async def save(self, entry: SecurityAuditEntry) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_tenant(self, tenant_id: str) -> list[SecurityAuditEntry]:
        return [e for e in self._store.values() if e.tenant_id == tenant_id]

    async def last_tamper_hash(self, tenant_id: str) -> str | None:
        entries = [e for e in self._store.values() if e.tenant_id == tenant_id]
        if not entries:
            return None
        entries.sort(key=lambda e: e.created_at)
        return entries[-1].tamper_hash

    def next_audit_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"AUD{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryLimitUsageRepository:
    _store: dict[str, LimitUsageTracker] = {}

    async def save(self, tracker: LimitUsageTracker) -> None:
        self._store[str(tracker.id)] = tracker

    async def get_for_user(self, tenant_id: str, user_id: str, usage_date: str) -> LimitUsageTracker | None:
        return next(
            (
                t
                for t in self._store.values()
                if t.tenant_id == tenant_id and t.user_id == user_id and t.usage_date == usage_date
            ),
            None,
        )

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
