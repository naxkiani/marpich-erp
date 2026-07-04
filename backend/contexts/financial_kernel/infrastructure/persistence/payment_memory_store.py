"""In-memory Payment persistence."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.payment import InstallmentPlan, Payment
from contexts.financial_kernel.domain.aggregates.payment_reconciliation import PaymentReconciliation
from contexts.financial_kernel.domain.ports.payment_repositories import (
    IInstallmentPlanRepository,
    IPaymentReconciliationRepository,
    IPaymentRepository,
)


class InMemoryPaymentRepository(IPaymentRepository):
    _payments: dict[str, Payment] = {}

    @classmethod
    def reset(cls) -> None:
        cls._payments = {}

    async def save(self, payment: Payment) -> None:
        self._payments[str(payment.id)] = payment
        self._payments[f"idemp:{payment.tenant_id}:{payment.idempotency_key}"] = payment

    async def find_by_id(self, payment_id: str) -> Payment | None:
        p = self._payments.get(payment_id)
        return p if isinstance(p, Payment) else None

    async def find_by_idempotency(self, tenant_id: str, key: str) -> Payment | None:
        p = self._payments.get(f"idemp:{tenant_id}:{key}")
        return p if isinstance(p, Payment) else None

    async def list_by_tenant(self, tenant_id: str) -> list[Payment]:
        seen: set[str] = set()
        result = []
        for p in self._payments.values():
            if isinstance(p, Payment) and p.tenant_id == tenant_id and str(p.id) not in seen:
                seen.add(str(p.id))
                result.append(p)
        return result

    async def list_children(self, parent_payment_id: str) -> list[Payment]:
        return [
            p
            for p in self._payments.values()
            if isinstance(p, Payment) and p.parent_payment_id == parent_payment_id
        ]


class InMemoryInstallmentPlanRepository(IInstallmentPlanRepository):
    _plans: dict[str, InstallmentPlan] = {}

    @classmethod
    def reset(cls) -> None:
        cls._plans = {}

    async def save(self, plan: InstallmentPlan) -> None:
        self._plans[str(plan.id)] = plan

    async def find_by_id(self, plan_id: str) -> InstallmentPlan | None:
        return self._plans.get(plan_id)

    async def list_by_tenant(self, tenant_id: str) -> list[InstallmentPlan]:
        return [p for p in self._plans.values() if p.tenant_id == tenant_id]


class InMemoryPaymentReconciliationRepository(IPaymentReconciliationRepository):
    _records: dict[str, PaymentReconciliation] = {}

    @classmethod
    def reset(cls) -> None:
        cls._records = {}

    async def save(self, record: PaymentReconciliation) -> None:
        self._records[str(record.id)] = record

    async def find_by_id(self, record_id: str) -> PaymentReconciliation | None:
        return self._records.get(record_id)

    async def list_by_tenant(self, tenant_id: str) -> list[PaymentReconciliation]:
        return [r for r in self._records.values() if r.tenant_id == tenant_id]
