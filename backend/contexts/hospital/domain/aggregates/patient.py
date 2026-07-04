"""Patient aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Patient(AggregateRoot):
    tenant_id: str
    mrn: str
    first_name: str
    last_name: str
    date_of_birth: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        mrn: str,
        first_name: str,
        last_name: str,
        date_of_birth: str,
    ) -> Patient:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            mrn=mrn.strip().upper(),
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            date_of_birth=date_of_birth,
        )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "mrn": self.mrn,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth,
            "created_at": self.created_at.isoformat(),
        }
