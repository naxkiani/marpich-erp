"""P215-H aggregates — quantum security/trust invariants."""
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
class QuantumSecurityPlatformRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.security.quantum_security_platform_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "quantum.security.quantum_security_platform_is_missing", "QuantumSecurityPolicyCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class PostQuantumCryptoRoot(AggregateRoot):
    tenant_id: str; pqc_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC)); pqc_remains_secrets: bool = True
    @classmethod
    def enable(cls, *, tenant_id: str, pqc_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.security.post_quantum_cryptography_platform_is_missing")
        obj = _mk(cls, tenant_id, "pqc_ref", pqc_ref, "quantum.security.post_quantum_cryptography_platform_is_missing", "CryptographicMigrationStartedEvent")
        obj.pqc_remains_secrets = True
        return obj
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class QuantumTrustRoot(AggregateRoot):
    tenant_id: str; trust_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, trust_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.security.quantum_trust_architecture_is_missing")
        return _mk(cls, tenant_id, "trust_ref", trust_ref, "quantum.security.quantum_trust_architecture_is_missing", "QuantumTrustEstablishedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class QuantumIdentitySecurityRoot(AggregateRoot):
    tenant_id: str; identity_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, identity_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.security.quantum_identity_security_is_missing")
        return _mk(cls, tenant_id, "identity_ref", identity_ref, "quantum.security.quantum_identity_security_is_missing", "TrustEstablishedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class QuantumKeyManagementRoot(AggregateRoot):
    tenant_id: str; key_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC)); no_local_key_store: bool = True
    @classmethod
    def enable(cls, *, tenant_id: str, key_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.security.quantum_key_management_is_missing")
        obj = _mk(cls, tenant_id, "key_ref", key_ref, "quantum.security.quantum_key_management_is_missing", "KeyRotatedEvent")
        obj.no_local_key_store = True
        return obj
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class ThreatIntelligenceRoot(AggregateRoot):
    tenant_id: str; threat_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, threat_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.security.threat_intelligence_platform_is_missing")
        return _mk(cls, tenant_id, "threat_ref", threat_ref, "quantum.security.threat_intelligence_platform_is_missing", "QuantumThreatDetectedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class SecTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.security.security_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "quantum.security.security_digital_twin_is_missing", "QuantumThreatDetectedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class SecKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; graph_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, graph_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.security.security_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "graph_ref", graph_ref, "quantum.security.security_knowledge_graph_is_missing", "QuantumSecurityPolicyCreatedEvent")
    def is_missing(self)->bool: return not self.present
@dataclass(eq=False, kw_only=True)
class ZeroTrustRoot(AggregateRoot):
    tenant_id: str; zero_trust_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, zero_trust_ref: str, present: bool = True):
        if not present: raise ValueError("quantum.security.zero_trust_architecture_is_missing")
        return _mk(cls, tenant_id, "zero_trust_ref", zero_trust_ref, "quantum.security.zero_trust_architecture_is_missing", "SecurityValidationCompletedEvent")
    def is_missing(self)->bool: return not self.present
