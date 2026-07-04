"""Treasury account aggregates — cash, bank, petty cash, vault, safe."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class TreasuryAccountType(StrEnum):
    CASH = "cash"
    BANK = "bank"
    PETTY_CASH = "petty_cash"
    VAULT = "vault"
    SAFE = "safe"


@dataclass(eq=False, kw_only=True)
class TreasuryAccount(AggregateRoot):
    tenant_id: str
    code: str
    name: str
    account_type: str
    currency: str
    balance: float = 0.0
    bank_name: str | None = None
    account_number: str | None = None
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        code: str,
        name: str,
        account_type: str,
        currency: str = "USD",
        bank_name: str | None = None,
        account_number: str | None = None,
    ) -> TreasuryAccount:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            code=code.strip().upper(),
            name=name.strip(),
            account_type=account_type,
            currency=currency.strip().upper(),
            bank_name=bank_name,
            account_number=account_number,
        )

    def credit(self, amount: float) -> None:
        self.balance = round(self.balance + amount, 2)

    def debit(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("insufficient_balance")
        self.balance = round(self.balance - amount, 2)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "code": self.code,
            "name": self.name,
            "account_type": self.account_type,
            "currency": self.currency,
            "balance": self.balance,
            "bank_name": self.bank_name,
            "account_number": self.account_number,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }
