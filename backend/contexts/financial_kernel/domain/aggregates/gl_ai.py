"""General Ledger AI Assistant aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class GLAICapability(StrEnum):
    POSTING_SUGGESTIONS = "posting_suggestions"
    ACCOUNT_SUGGESTIONS = "account_suggestions"
    DUPLICATE_DETECTION = "duplicate_detection"
    FRAUD_DETECTION = "fraud_detection"
    CLOSING_ASSISTANT = "closing_assistant"
    ANOMALY_DETECTION = "anomaly_detection"
    FINANCIAL_INSIGHTS = "financial_insights"
    AUTOMATIC_CLASSIFICATION = "automatic_classification"
    FORECASTING = "forecasting"
    JOURNAL_EXPLANATION = "journal_explanation"
    VARIANCE_ANALYSIS = "variance_analysis"
    AI_CFO_DASHBOARD = "ai_cfo_dashboard"


class GLAIJobStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(eq=False, kw_only=True)
class GLAIJob(AggregateRoot):
    tenant_id: str
    capability: str
    status: GLAIJobStatus
    input_data: dict
    result: dict | None
    confidence: float | None
    recommendations: list[dict]
    correlation_id: str
    created_by: str | None
    completed_at: datetime | None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        capability: str,
        input_data: dict,
        correlation_id: str,
        created_by: str | None = None,
    ) -> GLAIJob:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            capability=capability,
            status=GLAIJobStatus.PENDING,
            input_data=input_data,
            result=None,
            confidence=None,
            recommendations=[],
            correlation_id=correlation_id,
            created_by=created_by,
            completed_at=None,
        )

    def complete(
        self, result: dict, confidence: float, recommendations: list[dict] | None = None
    ) -> None:
        self.status = GLAIJobStatus.COMPLETED
        self.result = result
        self.confidence = round(confidence, 2)
        self.recommendations = recommendations or result.get("recommendations", [])
        self.completed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "capability": self.capability,
            "status": self.status.value,
            "input_data": self.input_data,
            "result": self.result,
            "confidence": self.confidence,
            "recommendations": self.recommendations,
            "correlation_id": self.correlation_id,
            "created_by": self.created_by,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat(),
        }
