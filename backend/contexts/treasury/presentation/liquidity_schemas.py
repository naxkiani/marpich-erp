"""Enterprise Liquidity Engine API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateCashPoolRequest(BaseModel):
    code: str
    name: str
    currency: str = "USD"
    target_balance: float = 0.0
    minimum_balance: float = 0.0
    member_account_ids: list[str] | None = None


class CreateFundingNeedRequest(BaseModel):
    label: str
    currency: str = "USD"
    required_amount: float = Field(gt=0)
    available_amount: float = Field(ge=0)
    due_date: str


class LiquidityPredictionRequest(BaseModel):
    horizon_days: int = Field(default=30, ge=7, le=90)
