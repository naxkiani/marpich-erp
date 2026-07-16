"""Marpich Connector SDK — base types for external system adapters."""
from __future__ import annotations

from enum import StrEnum


class ConnectorAuthMethod(StrEnum):
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    OAUTH2_CLIENT = "oauth2_client"
    BASIC = "basic"
    MTLS = "mtls"
    BIND_CREDENTIALS = "bind_credentials"
    SERVICE_ACCOUNT = "service_account"
    WEBHOOK_HMAC = "webhook_hmac"
    BOT_TOKEN = "bot_token"
    SMTP_CREDENTIALS = "smtp_credentials"


class ConnectorDirection(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    BIDIRECTIONAL = "bidirectional"


class ConnectorCategory(StrEnum):
    FINANCIAL = "financial"
    MESSAGING = "messaging"
    REGULATORY = "regulatory"
    EDUCATION = "education"
    PRODUCTIVITY = "productivity"
    DIRECTORY = "directory"
    ENTERPRISE = "enterprise"
    STORAGE = "storage"
    DOCUMENT = "document"
    CUSTOM = "custom"
