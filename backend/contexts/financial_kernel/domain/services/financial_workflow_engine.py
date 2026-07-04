"""Financial workflow engine — SLA, escalation, AI, signature."""
from __future__ import annotations

import hashlib
import hmac
from datetime import UTC, datetime, timedelta

SIGNING_SECRET = "marpich-financial-workflow-sign-v1"

DEFAULT_SLA_HOURS: dict[str, int] = {
    "approval": 24,
    "payment": 8,
    "purchase": 48,
    "expense": 24,
    "transfer": 4,
    "budget": 72,
    "invoice": 24,
    "payroll": 48,
    "tax": 72,
    "treasury": 4,
}

DEFAULT_ESCALATION_TARGET = "finance_manager"


def default_sla_hours(workflow_type: str) -> int:
    return DEFAULT_SLA_HOURS.get(workflow_type, 24)


def compute_sla_deadline(sla_hours: int, start: datetime | None = None) -> datetime:
    base = start or datetime.now(UTC)
    return base + timedelta(hours=sla_hours)


def generate_ai_recommendation(
    *,
    workflow_type: str,
    amount: float | None,
    currency: str,
    metadata: dict,
) -> dict:
    """Stub AI recommendation — delegates to AI Platform in production."""
    risk_score = 0.3
    if amount and amount > 10000:
        risk_score = 0.7
    elif amount and amount > 5000:
        risk_score = 0.5

    recommend = "approve"
    if risk_score >= 0.7:
        recommend = "review"
    elif workflow_type in ("transfer", "treasury") and amount and amount > 50000:
        recommend = "escalate"

    return {
        "recommendation": recommend,
        "confidence": round(1 - risk_score, 2),
        "risk_score": risk_score,
        "reasoning": f"Based on {workflow_type} workflow amount {currency} {amount or 0}",
        "factors": {
            "amount": amount,
            "workflow_type": workflow_type,
            "metadata_keys": list(metadata.keys()),
        },
        "generated_at": datetime.now(UTC).isoformat(),
        "source": "financial_kernel.ai.stub",
    }


def sign_workflow(*, workflow_id: str, workflow_type: str, signer_id: str, algorithm: str = "RS256") -> dict:
    payload = f"{workflow_id}:{workflow_type}:{signer_id}"
    signature = hmac.new(SIGNING_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return {
        "signer_id": signer_id,
        "algorithm": algorithm,
        "signature": signature,
        "signed_at": datetime.now(UTC).isoformat(),
        "workflow_id": workflow_id,
    }


def escalation_target(workflow_type: str, metadata: dict) -> str:
    return metadata.get("escalation_target") or DEFAULT_ESCALATION_TARGET
