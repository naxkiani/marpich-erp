"""Plugin application service."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from contexts.plugins.application.constants.seed_listings import SEED_LISTINGS
from contexts.plugins.domain.aggregates.plugin import Plugin
from contexts.plugins.domain.aggregates.plugin import PluginInstallation
from contexts.plugins.domain.events.integration_events import (
    PluginInstalledIntegration,
    PluginPublishedIntegration,
    PluginRegisteredIntegration,
    PluginUninstalledIntegration,
    PluginUpgradedIntegration,
    SandboxViolationIntegration,
)
from contexts.plugins.domain.ports.repositories import (
    IPluginInstallationRepository,
    IPluginRepository,
)
from contexts.plugins.domain.services.plugin_services import (
    is_upgrade_compatible,
    resolve_sandbox_profile,
    validate_permission_grants,
    verify_signature,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class PluginApplicationService:
    def __init__(
        self,
        plugins: IPluginRepository,
        installations: IPluginInstallationRepository,
    ) -> None:
        self._plugins = plugins
        self._installations = installations
        self._seeded = False

    async def ensure_seed_listings(self) -> None:
        if self._seeded:
            return
        for row in SEED_LISTINGS:
            plugin_id = row[0]
            if await self._plugins.find_by_id(plugin_id):
                continue
            plugin = Plugin.register(
                plugin_id=plugin_id,
                plugin_type=row[1],
                display_name=row[2],
                description=row[3],
                publisher_id=row[4],
                publisher_name=row[5],
                version=row[6],
                permissions=list(row[7]),
                extension_points=list(row[8]),
                sandbox_profile=row[9],
                trust_level=row[10],
                signature_algorithm="ed25519",
                public_key_fingerprint=row[12],
                package_checksum=row[11],
            )
            await self._plugins.save(plugin)
            await publish_integration_event(
                PluginPublishedIntegration(
                    tenant_id=TenantId.create("platform"),
                    correlation_id=f"seed-{plugin_id}",
                    plugin_id=plugin_id,
                    version=row[6],
                    trust_level=row[10],
                )
            )
        self._seeded = True

    async def register_plugin(
        self,
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
        sandbox_profile: str | None,
        trust_level: str,
        signature_algorithm: str,
        public_key_fingerprint: str,
        package_checksum: str,
        correlation_id: str,
    ) -> Result[dict]:
        await self.ensure_seed_listings()
        if await self._plugins.find_by_id(plugin_id):
            return Result.fail("plugins.errors.already_exists")
        ok, reason = verify_signature(
            package_checksum=package_checksum,
            public_key_fingerprint=public_key_fingerprint,
            algorithm=signature_algorithm,
        )
        if not ok:
            return Result.fail(f"plugins.errors.signature.{reason}")
        profile = resolve_sandbox_profile(plugin_type, sandbox_profile)
        plugin = Plugin.register(
            plugin_id=plugin_id,
            plugin_type=plugin_type,
            display_name=display_name,
            description=description,
            publisher_id=publisher_id,
            publisher_name=publisher_name,
            version=version,
            permissions=permissions,
            extension_points=extension_points,
            sandbox_profile=profile,
            trust_level=trust_level,
            signature_algorithm=signature_algorithm,
            public_key_fingerprint=public_key_fingerprint,
            package_checksum=package_checksum,
        )
        await self._plugins.save(plugin)
        await publish_integration_event(
            PluginRegisteredIntegration(
                tenant_id=TenantId.create("platform"),
                correlation_id=correlation_id,
                plugin_id=plugin_id,
                plugin_type=plugin_type,
                version=version,
            )
        )
        return Result.ok(plugin.to_dict())

    async def list_plugins(self) -> Result[list[dict]]:
        await self.ensure_seed_listings()
        plugins = await self._plugins.list_all()
        return Result.ok([p.to_dict() for p in sorted(plugins, key=lambda x: x.plugin_id)])

    async def get_plugin(self, plugin_id: str) -> Result[dict]:
        await self.ensure_seed_listings()
        plugin = await self._plugins.find_by_id(plugin_id)
        if not plugin:
            return Result.fail("plugins.errors.not_found")
        data = plugin.to_dict()
        data["versions"] = plugin.versions
        return Result.ok(data)

    async def list_marketplace(
        self,
        *,
        plugin_type: str | None = None,
        trust_level: str | None = None,
        query: str | None = None,
    ) -> Result[list[dict]]:
        await self.ensure_seed_listings()
        if query:
            plugins = await self._plugins.search(query)
        elif plugin_type:
            plugins = await self._plugins.list_by_type(plugin_type)
        else:
            plugins = await self._plugins.list_all()
        if trust_level:
            plugins = [p for p in plugins if p.trust_level == trust_level]
        plugins = [p for p in plugins if p.status == "published"]
        return Result.ok([p.to_dict() for p in sorted(plugins, key=lambda x: x.display_name)])

    async def submit_listing(
        self,
        *,
        plugin_id: str,
        version: str,
        package_checksum: str,
        public_key_fingerprint: str,
        correlation_id: str,
    ) -> Result[dict]:
        plugin = await self._plugins.find_by_id(plugin_id)
        if not plugin:
            return Result.fail("plugins.errors.not_found")
        ok, reason = verify_signature(
            package_checksum=package_checksum,
            public_key_fingerprint=public_key_fingerprint,
            algorithm=plugin.signature_algorithm,
        )
        if not ok:
            return Result.fail(f"plugins.errors.signature.{reason}")
        plugin.publish_version(version, package_checksum, public_key_fingerprint)
        await self._plugins.save(plugin)
        await publish_integration_event(
            PluginPublishedIntegration(
                tenant_id=TenantId.create("platform"),
                correlation_id=correlation_id,
                plugin_id=plugin_id,
                version=version,
                trust_level=plugin.trust_level,
            )
        )
        return Result.ok(plugin.to_dict())

    async def list_installed(self, tenant_id: str) -> Result[list[dict]]:
        installs = await self._installations.list_by_tenant(tenant_id)
        return Result.ok([i.to_dict() for i in sorted(installs, key=lambda x: x.plugin_id)])

    async def install_plugin(
        self,
        *,
        tenant_id: str,
        plugin_id: str,
        granted_permissions: list[str],
        config: dict | None,
        correlation_id: str,
    ) -> Result[dict]:
        await self.ensure_seed_listings()
        plugin = await self._plugins.find_by_id(plugin_id)
        if not plugin or plugin.status != "published":
            return Result.fail("plugins.errors.not_found")
        ok, missing = validate_permission_grants(plugin.permissions, granted_permissions)
        if not ok:
            return Result.fail(f"plugins.errors.missing_permissions:{','.join(missing)}")
        existing = await self._installations.find(tenant_id, plugin_id)
        if existing:
            return Result.fail("plugins.errors.already_installed")
        installation = PluginInstallation.install(
            tenant_id=tenant_id,
            plugin_id=plugin_id,
            version=plugin.current_version,
            granted_permissions=granted_permissions,
            config=config,
            sandbox_profile=plugin.sandbox_profile,
        )
        await self._installations.save(installation)
        await publish_integration_event(
            PluginInstalledIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                plugin_id=plugin_id,
                version=plugin.current_version,
                granted_permissions=tuple(granted_permissions),
            )
        )
        return Result.ok(installation.to_dict())

    async def upgrade_plugin(
        self,
        *,
        tenant_id: str,
        plugin_id: str,
        target_version: str,
        correlation_id: str,
    ) -> Result[dict]:
        plugin = await self._plugins.find_by_id(plugin_id)
        installation = await self._installations.find(tenant_id, plugin_id)
        if not plugin or not installation:
            return Result.fail("plugins.errors.not_installed")
        if not is_upgrade_compatible(installation.installed_version, target_version):
            return Result.fail("plugins.errors.incompatible_upgrade")
        if target_version != plugin.current_version:
            return Result.fail("plugins.errors.version_not_published")
        from_version = installation.installed_version
        installation.upgrade(target_version)
        await self._installations.save(installation)
        await publish_integration_event(
            PluginUpgradedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                plugin_id=plugin_id,
                from_version=from_version,
                to_version=target_version,
            )
        )
        return Result.ok(installation.to_dict())

    async def uninstall_plugin(
        self,
        *,
        tenant_id: str,
        plugin_id: str,
        correlation_id: str,
    ) -> Result[dict]:
        if not await self._installations.delete(tenant_id, plugin_id):
            return Result.fail("plugins.errors.not_installed")
        await publish_integration_event(
            PluginUninstalledIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                plugin_id=plugin_id,
            )
        )
        return Result.ok({"plugin_id": plugin_id, "uninstalled": True})

    async def verify_plugin(self, plugin_id: str) -> Result[dict]:
        plugin = await self._plugins.find_by_id(plugin_id)
        if not plugin:
            return Result.fail("plugins.errors.not_found")
        ok, reason = verify_signature(
            package_checksum=plugin.package_checksum,
            public_key_fingerprint=plugin.public_key_fingerprint,
            algorithm=plugin.signature_algorithm,
        )
        return Result.ok({"plugin_id": plugin_id, "valid": ok, "reason": reason})

    async def invoke_plugin(
        self,
        *,
        tenant_id: str,
        plugin_id: str,
        extension_point: str,
        payload: dict,
    ) -> Result[dict]:
        installation = await self._installations.find(tenant_id, plugin_id)
        if not installation or not installation.enabled:
            return Result.fail("plugins.errors.not_installed")
        plugin = await self._plugins.find_by_id(plugin_id)
        if not plugin:
            return Result.fail("plugins.errors.not_found")
        if extension_point not in plugin.extension_points:
            return Result.fail("plugins.errors.invalid_extension_point")
        return Result.ok({
            "plugin_id": plugin_id,
            "extension_point": extension_point,
            "sandbox_profile": installation.sandbox_profile,
            "result": {
                "status": "ok",
                "echo": payload,
                "plugin_version": installation.installed_version,
            },
        })

    async def list_extensions(
        self,
        tenant_id: str,
        extension_point: str,
    ) -> Result[list[dict]]:
        installs = await self._installations.list_by_tenant(tenant_id)
        results = []
        for inst in installs:
            if not inst.enabled:
                continue
            plugin = await self._plugins.find_by_id(inst.plugin_id)
            if plugin and extension_point in plugin.extension_points:
                results.append({
                    "plugin_id": inst.plugin_id,
                    "display_name": plugin.display_name,
                    "plugin_type": plugin.plugin_type,
                    "version": inst.installed_version,
                    "extension_point": extension_point,
                })
        return Result.ok(results)

    async def get_upgrade_path(self, tenant_id: str, plugin_id: str) -> Result[dict]:
        plugin = await self._plugins.find_by_id(plugin_id)
        installation = await self._installations.find(tenant_id, plugin_id)
        if not plugin or not installation:
            return Result.fail("plugins.errors.not_installed")
        upgrade_available = is_upgrade_compatible(
            installation.installed_version, plugin.current_version
        )
        return Result.ok({
            "plugin_id": plugin_id,
            "current_version": installation.installed_version,
            "latest_version": plugin.current_version,
            "upgrade_available": upgrade_available,
            "requires_approval": (
                parse_major(plugin.current_version) > parse_major(installation.installed_version)
            ),
        })

    async def get_marketplace_dashboard(self, tenant_id: str) -> Result[dict]:
        await self.ensure_seed_listings()
        all_plugins = await self._plugins.list_all()
        installs = await self._installations.list_by_tenant(tenant_id)
        by_type: dict[str, int] = {}
        for p in all_plugins:
            if p.status == "published":
                by_type[p.plugin_type] = by_type.get(p.plugin_type, 0) + 1
        backlog = []
        for inst in installs:
            plugin = await self._plugins.find_by_id(inst.plugin_id)
            if plugin and is_upgrade_compatible(inst.installed_version, plugin.current_version):
                backlog.append({
                    "plugin_id": inst.plugin_id,
                    "current_version": inst.installed_version,
                    "latest_version": plugin.current_version,
                })
        return Result.ok({
            "listings_by_type": by_type,
            "installed_count": len(installs),
            "pending_submissions": 0,
            "sandbox_violations_24h": 0,
            "top_publishers": _top_publishers(all_plugins),
            "upgrade_backlog": backlog,
        })


def parse_major(version: str) -> int:
    parts = version.split(".")
    return int(parts[0]) if parts else 0


def _top_publishers(plugins: list[Plugin]) -> list[dict]:
    counts: dict[str, dict] = {}
    for p in plugins:
        if p.publisher_id not in counts:
            counts[p.publisher_id] = {
                "publisher": p.publisher_name,
                "listings": 0,
                "installs": 0,
            }
        counts[p.publisher_id]["listings"] += 1
    return sorted(counts.values(), key=lambda x: x["listings"], reverse=True)[:5]
