"""Integration API schemas."""
from pydantic import BaseModel, Field


class RegisterConnectorRequest(BaseModel):
    connector_type: str = Field(pattern=r"^(crm|erp|custom)$")
    name: str = Field(min_length=2, max_length=128)
    config: dict | None = None


class CreateWebhookRequest(BaseModel):
    target_url: str = Field(min_length=4, max_length=512)
    event_pattern: str = Field(min_length=1, max_length=128)
    secret: str = ""
    description: str = ""


class TriggerSyncJobRequest(BaseModel):
    connector_id: str
    job_type: str = Field(default="full_sync", min_length=2, max_length=64)
