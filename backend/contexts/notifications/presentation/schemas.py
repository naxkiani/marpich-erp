"""Notifications API schemas."""
from pydantic import BaseModel, Field


class SendNotificationRequest(BaseModel):
    channel: str = Field(pattern=r"^(inbox|email)$")
    title: str = Field(min_length=1, max_length=256)
    body: str = Field(min_length=1, max_length=4096)
    category: str = Field(default="general", max_length=64)
    user_id: str | None = None
    recipient_email: str | None = None
