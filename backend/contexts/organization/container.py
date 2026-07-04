"""Organization DI + event subscriptions."""
from __future__ import annotations

from contexts.organization.application.service import OrganizationApplicationService
from contexts.organization.infrastructure.acl.platform_events import OrganizationEventAdapter
from contexts.organization.infrastructure.persistence.memory_store import (
    InMemoryMembershipRepository,
    InMemoryOrganizationRepository,
    InMemoryOrgUnitRepository,
)
from contexts.organization.infrastructure.persistence.postgres_store import (
    PostgresMembershipRepository,
    PostgresOrganizationRepository,
    PostgresOrgUnitRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: OrganizationApplicationService | None = None
_registered = False


def get_organization_service() -> OrganizationApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = OrganizationApplicationService(
                orgs=PostgresOrganizationRepository(),
                units=PostgresOrgUnitRepository(),
                memberships=PostgresMembershipRepository(),
                platform_events=OrganizationEventAdapter(),
            )
        else:
            _service = OrganizationApplicationService(
                orgs=InMemoryOrganizationRepository(),
                units=InMemoryOrgUnitRepository(),
                memberships=InMemoryMembershipRepository(),
                platform_events=OrganizationEventAdapter(),
            )
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        InProcessEventBus.subscribe(
            "identity.user.created",
            _service.handle_user_created,
        )
        _registered = True
    return _service


def reset_organization_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
