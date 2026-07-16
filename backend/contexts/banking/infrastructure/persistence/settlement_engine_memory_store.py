"""In-memory Banking Settlement Engine repositories."""
from __future__ import annotations

from contexts.banking.domain.aggregates.settlement_engine import (
    BankReconciliationRun,
    ReconciliationMatch,
    SettlementAdjustment,
    SettlementAuditEntry,
    SettlementBatch,
    SettlementDifference,
    SettlementException,
    SettlementItem,
    SettlementReport,
)


class InMemorySettlementBatchRepository:
    _store: dict[str, SettlementBatch] = {}
    _counter: dict[str, int] = {}

    async def save(self, batch: SettlementBatch) -> None:
        self._store[str(batch.id)] = batch

    async def find_by_id(self, batch_id: str) -> SettlementBatch | None:
        return self._store.get(batch_id)

    async def list_by_tenant(self, tenant_id: str) -> list[SettlementBatch]:
        return [b for b in self._store.values() if b.tenant_id == tenant_id]

    def next_batch_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"SET{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemorySettlementItemRepository:
    _store: dict[str, SettlementItem] = {}
    _counter: dict[str, int] = {}

    async def save(self, item: SettlementItem) -> None:
        self._store[str(item.id)] = item

    async def list_by_batch(self, batch_id: str) -> list[SettlementItem]:
        return [i for i in self._store.values() if i.batch_id == batch_id]

    def next_item_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"ITM{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryReconciliationRunRepository:
    _store: dict[str, BankReconciliationRun] = {}
    _counter: dict[str, int] = {}

    async def save(self, run: BankReconciliationRun) -> None:
        self._store[str(run.id)] = run

    async def find_by_id(self, run_id: str) -> BankReconciliationRun | None:
        return self._store.get(run_id)

    async def list_by_tenant(self, tenant_id: str) -> list[BankReconciliationRun]:
        return [r for r in self._store.values() if r.tenant_id == tenant_id]

    def next_run_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"REC{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryReconciliationMatchRepository:
    _store: dict[str, ReconciliationMatch] = {}

    async def save(self, match: ReconciliationMatch) -> None:
        self._store[str(match.id)] = match

    async def list_by_run(self, run_id: str) -> list[ReconciliationMatch]:
        return [m for m in self._store.values() if m.run_id == run_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemorySettlementExceptionRepository:
    _store: dict[str, SettlementException] = {}
    _counter: dict[str, int] = {}

    async def save(self, exception: SettlementException) -> None:
        self._store[str(exception.id)] = exception

    async def find_by_id(self, exception_id: str) -> SettlementException | None:
        return self._store.get(exception_id)

    async def list_by_tenant(self, tenant_id: str) -> list[SettlementException]:
        return [e for e in self._store.values() if e.tenant_id == tenant_id]

    def next_exception_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"EXC{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemorySettlementDifferenceRepository:
    _store: dict[str, SettlementDifference] = {}
    _counter: dict[str, int] = {}

    async def save(self, difference: SettlementDifference) -> None:
        self._store[str(difference.id)] = difference

    async def list_by_run(self, run_id: str) -> list[SettlementDifference]:
        return [d for d in self._store.values() if d.run_id == run_id]

    def next_difference_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"DIF{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemorySettlementAdjustmentRepository:
    _store: dict[str, SettlementAdjustment] = {}
    _counter: dict[str, int] = {}

    async def save(self, adjustment: SettlementAdjustment) -> None:
        self._store[str(adjustment.id)] = adjustment

    async def find_by_id(self, adjustment_id: str) -> SettlementAdjustment | None:
        return self._store.get(adjustment_id)

    async def list_by_tenant(self, tenant_id: str) -> list[SettlementAdjustment]:
        return [a for a in self._store.values() if a.tenant_id == tenant_id]

    def next_adjustment_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"ADJ{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemorySettlementAuditRepository:
    _store: dict[str, SettlementAuditEntry] = {}

    async def save(self, entry: SettlementAuditEntry) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_source(self, source_type: str, source_id: str) -> list[SettlementAuditEntry]:
        return [
            e
            for e in self._store.values()
            if e.source_type == source_type and e.source_id == source_id
        ]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemorySettlementReportRepository:
    _store: dict[str, SettlementReport] = {}
    _counter: dict[str, int] = {}

    async def save(self, report: SettlementReport) -> None:
        self._store[str(report.id)] = report

    async def list_by_tenant(self, tenant_id: str) -> list[SettlementReport]:
        return [r for r in self._store.values() if r.tenant_id == tenant_id]

    def next_report_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"RPT{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}
