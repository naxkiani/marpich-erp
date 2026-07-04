from __future__ import annotations

from typing import Protocol

from contexts.integration.application.commands.provision_connectors import ProvisionConnectorsCommand


class IIntegrationPlatformAdapter(Protocol):
    async def parse_tenant_provisioned(self, envelope: dict) -> ProvisionConnectorsCommand: ...


class IWebhookChannel(Protocol):
    async def deliver(self, *, target_url: str, payload: dict, secret: str = "") -> None: ...
