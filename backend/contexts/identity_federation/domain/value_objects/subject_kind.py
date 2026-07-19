"""Subject kind value object for federation taxonomy."""
from __future__ import annotations

from enum import StrEnum


class SubjectKind(StrEnum):
    HUMAN = "human"
    MACHINE = "machine"
    SERVICE = "service"
    AI_AGENT = "ai_agent"
    DEVICE = "device"
    PARTNER = "partner"
    API = "api"
