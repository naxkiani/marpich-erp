"""Money value object — amount + currency."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from shared.domain.value_objects.currency import Currency


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: Currency

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")

    def add(self, other: Money) -> Money:
        self._assert_same_currency(other)
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def subtract(self, other: Money) -> Money:
        self._assert_same_currency(other)
        result = self.amount - other.amount
        if result < 0:
            raise ValueError("Money subtraction would be negative")
        return Money(amount=result, currency=self.currency)

    def multiply(self, factor: Decimal) -> Money:
        return Money(amount=self.amount * factor, currency=self.currency)

    def _assert_same_currency(self, other: Money) -> None:
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")

    def to_dict(self) -> dict:
        return {"amount": str(self.amount), "currency": str(self.currency)}
