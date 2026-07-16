"""Enterprise Integration Studio presentation schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateProjectRequest(BaseModel):
    name: str
    workspace_type: str = "developer"
    description: str = ""


class CreateArtifactRequest(BaseModel):
    project_ref: str
    name: str
    artifact_type: str
    mapping: dict = Field(default_factory=dict)
    transformation: dict = Field(default_factory=dict)


class DeployArtifactRequest(BaseModel):
    environment: str = "sandbox"


class TestArtifactRequest(BaseModel):
    use_mock: bool = True
