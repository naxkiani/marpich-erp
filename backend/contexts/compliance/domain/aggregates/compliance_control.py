"""Registered compliance control."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class ComplianceControl(AggregateRoot):
    tenant_id: str
    domain: str
    control_id: str
    name: str
    severity: str
    is_active: bool = True

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        domain: str,
        control_id: str,
        name: str,
        severity: str,
    ) -> ComplianceControl:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            domain=domain,
            control_id=control_id,
            name=name,
            severity=severity,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "domain": self.domain,
            "control_id": self.control_id,
            "name": self.name,
            "severity": self.severity,
            "is_active": self.is_active,
        }
