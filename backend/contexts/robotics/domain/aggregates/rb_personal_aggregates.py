"""P216-W aggregates — personal robotics / home intelligence invariants."""
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
class PersonalRoboticsRoot(AggregateRoot):
    tenant_id: str; robotics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, robotics_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.personal.personal_robotics_platform_is_missing")
        return _mk(cls, tenant_id, "robotics_ref", robotics_ref, "robotics.personal.personal_robotics_platform_is_missing", "RobotConnectedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AiCompanionRoot(AggregateRoot):
    tenant_id: str; companion_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, companion_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.personal.ai_companion_platform_is_missing")
        return _mk(cls, tenant_id, "companion_ref", companion_ref, "robotics.personal.ai_companion_platform_is_missing", "AssistantActivatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SmartHomeIntelligenceRoot(AggregateRoot):
    tenant_id: str; home_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, home_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.personal.smart_home_intelligence_is_missing")
        return _mk(cls, tenant_id, "home_ref", home_ref, "robotics.personal.smart_home_intelligence_is_missing", "AutomationExecutedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HumanAugmentationRoot(AggregateRoot):
    tenant_id: str; augmentation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, augmentation_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.personal.human_augmentation_platform_is_missing")
        return _mk(cls, tenant_id, "augmentation_ref", augmentation_ref, "robotics.personal.human_augmentation_platform_is_missing", "CapabilityImprovedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class LifeAutomationRoot(AggregateRoot):
    tenant_id: str; automation_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, automation_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.personal.life_automation_platform_is_missing")
        return _mk(cls, tenant_id, "automation_ref", automation_ref, "robotics.personal.life_automation_platform_is_missing", "AutomationExecutedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PersonalDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.personal.personal_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "robotics.personal.personal_digital_twin_is_missing", "PreferenceLearnedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PersonalKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.personal.personal_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "robotics.personal.personal_knowledge_graph_is_missing", "PreferenceLearnedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PersonalSecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.personal.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "robotics.personal.security_architecture_is_missing", "PersonalCreatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class PrivacySovereigntyRoot(AggregateRoot):
    tenant_id: str; privacy_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, privacy_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.personal.privacy_sovereignty_is_missing")
        return _mk(cls, tenant_id, "privacy_ref", privacy_ref, "robotics.personal.privacy_sovereignty_is_missing", "PersonalCreatedEvent")
    def is_missing(self)->bool: return not self.present
