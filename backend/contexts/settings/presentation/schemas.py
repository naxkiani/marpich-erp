"""Settings API schemas."""
from typing import Any

from pydantic import BaseModel, Field


class UpdateConfigRequest(BaseModel):
    value: Any


class ToggleFeatureRequest(BaseModel):
    enabled: bool


class UpdateBrandingRequest(BaseModel):
    app_name: str | None = None
    primary_color: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")
    logo_url: str | None = None
