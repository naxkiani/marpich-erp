"""Financial document aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class FinancialDocumentType(StrEnum):
    INVOICE = "invoice"
    BILL = "bill"
    VOUCHER = "voucher"
    RECEIPT = "receipt"
    PAYMENT_ORDER = "payment_order"
    PURCHASE_INVOICE = "purchase_invoice"
    SALES_INVOICE = "sales_invoice"
    CREDIT_NOTE = "credit_note"
    DEBIT_NOTE = "debit_note"
    JOURNAL_VOUCHER = "journal_voucher"
    CASH_VOUCHER = "cash_voucher"
    BANK_VOUCHER = "bank_voucher"


class FinancialDocumentStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SIGNED = "signed"
    ISSUED = "issued"
    VOIDED = "voided"


@dataclass(eq=False, kw_only=True)
class FinancialDocumentVersion(AggregateRoot):
    tenant_id: str
    document_id: UniqueId
    version_number: int
    content_snapshot: dict
    checksum: str
    pdf_base64: str
    created_by: str | None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        document_id: UniqueId,
        version_number: int,
        content_snapshot: dict,
        checksum: str,
        pdf_base64: str,
        created_by: str | None = None,
    ) -> FinancialDocumentVersion:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            document_id=document_id,
            version_number=version_number,
            content_snapshot=content_snapshot,
            checksum=checksum,
            pdf_base64=pdf_base64,
            created_by=created_by,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "document_id": str(self.document_id),
            "version_number": self.version_number,
            "content_snapshot": self.content_snapshot,
            "checksum": self.checksum,
            "pdf_base64": self.pdf_base64,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class FinancialDocument(AggregateRoot):
    tenant_id: str
    source_context: str
    source_document_id: str
    idempotency_key: str
    document_type: str
    document_number: str
    status: FinancialDocumentStatus
    currency: str
    total_amount: float
    counterparty_name: str
    counterparty_id: str | None
    reference: str
    lines: list[dict]
    metadata: dict
    current_version_id: UniqueId | None
    qr_token: str | None
    signature: dict | None
    approval_workflow_id: str | None
    issued_at: datetime | None
    created_by: str | None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        source_context: str,
        source_document_id: str,
        idempotency_key: str,
        document_type: str,
        document_number: str,
        currency: str,
        total_amount: float,
        counterparty_name: str,
        reference: str,
        lines: list[dict] | None = None,
        metadata: dict | None = None,
        counterparty_id: str | None = None,
        created_by: str | None = None,
    ) -> FinancialDocument:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=idempotency_key,
            document_type=document_type,
            document_number=document_number,
            status=FinancialDocumentStatus.DRAFT,
            currency=currency.strip().upper(),
            total_amount=round(total_amount, 2),
            counterparty_name=counterparty_name.strip(),
            counterparty_id=counterparty_id,
            reference=reference.strip(),
            lines=list(lines or []),
            metadata=dict(metadata or {}),
            current_version_id=None,
            qr_token=None,
            signature=None,
            approval_workflow_id=None,
            issued_at=None,
            created_by=created_by,
        )

    def set_current_version(self, version_id: UniqueId) -> None:
        self.current_version_id = version_id

    def set_qr_token(self, token: str) -> None:
        self.qr_token = token

    def request_approval(self, workflow_id: str) -> None:
        if self.status not in (FinancialDocumentStatus.DRAFT, FinancialDocumentStatus.PENDING_APPROVAL):
            raise ValueError("invalid_status_for_approval")
        self.status = FinancialDocumentStatus.PENDING_APPROVAL
        self.approval_workflow_id = workflow_id

    def approve(self) -> None:
        if self.status != FinancialDocumentStatus.PENDING_APPROVAL:
            raise ValueError("not_pending_approval")
        self.status = FinancialDocumentStatus.APPROVED

    def sign(self, signature: dict) -> None:
        if self.status not in (FinancialDocumentStatus.APPROVED, FinancialDocumentStatus.DRAFT):
            raise ValueError("invalid_status_for_signature")
        self.signature = signature
        self.status = FinancialDocumentStatus.SIGNED

    def issue(self, *, allow_draft: bool = False) -> None:
        allowed = {FinancialDocumentStatus.SIGNED, FinancialDocumentStatus.APPROVED}
        if allow_draft:
            allowed.add(FinancialDocumentStatus.DRAFT)
        if self.status not in allowed:
            raise ValueError("not_ready_to_issue")
        self.status = FinancialDocumentStatus.ISSUED
        self.issued_at = datetime.now(UTC)

    def void(self) -> None:
        if self.status == FinancialDocumentStatus.VOIDED:
            raise ValueError("already_voided")
        self.status = FinancialDocumentStatus.VOIDED

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "source_context": self.source_context,
            "source_document_id": self.source_document_id,
            "idempotency_key": self.idempotency_key,
            "document_type": self.document_type,
            "document_number": self.document_number,
            "status": self.status.value,
            "currency": self.currency,
            "total_amount": self.total_amount,
            "counterparty_name": self.counterparty_name,
            "counterparty_id": self.counterparty_id,
            "reference": self.reference,
            "lines": self.lines,
            "metadata": self.metadata,
            "current_version_id": str(self.current_version_id) if self.current_version_id else None,
            "qr_token": self.qr_token,
            "signature": self.signature,
            "approval_workflow_id": self.approval_workflow_id,
            "issued_at": self.issued_at.isoformat() if self.issued_at else None,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
        }
