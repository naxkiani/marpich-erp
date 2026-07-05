"""In-memory Loan Management repositories."""
from __future__ import annotations

from contexts.banking.domain.aggregates.loan_management_engine import (
    LoanAuditEntry,
    LoanCollateral,
    LoanCreditRiskAnalysis,
    LoanGuarantor,
    LoanInstallment,
    LoanProfile,
    LoanTransaction,
    LoanWorkflowRequest,
)


class InMemoryLoanProfileRepository:
    _store: dict[str, LoanProfile] = {}
    _counter: dict[str, int] = {}

    async def save(self, loan: LoanProfile) -> None:
        self._store[str(loan.id)] = loan

    async def find_by_id(self, loan_id: str) -> LoanProfile | None:
        return self._store.get(loan_id)

    async def find_by_account(self, account_id: str) -> LoanProfile | None:
        for loan in self._store.values():
            if loan.account_id == account_id:
                return loan
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[LoanProfile]:
        return [l for l in self._store.values() if l.tenant_id == tenant_id]

    def next_loan_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"LN{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryLoanCollateralRepository:
    _store: dict[str, LoanCollateral] = {}

    async def save(self, collateral: LoanCollateral) -> None:
        self._store[str(collateral.id)] = collateral

    async def list_by_loan(self, loan_id: str) -> list[LoanCollateral]:
        return [c for c in self._store.values() if c.loan_id == loan_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryLoanGuarantorRepository:
    _store: dict[str, LoanGuarantor] = {}

    async def save(self, guarantor: LoanGuarantor) -> None:
        self._store[str(guarantor.id)] = guarantor

    async def list_by_loan(self, loan_id: str) -> list[LoanGuarantor]:
        return [g for g in self._store.values() if g.loan_id == loan_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryLoanInstallmentRepository:
    _store: dict[str, LoanInstallment] = {}

    async def save(self, installment: LoanInstallment) -> None:
        self._store[str(installment.id)] = installment

    async def list_by_loan(self, loan_id: str) -> list[LoanInstallment]:
        return sorted(
            [i for i in self._store.values() if i.loan_id == loan_id],
            key=lambda i: i.installment_number,
        )

    async def find_by_id(self, installment_id: str) -> LoanInstallment | None:
        return self._store.get(installment_id)

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryLoanTransactionRepository:
    _store: dict[str, LoanTransaction] = {}
    _counter: dict[str, int] = {}

    async def save(self, transaction: LoanTransaction) -> None:
        self._store[str(transaction.id)] = transaction

    async def find_by_id(self, transaction_id: str) -> LoanTransaction | None:
        return self._store.get(transaction_id)

    async def list_by_loan(self, loan_id: str) -> list[LoanTransaction]:
        return sorted(
            [t for t in self._store.values() if t.loan_id == loan_id],
            key=lambda t: t.created_at,
        )

    async def list_by_tenant(self, tenant_id: str) -> list[LoanTransaction]:
        return [t for t in self._store.values() if t.tenant_id == tenant_id]

    def next_transaction_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"LTX{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryLoanCreditRiskRepository:
    _store: dict[str, LoanCreditRiskAnalysis] = {}

    async def save(self, analysis: LoanCreditRiskAnalysis) -> None:
        self._store[str(analysis.id)] = analysis

    async def find_by_loan(self, loan_id: str) -> LoanCreditRiskAnalysis | None:
        for a in self._store.values():
            if a.loan_id == loan_id:
                return a
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[LoanCreditRiskAnalysis]:
        return [a for a in self._store.values() if a.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryLoanWorkflowRepository:
    _store: dict[str, LoanWorkflowRequest] = {}

    async def save(self, request: LoanWorkflowRequest) -> None:
        self._store[str(request.id)] = request

    async def list_by_loan(self, loan_id: str) -> list[LoanWorkflowRequest]:
        return [w for w in self._store.values() if w.loan_id == loan_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryLoanAuditRepository:
    _store: dict[str, LoanAuditEntry] = {}

    async def save(self, entry: LoanAuditEntry) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_loan(self, loan_id: str) -> list[LoanAuditEntry]:
        return sorted(
            [e for e in self._store.values() if e.loan_id == loan_id],
            key=lambda e: e.occurred_at,
            reverse=True,
        )

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
