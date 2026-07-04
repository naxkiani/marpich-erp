"""Ledger account — Finance bounded context."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class AccountType(StrEnum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


@dataclass(eq=False, kw_only=True)
class Account(AggregateRoot):
    tenant_id: str
    code: str
    name: str
    account_type: AccountType
    balance: float = 0.0
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        code: str,
        name: str,
        account_type: AccountType,
    ) -> Account:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            code=code.strip(),
            name=name.strip(),
            account_type=account_type,
        )

    def apply_debit(self, amount: float) -> None:
        if self.account_type in (AccountType.ASSET, AccountType.EXPENSE):
            self.balance = round(self.balance + amount, 2)
        else:
            self.balance = round(self.balance - amount, 2)

    def apply_credit(self, amount: float) -> None:
        if self.account_type in (AccountType.ASSET, AccountType.EXPENSE):
            self.balance = round(self.balance - amount, 2)
        else:
            self.balance = round(self.balance + amount, 2)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "code": self.code,
            "name": self.name,
            "account_type": self.account_type.value,
            "balance": self.balance,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }
