"""HTTP request/response schemas — not application DTOs."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateExampleRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class ExampleResponse(BaseModel):
    id: str
    name: str
