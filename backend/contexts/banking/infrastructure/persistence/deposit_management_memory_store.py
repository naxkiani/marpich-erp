"""In-memory Deposit Management repositories."""
from __future__ import annotations

from contexts.banking.domain.aggregates.deposit_management_engine import (
    DepositAuditEntry,
    DepositCertificate,
    DepositInterestAccrual,
    DepositProfile,
    DepositStatement,
    DepositTransaction,
    DepositWorkflowRequest,
    ProfitDistributionRule,
)


class InMemoryProfitRuleRepository:
    _store: dict[str, ProfitDistributionRule] = {}

    async def save(self, rule: ProfitDistributionRule) -> None:
        self._store[str(rule.id)] = rule

    async def find_by_code(self, tenant_id: str, rule_code: str) -> ProfitDistributionRule | None:
        for r in self._store.values():
            if r.tenant_id == tenant_id and r.rule_code == rule_code.upper():
                return r
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[ProfitDistributionRule]:
        return [r for r in self._store.values() if r.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryDepositProfileRepository:
    _store: dict[str, DepositProfile] = {}

    async def save(self, deposit: DepositProfile) -> None:
        self._store[str(deposit.id)] = deposit

    async def find_by_id(self, deposit_id: str) -> DepositProfile | None:
        return self._store.get(deposit_id)

    async def find_by_account(self, account_id: str) -> DepositProfile | None:
        for d in self._store.values():
            if d.account_id == account_id:
                return d
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[DepositProfile]:
        return [d for d in self._store.values() if d.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryDepositTransactionRepository:
    _store: dict[str, DepositTransaction] = {}
    _counter: dict[str, int] = {}

    async def save(self, transaction: DepositTransaction) -> None:
        self._store[str(transaction.id)] = transaction

    async def find_by_id(self, transaction_id: str) -> DepositTransaction | None:
        return self._store.get(transaction_id)

    async def list_by_deposit(self, deposit_id: str) -> list[DepositTransaction]:
        return [t for t in self._store.values() if t.deposit_id == deposit_id]

    async def list_by_tenant(self, tenant_id: str) -> list[DepositTransaction]:
        return [t for t in self._store.values() if t.tenant_id == tenant_id]

    def next_transaction_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"DTX{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryDepositAccrualRepository:
    _store: dict[str, DepositInterestAccrual] = {}
    _counter: dict[str, int] = {}

    async def save(self, accrual: DepositInterestAccrual) -> None:
        self._store[str(accrual.id)] = accrual

    async def list_by_deposit(self, deposit_id: str) -> list[DepositInterestAccrual]:
        return [a for a in self._store.values() if a.deposit_id == deposit_id]

    async def list_by_tenant(self, tenant_id: str) -> list[DepositInterestAccrual]:
        return [a for a in self._store.values() if a.tenant_id == tenant_id]

    def next_accrual_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"ACC{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryDepositCertificateRepository:
    _store: dict[str, DepositCertificate] = {}
    _counter: dict[str, int] = {}

    async def save(self, certificate: DepositCertificate) -> None:
        self._store[str(certificate.id)] = certificate

    async def list_by_deposit(self, deposit_id: str) -> list[DepositCertificate]:
        return [c for c in self._store.values() if c.deposit_id == deposit_id]

    async def list_by_tenant(self, tenant_id: str) -> list[DepositCertificate]:
        return [c for c in self._store.values() if c.tenant_id == tenant_id]

    def next_certificate_number(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"DCERT{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryDepositStatementRepository:
    _store: dict[str, DepositStatement] = {}
    _counter: dict[str, int] = {}

    async def save(self, statement: DepositStatement) -> None:
        self._store[str(statement.id)] = statement

    async def list_by_deposit(self, deposit_id: str) -> list[DepositStatement]:
        return [s for s in self._store.values() if s.deposit_id == deposit_id]

    def next_statement_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"STMT{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryDepositWorkflowRepository:
    _store: dict[str, DepositWorkflowRequest] = {}

    async def save(self, request: DepositWorkflowRequest) -> None:
        self._store[str(request.id)] = request

    async def list_by_deposit(self, deposit_id: str) -> list[DepositWorkflowRequest]:
        return [w for w in self._store.values() if w.deposit_id == deposit_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryDepositAuditRepository:
    _store: dict[str, DepositAuditEntry] = {}

    async def save(self, entry: DepositAuditEntry) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_deposit(self, deposit_id: str) -> list[DepositAuditEntry]:
        return sorted(
            [e for e in self._store.values() if e.deposit_id == deposit_id],
            key=lambda e: e.occurred_at,
            reverse=True,
        )

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
