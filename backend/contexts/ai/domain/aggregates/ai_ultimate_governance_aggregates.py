"""P214-Y aggregates - constitutional trust invariants."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

def _tid(tenant_id: str, code: str) -> str:
    if not tenant_id.strip():
        raise ValueError(code)
    return tenant_id.strip()

def _mk(root_cls, tenant_id: str, ref_name: str, ref_value: str, err: str, event: str):
    tid = _tid(tenant_id, err + ".tenant")
    obj = root_cls(id=UniqueId.generate(), tenant_id=tid, **{ref_name: ref_value.strip()}, present=True, status="enabled")
    obj.pending_events.append(event)
    return obj
@dataclass(eq=False, kw_only=True)
class ConstitutionRoot(AggregateRoot):
    tenant_id: str; constitution_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, constitution_ref: str, present: bool = True):
        if not present: raise ValueError("ai.ultimate.ai_constitutional_framework_is_missing")
        return _mk(cls, tenant_id, "constitution_ref", constitution_ref, "ai.ultimate.ai_constitutional_framework_is_missing", "AIConstitutionCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class AlignmentRoot(AggregateRoot):
    tenant_id: str; alignment_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, alignment_ref: str, present: bool = True):
        if not present: raise ValueError("ai.ultimate.ai_alignment_platform_is_missing")
        return _mk(cls, tenant_id, "alignment_ref", alignment_ref, "ai.ultimate.ai_alignment_platform_is_missing", "AlignmentVerifiedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class EthicsRoot(AggregateRoot):
    tenant_id: str; ethics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ethics_ref: str, present: bool = True):
        if not present: raise ValueError("ai.ultimate.ai_ethics_intelligence_is_missing")
        return _mk(cls, tenant_id, "ethics_ref", ethics_ref, "ai.ultimate.ai_ethics_intelligence_is_missing", "EthicsCompletedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class TrustCertificationRoot(AggregateRoot):
    tenant_id: str; trust_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, trust_ref: str, present: bool = True):
        if not present: raise ValueError("ai.ultimate.ai_trust_certification_is_missing")
        return _mk(cls, tenant_id, "trust_ref", trust_ref, "ai.ultimate.ai_trust_certification_is_missing", "TrustCertifiedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class AccountabilityRoot(AggregateRoot):
    tenant_id: str; accountability_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, accountability_ref: str, present: bool = True):
        if not present: raise ValueError("ai.ultimate.ai_accountability_framework_is_missing")
        return _mk(cls, tenant_id, "accountability_ref", accountability_ref, "ai.ultimate.ai_accountability_framework_is_missing", "GovernanceUpdatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class ValuesRoot(AggregateRoot):
    tenant_id: str; values_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, values_ref: str, present: bool = True):
        if not present: raise ValueError("ai.ultimate.civilization_values_model_is_missing")
        return _mk(cls, tenant_id, "values_ref", values_ref, "ai.ultimate.civilization_values_model_is_missing", "GovernanceUpdatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class TrustTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("ai.ultimate.digital_twin_integration_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "ai.ultimate.digital_twin_integration_is_missing", "GovernanceUpdatedEvent")
    def is_missing(self)->bool: return not self.present
