"""Multi-Currency Treasury aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class RateType(StrEnum):
    CENTRAL_BANK = "central_bank"
    MARKET = "market"
    MANUAL = "manual"
    HISTORICAL = "historical"


class FxTransactionType(StrEnum):
    CONVERSION = "conversion"
    REVALUATION = "revaluation"
    CROSS_CURRENCY_TRANSFER = "cross_currency_transfer"
    EXCHANGE_GAIN = "exchange_gain"
    EXCHANGE_LOSS = "exchange_loss"


BASE_CURRENCY = "USD"


@dataclass(eq=False, kw_only=True)
class ExchangeRate(AggregateRoot):
    tenant_id: str
    base_currency: str
    quote_currency: str
    rate: float
    rate_type: str
    effective_date: str
    source: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        base_currency: str,
        quote_currency: str,
        rate: float,
        rate_type: str,
        effective_date: str,
        source: str = "",
    ) -> ExchangeRate:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            base_currency=base_currency.strip().upper(),
            quote_currency=quote_currency.strip().upper(),
            rate=round(rate, 6),
            rate_type=rate_type,
            effective_date=effective_date,
            source=source,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "base_currency": self.base_currency,
            "quote_currency": self.quote_currency,
            "rate": self.rate,
            "rate_type": self.rate_type,
            "effective_date": self.effective_date,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class FxTransaction(AggregateRoot):
    tenant_id: str
    transaction_type: str
    from_currency: str
    to_currency: str
    from_amount: float
    to_amount: float
    exchange_rate: float
    rate_type: str
    gain_loss: float
    from_account_id: str | None = None
    to_account_id: str | None = None
    reference: str = ""
    transaction_date: str = ""
    notes: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        transaction_type: str,
        from_currency: str,
        to_currency: str,
        from_amount: float,
        to_amount: float,
        exchange_rate: float,
        rate_type: str,
        gain_loss: float = 0.0,
        from_account_id: str | None = None,
        to_account_id: str | None = None,
        reference: str = "",
        transaction_date: str = "",
        notes: str | None = None,
    ) -> FxTransaction:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            transaction_type=transaction_type,
            from_currency=from_currency.strip().upper(),
            to_currency=to_currency.strip().upper(),
            from_amount=round(from_amount, 2),
            to_amount=round(to_amount, 2),
            exchange_rate=round(exchange_rate, 6),
            rate_type=rate_type,
            gain_loss=round(gain_loss, 2),
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            reference=reference,
            transaction_date=transaction_date,
            notes=notes,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "transaction_type": self.transaction_type,
            "from_currency": self.from_currency,
            "to_currency": self.to_currency,
            "from_amount": self.from_amount,
            "to_amount": self.to_amount,
            "exchange_rate": self.exchange_rate,
            "rate_type": self.rate_type,
            "gain_loss": self.gain_loss,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
            "reference": self.reference,
            "transaction_date": self.transaction_date,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }
