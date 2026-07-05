"""In-memory Branch Banking Platform repositories."""
from __future__ import annotations

from contexts.banking.domain.aggregates.branch_banking_engine import (
    BranchAuditEntry,
    BranchCashLimit,
    BranchDaySession,
    BranchEmployeeAssignment,
    BranchExtension,
    BranchKPIRecord,
    BranchOffice,
    BranchVault,
    BranchVaultMovement,
)


class InMemoryBranchOfficeRepository:
    _store: dict[str, BranchOffice] = {}
    _counter: dict[str, int] = {}

    async def save(self, office: BranchOffice) -> None:
        self._store[str(office.id)] = office

    async def find_by_id(self, office_id: str) -> BranchOffice | None:
        return self._store.get(office_id)

    async def find_by_code(self, tenant_id: str, code: str) -> BranchOffice | None:
        code = code.strip().upper()
        return next(
            (o for o in self._store.values() if o.tenant_id == tenant_id and o.code == code),
            None,
        )

    async def list_by_tenant(self, tenant_id: str) -> list[BranchOffice]:
        return [o for o in self._store.values() if o.tenant_id == tenant_id]

    def next_office_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"BR{self._counter[tenant_id]:06d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryBranchExtensionRepository:
    _store: dict[str, BranchExtension] = {}
    _counter: dict[str, int] = {}

    async def save(self, extension: BranchExtension) -> None:
        self._store[str(extension.id)] = extension

    async def list_by_office(self, office_id: str) -> list[BranchExtension]:
        return [e for e in self._store.values() if e.office_id == office_id]

    async def list_by_tenant(self, tenant_id: str) -> list[BranchExtension]:
        return [e for e in self._store.values() if e.tenant_id == tenant_id]

    def next_extension_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"EXT{self._counter[tenant_id]:06d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryBranchDaySessionRepository:
    _store: dict[str, BranchDaySession] = {}
    _counter: dict[str, int] = {}

    async def save(self, session: BranchDaySession) -> None:
        self._store[str(session.id)] = session

    async def list_by_office(self, office_id: str) -> list[BranchDaySession]:
        return [s for s in self._store.values() if s.office_id == office_id]

    async def list_by_tenant(self, tenant_id: str) -> list[BranchDaySession]:
        return [s for s in self._store.values() if s.tenant_id == tenant_id]

    def next_session_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"SES{self._counter[tenant_id]:06d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryBranchVaultRepository:
    _store: dict[str, BranchVault] = {}
    _counter: dict[str, int] = {}

    async def save(self, vault: BranchVault) -> None:
        self._store[str(vault.id)] = vault

    async def find_by_office(self, office_id: str) -> BranchVault | None:
        return next((v for v in self._store.values() if v.office_id == office_id), None)

    async def list_by_tenant(self, tenant_id: str) -> list[BranchVault]:
        return [v for v in self._store.values() if v.tenant_id == tenant_id]

    def next_vault_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"VLT{self._counter[tenant_id]:06d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryBranchVaultMovementRepository:
    _store: dict[str, BranchVaultMovement] = {}
    _counter: dict[str, int] = {}

    async def save(self, movement: BranchVaultMovement) -> None:
        self._store[str(movement.id)] = movement

    async def list_by_vault(self, vault_id: str) -> list[BranchVaultMovement]:
        return [m for m in self._store.values() if m.vault_id == vault_id]

    def next_movement_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"MVT{self._counter[tenant_id]:06d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryBranchCashLimitRepository:
    _store: dict[str, BranchCashLimit] = {}
    _counter: dict[str, int] = {}

    async def save(self, limit: BranchCashLimit) -> None:
        self._store[str(limit.id)] = limit

    async def list_by_office(self, office_id: str) -> list[BranchCashLimit]:
        return [l for l in self._store.values() if l.office_id == office_id]

    async def list_by_tenant(self, tenant_id: str) -> list[BranchCashLimit]:
        return [l for l in self._store.values() if l.tenant_id == tenant_id]

    def next_limit_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"LMT{self._counter[tenant_id]:06d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryBranchEmployeeAssignmentRepository:
    _store: dict[str, BranchEmployeeAssignment] = {}
    _counter: dict[str, int] = {}

    async def save(self, assignment: BranchEmployeeAssignment) -> None:
        self._store[str(assignment.id)] = assignment

    async def list_by_office(self, office_id: str) -> list[BranchEmployeeAssignment]:
        return [a for a in self._store.values() if a.office_id == office_id]

    async def list_by_tenant(self, tenant_id: str) -> list[BranchEmployeeAssignment]:
        return [a for a in self._store.values() if a.tenant_id == tenant_id]

    def next_assignment_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"ASN{self._counter[tenant_id]:06d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryBranchKPIRepository:
    _store: dict[str, BranchKPIRecord] = {}
    _counter: dict[str, int] = {}

    async def save(self, kpi: BranchKPIRecord) -> None:
        self._store[str(kpi.id)] = kpi

    async def list_by_office(self, office_id: str) -> list[BranchKPIRecord]:
        return [k for k in self._store.values() if k.office_id == office_id]

    async def list_by_tenant(self, tenant_id: str) -> list[BranchKPIRecord]:
        return [k for k in self._store.values() if k.tenant_id == tenant_id]

    def next_kpi_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"KPI{self._counter[tenant_id]:06d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryBranchAuditRepository:
    _store: dict[str, BranchAuditEntry] = {}

    async def save(self, entry: BranchAuditEntry) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_office(self, office_id: str) -> list[BranchAuditEntry]:
        return [e for e in self._store.values() if e.office_id == office_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
