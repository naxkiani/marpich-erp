"""Identity resilience API schemas."""
from __future__ import annotations

from pydantic import BaseModel


class RegisterRegionRequest(BaseModel):
    region_id: str
    display_name: str
    is_primary: bool = False


class DeployWorkerRequest(BaseModel):
    worker_type: str
    region_id: str
    role: str = "standby"


class FailoverRequest(BaseModel):
    worker_type: str
    reason: str = "manual_failover"
