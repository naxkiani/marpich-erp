"""In-memory Banking Customer and Account repositories."""
from __future__ import annotations

from contexts.banking.domain.aggregates.customer_account_engine import (
    BankingAccount,
    BankingAccountAudit,
    BankingAccountProduct,
    BankingCustomer,
    BankingCustomerKYC,
)


class InMemoryCustomerRepository:
    _store: dict[str, BankingCustomer] = {}

    async def save(self, customer: BankingCustomer) -> None:
        self._store[str(customer.id)] = customer

    async def find_by_id(self, customer_id: str) -> BankingCustomer | None:
        return self._store.get(customer_id)

    async def find_by_email(self, tenant_id: str, email: str) -> BankingCustomer | None:
        for c in self._store.values():
            if c.tenant_id == tenant_id and c.email == email.lower():
                return c
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[BankingCustomer]:
        return [c for c in self._store.values() if c.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryKycRepository:
    _store: dict[str, BankingCustomerKYC] = {}

    async def save(self, kyc: BankingCustomerKYC) -> None:
        self._store[str(kyc.id)] = kyc

    async def find_by_id(self, kyc_id: str) -> BankingCustomerKYC | None:
        return self._store.get(kyc_id)

    async def list_by_customer(self, customer_id: str) -> list[BankingCustomerKYC]:
        return [k for k in self._store.values() if k.customer_id == customer_id]

    async def list_by_tenant(self, tenant_id: str) -> list[BankingCustomerKYC]:
        return [k for k in self._store.values() if k.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryAccountProductRepository:
    _store: dict[str, BankingAccountProduct] = {}

    async def save(self, product: BankingAccountProduct) -> None:
        self._store[str(product.id)] = product

    async def find_by_code(self, tenant_id: str, product_code: str) -> BankingAccountProduct | None:
        for p in self._store.values():
            if p.tenant_id == tenant_id and p.product_code == product_code.upper():
                return p
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[BankingAccountProduct]:
        return [p for p in self._store.values() if p.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryAccountRepository:
    _store: dict[str, BankingAccount] = {}
    _counter: dict[str, int] = {}

    async def save(self, account: BankingAccount) -> None:
        self._store[str(account.id)] = account

    async def find_by_id(self, account_id: str) -> BankingAccount | None:
        return self._store.get(account_id)

    async def find_by_number(self, tenant_id: str, account_number: str) -> BankingAccount | None:
        for a in self._store.values():
            if a.tenant_id == tenant_id and a.account_number == account_number.upper():
                return a
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[BankingAccount]:
        return [a for a in self._store.values() if a.tenant_id == tenant_id]

    async def list_by_customer(self, customer_id: str) -> list[BankingAccount]:
        return [a for a in self._store.values() if a.customer_id == customer_id]

    def next_account_number(self, tenant_id: str, prefix: str = "ACC") -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"{prefix}{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryAccountAuditRepository:
    _store: dict[str, BankingAccountAudit] = {}

    async def save(self, entry: BankingAccountAudit) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_account(self, account_id: str) -> list[BankingAccountAudit]:
        return [e for e in self._store.values() if e.account_id == account_id]

    async def list_by_tenant(self, tenant_id: str) -> list[BankingAccountAudit]:
        return sorted(
            [e for e in self._store.values() if e.tenant_id == tenant_id],
            key=lambda e: e.occurred_at,
            reverse=True,
        )

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
