"""Documents API schemas."""
from pydantic import BaseModel, Field


class CreateFolderRequest(BaseModel):
    parent_id: str | None = None
    name: str = Field(min_length=1, max_length=128)


class CreateDocumentRequest(BaseModel):
    folder_id: str
    title: str = Field(min_length=1, max_length=256)
    description: str = ""
    file_name: str = Field(min_length=1, max_length=256)
    content_type: str = "text/plain"
    content: str = Field(min_length=1)
    metadata: dict | None = None


class AddVersionRequest(BaseModel):
    file_name: str = Field(min_length=1, max_length=256)
    content_type: str = "text/plain"
    content: str = Field(min_length=1)


class SignDocumentRequest(BaseModel):
    signers: list[str] = Field(min_length=1)


class AssignPhysicalLocationRequest(BaseModel):
    site_code: str = Field(min_length=1, max_length=64)
    room: str = Field(default="", max_length=64)
    cabinet: str = Field(default="", max_length=64)
    shelf: str = Field(default="", max_length=64)
    box: str = Field(default="", max_length=64)
    file_ref: str = Field(default="", max_length=128)
