"""Enterprise Cash Management aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class CashLocationType(StrEnum):
    CASH_REGISTER = "cash_register"
    PETTY_CASH = "petty_cash"
    MAIN_CASH_OFFICE = "main_cash_office"
    VAULT = "vault"
    SAFE = "safe"
    BRANCH_CASH = "branch_cash"
    DEPARTMENT_CASH = "department_cash"


class CashLocationStatus(StrEnum):
    ACTIVE = "active"
    CLOSED = "closed"
    SUSPENDED = "suspended"


class CashTransactionType(StrEnum):
    TRANSFER = "transfer"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    RECEIPT = "receipt"
    PAYMENT = "payment"
    ADJUSTMENT = "adjustment"


class CashCountStatus(StrEnum):
    DRAFT = "draft"
    VERIFIED = "verified"
    REJECTED = "rejected"


class CashClosingStatus(StrEnum):
    OPEN = "open"
    CLOSED = "closed"


@dataclass(eq=False, kw_only=True)
class CashLocation(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    branch_id: str | None
    department_id: str | None
    code: str
    name: str
    location_type: str
    currency: str
    balance: float
    status: str
    gl_account_code: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        code: str,
        name: str,
        location_type: str,
        currency: str = "USD",
        organization_id: str | None = None,
        branch_id: str | None = None,
        department_id: str | None = None,
        opening_balance: float = 0.0,
        gl_account_code: str | None = None,
    ) -> CashLocation:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            branch_id=branch_id,
            department_id=department_id,
            code=code.strip().upper(),
            name=name.strip(),
            location_type=location_type,
            currency=currency.strip().upper(),
            balance=round(opening_balance, 2),
            status=CashLocationStatus.ACTIVE.value,
            gl_account_code=gl_account_code,
        )

    def credit(self, amount: float) -> None:
        self.balance = round(self.balance + amount, 2)

    def debit(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("insufficient_balance")
        self.balance = round(self.balance - amount, 2)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "branch_id": self.branch_id,
            "department_id": self.department_id,
            "code": self.code,
            "name": self.name,
            "location_type": self.location_type,
            "currency": self.currency,
            "balance": self.balance,
            "status": self.status,
            "gl_account_code": self.gl_account_code,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class CashTransaction(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    location_id: str
    transaction_type: str
    amount: float
    currency: str
    reference: str
    description: str | None
    counterpart_location_id: str | None
    direction: str
    created_by: str | None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        location_id: str,
        transaction_type: str,
        amount: float,
        currency: str,
        reference: str,
        direction: str,
        organization_id: str | None = None,
        description: str | None = None,
        counterpart_location_id: str | None = None,
        created_by: str | None = None,
    ) -> CashTransaction:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            location_id=location_id,
            transaction_type=transaction_type,
            amount=round(amount, 2),
            currency=currency.strip().upper(),
            reference=reference,
            description=description,
            counterpart_location_id=counterpart_location_id,
            direction=direction,
            created_by=created_by,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "location_id": self.location_id,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "currency": self.currency,
            "reference": self.reference,
            "description": self.description,
            "counterpart_location_id": self.counterpart_location_id,
            "direction": self.direction,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class CashCount(AggregateRoot):
    tenant_id: str
    location_id: str
    system_balance: float
    counted_amount: float
    variance: float
    currency: str
    status: str
    counted_by: str
    notes: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        location_id: str,
        system_balance: float,
        counted_amount: float,
        currency: str,
        counted_by: str,
        notes: str | None = None,
    ) -> CashCount:
        variance = round(counted_amount - system_balance, 2)
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            location_id=location_id,
            system_balance=round(system_balance, 2),
            counted_amount=round(counted_amount, 2),
            variance=variance,
            currency=currency,
            status=CashCountStatus.DRAFT.value,
            counted_by=counted_by,
            notes=notes,
        )

    def verify(self) -> None:
        self.status = CashCountStatus.VERIFIED.value

    def reject(self) -> None:
        self.status = CashCountStatus.REJECTED.value

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "location_id": self.location_id,
            "system_balance": self.system_balance,
            "counted_amount": self.counted_amount,
            "variance": self.variance,
            "currency": self.currency,
            "status": self.status,
            "counted_by": self.counted_by,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class CashVerification(AggregateRoot):
    tenant_id: str
    cash_count_id: str
    verified_by: str
    approved: bool
    notes: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        cash_count_id: str,
        verified_by: str,
        approved: bool,
        notes: str | None = None,
    ) -> CashVerification:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            cash_count_id=cash_count_id,
            verified_by=verified_by,
            approved=approved,
            notes=notes,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "cash_count_id": self.cash_count_id,
            "verified_by": self.verified_by,
            "approved": self.approved,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class CashClosing(AggregateRoot):
    tenant_id: str
    location_id: str
    opening_balance: float
    closing_balance: float
    counted_amount: float
    variance: float
    currency: str
    status: str
    closed_by: str
    closed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def open_session(
        cls,
        *,
        tenant_id: str,
        location_id: str,
        opening_balance: float,
        currency: str,
        closed_by: str,
    ) -> CashClosing:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            location_id=location_id,
            opening_balance=round(opening_balance, 2),
            closing_balance=round(opening_balance, 2),
            counted_amount=0.0,
            variance=0.0,
            currency=currency,
            status=CashClosingStatus.OPEN.value,
            closed_by=closed_by,
        )

    def close(self, *, counted_amount: float, closing_balance: float) -> None:
        if self.status != CashClosingStatus.OPEN.value:
            raise ValueError("session_not_open")
        self.counted_amount = round(counted_amount, 2)
        self.closing_balance = round(closing_balance, 2)
        self.variance = round(counted_amount - closing_balance, 2)
        self.status = CashClosingStatus.CLOSED.value
        self.closed_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "location_id": self.location_id,
            "opening_balance": self.opening_balance,
            "closing_balance": self.closing_balance,
            "counted_amount": self.counted_amount,
            "variance": self.variance,
            "currency": self.currency,
            "status": self.status,
            "closed_by": self.closed_by,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class CashReconciliation(AggregateRoot):
    tenant_id: str
    location_id: str
    period_start: str
    period_end: str
    book_balance: float
    counted_balance: float
    variance: float
    currency: str
    status: str
    reconciled_by: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        location_id: str,
        period_start: str,
        period_end: str,
        book_balance: float,
        counted_balance: float,
        currency: str,
        reconciled_by: str | None = None,
    ) -> CashReconciliation:
        variance = round(counted_balance - book_balance, 2)
        status = "reconciled" if abs(variance) < 0.01 else "variance"
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            location_id=location_id,
            period_start=period_start,
            period_end=period_end,
            book_balance=round(book_balance, 2),
            counted_balance=round(counted_balance, 2),
            variance=variance,
            currency=currency,
            status=status,
            reconciled_by=reconciled_by,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "location_id": self.location_id,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "book_balance": self.book_balance,
            "counted_balance": self.counted_balance,
            "variance": self.variance,
            "currency": self.currency,
            "status": self.status,
            "reconciled_by": self.reconciled_by,
            "created_at": self.created_at.isoformat(),
        }
