"""Plugin and installation aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

PLUGIN_TYPES = frozenset({
    "module",
    "widget",
    "report",
    "dashboard",
    "theme",
    "ai_skill",
    "integration",
    "workflow_extension",
})

TRUST_LEVELS = frozenset({"community", "verified", "enterprise"})


@dataclass(eq=False, kw_only=True)
class Plugin(AggregateRoot):
    plugin_id: str
    plugin_type: str
    display_name: str
    description: str
    publisher_id: str
    publisher_name: str
    current_version: str
    permissions: list[str] = field(default_factory=list)
    extension_points: list[str] = field(default_factory=list)
    sandbox_profile: str = "standard"
    trust_level: str = "community"
    signature_algorithm: str = "ed25519"
    public_key_fingerprint: str = ""
    package_checksum: str = ""
    status: str = "published"
    versions: list[dict] = field(default_factory=list)
    industry_packs: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        plugin_id: str,
        plugin_type: str,
        display_name: str,
        description: str,
        publisher_id: str,
        publisher_name: str,
        version: str,
        permissions: list[str],
        extension_points: list[str],
        sandbox_profile: str,
        trust_level: str,
        signature_algorithm: str,
        public_key_fingerprint: str,
        package_checksum: str,
        industry_packs: list[str] | None = None,
    ) -> Plugin:
        if plugin_type not in PLUGIN_TYPES:
            raise ValueError(f"Invalid plugin type: {plugin_type}")
        plugin = cls(
            id=UniqueId.generate(),
            plugin_id=plugin_id.strip().lower(),
            plugin_type=plugin_type,
            display_name=display_name.strip(),
            description=description.strip(),
            publisher_id=publisher_id,
            publisher_name=publisher_name,
            current_version=version,
            permissions=permissions,
            extension_points=extension_points,
            sandbox_profile=sandbox_profile,
            trust_level=trust_level if trust_level in TRUST_LEVELS else "community",
            signature_algorithm=signature_algorithm,
            public_key_fingerprint=public_key_fingerprint,
            package_checksum=package_checksum,
            industry_packs=industry_packs or [],
        )
        plugin._add_version(version, "registered")
        return plugin

    def _add_version(self, version: str, action: str) -> None:
        self.versions.append({
            "version": version,
            "action": action,
            "checksum": self.package_checksum,
            "fingerprint": self.public_key_fingerprint,
            "recorded_at": datetime.now(UTC).isoformat(),
        })
        self.updated_at = datetime.now(UTC)

    def publish_version(self, version: str, package_checksum: str, fingerprint: str) -> None:
        self.current_version = version
        self.package_checksum = package_checksum
        self.public_key_fingerprint = fingerprint
        self.status = "published"
        self._add_version(version, "published")

    def revoke(self) -> None:
        self.status = "revoked"
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "plugin_id": self.plugin_id,
            "plugin_type": self.plugin_type,
            "display_name": self.display_name,
            "description": self.description,
            "publisher_id": self.publisher_id,
            "publisher_name": self.publisher_name,
            "current_version": self.current_version,
            "permissions": self.permissions,
            "extension_points": self.extension_points,
            "sandbox_profile": self.sandbox_profile,
            "trust_level": self.trust_level,
            "signature": {
                "algorithm": self.signature_algorithm,
                "public_key_fingerprint": self.public_key_fingerprint,
                "package_checksum": self.package_checksum,
            },
            "status": self.status,
            "industry_packs": self.industry_packs,
            "version_count": len(self.versions),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class PluginInstallation(AggregateRoot):
    tenant_id: str
    plugin_id: str
    installed_version: str
    enabled: bool = True
    granted_permissions: list[str] = field(default_factory=list)
    config: dict = field(default_factory=dict)
    sandbox_profile: str = "standard"
    installed_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    upgraded_at: datetime | None = None

    @classmethod
    def install(
        cls,
        *,
        tenant_id: str,
        plugin_id: str,
        version: str,
        granted_permissions: list[str],
        config: dict | None,
        sandbox_profile: str,
    ) -> PluginInstallation:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            plugin_id=plugin_id,
            installed_version=version,
            granted_permissions=granted_permissions,
            config=config or {},
            sandbox_profile=sandbox_profile,
        )

    def upgrade(self, version: str) -> None:
        self.installed_version = version
        self.upgraded_at = datetime.now(UTC)

    def disable(self) -> None:
        self.enabled = False

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "plugin_id": self.plugin_id,
            "installed_version": self.installed_version,
            "enabled": self.enabled,
            "granted_permissions": self.granted_permissions,
            "config": self.config,
            "sandbox_profile": self.sandbox_profile,
            "installed_at": self.installed_at.isoformat(),
            "upgraded_at": self.upgraded_at.isoformat() if self.upgraded_at else None,
        }
