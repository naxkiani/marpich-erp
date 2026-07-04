"""Workflow API schemas."""
from pydantic import BaseModel, Field


class WorkflowStepRequest(BaseModel):
    key: str = Field(min_length=2, max_length=64)
    name: str = Field(min_length=2, max_length=128)


class DeployDefinitionRequest(BaseModel):
    key: str = Field(min_length=2, max_length=64)
    name: str = Field(min_length=2, max_length=128)
    steps: list[WorkflowStepRequest] = Field(min_length=1)


class StartInstanceRequest(BaseModel):
    definition_key: str
    context: dict = Field(default_factory=dict)
    assignees: dict[str, str] = Field(default_factory=dict)


class CompleteTaskRequest(BaseModel):
    outcome: str = Field(pattern=r"^(approved|rejected)$")
    comment: str = ""


class DelegateTaskRequest(BaseModel):
    to_user_id: str = Field(min_length=1, max_length=64)
