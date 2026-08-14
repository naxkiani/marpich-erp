"""CRM Contact aggregate — CAP-ENT-001 Customer Management."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Contact(AggregateRoot):
    tenant_id: str
    email: str
    full_name: str
    company: str | None = None
    phone: str | None = None
    status: str = "active"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        email: str,
        full_name: str,
        company: str | None = None,
        phone: str | None = None,
    ) -> Contact:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            email=email.strip().lower(),
            full_name=full_name.strip(),
            company=company.strip() if company else None,
            phone=phone.strip() if phone else None,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "email": self.email,
            "full_name": self.full_name,
            "company": self.company,
            "phone": self.phone,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
