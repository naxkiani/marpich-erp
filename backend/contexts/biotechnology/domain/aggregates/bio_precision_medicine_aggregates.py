"""P217-I aggregates — biotechnology precision medicine invariants."""
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
class PrecisionMedicinePlatformRoot(AggregateRoot):
    tenant_id: str; platform_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, platform_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.precision_medicine.precision_medicine_platform_is_missing")
        return _mk(cls, tenant_id, "platform_ref", platform_ref, "biotechnology.precision_medicine.precision_medicine_platform_is_missing", "PrecisionMedicinePlatformActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class GenomicsAiRoot(AggregateRoot):
    tenant_id: str; genomics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, genomics_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.precision_medicine.genomics_ai_is_missing")
        return _mk(cls, tenant_id, "genomics_ref", genomics_ref, "biotechnology.precision_medicine.genomics_ai_is_missing", "GenomeProfileCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class OmicsIntelligenceRoot(AggregateRoot):
    tenant_id: str; omics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, omics_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.precision_medicine.omics_intelligence_is_missing")
        return _mk(cls, tenant_id, "omics_ref", omics_ref, "biotechnology.precision_medicine.omics_intelligence_is_missing", "MolecularProfileUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class MolecularMedicineRoot(AggregateRoot):
    tenant_id: str; molecular_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, molecular_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.precision_medicine.molecular_medicine_is_missing")
        return _mk(cls, tenant_id, "molecular_ref", molecular_ref, "biotechnology.precision_medicine.molecular_medicine_is_missing", "MolecularPredictionGeneratedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PersonalizedTherapyRoot(AggregateRoot):
    tenant_id: str; therapy_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, therapy_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.precision_medicine.personalized_therapy_is_missing")
        return _mk(cls, tenant_id, "therapy_ref", therapy_ref, "biotechnology.precision_medicine.personalized_therapy_is_missing", "TherapyRecommendedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PatientMolecularProfileRoot(AggregateRoot):
    tenant_id: str; profile_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, profile_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.precision_medicine.precision_medicine_platform_is_missing")
        return _mk(cls, tenant_id, "profile_ref", profile_ref, "biotechnology.precision_medicine.precision_medicine_platform_is_missing", "VariantDetectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PrecisionDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.precision_medicine.precision_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "biotechnology.precision_medicine.precision_digital_twin_is_missing", "TreatmentOutcomeRecordedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PrecisionMedicineGovernanceRoot(AggregateRoot):
    tenant_id: str; governance_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, governance_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.precision_medicine.governance_is_missing")
        return _mk(cls, tenant_id, "governance_ref", governance_ref, "biotechnology.precision_medicine.governance_is_missing", "PrecisionMedicineGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PrecisionMedicineSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("biotechnology.precision_medicine.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "biotechnology.precision_medicine.security_architecture_is_missing", "PrecisionMedicineGovernanceViolationEvent")
    def is_missing(self)->bool: return not self.present
