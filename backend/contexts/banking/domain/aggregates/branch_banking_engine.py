"""Branch Banking Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class BranchOfficeType(StrEnum):
    HEAD_OFFICE = "head_office"
    REGIONAL_OFFICE = "regional_office"
    BRANCH = "branch"
    SUB_BRANCH = "sub_branch"


class BranchExtensionType(StrEnum):
    CASH_COUNTER = "cash_counter"
    ATM_EXTENSION = "atm_extension"
    SELF_SERVICE_KIOSK = "self_service_kiosk_extension"


class BranchSessionStatus(StrEnum):
    CLOSED = "closed"
    OPENING = "opening"
    OPEN = "open"
    CLOSING = "closing"


class VaultMovementType(StrEnum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER_TO_DRAWER = "transfer_to_drawer"
    TRANSFER_FROM_DRAWER = "transfer_from_drawer"


@dataclass(eq=False, kw_only=True)
class BranchOffice(AggregateRoot):
    tenant_id: str
    office_ref: str
    office_type: str
    name: str
    code: str
    parent_office_id: str | None = None
    region: str = ""
    address: str = ""
    currency: str = "USD"
    status: str = BranchSessionStatus.CLOSED.value
    active: bool = True
    opened_at: datetime | None = None
    closed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        office_ref: str,
        office_type: str,
        name: str,
        code: str,
        parent_office_id: str | None = None,
        region: str = "",
        address: str = "",
        currency: str = "USD",
    ) -> BranchOffice:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            office_ref=office_ref,
            office_type=office_type,
            name=name.strip(),
            code=code.strip().upper(),
            parent_office_id=parent_office_id,
            region=region,
            address=address,
            currency=currency,
        )

    def open_branch(self) -> None:
        if self.status == BranchSessionStatus.OPEN.value:
            raise ValueError("already_open")
        self.status = BranchSessionStatus.OPEN.value
        self.opened_at = datetime.now(UTC)
        self.closed_at = None

    def close_branch(self) -> None:
        if self.status != BranchSessionStatus.OPEN.value:
            raise ValueError("not_open")
        self.status = BranchSessionStatus.CLOSED.value
        self.closed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "office_ref": self.office_ref,
            "office_type": self.office_type,
            "name": self.name,
            "code": self.code,
            "parent_office_id": self.parent_office_id,
            "region": self.region,
            "address": self.address,
            "currency": self.currency,
            "status": self.status,
            "active": self.active,
            "opened_at": self.opened_at.isoformat() if self.opened_at else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BranchExtension(AggregateRoot):
    tenant_id: str
    office_id: str
    extension_ref: str
    extension_type: str
    label: str
    terminal_id: str = ""
    active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        office_id: str,
        extension_ref: str,
        extension_type: str,
        label: str,
        terminal_id: str = "",
    ) -> BranchExtension:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            office_id=office_id,
            extension_ref=extension_ref,
            extension_type=extension_type,
            label=label.strip(),
            terminal_id=terminal_id,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "office_id": self.office_id,
            "extension_ref": self.extension_ref,
            "extension_type": self.extension_type,
            "label": self.label,
            "terminal_id": self.terminal_id,
            "active": self.active,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BranchDaySession(AggregateRoot):
    tenant_id: str
    office_id: str
    session_ref: str
    session_type: str
    opening_balance: float = 0.0
    closing_balance: float = 0.0
    operator_id: str = ""
    notes: str = ""
    completed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        office_id: str,
        session_ref: str,
        session_type: str,
        opening_balance: float = 0.0,
        closing_balance: float = 0.0,
        operator_id: str = "",
        notes: str = "",
    ) -> BranchDaySession:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            office_id=office_id,
            session_ref=session_ref,
            session_type=session_type,
            opening_balance=round(opening_balance, 2),
            closing_balance=round(closing_balance, 2),
            operator_id=operator_id,
            notes=notes,
            completed_at=datetime.now(UTC),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "office_id": self.office_id,
            "session_ref": self.session_ref,
            "session_type": self.session_type,
            "opening_balance": self.opening_balance,
            "closing_balance": self.closing_balance,
            "operator_id": self.operator_id,
            "notes": self.notes,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BranchVault(AggregateRoot):
    tenant_id: str
    office_id: str
    vault_ref: str
    currency: str = "USD"
    balance: float = 0.0
    limit_amount: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        office_id: str,
        vault_ref: str,
        currency: str = "USD",
        limit_amount: float = 0.0,
    ) -> BranchVault:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            office_id=office_id,
            vault_ref=vault_ref,
            currency=currency,
            limit_amount=round(limit_amount, 2),
        )

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("invalid_amount")
        if self.limit_amount > 0 and self.balance + amount > self.limit_amount:
            raise ValueError("vault_limit_exceeded")
        self.balance = round(self.balance + amount, 2)

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("invalid_amount")
        if self.balance < amount:
            raise ValueError("insufficient_vault_balance")
        self.balance = round(self.balance - amount, 2)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "office_id": self.office_id,
            "vault_ref": self.vault_ref,
            "currency": self.currency,
            "balance": self.balance,
            "limit_amount": self.limit_amount,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BranchVaultMovement(AggregateRoot):
    tenant_id: str
    vault_id: str
    office_id: str
    movement_ref: str
    movement_type: str
    amount: float
    currency: str = "USD"
    operator_id: str = ""
    narrative: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        vault_id: str,
        office_id: str,
        movement_ref: str,
        movement_type: str,
        amount: float,
        currency: str = "USD",
        operator_id: str = "",
        narrative: str = "",
    ) -> BranchVaultMovement:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            vault_id=vault_id,
            office_id=office_id,
            movement_ref=movement_ref,
            movement_type=movement_type,
            amount=round(amount, 2),
            currency=currency,
            operator_id=operator_id,
            narrative=narrative,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "vault_id": self.vault_id,
            "office_id": self.office_id,
            "movement_ref": self.movement_ref,
            "movement_type": self.movement_type,
            "amount": self.amount,
            "currency": self.currency,
            "operator_id": self.operator_id,
            "narrative": self.narrative,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BranchCashLimit(AggregateRoot):
    tenant_id: str
    office_id: str
    limit_ref: str
    limit_type: str
    max_amount: float
    currency: str = "USD"
    extension_id: str | None = None
    active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        office_id: str,
        limit_ref: str,
        limit_type: str,
        max_amount: float,
        currency: str = "USD",
        extension_id: str | None = None,
    ) -> BranchCashLimit:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            office_id=office_id,
            limit_ref=limit_ref,
            limit_type=limit_type,
            max_amount=round(max_amount, 2),
            currency=currency,
            extension_id=extension_id,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "office_id": self.office_id,
            "limit_ref": self.limit_ref,
            "limit_type": self.limit_type,
            "max_amount": self.max_amount,
            "currency": self.currency,
            "extension_id": self.extension_id,
            "active": self.active,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BranchEmployeeAssignment(AggregateRoot):
    tenant_id: str
    office_id: str
    assignment_ref: str
    employee_id: str
    role: str
    extension_id: str | None = None
    active: bool = True
    assigned_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        office_id: str,
        assignment_ref: str,
        employee_id: str,
        role: str,
        extension_id: str | None = None,
    ) -> BranchEmployeeAssignment:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            office_id=office_id,
            assignment_ref=assignment_ref,
            employee_id=employee_id,
            role=role,
            extension_id=extension_id,
        )

    def deactivate(self) -> None:
        self.active = False

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "office_id": self.office_id,
            "assignment_ref": self.assignment_ref,
            "employee_id": self.employee_id,
            "role": self.role,
            "extension_id": self.extension_id,
            "active": self.active,
            "assigned_at": self.assigned_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BranchKPIRecord(AggregateRoot):
    tenant_id: str
    office_id: str
    kpi_ref: str
    metric_key: str
    metric_value: float
    target_value: float = 0.0
    period: str = "daily"
    recorded_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        office_id: str,
        kpi_ref: str,
        metric_key: str,
        metric_value: float,
        target_value: float = 0.0,
        period: str = "daily",
    ) -> BranchKPIRecord:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            office_id=office_id,
            kpi_ref=kpi_ref,
            metric_key=metric_key,
            metric_value=round(metric_value, 2),
            target_value=round(target_value, 2),
            period=period,
        )

    def to_dict(self) -> dict:
        achievement = (
            round((self.metric_value / self.target_value) * 100, 2) if self.target_value > 0 else None
        )
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "office_id": self.office_id,
            "kpi_ref": self.kpi_ref,
            "metric_key": self.metric_key,
            "metric_value": self.metric_value,
            "target_value": self.target_value,
            "achievement_pct": achievement,
            "period": self.period,
            "recorded_at": self.recorded_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BranchAuditEntry(AggregateRoot):
    tenant_id: str
    office_id: str
    action: str
    actor_id: str | None = None
    detail: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        office_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
    ) -> BranchAuditEntry:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            office_id=office_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "office_id": self.office_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "detail": self.detail,
            "created_at": self.created_at.isoformat(),
        }
