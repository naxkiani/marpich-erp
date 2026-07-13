"""LDAP directory client — stub for dev/test; real ldap3 in production."""
from __future__ import annotations

from contexts.directory.domain.aggregates.directory_platform import LdapConnector
from contexts.directory.domain.ports.directory_repositories import ILdapDirectoryClient
from contexts.directory.infrastructure.persistence.directory_memory_store import InMemoryDirectoryStore


class StubLdapDirectoryClient(ILdapDirectoryClient):
    async def search_users(self, connector: LdapConnector) -> list[dict]:
        seeded = InMemoryDirectoryStore.ldap_seed_users.get(connector.connector_ref)
        if seeded is not None:
            return seeded
        if connector.host.endswith(".mock"):
            return [
                {
                    "external_id": f"ldap-{connector.connector_ref}-001",
                    "email": f"sync-user@{connector.host}",
                    "display_name": f"LDAP User ({connector.name})",
                }
            ]
        return []
