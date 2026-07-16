"""Enterprise Identity Governance Platform DI + event subscriptions."""
from __future__ import annotations

from contexts.identity_governance.application.service import IdentityGovernanceApplicationService
from contexts.identity_governance.infrastructure.persistence.identity_governance_memory_store import (
    InMemoryAccessRequestRepository,
    InMemoryAccessReviewRepository,
    InMemoryEmergencyAccessGrantRepository,
    InMemoryGovernanceAuditEntryRepository,
    InMemoryIdentityGovernanceProfileRepository,
    InMemoryPrivilegeCertificationRepository,
    InMemoryTemporaryAccessGrantRepository,
)
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: IdentityGovernanceApplicationService | None = None
_registered = False


def get_identity_governance_service() -> IdentityGovernanceApplicationService:
    global _service, _registered
    if _service is None:
        _service = IdentityGovernanceApplicationService(
            profiles=InMemoryIdentityGovernanceProfileRepository(),
            access_requests=InMemoryAccessRequestRepository(),
            access_reviews=InMemoryAccessReviewRepository(),
            certifications=InMemoryPrivilegeCertificationRepository(),
            temporary_grants=InMemoryTemporaryAccessGrantRepository(),
            emergency_grants=InMemoryEmergencyAccessGrantRepository(),
            audit_entries=InMemoryGovernanceAuditEntryRepository(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        InProcessEventBus.subscribe(
            "platform.tenant.provisioned",
            _service.handle_tenant_provisioned,
        )
        _registered = True
    return _service


def reset_identity_governance_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryIdentityGovernanceProfileRepository.reset()
    InMemoryAccessRequestRepository.reset()
    InMemoryAccessReviewRepository.reset()
    InMemoryPrivilegeCertificationRepository.reset()
    InMemoryTemporaryAccessGrantRepository.reset()
    InMemoryEmergencyAccessGrantRepository.reset()
    InMemoryGovernanceAuditEntryRepository.reset()
