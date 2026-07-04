"""Organization application service."""
from __future__ import annotations

import json
from datetime import UTC, datetime

from contexts.organization.application.commands.platform_events import (
    AssignMemberFromUserCreatedCommand,
    BootstrapOrganizationCommand,
)
from contexts.organization.application.ports.platform_events import IOrganizationEventAdapter
from contexts.organization.domain.aggregates.membership import Membership
from contexts.organization.domain.aggregates.org_unit import OrgUnit, OrgUnitType
from contexts.organization.domain.aggregates.organization import Organization
from contexts.organization.domain.events.integration_events import (
    MemberAddedIntegration,
    MemberRemovedIntegration,
    OrgCreatedIntegration,
    UnitCreatedIntegration,
)
from contexts.organization.domain.ports.repositories import (
    IMembershipRepository,
    IOrganizationRepository,
    IOrgUnitRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class ConsoleOrganizationAudit:
    async def log(self, **kwargs: object) -> None:
        entry = {
            "type": "audit",
            "context": "organization",
            **kwargs,
            "occurred_at": datetime.now(UTC).isoformat(),
        }
        print(json.dumps(entry, default=str))


class OrganizationApplicationService:
    def __init__(
        self,
        orgs: IOrganizationRepository,
        units: IOrgUnitRepository,
        memberships: IMembershipRepository,
        platform_events: IOrganizationEventAdapter,
        audit: ConsoleOrganizationAudit | None = None,
    ) -> None:
        self._orgs = orgs
        self._units = units
        self._memberships = memberships
        self._platform_events = platform_events
        self._audit = audit or ConsoleOrganizationAudit()

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        command = await self._platform_events.parse_tenant_provisioned(envelope)
        await self.bootstrap_organization(command)

    async def handle_user_created(self, envelope: dict) -> None:
        command = await self._platform_events.parse_user_created(envelope)
        org = await self._orgs.find_by_tenant(command.tenant_id)
        if not org or not org.root_unit_id:
            return
        await self.add_member(
            tenant_id=command.tenant_id,
            org_unit_id=str(org.root_unit_id),
            user_id=command.user_id,
            title=command.display_name,
            is_primary=True,
            correlation_id=command.correlation_id,
        )

    async def bootstrap_organization(self, command: BootstrapOrganizationCommand) -> Result[dict]:
        if await self._orgs.exists(command.tenant_id):
            org = await self._orgs.find_by_tenant(command.tenant_id)
            return Result.ok(org.to_dict() if org else {})

        org = Organization.create(
            tenant_id=command.tenant_id,
            name=command.name,
            legal_name=command.name,
        )
        root = OrgUnit.create(
            tenant_id=command.tenant_id,
            organization_id=org.id,
            parent_id=None,
            unit_type=OrgUnitType.ROOT,
            code="ROOT",
            name=command.name,
        )
        org.root_unit_id = root.id
        await self._orgs.save(org)
        await self._units.save(root)

        await publish_integration_event(
            OrgCreatedIntegration(
                tenant_id=TenantId.create(command.tenant_id),
                correlation_id=command.correlation_id,
                organization_id=org.id,
                name=org.name,
            )
        )
        await publish_integration_event(
            UnitCreatedIntegration(
                tenant_id=TenantId.create(command.tenant_id),
                correlation_id=command.correlation_id,
                unit_id=root.id,
                organization_id=org.id,
                unit_type=root.unit_type.value,
                code=root.code,
                name=root.name,
            )
        )
        await self._audit.log(
            tenant_id=command.tenant_id,
            correlation_id=command.correlation_id,
            action="organization.bootstrap",
            resource_type="organization",
            resource_id=str(org.id),
        )
        return Result.ok(org.to_dict())

    async def get_organization(self, tenant_id: str) -> Result[dict]:
        org = await self._orgs.find_by_tenant(tenant_id)
        if not org:
            return Result.fail("organization.errors.not_found")
        return Result.ok(org.to_dict())

    async def get_tree(self, tenant_id: str) -> Result[dict]:
        org = await self._orgs.find_by_tenant(tenant_id)
        if not org:
            return Result.fail("organization.errors.not_found")

        units = await self._units.list_by_org(tenant_id, org.id)
        unit_dicts = {str(u.id): {**u.to_dict(), "children": []} for u in units}
        root_nodes: list[dict] = []
        for unit in units:
            node = unit_dicts[str(unit.id)]
            if unit.parent_id:
                parent = unit_dicts.get(str(unit.parent_id))
                if parent:
                    parent["children"].append(node)
            else:
                root_nodes.append(node)

        memberships_by_unit: dict[str, list] = {}
        for unit in units:
            members = await self._memberships.list_by_unit(tenant_id, unit.id)
            memberships_by_unit[str(unit.id)] = [m.to_dict() for m in members]

        return Result.ok(
            {
                "organization": org.to_dict(),
                "tree": root_nodes,
                "memberships_by_unit": memberships_by_unit,
            }
        )

    async def create_unit(
        self,
        *,
        tenant_id: str,
        parent_id: str | None,
        unit_type: str,
        code: str,
        name: str,
        correlation_id: str,
    ) -> Result[dict]:
        org = await self._orgs.find_by_tenant(tenant_id)
        if not org:
            return Result.fail("organization.errors.not_found")

        if await self._units.find_by_code(tenant_id, code):
            return Result.fail("organization.errors.code_exists")

        parent_uid: UniqueId | None = None
        if parent_id:
            parent = await self._units.find_by_id(tenant_id, UniqueId.from_string(parent_id))
            if not parent:
                return Result.fail("organization.errors.parent_not_found")
            parent_uid = parent.id

        try:
            utype = OrgUnitType(unit_type)
        except ValueError:
            return Result.fail("organization.errors.invalid_unit_type")

        if utype == OrgUnitType.ROOT:
            return Result.fail("organization.errors.cannot_create_root")

        unit = OrgUnit.create(
            tenant_id=tenant_id,
            organization_id=org.id,
            parent_id=parent_uid,
            unit_type=utype,
            code=code,
            name=name,
        )
        await self._units.save(unit)

        await publish_integration_event(
            UnitCreatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                unit_id=unit.id,
                organization_id=org.id,
                unit_type=unit.unit_type.value,
                code=unit.code,
                name=unit.name,
            )
        )
        return Result.ok(unit.to_dict())

    async def add_member(
        self,
        *,
        tenant_id: str,
        org_unit_id: str,
        user_id: str,
        title: str,
        is_primary: bool = False,
        correlation_id: str,
    ) -> Result[dict]:
        unit = await self._units.find_by_id(tenant_id, UniqueId.from_string(org_unit_id))
        if not unit:
            return Result.fail("organization.errors.unit_not_found")

        existing = await self._memberships.find(tenant_id, unit.id, user_id)
        if existing:
            return Result.ok(existing.to_dict())

        membership = Membership.assign(
            tenant_id=tenant_id,
            org_unit_id=unit.id,
            user_id=user_id,
            title=title,
            is_primary=is_primary,
        )
        await self._memberships.save(membership)

        await publish_integration_event(
            MemberAddedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                membership_id=membership.id,
                org_unit_id=unit.id,
                user_id=user_id,
                title=title,
            )
        )
        return Result.ok(membership.to_dict())

    async def remove_member(
        self, tenant_id: str, org_unit_id: str, user_id: str, correlation_id: str
    ) -> Result[dict]:
        unit = await self._units.find_by_id(tenant_id, UniqueId.from_string(org_unit_id))
        if not unit:
            return Result.fail("organization.errors.unit_not_found")

        removed = await self._memberships.delete(tenant_id, unit.id, user_id)
        if not removed:
            return Result.fail("organization.errors.member_not_found")

        await publish_integration_event(
            MemberRemovedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                org_unit_id=unit.id,
                user_id=user_id,
            )
        )
        return Result.ok({"org_unit_id": org_unit_id, "user_id": user_id})

    async def list_user_units(self, tenant_id: str, user_id: str) -> Result[list[dict]]:
        memberships = await self._memberships.list_by_user(tenant_id, user_id)
        result = []
        for m in memberships:
            unit = await self._units.find_by_id(tenant_id, m.org_unit_id)
            result.append(
                {
                    **m.to_dict(),
                    "unit": unit.to_dict() if unit else None,
                }
            )
        return Result.ok(result)
