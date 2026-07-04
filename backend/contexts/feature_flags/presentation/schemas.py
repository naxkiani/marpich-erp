"""Feature flag API schemas."""
from pydantic import BaseModel, Field


class CreateFlagRequest(BaseModel):
    key: str = Field(min_length=2, max_length=128, pattern=r"^[a-z][a-z0-9_]*$")
    name: str = Field(min_length=2, max_length=256)
    default_enabled: bool = False


class UpdateFlagRequest(BaseModel):
    default_enabled: bool | None = None
    tenant_rules: dict[str, bool] | None = None
    organization_rules: dict[str, bool] | None = None
    user_rules: dict[str, bool] | None = None
    environment_rules: dict[str, bool] | None = None
    country_rules: dict[str, bool] | None = None
    industry_rules: dict[str, bool] | None = None


class EvaluateRequest(BaseModel):
    flags: list[str] = Field(min_length=1)
    context: dict = Field(default_factory=dict)


class RolloutRequest(BaseModel):
    percentage: int = Field(ge=0, le=100)
    stage: str = Field(pattern=r"^(off|canary|full)$")


class AbTestRequest(BaseModel):
    variants: list[dict] = Field(min_length=2)


class EmergencyDisableRequest(BaseModel):
    reason: str = Field(min_length=3, max_length=512)


class RollbackRequest(BaseModel):
    target_version: int = Field(ge=1)
