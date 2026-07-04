"""Core Platform API schemas."""
from pydantic import BaseModel, Field


class ProvisionTenantRequest(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    slug: str = Field(min_length=3, max_length=64, pattern=r"^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$")
    industry_pack: str = Field(min_length=2, max_length=64)
    tier: str = Field(default="professional", pattern=r"^(starter|professional|enterprise)$")
    optional_modules: list[str] = Field(default_factory=list)
    locale: str | None = None
    timezone: str = "UTC"
    data_region: str = "us-east"


class ActivateModuleRequest(BaseModel):
    module_id: str = Field(min_length=3, max_length=128)
