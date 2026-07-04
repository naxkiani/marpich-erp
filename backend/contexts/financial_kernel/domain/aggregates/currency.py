"""Enterprise Currency Engine aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class RateType(StrEnum):
    SPOT = "spot"
    HISTORICAL = "historical"
    AVERAGE = "average"
    MANUAL = "manual"
    CENTRAL_BANK = "central_bank"


class RateSource(StrEnum):
    MANUAL = "manual"
    CENTRAL_BANK = "central_bank"
    EXCHANGE_API = "exchange_api"
    SYSTEM = "system"


@dataclass(eq=False, kw_only=True)
class TenantCurrencySettings(AggregateRoot):
    tenant_id: str
    base_currency: str
    reporting_currency: str
    enabled_currencies: list[str] = field(default_factory=list)
    auto_update_enabled: bool = True
    auto_update_provider: str = "ecb"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create_default(cls, *, tenant_id: str, base_currency: str = "USD") -> TenantCurrencySettings:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            base_currency=base_currency,
            reporting_currency=base_currency,
            enabled_currencies=[base_currency, "EUR", "GBP", "IRR", "AED"],
        )

    def add_currency(self, code: str) -> None:
        normalized = code.strip().upper()
        if normalized not in self.enabled_currencies:
            self.enabled_currencies.append(normalized)
            self.updated_at = datetime.now(UTC)

    def set_base_currency(self, code: str) -> None:
        self.base_currency = code.strip().upper()
        self.add_currency(self.base_currency)
        self.updated_at = datetime.now(UTC)

    def set_reporting_currency(self, code: str) -> None:
        self.reporting_currency = code.strip().upper()
        self.add_currency(self.reporting_currency)
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "base_currency": self.base_currency,
            "reporting_currency": self.reporting_currency,
            "enabled_currencies": list(self.enabled_currencies),
            "auto_update_enabled": self.auto_update_enabled,
            "auto_update_provider": self.auto_update_provider,
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class ExchangeRate(AggregateRoot):
    tenant_id: str
    from_currency: str
    to_currency: str
    rate: float
    rate_type: str
    rate_source: str
    effective_date: str
    provider: str | None = None
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        from_currency: str,
        to_currency: str,
        rate: float,
        rate_type: str,
        rate_source: str,
        effective_date: str | None = None,
        provider: str | None = None,
    ) -> ExchangeRate:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            from_currency=from_currency.strip().upper(),
            to_currency=to_currency.strip().upper(),
            rate=round(rate, 8),
            rate_type=rate_type,
            rate_source=rate_source,
            effective_date=effective_date or date.today().isoformat(),
            provider=provider,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "from_currency": self.from_currency,
            "to_currency": self.to_currency,
            "rate": self.rate,
            "rate_type": self.rate_type,
            "rate_source": self.rate_source,
            "effective_date": self.effective_date,
            "provider": self.provider,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class ExchangeRateSnapshot(AggregateRoot):
    """Immutable rate snapshot stored on every financial transaction."""

    tenant_id: str
    transaction_currency: str
    base_currency: str
    reporting_currency: str
    transaction_to_base_rate: float
    transaction_to_reporting_rate: float
    base_to_reporting_rate: float
    rate_type: str
    rate_source: str
    effective_date: str
    journal_id: str | None = None
    source_context: str | None = None
    source_document_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def from_rates(
        cls,
        *,
        tenant_id: str,
        transaction_currency: str,
        base_currency: str,
        reporting_currency: str,
        transaction_to_base_rate: float,
        transaction_to_reporting_rate: float,
        rate_type: str,
        rate_source: str,
        effective_date: str,
        journal_id: str | None = None,
        source_context: str | None = None,
        source_document_id: str | None = None,
    ) -> ExchangeRateSnapshot:
        base_to_reporting = (
            1.0
            if base_currency == reporting_currency
            else round(transaction_to_reporting_rate / transaction_to_base_rate, 8)
            if transaction_to_base_rate
            else 1.0
        )
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            transaction_currency=transaction_currency,
            base_currency=base_currency,
            reporting_currency=reporting_currency,
            transaction_to_base_rate=round(transaction_to_base_rate, 8),
            transaction_to_reporting_rate=round(transaction_to_reporting_rate, 8),
            base_to_reporting_rate=base_to_reporting,
            rate_type=rate_type,
            rate_source=rate_source,
            effective_date=effective_date,
            journal_id=journal_id,
            source_context=source_context,
            source_document_id=source_document_id,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "transaction_currency": self.transaction_currency,
            "base_currency": self.base_currency,
            "reporting_currency": self.reporting_currency,
            "transaction_to_base_rate": self.transaction_to_base_rate,
            "transaction_to_reporting_rate": self.transaction_to_reporting_rate,
            "base_to_reporting_rate": self.base_to_reporting_rate,
            "rate_type": self.rate_type,
            "rate_source": self.rate_source,
            "effective_date": self.effective_date,
            "journal_id": self.journal_id,
            "source_context": self.source_context,
            "source_document_id": self.source_document_id,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class CurrencyRevaluation(AggregateRoot):
    tenant_id: str
    period_id: str | None
    revaluation_date: str
    base_currency: str
    reporting_currency: str
    rate_type: str
    total_gain: float
    total_loss: float
    net_gain_loss: float
    lines: list[dict]
    journal_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        period_id: str | None,
        revaluation_date: str,
        base_currency: str,
        reporting_currency: str,
        rate_type: str,
        lines: list[dict],
    ) -> CurrencyRevaluation:
        total_gain = round(sum(l.get("gain", 0) for l in lines), 2)
        total_loss = round(sum(l.get("loss", 0) for l in lines), 2)
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            period_id=period_id,
            revaluation_date=revaluation_date,
            base_currency=base_currency,
            reporting_currency=reporting_currency,
            rate_type=rate_type,
            total_gain=total_gain,
            total_loss=total_loss,
            net_gain_loss=round(total_gain - total_loss, 2),
            lines=lines,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "period_id": self.period_id,
            "revaluation_date": self.revaluation_date,
            "base_currency": self.base_currency,
            "reporting_currency": self.reporting_currency,
            "rate_type": self.rate_type,
            "total_gain": self.total_gain,
            "total_loss": self.total_loss,
            "net_gain_loss": self.net_gain_loss,
            "lines": self.lines,
            "journal_id": self.journal_id,
            "created_at": self.created_at.isoformat(),
        }
