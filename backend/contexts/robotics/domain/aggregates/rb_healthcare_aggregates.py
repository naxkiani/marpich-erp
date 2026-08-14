"""P216-I aggregates — healthcare robotics / medical AI / surgical invariants."""
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
class HealthcareRoboticsRoot(AggregateRoot):
    tenant_id: str; robotics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, robotics_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.healthcare.healthcare_robotics_platform_is_missing")
        return _mk(cls, tenant_id, "robotics_ref", robotics_ref, "robotics.healthcare.healthcare_robotics_platform_is_missing", "RobotAssignedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MedicalAiRoot(AggregateRoot):
    tenant_id: str; medical_ai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, medical_ai_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.healthcare.medical_ai_platform_is_missing")
        return _mk(cls, tenant_id, "medical_ai_ref", medical_ai_ref, "robotics.healthcare.medical_ai_platform_is_missing", "DiagnosisGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SurgicalRoboticsRoot(AggregateRoot):
    tenant_id: str; surgical_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, surgical_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.healthcare.surgical_robotics_platform_is_missing")
        return _mk(cls, tenant_id, "surgical_ref", surgical_ref, "robotics.healthcare.surgical_robotics_platform_is_missing", "SurgeryInitiatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class DigitalHealthcareAutomationRoot(AggregateRoot):
    tenant_id: str; automation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, automation_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.healthcare.digital_healthcare_automation_platform_is_missing")
        return _mk(cls, tenant_id, "automation_ref", automation_ref, "robotics.healthcare.digital_healthcare_automation_platform_is_missing", "PatientAdmittedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class ClinicalDecisionRoot(AggregateRoot):
    tenant_id: str; decision_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, decision_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.healthcare.clinical_decision_intelligence_is_missing")
        return _mk(cls, tenant_id, "decision_ref", decision_ref, "robotics.healthcare.clinical_decision_intelligence_is_missing", "TreatmentPlanApprovedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HealthcareDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.healthcare.healthcare_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "robotics.healthcare.healthcare_digital_twin_is_missing", "ProcedureCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MedicalKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.healthcare.medical_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "robotics.healthcare.medical_knowledge_graph_is_missing", "DiagnosisGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HealthcareSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.healthcare.security_compliance_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "robotics.healthcare.security_compliance_architecture_is_missing", "EmergencyDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HealthcareObservabilityRoot(AggregateRoot):
    tenant_id: str; observability_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, observability_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.healthcare.testing_validation_architecture_is_missing")
        return _mk(cls, tenant_id, "observability_ref", observability_ref, "robotics.healthcare.testing_validation_architecture_is_missing", "PatientAdmittedEvent")
    def is_missing(self)->bool: return not self.present
