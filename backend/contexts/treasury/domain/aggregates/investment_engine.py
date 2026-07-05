"""Enterprise Investment Management aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class InvestmentType(StrEnum):
    FIXED_DEPOSIT = "fixed_deposit"
    BONDS = "bonds"
    GOVERNMENT_SECURITIES = "government_securities"
    MUTUAL_FUNDS = "mutual_funds"


class InvestmentStatus(StrEnum):
    ACTIVE = "active"
    MATURED = "matured"
    REDEEMED = "redeemed"
    SOLD = "sold"


class RiskRating(StrEnum):
    AAA = "aaa"
    AA = "aa"
    A = "a"
    BBB = "bbb"
    BB = "bb"
    B = "b"
    UNRATED = "unrated"


class InvestmentTransactionType(StrEnum):
    PURCHASE = "purchase"
    INTEREST_ACCRUAL = "interest_accrual"
    INCOME = "income"
    MATURITY = "maturity"
    REDEMPTION = "redemption"
    SALE = "sale"


DEFAULT_RISK_BY_TYPE: dict[str, str] = {
    InvestmentType.GOVERNMENT_SECURITIES.value: RiskRating.AAA.value,
    InvestmentType.FIXED_DEPOSIT.value: RiskRating.A.value,
    InvestmentType.BONDS.value: RiskRating.BBB.value,
    InvestmentType.MUTUAL_FUNDS.value: RiskRating.BBB.value,
}


@dataclass(eq=False, kw_only=True)
class Investment(AggregateRoot):
    tenant_id: str
    portfolio_name: str
    investment_type: str
    name: str
    instrument_code: str
    principal_amount: float
    current_value: float
    currency: str
    interest_rate: float
    accrued_interest: float
    total_income: float
    purchase_date: str
    maturity_date: str | None
    risk_rating: str
    status: str
    treasury_account_id: str | None = None
    notes: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        portfolio_name: str,
        investment_type: str,
        name: str,
        instrument_code: str,
        principal_amount: float,
        currency: str,
        interest_rate: float = 0.0,
        purchase_date: str,
        maturity_date: str | None = None,
        risk_rating: str | None = None,
        treasury_account_id: str | None = None,
        notes: str | None = None,
    ) -> Investment:
        rating = risk_rating or DEFAULT_RISK_BY_TYPE.get(investment_type, RiskRating.UNRATED.value)
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            portfolio_name=portfolio_name.strip(),
            investment_type=investment_type,
            name=name.strip(),
            instrument_code=instrument_code.strip().upper(),
            principal_amount=round(principal_amount, 2),
            current_value=round(principal_amount, 2),
            currency=currency.strip().upper(),
            interest_rate=round(interest_rate, 4),
            accrued_interest=0.0,
            total_income=0.0,
            purchase_date=purchase_date,
            maturity_date=maturity_date,
            risk_rating=rating,
            status=InvestmentStatus.ACTIVE.value,
            treasury_account_id=treasury_account_id,
            notes=notes,
        )

    def accrue_interest(self, amount: float) -> None:
        if self.status != InvestmentStatus.ACTIVE.value:
            raise ValueError("not_active")
        self.accrued_interest = round(self.accrued_interest + amount, 2)
        self.current_value = round(self.principal_amount + self.accrued_interest, 2)
        self.updated_at = datetime.now(UTC)

    def record_income(self, amount: float) -> None:
        if self.status != InvestmentStatus.ACTIVE.value:
            raise ValueError("not_active")
        self.total_income = round(self.total_income + amount, 2)
        self.accrued_interest = round(max(0, self.accrued_interest - amount), 2)
        self.current_value = round(self.principal_amount + self.accrued_interest, 2)
        self.updated_at = datetime.now(UTC)

    def mature(self) -> float:
        if self.status != InvestmentStatus.ACTIVE.value:
            raise ValueError("not_active")
        proceeds = round(self.principal_amount + self.accrued_interest, 2)
        self.status = InvestmentStatus.MATURED.value
        self.current_value = proceeds
        self.updated_at = datetime.now(UTC)
        return proceeds

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "portfolio_name": self.portfolio_name,
            "investment_type": self.investment_type,
            "name": self.name,
            "instrument_code": self.instrument_code,
            "principal_amount": self.principal_amount,
            "current_value": self.current_value,
            "currency": self.currency,
            "interest_rate": self.interest_rate,
            "accrued_interest": self.accrued_interest,
            "total_income": self.total_income,
            "purchase_date": self.purchase_date,
            "maturity_date": self.maturity_date,
            "risk_rating": self.risk_rating,
            "status": self.status,
            "treasury_account_id": self.treasury_account_id,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class InvestmentTransaction(AggregateRoot):
    tenant_id: str
    investment_id: str
    transaction_type: str
    amount: float
    currency: str
    transaction_date: str
    reference: str = ""
    notes: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        investment_id: str,
        transaction_type: str,
        amount: float,
        currency: str,
        transaction_date: str,
        reference: str = "",
        notes: str | None = None,
    ) -> InvestmentTransaction:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            investment_id=investment_id,
            transaction_type=transaction_type,
            amount=round(amount, 2),
            currency=currency.strip().upper(),
            transaction_date=transaction_date,
            reference=reference,
            notes=notes,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "investment_id": self.investment_id,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "currency": self.currency,
            "transaction_date": self.transaction_date,
            "reference": self.reference,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }
