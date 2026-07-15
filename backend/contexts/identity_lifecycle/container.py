"""Identity lifecycle DI container."""
from __future__ import annotations

from contexts.identity_lifecycle.application.registration_service import (
    RegistrationOnboardingApplicationService,
)
from contexts.identity_lifecycle.application.service import IdentityLifecycleApplicationService
from contexts.identity_lifecycle.infrastructure.adapters.lifecycle_status_adapter import (
    IdentityLifecycleStatusAdapter,
)
from contexts.identity_lifecycle.infrastructure.persistence.identity_lifecycle_memory_store import (
    InMemoryConsentRecordRepository,
    InMemoryLifecycleAuditRepository,
    InMemoryLifecycleCaseRepository,
    InMemoryLifecycleInvitationRepository,
    InMemoryLifecycleProfileRepository,
    InMemoryLifecycleStore,
    InMemoryLifecycleTransitionRepository,
    InMemoryVerificationTaskRepository,
)
from contexts.identity_lifecycle.infrastructure.persistence.registration_memory_store import (
    InMemoryIdentityRegistrationRepository,
    InMemoryRegistrationStore,
)
from contexts.policy.container import get_policy_evaluator
from shared.application.ports.identity_lifecycle import IIdentityLifecycleStatus
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: IdentityLifecycleApplicationService | None = None
_registration: RegistrationOnboardingApplicationService | None = None
_status_port: IIdentityLifecycleStatus | None = None
_registered = False


def get_identity_lifecycle_service() -> IdentityLifecycleApplicationService:
    global _service, _registered
    if _service is None:
        _service = IdentityLifecycleApplicationService(
            profiles=InMemoryLifecycleProfileRepository(),
            cases=InMemoryLifecycleCaseRepository(),
            transitions=InMemoryLifecycleTransitionRepository(),
            verifications=InMemoryVerificationTaskRepository(),
            consents=InMemoryConsentRecordRepository(),
            audits=InMemoryLifecycleAuditRepository(),
            invitations=InMemoryLifecycleInvitationRepository(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        InProcessEventBus.subscribe("platform.tenant.provisioned", _service.handle_tenant_provisioned)
        _registered = True
    return _service


def get_registration_onboarding_service() -> RegistrationOnboardingApplicationService:
    global _registration
    if _registration is None:
        _registration = RegistrationOnboardingApplicationService(
            registrations=InMemoryIdentityRegistrationRepository(),
            lifecycle=get_identity_lifecycle_service(),
        )
    return _registration


def get_identity_lifecycle_status_port() -> IIdentityLifecycleStatus:
    global _status_port
    if _status_port is None:
        _status_port = IdentityLifecycleStatusAdapter(
            registrations=get_registration_onboarding_service(),
            lifecycle=get_identity_lifecycle_service(),
        )
    return _status_port


def reset_identity_lifecycle_service() -> None:
    global _service, _registration, _status_port, _registered
    _service = None
    _registration = None
    _status_port = None
    _registered = False
    InMemoryLifecycleStore.reset()
    InMemoryRegistrationStore.reset()
