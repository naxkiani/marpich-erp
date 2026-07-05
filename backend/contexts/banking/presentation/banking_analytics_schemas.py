"""Banking Analytics Platform API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class RunAnalysisRequest(BaseModel):
    input_data: dict = Field(default_factory=dict)


class AIAssistantRequest(BaseModel):
    query: str = ""
