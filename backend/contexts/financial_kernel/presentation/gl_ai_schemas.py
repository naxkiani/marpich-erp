"""General Ledger AI API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class GLAnalyzeRequest(BaseModel):
    input_data: dict = Field(default_factory=dict)


class GLExplainJournalRequest(BaseModel):
    journal_id: str
