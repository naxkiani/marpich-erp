"""Identity lifecycle DI container."""
from __future__ import annotations

from contexts.identity_lifecycle.application.registration_service import (
    RegistrationOnboardingApplicationService,
)
from contexts.identity_lifecycle.application.service import IdentityLifecycleApplicationService
from contexts.identity_lifecycle.infrastructure.acl.credential_lifecycle_acl import (
    handle_activation_requested,
)
from contexts.identity_lifecycle.infrastructure.acl.provisioning_execution_acl import (
    handle_provisioning_requested,
)
from contexts.identity_lifecycle.infrastructure.acl.workflow_approval_acl import (
    handle_workflow_process_completed,
)
from contexts.identity_lifecycle.infrastructure.adapters.authentication_credential_adapter import (
    AuthenticationCredentialAdapter,
)
from contexts.identity_lifecycle.infrastructure.adapters.identity_credential_adapter import (
    IdentityCredentialAdapter,
)
from contexts.identity_lifecycle.infrastructure.adapters.identity_user_provisioner import (
    IdentityUserProvisionerAdapter,
)
from contexts.identity_lifecycle.infrastructure.adapters.lifecycle_status_adapter import (
    IdentityLifecycleStatusAdapter,
)
from contexts.identity_lifecycle.infrastructure.adapters.workflow_approval_adapter import (
    WorkflowApprovalAdapter,
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
_a2_registered = False
_a3_registered = False


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
    global _registration, _a2_registered, _a3_registered
    if _registration is None:
        _registration = RegistrationOnboardingApplicationService(
            registrations=InMemoryIdentityRegistrationRepository(),
            lifecycle=get_identity_lifecycle_service(),
            user_provisioner=IdentityUserProvisionerAdapter(),
            workflow_approvals=WorkflowApprovalAdapter(),
            credentials=IdentityCredentialAdapter(),
            passkey_revoker=AuthenticationCredentialAdapter(),
        )
    if not _a2_registered:
        InProcessEventBus.subscribe(
            "identity_lifecycle.provisioning.requested",
            handle_provisioning_requested,
        )
        InProcessEventBus.subscribe(
            "workflow.process.completed",
            handle_workflow_process_completed,
        )
        _a2_registered = True
    if not _a3_registered:
        InProcessEventBus.subscribe(
            "identity_lifecycle.activation.requested",
            handle_activation_requested,
        )
        _a3_registered = True
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
    global _service, _registration, _status_port, _registered, _a2_registered, _a3_registered
    _service = None
    _registration = None
    _status_port = None
    _registered = False
    _a2_registered = False
    _a3_registered = False
    InMemoryLifecycleStore.reset()
    InMemoryRegistrationStore.reset()
