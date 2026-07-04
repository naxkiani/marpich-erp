"""Financial AI API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    input_data: dict = Field(default_factory=dict)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class InvoiceClassifyRequest(BaseModel):
    text: str
    amount: float | None = None


class DocumentOCRRequest(BaseModel):
    text: str
