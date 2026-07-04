"""Organization API schemas."""
from pydantic import BaseModel, Field


class CreateUnitRequest(BaseModel):
    parent_id: str | None = None
    unit_type: str = Field(pattern=r"^(branch|department|ward|cost_center)$")
    code: str = Field(min_length=2, max_length=32)
    name: str = Field(min_length=2, max_length=128)


class AddMemberRequest(BaseModel):
    user_id: str
    title: str = Field(min_length=1, max_length=128)
    is_primary: bool = False
