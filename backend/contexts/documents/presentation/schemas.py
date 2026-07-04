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
