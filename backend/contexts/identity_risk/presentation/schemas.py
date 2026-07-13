"""Identity risk API schemas."""
from __future__ import annotations

from pydantic import BaseModel


class EvaluateRiskRequest(BaseModel):
    event_type: str
    payload: dict = {}
