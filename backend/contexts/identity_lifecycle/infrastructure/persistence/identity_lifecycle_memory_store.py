"""In-memory identity lifecycle persistence."""
from __future__ import annotations

from contexts.identity_lifecycle.domain.aggregates.identity_lifecycle_platform import (
    ConsentRecord,
    LifecycleAuditEntry,
    LifecycleCase,
    LifecycleInvitation,
    LifecycleProfile,
    LifecycleTransition,
    VerificationTask,
)
from contexts.identity_lifecycle.domain.ports.identity_lifecycle_repositories import (
    IConsentRecordRepository,
    ILifecycleAuditRepository,
    ILifecycleCaseRepository,
    ILifecycleInvitationRepository,
    ILifecycleProfileRepository,
    ILifecycleTransitionRepository,
    IVerificationTaskRepository,
)


class InMemoryLifecycleStore:
    profiles: dict[str, LifecycleProfile] = {}
    cases: dict[str, LifecycleCase] = {}
    transitions: dict[str, LifecycleTransition] = {}
    verifications: dict[str, VerificationTask] = {}
    consents: dict[str, ConsentRecord] = {}
    audits: dict[str, LifecycleAuditEntry] = {}
    invitations: dict[str, LifecycleInvitation] = {}
    profile_counter: dict[str, int] = {}
    case_counter: dict[str, int] = {}
    transition_counter: dict[str, int] = {}
    task_counter: dict[str, int] = {}
    consent_counter: dict[str, int] = {}
    audit_counter: dict[str, int] = {}
    invitation_counter: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls.profiles.clear()
        cls.cases.clear()
        cls.transitions.clear()
        cls.verifications.clear()
        cls.consents.clear()
        cls.audits.clear()
        cls.invitations.clear()
        cls.profile_counter.clear()
        cls.case_counter.clear()
        cls.transition_counter.clear()
        cls.task_counter.clear()
        cls.consent_counter.clear()
        cls.audit_counter.clear()
        cls.invitation_counter.clear()


class InMemoryLifecycleProfileRepository(ILifecycleProfileRepository):
    async def find_by_tenant(self, tenant_id: str) -> LifecycleProfile | None:
        return InMemoryLifecycleStore.profiles.get(tenant_id)

    async def save(self, profile: LifecycleProfile) -> None:
        InMemoryLifecycleStore.profiles[profile.tenant_id] = profile

    def next_profile_ref(self, tenant_id: str) -> str:
        n = InMemoryLifecycleStore.profile_counter.get(tenant_id, 0) + 1
        InMemoryLifecycleStore.profile_counter[tenant_id] = n
        return f"lc-profile-{tenant_id}-{n:04d}"


class InMemoryLifecycleCaseRepository(ILifecycleCaseRepository):
    async def save(self, case: LifecycleCase) -> None:
        InMemoryLifecycleStore.cases[case.case_ref] = case

    async def list_by_tenant(self, tenant_id: str) -> list[LifecycleCase]:
        return [c for c in InMemoryLifecycleStore.cases.values() if c.tenant_id == tenant_id]

    async def find_by_ref(self, tenant_id: str, case_ref: str) -> LifecycleCase | None:
        case = InMemoryLifecycleStore.cases.get(case_ref)
        if case and case.tenant_id == tenant_id:
            return case
        return None

    def next_case_ref(self, tenant_id: str) -> str:
        n = InMemoryLifecycleStore.case_counter.get(tenant_id, 0) + 1
        InMemoryLifecycleStore.case_counter[tenant_id] = n
        return f"lc-case-{tenant_id}-{n:04d}"


class InMemoryLifecycleTransitionRepository(ILifecycleTransitionRepository):
    async def save(self, transition: LifecycleTransition) -> None:
        InMemoryLifecycleStore.transitions[transition.transition_ref] = transition

    async def list_by_case(self, tenant_id: str, case_ref: str) -> list[LifecycleTransition]:
        return [
            t
            for t in InMemoryLifecycleStore.transitions.values()
            if t.tenant_id == tenant_id and t.case_ref == case_ref
        ]

    def next_transition_ref(self, tenant_id: str) -> str:
        n = InMemoryLifecycleStore.transition_counter.get(tenant_id, 0) + 1
        InMemoryLifecycleStore.transition_counter[tenant_id] = n
        return f"lc-transition-{tenant_id}-{n:04d}"


class InMemoryVerificationTaskRepository(IVerificationTaskRepository):
    async def save(self, task: VerificationTask) -> None:
        InMemoryLifecycleStore.verifications[task.task_ref] = task

    async def list_by_case(self, tenant_id: str, case_ref: str) -> list[VerificationTask]:
        return [
            t
            for t in InMemoryLifecycleStore.verifications.values()
            if t.tenant_id == tenant_id and t.case_ref == case_ref
        ]

    async def find_by_ref(self, tenant_id: str, task_ref: str) -> VerificationTask | None:
        task = InMemoryLifecycleStore.verifications.get(task_ref)
        if task and task.tenant_id == tenant_id:
            return task
        return None

    def next_task_ref(self, tenant_id: str) -> str:
        n = InMemoryLifecycleStore.task_counter.get(tenant_id, 0) + 1
        InMemoryLifecycleStore.task_counter[tenant_id] = n
        return f"lc-task-{tenant_id}-{n:04d}"


class InMemoryConsentRecordRepository(IConsentRecordRepository):
    async def save(self, consent: ConsentRecord) -> None:
        InMemoryLifecycleStore.consents[consent.consent_ref] = consent

    async def list_by_case(self, tenant_id: str, case_ref: str) -> list[ConsentRecord]:
        return [
            c
            for c in InMemoryLifecycleStore.consents.values()
            if c.tenant_id == tenant_id and c.case_ref == case_ref
        ]

    def next_consent_ref(self, tenant_id: str) -> str:
        n = InMemoryLifecycleStore.consent_counter.get(tenant_id, 0) + 1
        InMemoryLifecycleStore.consent_counter[tenant_id] = n
        return f"lc-consent-{tenant_id}-{n:04d}"


class InMemoryLifecycleAuditRepository(ILifecycleAuditRepository):
    async def save(self, entry: LifecycleAuditEntry) -> None:
        InMemoryLifecycleStore.audits[entry.audit_ref] = entry

    async def list_by_case(self, tenant_id: str, case_ref: str) -> list[LifecycleAuditEntry]:
        return [
            a
            for a in InMemoryLifecycleStore.audits.values()
            if a.tenant_id == tenant_id and a.case_ref == case_ref
        ]

    async def list_by_tenant(self, tenant_id: str) -> list[LifecycleAuditEntry]:
        return [a for a in InMemoryLifecycleStore.audits.values() if a.tenant_id == tenant_id]

    def next_audit_ref(self, tenant_id: str) -> str:
        n = InMemoryLifecycleStore.audit_counter.get(tenant_id, 0) + 1
        InMemoryLifecycleStore.audit_counter[tenant_id] = n
        return f"lc-audit-{tenant_id}-{n:04d}"


class InMemoryLifecycleInvitationRepository(ILifecycleInvitationRepository):
    async def save(self, invitation: LifecycleInvitation) -> None:
        InMemoryLifecycleStore.invitations[invitation.invitation_ref] = invitation

    async def find_by_token(self, tenant_id: str, token: str) -> LifecycleInvitation | None:
        for inv in InMemoryLifecycleStore.invitations.values():
            if inv.tenant_id == tenant_id and inv.token == token:
                return inv
        return None

    def next_invitation_ref(self, tenant_id: str) -> str:
        n = InMemoryLifecycleStore.invitation_counter.get(tenant_id, 0) + 1
        InMemoryLifecycleStore.invitation_counter[tenant_id] = n
        return f"lc-invite-{tenant_id}-{n:04d}"
