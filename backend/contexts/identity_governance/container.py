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
from contexts.identity_governance.infrastructure.persistence.identity_governance_postgres_store import (
    PostgresAccessRequestRepository,
    PostgresAccessReviewRepository,
    PostgresEmergencyAccessGrantRepository,
    PostgresGovernanceAuditEntryRepository,
    PostgresIdentityGovernanceProfileRepository,
    PostgresPrivilegeCertificationRepository,
    PostgresTemporaryAccessGrantRepository,
    _RefCounterMixin as _IgaPgRefCounter,
)
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: IdentityGovernanceApplicationService | None = None
_registered = False


def get_identity_governance_service() -> IdentityGovernanceApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            profiles: object = PostgresIdentityGovernanceProfileRepository()
            access_requests: object = PostgresAccessRequestRepository()
            access_reviews: object = PostgresAccessReviewRepository()
            certifications: object = PostgresPrivilegeCertificationRepository()
            temporary_grants: object = PostgresTemporaryAccessGrantRepository()
            emergency_grants: object = PostgresEmergencyAccessGrantRepository()
            audit_entries: object = PostgresGovernanceAuditEntryRepository()
        else:
            profiles = InMemoryIdentityGovernanceProfileRepository()
            access_requests = InMemoryAccessRequestRepository()
            access_reviews = InMemoryAccessReviewRepository()
            certifications = InMemoryPrivilegeCertificationRepository()
            temporary_grants = InMemoryTemporaryAccessGrantRepository()
            emergency_grants = InMemoryEmergencyAccessGrantRepository()
            audit_entries = InMemoryGovernanceAuditEntryRepository()
        _service = IdentityGovernanceApplicationService(
            profiles=profiles,
            access_requests=access_requests,
            access_reviews=access_reviews,
            certifications=certifications,
            temporary_grants=temporary_grants,
            emergency_grants=emergency_grants,
            audit_entries=audit_entries,
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
    _IgaPgRefCounter.reset_counters()
