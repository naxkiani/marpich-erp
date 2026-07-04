"""Financial AI aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class AICapability(StrEnum):
    FRAUD_DETECTION = "fraud_detection"
    CASH_FLOW_PREDICTION = "cash_flow_prediction"
    BUDGET_FORECAST = "budget_forecast"
    EXPENSE_ANALYSIS = "expense_analysis"
    REVENUE_PREDICTION = "revenue_prediction"
    FINANCIAL_SUMMARY = "financial_summary"
    RISK_ANALYSIS = "risk_analysis"
    RECOMMENDATION = "recommendation"
    INVOICE_CLASSIFICATION = "invoice_classification"
    DOCUMENT_OCR = "document_ocr"
    FINANCIAL_CHATBOT = "financial_chatbot"
    DASHBOARD = "dashboard"
    CFO_ASSISTANT = "cfo_assistant"


class AIJobStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(eq=False, kw_only=True)
class FinancialAIJob(AggregateRoot):
    tenant_id: str
    capability: str
    status: AIJobStatus
    input_data: dict
    result: dict | None
    confidence: float | None
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
    ) -> FinancialAIJob:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            capability=capability,
            status=AIJobStatus.PENDING,
            input_data=input_data,
            result=None,
            confidence=None,
            correlation_id=correlation_id,
            created_by=created_by,
            completed_at=None,
        )

    def complete(self, result: dict, confidence: float) -> None:
        self.status = AIJobStatus.COMPLETED
        self.result = result
        self.confidence = round(confidence, 2)
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
            "correlation_id": self.correlation_id,
            "created_by": self.created_by,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class FinancialAIChatSession(AggregateRoot):
    tenant_id: str
    session_type: str
    messages: list[dict]
    context: dict
    created_by: str | None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        session_type: str,
        context: dict | None = None,
        created_by: str | None = None,
    ) -> FinancialAIChatSession:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            session_type=session_type,
            messages=[],
            context=dict(context or {}),
            created_by=created_by,
        )

    def add_message(self, role: str, content: str, metadata: dict | None = None) -> dict:
        msg = {
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now(UTC).isoformat(),
        }
        self.messages.append(msg)
        return msg

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "session_type": self.session_type,
            "messages": self.messages,
            "context": self.context,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
        }
