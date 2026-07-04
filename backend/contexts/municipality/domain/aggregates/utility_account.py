"""Municipality utility account aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

from contexts.municipality.domain.events.integration_events import UtilityBillIssuedIntegration


class UtilityType(StrEnum):
    WATER = "water"
    WASTE = "waste"
    ELECTRICITY = "electricity"


@dataclass(eq=False, kw_only=True)
class UtilityAccount(AggregateRoot):
    tenant_id: str
    account_number: str
    holder_name: str
    utility_type: UtilityType
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        account_number: str,
        holder_name: str,
        utility_type: UtilityType,
    ) -> UtilityAccount:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            account_number=account_number.strip().upper(),
            holder_name=holder_name.strip(),
            utility_type=utility_type,
        )

    def issue_bill(
        self,
        *,
        correlation_id: str,
        amount: Decimal,
        period: str,
    ) -> UtilityBillIssuedIntegration:
        if amount <= 0:
            raise ValueError("municipality.errors.invalid_bill_amount")
        return UtilityBillIssuedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            account_id=self.id,
            account_number=self.account_number,
            utility_type=self.utility_type.value,
            amount=str(amount),
            period=period,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "account_number": self.account_number,
            "holder_name": self.holder_name,
            "utility_type": self.utility_type.value,
            "created_at": self.created_at.isoformat(),
        }
