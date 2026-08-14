"""P211-E Classification / labeling aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsClassifiableDataRoot(AggregateRoot):
    tenant_id: str
    asset_ref: str
    classifiable: bool
    level: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def classify(
        cls,
        *,
        tenant_id: str,
        asset_ref: str,
        classifiable: bool = True,
        level: str = "confidential",
    ) -> DsClassifiableDataRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.classification.tenant_required")
        if not classifiable:
            raise ValueError(
                "data_security.classification.data_cannot_be_classified"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            asset_ref=asset_ref.strip(),
            classifiable=True,
            level=level.strip(),
            status="classified",
        )
        root.pending_events.append("DataClassified")
        root.pending_events.append("UnclassifiableDataRejected")
        root.history.append({"event": "DataClassified"})
        return root

    def is_unclassifiable(self) -> bool:
        return not self.classifiable


@dataclass(eq=False, kw_only=True)
class DsSensitiveDetectionRoot(AggregateRoot):
    tenant_id: str
    detection_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls, *, tenant_id: str, detection_ref: str, available: bool = True
    ) -> DsSensitiveDetectionRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.classification.sens_tenant_required")
        if not available:
            raise ValueError(
                "data_security.classification.sensitive_data_detection_is_unavailable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            detection_ref=detection_ref.strip(),
            available=True,
            status="detected",
        )
        root.pending_events.append("SensitiveInformationDetected")
        root.pending_events.append("UnavailableSensitiveDetectionRejected")
        root.history.append({"event": "SensitiveDetected"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class DsManagedLabelsRoot(AggregateRoot):
    tenant_id: str
    label_ref: str
    managed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def apply(
        cls, *, tenant_id: str, label_ref: str, managed: bool = True
    ) -> DsManagedLabelsRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.classification.label_tenant_required")
        if not managed:
            raise ValueError(
                "data_security.classification.labels_are_unmanaged"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            label_ref=label_ref.strip(),
            managed=True,
            status="applied",
        )
        root.pending_events.append("LabelApplied")
        root.pending_events.append("UnmanagedLabelsRejected")
        root.history.append({"event": "LabelManaged"})
        return root

    def is_unmanaged(self) -> bool:
        return not self.managed


@dataclass(eq=False, kw_only=True)
class DsExplainableAiRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    explainable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def decide(
        cls, *, tenant_id: str, decision_ref: str, explainable: bool = True
    ) -> DsExplainableAiRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.classification.ai_tenant_required")
        if not explainable:
            raise ValueError(
                "data_security.classification.ai_decisions_are_unexplained"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            decision_ref=decision_ref.strip(),
            explainable=True,
            status="explained",
        )
        root.pending_events.append("DataClassified")
        root.pending_events.append("UnexplainedAiRejected")
        root.history.append({"event": "AiExplained"})
        return root

    def is_unexplained(self) -> bool:
        return not self.explainable


@dataclass(eq=False, kw_only=True)
class DsClassificationPoliciesRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def update(
        cls, *, tenant_id: str, policy_ref: str, present: bool = True
    ) -> DsClassificationPoliciesRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.classification.pol_tenant_required")
        if not present:
            raise ValueError(
                "data_security.classification.classification_policies_are_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            present=True,
            status="present",
        )
        root.pending_events.append("ClassificationPolicyChanged")
        root.pending_events.append("MissingPoliciesRejected")
        root.history.append({"event": "PoliciesPresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DsClassificationLifecycleRoot(AggregateRoot):
    tenant_id: str
    lifecycle_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, lifecycle_ref: str, defined: bool = True
    ) -> DsClassificationLifecycleRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.classification.life_tenant_required")
        if not defined:
            raise ValueError(
                "data_security.classification.classification_lifecycle_is_undefined"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            lifecycle_ref=lifecycle_ref.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("ClassificationReviewed")
        root.pending_events.append("UndefinedLifecycleRejected")
        root.history.append({"event": "LifecycleDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class DsClassificationDecisionRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    approved: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def approve(
        cls, *, tenant_id: str, decision_ref: str, approved: bool = True
    ) -> DsClassificationDecisionRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.classification.dec_tenant_required")
        if not approved:
            raise ValueError(
                "data_security.classification.classification_not_approved"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            decision_ref=decision_ref.strip(),
            approved=True,
            status="approved",
        )
        root.pending_events.append("ClassificationReviewed")
        root.history.append({"event": "ClassificationApproved"})
        return root


@dataclass(eq=False, kw_only=True)
class DsLabelAppliedRoot(AggregateRoot):
    tenant_id: str
    label_ref: str
    applied: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def apply(
        cls, *, tenant_id: str, label_ref: str, applied: bool = True
    ) -> DsLabelAppliedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.classification.app_tenant_required")
        if not applied:
            raise ValueError("data_security.classification.label_not_applied")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            label_ref=label_ref.strip(),
            applied=True,
            status="applied",
        )
        root.pending_events.append("LabelApplied")
        root.pending_events.append("LabelUpdated")
        root.history.append({"event": "LabelApplied"})
        return root
