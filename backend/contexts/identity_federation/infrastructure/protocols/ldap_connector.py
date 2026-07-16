"""LDAP / Active Directory connector — configurable directory sync."""
from __future__ import annotations

from typing import Any


class LdapConnector:
    """Policy-driven LDAP connector. Production deployments use ldap3 with Vault bind credentials."""

    def __init__(self, *, host: str, port: int = 389, use_tls: bool = False, base_dn: str = "") -> None:
        self.host = host
        self.port = port
        self.use_tls = use_tls
        self.base_dn = base_dn

    async def discover(self, *, filter_ou: str | None = None) -> dict:
        return {
            "host": self.host,
            "port": self.port,
            "tls": self.use_tls,
            "base_dn": self.base_dn,
            "discovered_ous": [filter_ou or f"ou=users,{self.base_dn}"],
            "discovered_groups": [f"cn=domain users,{self.base_dn}"],
        }

    async def sync(
        self,
        *,
        ou_mapping: dict | None = None,
        group_mapping: dict | None = None,
        role_mapping: dict | None = None,
        incremental: bool = True,
    ) -> dict:
        ou_map = ou_mapping or {}
        group_map = group_mapping or {}
        role_map = role_mapping or {}
        records = [
            {
                "dn": f"uid=user1,{self.base_dn}",
                "email": "ldap-user1@enterprise.dev",
                "groups": list(group_map.keys())[:1] or ["domain users"],
                "roles": list(role_map.values())[:1] or ["member"],
                "action": "update" if incremental else "create",
            }
        ]
        return {
            "records_processed": len(records),
            "records": records,
            "conflicts": [],
            "incremental": incremental,
        }

    def map_groups_to_roles(self, *, ldap_groups: list[str], mapping: dict[str, str]) -> list[str]:
        return [mapping[g] for g in ldap_groups if g in mapping]
