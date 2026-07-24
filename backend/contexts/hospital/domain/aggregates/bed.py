"""Bed aggregate — CAP-HLT-004 ward/room inventory (hospital only)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class BedStatus(StrEnum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    BLOCKED = "blocked"


@dataclass(eq=False, kw_only=True)
class Bed(AggregateRoot):
    tenant_id: str
    ward: str
    room: str
    bed_code: str
    status: BedStatus = BedStatus.AVAILABLE
    current_admission_id: UniqueId | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        ward: str,
        room: str,
        bed_code: str,
    ) -> Bed:
        ward_n = ward.strip()
        room_n = room.strip()
        code_n = bed_code.strip().upper()
        if not ward_n or not room_n or not code_n:
            raise ValueError("hospital.errors.invalid_bed_location")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            ward=ward_n,
            room=room_n,
            bed_code=code_n,
        )

    def occupy(self, admission_id: UniqueId) -> None:
        if self.status == BedStatus.BLOCKED:
            raise ValueError("hospital.errors.bed_blocked")
        if self.status == BedStatus.OCCUPIED:
            raise ValueError("hospital.errors.bed_occupied")
        self.status = BedStatus.OCCUPIED
        self.current_admission_id = admission_id

    def release(self) -> None:
        if self.status == BedStatus.BLOCKED:
            raise ValueError("hospital.errors.bed_blocked")
        self.status = BedStatus.AVAILABLE
        self.current_admission_id = None

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "ward": self.ward,
            "room": self.room,
            "bed_code": self.bed_code,
            "status": self.status.value,
            "current_admission_id": (
                str(self.current_admission_id) if self.current_admission_id else None
            ),
            "created_at": self.created_at.isoformat(),
        }
