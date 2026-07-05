"""Banking Analytics Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class AnalyticsCapability(StrEnum):
    LIQUIDITY_KPIS = "liquidity_kpis"
    DEPOSIT_TRENDS = "deposit_trends"
    LOAN_PORTFOLIO = "loan_portfolio"
    CUSTOMER_SEGMENTATION = "customer_segmentation"
    BRANCH_PERFORMANCE = "branch_performance"
    REVENUE_ANALYSIS = "revenue_analysis"
    RISK_INDICATORS = "risk_indicators"
    PORTFOLIO_QUALITY = "portfolio_quality"
    DELINQUENCY_ANALYSIS = "delinquency_analysis"
    FORECASTING = "forecasting"
    FRAUD_DETECTION = "fraud_detection"
    CUSTOMER_INSIGHTS = "customer_insights"
    EXECUTIVE_DASHBOARD = "executive_dashboard"
    AI_BANKING_ASSISTANT = "ai_banking_assistant"


class AnalyticsJobStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(eq=False, kw_only=True)
class BankingAnalyticsJob(AggregateRoot):
    tenant_id: str
    capability: str
    status: str = AnalyticsJobStatus.PENDING.value
    input_data: dict = field(default_factory=dict)
    result: dict | None = None
    confidence: float | None = None
    recommendations: list[dict] = field(default_factory=list)
    correlation_id: str = ""
    created_by: str | None = None
    completed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        capability: str,
        input_data: dict | None = None,
        correlation_id: str = "",
        created_by: str | None = None,
    ) -> BankingAnalyticsJob:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            capability=capability,
            input_data=input_data or {},
            correlation_id=correlation_id,
            created_by=created_by,
        )

    def complete(
        self, result: dict, confidence: float, recommendations: list[dict] | None = None
    ) -> None:
        self.status = AnalyticsJobStatus.COMPLETED.value
        self.result = result
        self.confidence = round(confidence, 2)
        self.recommendations = recommendations or result.get("recommendations", [])
        self.completed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "capability": self.capability,
            "status": self.status,
            "input_data": self.input_data,
            "result": self.result,
            "confidence": self.confidence,
            "recommendations": self.recommendations,
            "correlation_id": self.correlation_id,
            "created_by": self.created_by,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat(),
        }
