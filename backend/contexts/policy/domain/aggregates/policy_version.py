"""Immutable policy version — conditions, rules, exceptions."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class PolicyStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    EXPIRED = "expired"
    ROLLED_BACK = "rolled_back"


@dataclass(eq=False, kw_only=True)
class PolicyVersion(AggregateRoot):
    policy_id: str
    tenant_id: str
    version: int
    status: PolicyStatus
    effective_from: datetime
    expires_at: datetime | None
    priority: int
    conditions: list[dict]
    rules: list[dict]
    exceptions: list[dict]
    approval_required: bool
    workflow_key: str | None
    require_passing_tests: bool
    cache_allowed: bool
    metadata: dict
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create_draft(
        cls,
        *,
        policy_id: str,
        tenant_id: str,
        version: int,
        effective_from: datetime,
        priority: int = 100,
        conditions: list[dict] | None = None,
        rules: list[dict] | None,
        exceptions: list[dict] | None = None,
        expires_at: datetime | None = None,
        approval_required: bool = True,
        workflow_key: str | None = None,
        require_passing_tests: bool = False,
        cache_allowed: bool = True,
        metadata: dict | None = None,
    ) -> PolicyVersion:
        return cls(
            id=UniqueId.generate(),
            policy_id=policy_id,
            tenant_id=tenant_id,
            version=version,
            status=PolicyStatus.DRAFT,
            effective_from=effective_from,
            expires_at=expires_at,
            priority=priority,
            conditions=conditions or [],
            rules=rules or [],
            exceptions=exceptions or [],
            approval_required=approval_required,
            workflow_key=workflow_key,
            require_passing_tests=require_passing_tests,
            cache_allowed=cache_allowed,
            metadata=metadata or {},
        )

    def is_editable(self) -> bool:
        return self.status == PolicyStatus.DRAFT

    def is_effective_at(self, as_of: datetime) -> bool:
        if self.status != PolicyStatus.ACTIVE:
            return False
        if as_of < self.effective_from:
            return False
        if self.expires_at and as_of >= self.expires_at:
            return False
        return True

    def submit_for_approval(self) -> None:
        if self.status != PolicyStatus.DRAFT:
            raise ValueError("policy.errors.only_draft_submittable")
        self.status = PolicyStatus.PENDING_APPROVAL

    def activate(self) -> None:
        if self.status not in (PolicyStatus.DRAFT, PolicyStatus.PENDING_APPROVAL, PolicyStatus.ROLLED_BACK):
            raise ValueError("policy.errors.invalid_activate_status")
        self.status = PolicyStatus.ACTIVE

    def supersede(self) -> None:
        if self.status == PolicyStatus.ACTIVE:
            self.status = PolicyStatus.SUPERSEDED

    def mark_rolled_back(self) -> None:
        self.status = PolicyStatus.ROLLED_BACK

    def reject_to_draft(self) -> None:
        if self.status == PolicyStatus.PENDING_APPROVAL:
            self.status = PolicyStatus.DRAFT

    def update_draft(
        self,
        *,
        effective_from: datetime | None = None,
        expires_at: datetime | None = None,
        priority: int | None = None,
        conditions: list[dict] | None = None,
        rules: list[dict] | None = None,
        exceptions: list[dict] | None = None,
        metadata: dict | None = None,
    ) -> None:
        if not self.is_editable():
            raise ValueError("policy.errors.only_draft_editable")
        if effective_from is not None:
            self.effective_from = effective_from
        if expires_at is not None:
            self.expires_at = expires_at
        if priority is not None:
            self.priority = priority
        if conditions is not None:
            self.conditions = conditions
        if rules is not None:
            self.rules = rules
        if exceptions is not None:
            self.exceptions = exceptions
        if metadata is not None:
            self.metadata = {**self.metadata, **metadata}

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "policy_id": self.policy_id,
            "tenant_id": self.tenant_id,
            "version": self.version,
            "status": self.status.value,
            "effective_from": self.effective_from.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "priority": self.priority,
            "conditions": self.conditions,
            "rules": self.rules,
            "exceptions": self.exceptions,
            "approval_required": self.approval_required,
            "workflow_key": self.workflow_key,
            "require_passing_tests": self.require_passing_tests,
            "cache_allowed": self.cache_allowed,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }
