"""Local care-event projection — peer IDs + summary only (never peer aggregates)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class CareEventKind(StrEnum):
    LAB_RESULT = "lab_result"
    PHARMACY_DISPENSE = "pharmacy_dispense"


@dataclass(eq=False, kw_only=True)
class CareEventProjection(AggregateRoot):
    tenant_id: str
    source_event_id: str
    source_context: str
    event_kind: CareEventKind
    peer_id: str
    patient_id: str
    admission_id: str = ""
    encounter_id: str = ""
    summary: dict = field(default_factory=dict)
    correlation_id: str = ""
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        source_event_id: str,
        source_context: str,
        event_kind: CareEventKind,
        peer_id: str,
        patient_id: str,
        summary: dict,
        admission_id: str = "",
        encounter_id: str = "",
        correlation_id: str = "",
        occurred_at: datetime | None = None,
    ) -> CareEventProjection:
        if not tenant_id.strip():
            raise ValueError("hospital.care_event.tenant_required")
        if not source_event_id.strip():
            raise ValueError("hospital.care_event.source_event_required")
        if not patient_id.strip():
            raise ValueError("hospital.care_event.patient_required")
        if not peer_id.strip():
            raise ValueError("hospital.care_event.peer_id_required")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip().lower(),
            source_event_id=source_event_id.strip(),
            source_context=source_context.strip(),
            event_kind=event_kind,
            peer_id=peer_id.strip(),
            patient_id=patient_id.strip(),
            admission_id=(admission_id or "").strip(),
            encounter_id=(encounter_id or "").strip(),
            summary=dict(summary or {}),
            correlation_id=(correlation_id or "").strip(),
            occurred_at=occurred_at or datetime.now(UTC),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "source_event_id": self.source_event_id,
            "source_context": self.source_context,
            "event_kind": self.event_kind.value,
            "peer_id": self.peer_id,
            "patient_id": self.patient_id,
            "admission_id": self.admission_id or None,
            "encounter_id": self.encounter_id or None,
            "summary": self.summary,
            "correlation_id": self.correlation_id or None,
            "occurred_at": self.occurred_at.isoformat(),
        }
