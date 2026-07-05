"""Enterprise Treasury Risk Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class RiskType(StrEnum):
    LIQUIDITY_RISK = "liquidity_risk"
    INTEREST_RATE_RISK = "interest_rate_risk"
    FOREIGN_EXCHANGE_RISK = "foreign_exchange_risk"
    COUNTERPARTY_RISK = "counterparty_risk"
    OPERATIONAL_RISK = "operational_risk"


class LimitUnit(StrEnum):
    AMOUNT = "amount"
    PERCENT = "percent"
    COUNT = "count"


class AlertSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(StrEnum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


STRESS_SCENARIOS: dict[str, dict] = {
    "liquidity_shock": {
        "label": "Liquidity Shock",
        "risk_type": RiskType.LIQUIDITY_RISK.value,
        "shock_pct": -30,
    },
    "rate_shock_up": {
        "label": "Interest Rate +200bps",
        "risk_type": RiskType.INTEREST_RATE_RISK.value,
        "rate_bps": 200,
    },
    "fx_depreciation": {
        "label": "FX Depreciation -10%",
        "risk_type": RiskType.FOREIGN_EXCHANGE_RISK.value,
        "fx_shock_pct": -10,
    },
    "counterparty_default": {
        "label": "Top Counterparty Default",
        "risk_type": RiskType.COUNTERPARTY_RISK.value,
        "default_pct": 100,
    },
    "operational_disruption": {
        "label": "Operational Disruption",
        "risk_type": RiskType.OPERATIONAL_RISK.value,
        "exception_multiplier": 3,
    },
}


@dataclass(eq=False, kw_only=True)
class TreasuryRiskLimit(AggregateRoot):
    tenant_id: str
    risk_type: str
    name: str
    threshold_value: float
    threshold_unit: str
    currency: str = "USD"
    is_active: bool = True
    description: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        risk_type: str,
        name: str,
        threshold_value: float,
        threshold_unit: str,
        currency: str = "USD",
        description: str = "",
    ) -> TreasuryRiskLimit:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            risk_type=risk_type,
            name=name.strip(),
            threshold_value=round(threshold_value, 4),
            threshold_unit=threshold_unit,
            currency=currency.strip().upper(),
            description=description,
        )

    def update_threshold(self, value: float) -> None:
        self.threshold_value = round(value, 4)
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "risk_type": self.risk_type,
            "name": self.name,
            "threshold_value": self.threshold_value,
            "threshold_unit": self.threshold_unit,
            "currency": self.currency,
            "is_active": self.is_active,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class RiskAlert(AggregateRoot):
    tenant_id: str
    risk_type: str
    limit_id: str
    exposure_value: float
    limit_value: float
    severity: str
    message: str
    status: str = AlertStatus.OPEN.value
    acknowledged_by: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    resolved_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        risk_type: str,
        limit_id: str,
        exposure_value: float,
        limit_value: float,
        severity: str,
        message: str,
    ) -> RiskAlert:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            risk_type=risk_type,
            limit_id=limit_id,
            exposure_value=round(exposure_value, 4),
            limit_value=round(limit_value, 4),
            severity=severity,
            message=message,
        )

    def acknowledge(self, actor_id: str) -> None:
        self.status = AlertStatus.ACKNOWLEDGED.value
        self.acknowledged_by = actor_id

    def resolve(self) -> None:
        self.status = AlertStatus.RESOLVED.value
        self.resolved_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "risk_type": self.risk_type,
            "limit_id": self.limit_id,
            "exposure_value": self.exposure_value,
            "limit_value": self.limit_value,
            "severity": self.severity,
            "message": self.message,
            "status": self.status,
            "acknowledged_by": self.acknowledged_by,
            "created_at": self.created_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }


@dataclass(eq=False, kw_only=True)
class StressTestRun(AggregateRoot):
    tenant_id: str
    scenario: str
    parameters: dict
    results: dict
    impact_score: float
    run_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        scenario: str,
        parameters: dict,
        results: dict,
        impact_score: float,
    ) -> StressTestRun:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            scenario=scenario,
            parameters=parameters,
            results=results,
            impact_score=round(impact_score, 2),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "scenario": self.scenario,
            "parameters": self.parameters,
            "results": self.results,
            "impact_score": self.impact_score,
            "run_at": self.run_at.isoformat(),
        }
