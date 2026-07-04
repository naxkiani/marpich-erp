"""Localization API schemas."""
from pydantic import BaseModel, Field


class DefineKeyRequest(BaseModel):
    namespace: str = Field(min_length=1, max_length=64)
    key: str = Field(min_length=1, max_length=128)
    default_value: str = Field(min_length=0, max_length=2048)
    description: str = Field(default="", max_length=256)


class UpsertTranslationRequest(BaseModel):
    value: str = Field(min_length=0, max_length=2048)


class ReportMissingKeyRequest(BaseModel):
    locale_code: str = Field(min_length=2, max_length=16)
    namespace: str = Field(min_length=1, max_length=64)
    key: str = Field(min_length=1, max_length=128)
