from __future__ import annotations

from typing import Protocol

from contexts.documents.application.commands.bootstrap_root_folder import BootstrapRootFolderCommand


class IDocumentsPlatformAdapter(Protocol):
    async def parse_tenant_provisioned(self, envelope: dict) -> BootstrapRootFolderCommand: ...
