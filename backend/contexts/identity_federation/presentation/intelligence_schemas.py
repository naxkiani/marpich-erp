"""P198-C2 Intelligence / AI / Copilot API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AiPredictRequest(BaseModel):
    model_id: str = "identity_risk_predictor_v1"
    features: dict = Field(default_factory=dict)


class AiFeedbackRequest(BaseModel):
    prediction_id: str
    useful: bool
    label: str | None = None


class CopilotRequest(BaseModel):
    question: str
    context: dict = Field(default_factory=dict)


class ExplainDecisionRequest(BaseModel):
    decision: dict = Field(default_factory=dict)


class ExplainTrustRequest(BaseModel):
    trust: dict = Field(default_factory=dict)


class AiInferRequest(BaseModel):
    surface: str
    payload: dict = Field(default_factory=dict)


class ConsentRequest(BaseModel):
    subject_id: str
    purpose: str
    granted: bool = True
