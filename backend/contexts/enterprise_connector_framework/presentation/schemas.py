"""Enterprise Connector Framework presentation schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class RegisterConnectorRequest(BaseModel):
    connector_type: str = Field(min_length=2, max_length=64)
    display_name: str = Field(min_length=2, max_length=128)
    config: dict = Field(default_factory=dict)
    plugin_id: str = ""


class ExecuteOperationRequest(BaseModel):
    operation: str = Field(min_length=2, max_length=64)
    payload: dict = Field(default_factory=dict)
    idempotency_key: str = ""


class RegisterPluginBindingRequest(BaseModel):
    plugin_id: str = Field(min_length=3, max_length=128)
    instance_ref: str = Field(min_length=3, max_length=64)
    extension_point: str = "connector.execute"
