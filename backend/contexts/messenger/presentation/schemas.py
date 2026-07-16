"""Messenger API schemas."""
from pydantic import BaseModel, Field


class OpenConversationRequest(BaseModel):
    title: str = Field(default="Conversation", max_length=128)
    member_ids: list[str] = Field(min_length=1)
    e2ee_enabled: bool = False
    issue_livekit_token: bool = False


class SendMessageRequest(BaseModel):
    body: str = Field(default="", max_length=4000)
    ciphertext: str | None = Field(default=None, max_length=65536)
    ciphertext_type: str | None = Field(default=None, max_length=64)
