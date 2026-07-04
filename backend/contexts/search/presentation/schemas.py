"""Search API schemas."""
from pydantic import BaseModel, Field


class ReindexRequest(BaseModel):
    confirm: bool = Field(default=True)
