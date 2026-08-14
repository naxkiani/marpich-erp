"""P216-P aggregates — hospitality robotics / smart hotel invariants."""
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
class HospitalityRoboticsRoot(AggregateRoot):
    tenant_id: str; robotics_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, robotics_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.hospitality.hospitality_robotics_platform_is_missing")
        return _mk(cls, tenant_id, "robotics_ref", robotics_ref, "robotics.hospitality.hospitality_robotics_platform_is_missing", "RobotMissionCompletedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class SmartHotelRoot(AggregateRoot):
    tenant_id: str; hotel_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, hotel_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.hospitality.smart_hotel_platform_is_missing")
        return _mk(cls, tenant_id, "hotel_ref", hotel_ref, "robotics.hospitality.smart_hotel_platform_is_missing", "HotelOptimisedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class AutonomousGuestServicesRoot(AggregateRoot):
    tenant_id: str; services_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, services_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.hospitality.autonomous_guest_services_is_missing")
        return _mk(cls, tenant_id, "services_ref", services_ref, "robotics.hospitality.autonomous_guest_services_is_missing", "ServiceRequestedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class GuestExperienceRoot(AggregateRoot):
    tenant_id: str; experience_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, experience_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.hospitality.guest_experience_intelligence_is_missing")
        return _mk(cls, tenant_id, "experience_ref", experience_ref, "robotics.hospitality.guest_experience_intelligence_is_missing", "GuestExperienceUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HospitalityAiRoot(AggregateRoot):
    tenant_id: str; ai_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, ai_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.hospitality.hospitality_ai_platform_is_missing")
        return _mk(cls, tenant_id, "ai_ref", ai_ref, "robotics.hospitality.hospitality_ai_platform_is_missing", "GuestExperienceUpdatedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HotelDigitalTwinRoot(AggregateRoot):
    tenant_id: str; twin_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, twin_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.hospitality.hotel_digital_twin_is_missing")
        return _mk(cls, tenant_id, "twin_ref", twin_ref, "robotics.hospitality.hotel_digital_twin_is_missing", "HotelOptimisedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HospitalityKnowledgeGraphRoot(AggregateRoot):
    tenant_id: str; kg_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, kg_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.hospitality.hospitality_knowledge_graph_is_missing")
        return _mk(cls, tenant_id, "kg_ref", kg_ref, "robotics.hospitality.hospitality_knowledge_graph_is_missing", "GuestArrivalEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class HospitalitySecurityRoot(AggregateRoot):
    tenant_id: str; security_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, security_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.hospitality.security_architecture_is_missing")
        return _mk(cls, tenant_id, "security_ref", security_ref, "robotics.hospitality.security_architecture_is_missing", "ReservationConfirmedEvent")
    def is_missing(self)->bool: return not self.present

@dataclass(eq=False, kw_only=True)
class RoomIntelligenceRoot(AggregateRoot):
    tenant_id: str; room_ref: str; present: bool; status: str; pending_events: list[str]=field(default_factory=list); history: list[dict]=field(default_factory=list); created_at: datetime=field(default_factory=lambda: datetime.now(UTC))
    @classmethod
    def enable(cls, *, tenant_id: str, room_ref: str, present: bool = True):
        if not present: raise ValueError("robotics.hospitality.smart_hotel_platform_is_missing")
        return _mk(cls, tenant_id, "room_ref", room_ref, "robotics.hospitality.smart_hotel_platform_is_missing", "RoomPreparedEvent")
    def is_missing(self)->bool: return not self.present
