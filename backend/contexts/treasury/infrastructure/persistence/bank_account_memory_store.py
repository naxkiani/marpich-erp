"""In-memory Bank Account Management persistence."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.bank_account import (
    AuthorizedSignatory,
    Bank,
    BankAccount,
    BankAccountDocument,
    BankBranch,
)
from contexts.treasury.domain.ports.bank_account_repositories import (
    IBankAccountDocumentRepository,
    IBankAccountRepository,
    IBankBranchRepository,
    IBankRepository,
    ISignatoryRepository,
)


class InMemoryBankRepository(IBankRepository):
    _banks: dict[str, Bank] = {}

    @classmethod
    def reset(cls) -> None:
        cls._banks = {}

    async def save(self, bank: Bank) -> None:
        self._banks[str(bank.id)] = bank

    async def find_by_id(self, bank_id: str) -> Bank | None:
        return self._banks.get(bank_id)

    async def find_by_code(self, tenant_id: str, code: str) -> Bank | None:
        return next(
            (b for b in self._banks.values() if b.tenant_id == tenant_id and b.code == code.upper()),
            None,
        )

    async def list_by_tenant(self, tenant_id: str, organization_id: str | None = None) -> list[Bank]:
        banks = [b for b in self._banks.values() if b.tenant_id == tenant_id]
        if organization_id:
            banks = [b for b in banks if b.organization_id == organization_id]
        return banks


class InMemoryBankBranchRepository(IBankBranchRepository):
    _branches: dict[str, BankBranch] = {}

    @classmethod
    def reset(cls) -> None:
        cls._branches = {}

    async def save(self, branch: BankBranch) -> None:
        self._branches[str(branch.id)] = branch

    async def find_by_id(self, branch_id: str) -> BankBranch | None:
        return self._branches.get(branch_id)

    async def find_by_code(self, tenant_id: str, bank_id: str, code: str) -> BankBranch | None:
        return next(
            (
                b
                for b in self._branches.values()
                if b.tenant_id == tenant_id and b.bank_id == bank_id and b.code == code.upper()
            ),
            None,
        )

    async def list_by_bank(self, tenant_id: str, bank_id: str) -> list[BankBranch]:
        return [
            b for b in self._branches.values() if b.tenant_id == tenant_id and b.bank_id == bank_id
        ]

    async def list_by_tenant(self, tenant_id: str, organization_id: str | None = None) -> list[BankBranch]:
        branches = [b for b in self._branches.values() if b.tenant_id == tenant_id]
        if organization_id:
            branches = [b for b in branches if b.organization_id == organization_id]
        return branches


class InMemoryBankAccountRepository(IBankAccountRepository):
    _accounts: dict[str, BankAccount] = {}

    @classmethod
    def reset(cls) -> None:
        cls._accounts = {}

    async def save(self, account: BankAccount) -> None:
        self._accounts[str(account.id)] = account

    async def find_by_id(self, account_id: str) -> BankAccount | None:
        return self._accounts.get(account_id)

    async def find_by_code(self, tenant_id: str, code: str) -> BankAccount | None:
        return next(
            (a for a in self._accounts.values() if a.tenant_id == tenant_id and a.code == code.upper()),
            None,
        )

    async def list_by_tenant(
        self, tenant_id: str, organization_id: str | None = None
    ) -> list[BankAccount]:
        accounts = [a for a in self._accounts.values() if a.tenant_id == tenant_id]
        if organization_id:
            accounts = [a for a in accounts if a.organization_id == organization_id]
        return accounts

    async def list_by_bank(self, tenant_id: str, bank_id: str) -> list[BankAccount]:
        return [
            a for a in self._accounts.values() if a.tenant_id == tenant_id and a.bank_id == bank_id
        ]


class InMemorySignatoryRepository(ISignatoryRepository):
    _signatories: dict[str, AuthorizedSignatory] = {}

    @classmethod
    def reset(cls) -> None:
        cls._signatories = {}

    async def save(self, signatory: AuthorizedSignatory) -> None:
        self._signatories[str(signatory.id)] = signatory

    async def find_by_id(self, signatory_id: str) -> AuthorizedSignatory | None:
        return self._signatories.get(signatory_id)

    async def list_by_account(self, bank_account_id: str) -> list[AuthorizedSignatory]:
        return [s for s in self._signatories.values() if s.bank_account_id == bank_account_id]


class InMemoryBankAccountDocumentRepository(IBankAccountDocumentRepository):
    _documents: dict[str, BankAccountDocument] = {}

    @classmethod
    def reset(cls) -> None:
        cls._documents = {}

    async def save(self, document: BankAccountDocument) -> None:
        self._documents[str(document.id)] = document

    async def find_by_id(self, document_id: str) -> BankAccountDocument | None:
        return self._documents.get(document_id)

    async def list_by_account(self, bank_account_id: str) -> list[BankAccountDocument]:
        return [d for d in self._documents.values() if d.bank_account_id == bank_account_id]
