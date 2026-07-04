"""Media API schemas."""
from pydantic import BaseModel, Field


class RegisterAssetRequest(BaseModel):
    file_name: str = Field(min_length=1, max_length=256)
    content_type: str = Field(default="application/octet-stream", max_length=128)
    metadata: dict | None = None


class CompleteUploadRequest(BaseModel):
    checksum: str | None = None


class TranscodeRequest(BaseModel):
    profile: str = Field(default="thumbnail", min_length=2, max_length=32)
