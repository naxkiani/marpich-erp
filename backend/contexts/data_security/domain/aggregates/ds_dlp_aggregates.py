"""P211-G DLP aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsIdentifiableSensitiveRoot(AggregateRoot):
    tenant_id: str
    asset_ref: str
    identifiable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def identify(
        cls, *, tenant_id: str, asset_ref: str, identifiable: bool = True
    ) -> DsIdentifiableSensitiveRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dlp.tenant_required")
        if not identifiable:
            raise ValueError(
                "data_security.dlp.sensitive_data_cannot_be_identified"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            asset_ref=asset_ref.strip(),
            identifiable=True,
            status="identified",
        )
        root.pending_events.append("SensitiveDataDetected")
        root.pending_events.append("UnidentifiableSensitiveRejected")
        root.history.append({"event": "SensitiveIdentified"})
        return root

    def is_unidentifiable(self) -> bool:
        return not self.identifiable


@dataclass(eq=False, kw_only=True)
class DsMonitoredMovementRoot(AggregateRoot):
    tenant_id: str
    transfer_ref: str
    monitored: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def monitor(
        cls, *, tenant_id: str, transfer_ref: str, monitored: bool = True
    ) -> DsMonitoredMovementRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dlp.mon_tenant_required")
        if not monitored:
            raise ValueError(
                "data_security.dlp.data_movement_cannot_be_monitored"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            transfer_ref=transfer_ref.strip(),
            monitored=True,
            status="monitored",
        )
        root.pending_events.append("DataTransferDetected")
        root.pending_events.append("UnmonitoredMovementRejected")
        root.history.append({"event": "MovementMonitored"})
        return root

    def is_unmonitored(self) -> bool:
        return not self.monitored


@dataclass(eq=False, kw_only=True)
class DsEnforceablePolicyRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    enforceable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls, *, tenant_id: str, policy_ref: str, enforceable: bool = True
    ) -> DsEnforceablePolicyRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dlp.pol_tenant_required")
        if not enforceable:
            raise ValueError(
                "data_security.dlp.policies_cannot_be_enforced"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            enforceable=True,
            status="enforceable",
        )
        root.pending_events.append("PolicyUpdated")
        root.pending_events.append("UnenforceablePolicyRejected")
        root.history.append({"event": "PolicyEnforceable"})
        return root

    def is_unenforceable(self) -> bool:
        return not self.enforceable


@dataclass(eq=False, kw_only=True)
class DsManagedAiLeakageRoot(AggregateRoot):
    tenant_id: str
    ai_ref: str
    managed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def protect(
        cls, *, tenant_id: str, ai_ref: str, managed: bool = True
    ) -> DsManagedAiLeakageRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dlp.ai_tenant_required")
        if not managed:
            raise ValueError("data_security.dlp.ai_leakage_is_unmanaged")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            ai_ref=ai_ref.strip(),
            managed=True,
            status="managed",
        )
        root.pending_events.append("SensitiveDataDetected")
        root.pending_events.append("UnmanagedAiLeakageRejected")
        root.history.append({"event": "AiLeakageManaged"})
        return root

    def is_unmanaged(self) -> bool:
        return not self.managed


@dataclass(eq=False, kw_only=True)
class DsVisibleInsiderRiskRoot(AggregateRoot):
    tenant_id: str
    risk_ref: str
    visible: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls, *, tenant_id: str, risk_ref: str, visible: bool = True
    ) -> DsVisibleInsiderRiskRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dlp.ins_tenant_required")
        if not visible:
            raise ValueError("data_security.dlp.insider_risk_is_invisible")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            risk_ref=risk_ref.strip(),
            visible=True,
            status="visible",
        )
        root.pending_events.append("RiskScoreChanged")
        root.pending_events.append("InvisibleInsiderRiskRejected")
        root.history.append({"event": "InsiderRiskVisible"})
        return root

    def is_invisible(self) -> bool:
        return not self.visible


@dataclass(eq=False, kw_only=True)
class DsInvestigableViolationRoot(AggregateRoot):
    tenant_id: str
    violation_ref: str
    investigable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls, *, tenant_id: str, violation_ref: str, investigable: bool = True
    ) -> DsInvestigableViolationRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dlp.vio_tenant_required")
        if not investigable:
            raise ValueError(
                "data_security.dlp.violations_cannot_be_investigated"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            violation_ref=violation_ref.strip(),
            investigable=True,
            status="open",
        )
        root.pending_events.append("DLPViolationCreated")
        root.pending_events.append("IncidentCreated")
        root.pending_events.append("UninvestigableViolationRejected")
        root.history.append({"event": "ViolationInvestigable"})
        return root

    def is_uninvestigable(self) -> bool:
        return not self.investigable


@dataclass(eq=False, kw_only=True)
class DsAutomatedResponseRoot(AggregateRoot):
    tenant_id: str
    response_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def respond(
        cls, *, tenant_id: str, response_ref: str, available: bool = True
    ) -> DsAutomatedResponseRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dlp.resp_tenant_required")
        if not available:
            raise ValueError(
                "data_security.dlp.automated_response_is_unavailable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            response_ref=response_ref.strip(),
            available=True,
            status="responded",
        )
        root.pending_events.append("TransferBlocked")
        root.pending_events.append("UnavailableAutomatedResponseRejected")
        root.history.append({"event": "AutomatedResponse"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class DsBlockedTransferRoot(AggregateRoot):
    tenant_id: str
    transfer_ref: str
    blocked: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def block(
        cls, *, tenant_id: str, transfer_ref: str, blocked: bool = True
    ) -> DsBlockedTransferRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.dlp.blk_tenant_required")
        if not blocked:
            raise ValueError("data_security.dlp.transfer_not_blocked")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            transfer_ref=transfer_ref.strip(),
            blocked=True,
            status="blocked",
        )
        root.pending_events.append("TransferBlocked")
        root.history.append({"event": "TransferBlocked"})
        return root
