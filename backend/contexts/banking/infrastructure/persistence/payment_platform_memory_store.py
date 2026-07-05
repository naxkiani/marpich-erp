"""In-memory Banking Payment Platform repositories."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from contexts.banking.domain.aggregates.payment_platform_engine import (
    PaymentAuditEntry,
    PaymentBatch,
    PaymentBeneficiary,
    PaymentFraudCheck,
    PaymentTransfer,
    PaymentWorkflowRequest,
    StandingOrder,
    TransferStatus,
)


class InMemoryPaymentBeneficiaryRepository:
    _store: dict[str, PaymentBeneficiary] = {}
    _counter: dict[str, int] = {}

    async def save(self, beneficiary: PaymentBeneficiary) -> None:
        self._store[str(beneficiary.id)] = beneficiary

    async def find_by_id(self, beneficiary_id: str) -> PaymentBeneficiary | None:
        return self._store.get(beneficiary_id)

    async def list_by_customer(self, customer_id: str) -> list[PaymentBeneficiary]:
        return [b for b in self._store.values() if b.customer_id == customer_id]

    async def list_by_tenant(self, tenant_id: str) -> list[PaymentBeneficiary]:
        return [b for b in self._store.values() if b.tenant_id == tenant_id]

    def next_beneficiary_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"BEN{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryPaymentTransferRepository:
    _store: dict[str, PaymentTransfer] = {}
    _counter: dict[str, int] = {}

    async def save(self, transfer: PaymentTransfer) -> None:
        self._store[str(transfer.id)] = transfer

    async def find_by_id(self, transfer_id: str) -> PaymentTransfer | None:
        return self._store.get(transfer_id)

    async def list_by_tenant(self, tenant_id: str) -> list[PaymentTransfer]:
        return [t for t in self._store.values() if t.tenant_id == tenant_id]

    async def list_by_batch(self, batch_id: str) -> list[PaymentTransfer]:
        return [t for t in self._store.values() if t.batch_id == batch_id]

    async def daily_total_by_account(self, tenant_id: str, account_id: str) -> float:
        today = datetime.now(UTC).date()
        total = 0.0
        for t in self._store.values():
            if t.tenant_id != tenant_id or t.source_account_id != account_id:
                continue
            if t.status not in {TransferStatus.COMPLETED.value, TransferStatus.PROCESSING.value}:
                continue
            if t.created_at.date() == today:
                total += t.amount
        return round(total, 2)

    async def velocity_count(self, tenant_id: str, customer_id: str, hours: int = 24) -> int:
        cutoff = datetime.now(UTC) - timedelta(hours=hours)
        return sum(
            1
            for t in self._store.values()
            if t.tenant_id == tenant_id
            and t.customer_id == customer_id
            and t.created_at >= cutoff
            and t.status != TransferStatus.CANCELLED.value
        )

    def next_transfer_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"TXF{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryPaymentBatchRepository:
    _store: dict[str, PaymentBatch] = {}
    _counter: dict[str, int] = {}

    async def save(self, batch: PaymentBatch) -> None:
        self._store[str(batch.id)] = batch

    async def find_by_id(self, batch_id: str) -> PaymentBatch | None:
        return self._store.get(batch_id)

    async def list_by_tenant(self, tenant_id: str) -> list[PaymentBatch]:
        return [b for b in self._store.values() if b.tenant_id == tenant_id]

    def next_batch_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"BLK{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryStandingOrderRepository:
    _store: dict[str, StandingOrder] = {}
    _counter: dict[str, int] = {}

    async def save(self, order: StandingOrder) -> None:
        self._store[str(order.id)] = order

    async def find_by_id(self, order_id: str) -> StandingOrder | None:
        return self._store.get(order_id)

    async def list_by_tenant(self, tenant_id: str) -> list[StandingOrder]:
        return [o for o in self._store.values() if o.tenant_id == tenant_id]

    def next_order_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"STO{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryPaymentWorkflowRepository:
    _store: dict[str, PaymentWorkflowRequest] = {}

    async def save(self, workflow: PaymentWorkflowRequest) -> None:
        self._store[str(workflow.id)] = workflow

    async def list_by_transfer(self, transfer_id: str) -> list[PaymentWorkflowRequest]:
        return [w for w in self._store.values() if w.transfer_id == transfer_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryPaymentFraudRepository:
    _store: dict[str, PaymentFraudCheck] = {}

    async def save(self, check: PaymentFraudCheck) -> None:
        self._store[str(check.id)] = check

    async def find_by_transfer(self, transfer_id: str) -> PaymentFraudCheck | None:
        for c in self._store.values():
            if c.transfer_id == transfer_id:
                return c
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[PaymentFraudCheck]:
        return [c for c in self._store.values() if c.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryPaymentAuditRepository:
    _store: dict[str, PaymentAuditEntry] = {}

    async def save(self, entry: PaymentAuditEntry) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_transfer(self, transfer_id: str) -> list[PaymentAuditEntry]:
        return sorted(
            [e for e in self._store.values() if e.transfer_id == transfer_id],
            key=lambda e: e.created_at,
        )

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
