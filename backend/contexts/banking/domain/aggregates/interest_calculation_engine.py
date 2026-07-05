"""Interest Calculation Engine aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class CalcFrequency(StrEnum):
    DAILY = "daily"
    MONTHLY = "monthly"
    ANNUAL = "annual"


class InterestMethod(StrEnum):
    SIMPLE = "simple"
    COMPOUND = "compound"


class RateType(StrEnum):
    FIXED = "fixed"
    FLOATING = "floating"
    PROMOTIONAL = "promotional"


class CalcMode(StrEnum):
    PRODUCTION = "production"
    SIMULATION = "simulation"


class ProductContext(StrEnum):
    DEPOSIT = "deposit"
    LOAN = "loan"
    GENERIC = "generic"


@dataclass(eq=False, kw_only=True)
class InterestRateProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    product_context: str
    rate_type: str
    rate_annual: float
    spread_bps: float = 0.0
    index_ref: str = ""
    promotional_until: datetime | None = None
    promotional_rate_annual: float | None = None
    currency: str = "USD"
    active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        profile_ref: str,
        product_context: str,
        rate_type: str,
        rate_annual: float,
        spread_bps: float = 0.0,
        index_ref: str = "",
        promotional_until: datetime | None = None,
        promotional_rate_annual: float | None = None,
        currency: str = "USD",
    ) -> InterestRateProfile:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            profile_ref=profile_ref,
            product_context=product_context,
            rate_type=rate_type,
            rate_annual=round(rate_annual, 6),
            spread_bps=spread_bps,
            index_ref=index_ref,
            promotional_until=promotional_until,
            promotional_rate_annual=(
                round(promotional_rate_annual, 6) if promotional_rate_annual is not None else None
            ),
            currency=currency,
        )

    def update_rate(self, *, rate_annual: float, rate_type: str | None = None) -> None:
        self.rate_annual = round(rate_annual, 6)
        if rate_type:
            self.rate_type = rate_type
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "profile_ref": self.profile_ref,
            "product_context": self.product_context,
            "rate_type": self.rate_type,
            "rate_annual": self.rate_annual,
            "spread_bps": self.spread_bps,
            "index_ref": self.index_ref,
            "promotional_until": self.promotional_until.isoformat() if self.promotional_until else None,
            "promotional_rate_annual": self.promotional_rate_annual,
            "currency": self.currency,
            "active": self.active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class InterestRateChange(AggregateRoot):
    tenant_id: str
    profile_id: str
    previous_rate_annual: float
    new_rate_annual: float
    rate_type: str
    effective_from: datetime
    reason: str = ""
    changed_by: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        profile_id: str,
        previous_rate_annual: float,
        new_rate_annual: float,
        rate_type: str,
        effective_from: datetime,
        reason: str = "",
        changed_by: str | None = None,
    ) -> InterestRateChange:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            profile_id=profile_id,
            previous_rate_annual=round(previous_rate_annual, 6),
            new_rate_annual=round(new_rate_annual, 6),
            rate_type=rate_type,
            effective_from=effective_from,
            reason=reason.strip(),
            changed_by=changed_by,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "profile_id": self.profile_id,
            "previous_rate_annual": self.previous_rate_annual,
            "new_rate_annual": self.new_rate_annual,
            "rate_type": self.rate_type,
            "effective_from": self.effective_from.isoformat(),
            "reason": self.reason,
            "changed_by": self.changed_by,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class InterestCalculationAudit(AggregateRoot):
    tenant_id: str
    calc_ref: str
    mode: str
    product_context: str
    principal: float
    currency: str
    frequency: str
    method: str
    rate_annual: float
    rate_type: str
    effective_days: int
    grace_days_applied: int
    interest_amount: float
    penalty_interest: float
    profit_share_amount: float
    profile_id: str | None = None
    source_ref: str = ""
    policy_snapshot: dict = field(default_factory=dict)
    calculation_detail: dict = field(default_factory=dict)
    actor_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        calc_ref: str,
        mode: str,
        product_context: str,
        principal: float,
        currency: str,
        frequency: str,
        method: str,
        rate_annual: float,
        rate_type: str,
        effective_days: int,
        grace_days_applied: int,
        interest_amount: float,
        penalty_interest: float = 0.0,
        profit_share_amount: float = 0.0,
        profile_id: str | None = None,
        source_ref: str = "",
        policy_snapshot: dict | None = None,
        calculation_detail: dict | None = None,
        actor_id: str | None = None,
    ) -> InterestCalculationAudit:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            calc_ref=calc_ref,
            mode=mode,
            product_context=product_context,
            principal=round(principal, 2),
            currency=currency,
            frequency=frequency,
            method=method,
            rate_annual=round(rate_annual, 6),
            rate_type=rate_type,
            effective_days=effective_days,
            grace_days_applied=grace_days_applied,
            interest_amount=round(interest_amount, 2),
            penalty_interest=round(penalty_interest, 2),
            profit_share_amount=round(profit_share_amount, 2),
            profile_id=profile_id,
            source_ref=source_ref,
            policy_snapshot=policy_snapshot or {},
            calculation_detail=calculation_detail or {},
            actor_id=actor_id,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "calc_ref": self.calc_ref,
            "mode": self.mode,
            "product_context": self.product_context,
            "principal": self.principal,
            "currency": self.currency,
            "frequency": self.frequency,
            "method": self.method,
            "rate_annual": self.rate_annual,
            "rate_type": self.rate_type,
            "effective_days": self.effective_days,
            "grace_days_applied": self.grace_days_applied,
            "interest_amount": self.interest_amount,
            "penalty_interest": self.penalty_interest,
            "profit_share_amount": self.profit_share_amount,
            "profile_id": self.profile_id,
            "source_ref": self.source_ref,
            "policy_snapshot": self.policy_snapshot,
            "calculation_detail": self.calculation_detail,
            "actor_id": self.actor_id,
            "created_at": self.created_at.isoformat(),
        }
