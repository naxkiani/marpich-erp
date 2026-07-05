"""Financial Kernel integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class CoaSeededIntegration(IntegrationEvent):
    industry_pack: str
    account_count: int

    @property
    def event_name(self) -> str:
        return "financial_kernel.coa.seeded"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"industry_pack": self.industry_pack, "account_count": self.account_count}


@dataclass(frozen=True, kw_only=True)
class JournalPostedIntegration(IntegrationEvent):
    journal_id: str
    posting_source_context: str
    source_document_id: str
    total_debit: float
    total_credit: float
    posting_mode: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.journal.posted"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "journal_id": self.journal_id,
            "source_context": self.posting_source_context,
            "source_document_id": self.source_document_id,
            "total_debit": self.total_debit,
            "total_credit": self.total_credit,
            "posting_mode": self.posting_mode,
        }


@dataclass(frozen=True, kw_only=True)
class JournalReversedIntegration(IntegrationEvent):
    original_journal_id: str
    reversal_journal_id: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.journal.reversed"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "original_journal_id": self.original_journal_id,
            "reversal_journal_id": self.reversal_journal_id,
        }


@dataclass(frozen=True, kw_only=True)
class JournalApprovalRequestedIntegration(IntegrationEvent):
    journal_id: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.journal.approval.requested"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"journal_id": self.journal_id}


@dataclass(frozen=True, kw_only=True)
class JournalApprovedIntegration(IntegrationEvent):
    journal_id: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.journal.approved"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"journal_id": self.journal_id}


@dataclass(frozen=True, kw_only=True)
class RecurringExecutedIntegration(IntegrationEvent):
    template_id: str
    journal_id: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.recurring.executed"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"template_id": self.template_id, "journal_id": self.journal_id}


@dataclass(frozen=True, kw_only=True)
class BudgetExceededIntegration(IntegrationEvent):
    account_code: str
    cost_center: str | None
    requested_amount: float
    remaining: float

    @property
    def event_name(self) -> str:
        return "financial_kernel.budget.exceeded"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "account_code": self.account_code,
            "cost_center": self.cost_center,
            "requested_amount": self.requested_amount,
            "remaining": self.remaining,
        }


@dataclass(frozen=True, kw_only=True)
class ExchangeRatesUpdatedIntegration(IntegrationEvent):
    source: str
    rate_count: int

    @property
    def event_name(self) -> str:
        return "financial_kernel.currency.rates.updated"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"source": self.source, "rate_count": self.rate_count}


@dataclass(frozen=True, kw_only=True)
class CurrencyRevaluationCompletedIntegration(IntegrationEvent):
    revaluation_id: str
    net_gain_loss: float

    @property
    def event_name(self) -> str:
        return "financial_kernel.currency.revaluation.completed"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "revaluation_id": self.revaluation_id,
            "net_gain_loss": self.net_gain_loss,
        }


@dataclass(frozen=True, kw_only=True)
class PaymentSettledIntegration(IntegrationEvent):
    payment_id: str
    amount: float
    currency: str
    payment_method: str
    payment_source_context: str
    source_document_id: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.payment.settled"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "payment_id": self.payment_id,
            "amount": self.amount,
            "currency": self.currency,
            "payment_method": self.payment_method,
            "source_context": self.payment_source_context,
            "source_document_id": self.source_document_id,
        }


@dataclass(frozen=True, kw_only=True)
class PaymentAllocatedIntegration(IntegrationEvent):
    payment_id: str
    allocation_count: int
    allocated_amount: float

    @property
    def event_name(self) -> str:
        return "financial_kernel.payment.allocated"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "payment_id": self.payment_id,
            "allocation_count": self.allocation_count,
            "allocated_amount": self.allocated_amount,
        }


@dataclass(frozen=True, kw_only=True)
class PaymentRefundedIntegration(IntegrationEvent):
    payment_id: str
    refund_amount: float
    remaining_paid: float

    @property
    def event_name(self) -> str:
        return "financial_kernel.payment.refunded"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "payment_id": self.payment_id,
            "refund_amount": self.refund_amount,
            "remaining_paid": self.remaining_paid,
        }


@dataclass(frozen=True, kw_only=True)
class PaymentChargebackIntegration(IntegrationEvent):
    payment_id: str
    chargeback_amount: float

    @property
    def event_name(self) -> str:
        return "financial_kernel.payment.chargeback"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "payment_id": self.payment_id,
            "chargeback_amount": self.chargeback_amount,
        }


@dataclass(frozen=True, kw_only=True)
class PaymentReconciledIntegration(IntegrationEvent):
    reconciliation_id: str
    status: str
    matched_amount: float
    variance: float

    @property
    def event_name(self) -> str:
        return "financial_kernel.payment.reconciled"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "reconciliation_id": self.reconciliation_id,
            "status": self.status,
            "matched_amount": self.matched_amount,
            "variance": self.variance,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialDocumentCreatedIntegration(IntegrationEvent):
    document_id: str
    document_type: str
    document_number: str
    total_amount: float
    fin_doc_source_context: str
    source_document_id: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.document.created"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "document_id": self.document_id,
            "document_type": self.document_type,
            "document_number": self.document_number,
            "total_amount": self.total_amount,
            "source_context": self.fin_doc_source_context,
            "source_document_id": self.source_document_id,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialDocumentVersionCreatedIntegration(IntegrationEvent):
    document_id: str
    version_id: str
    version_number: int
    checksum: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.document.version.created"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "document_id": self.document_id,
            "version_id": self.version_id,
            "version_number": self.version_number,
            "checksum": self.checksum,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialDocumentApprovalRequestedIntegration(IntegrationEvent):
    document_id: str
    document_type: str
    workflow_id: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.document.approval.requested"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "document_id": self.document_id,
            "document_type": self.document_type,
            "workflow_id": self.workflow_id,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialDocumentApprovedIntegration(IntegrationEvent):
    document_id: str
    document_type: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.document.approved"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"document_id": self.document_id, "document_type": self.document_type}


@dataclass(frozen=True, kw_only=True)
class FinancialDocumentSignedIntegration(IntegrationEvent):
    document_id: str
    signer_id: str
    version_checksum: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.document.signed"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "document_id": self.document_id,
            "signer_id": self.signer_id,
            "version_checksum": self.version_checksum,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialDocumentIssuedIntegration(IntegrationEvent):
    document_id: str
    document_type: str
    document_number: str
    total_amount: float

    @property
    def event_name(self) -> str:
        return "financial_kernel.document.issued"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "document_id": self.document_id,
            "document_type": self.document_type,
            "document_number": self.document_number,
            "total_amount": self.total_amount,
        }


@dataclass(frozen=True, kw_only=True)
class CostCenterCreatedIntegration(IntegrationEvent):
    cost_center_id: str
    code: str
    center_type: str
    name: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.cost_center.created"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "cost_center_id": self.cost_center_id,
            "code": self.code,
            "center_type": self.center_type,
            "name": self.name,
        }


@dataclass(frozen=True, kw_only=True)
class ProfitCenterCreatedIntegration(IntegrationEvent):
    profit_center_id: str
    code: str
    name: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.profit_center.created"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "profit_center_id": self.profit_center_id,
            "code": self.code,
            "name": self.name,
        }


@dataclass(frozen=True, kw_only=True)
class CenterAllocationCreatedIntegration(IntegrationEvent):
    allocation_id: str
    allocation_type: str
    cost_center_code: str
    amount: float

    @property
    def event_name(self) -> str:
        return "financial_kernel.allocation.created"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "allocation_id": self.allocation_id,
            "allocation_type": self.allocation_type,
            "cost_center_code": self.cost_center_code,
            "amount": self.amount,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialWorkflowStartedIntegration(IntegrationEvent):
    workflow_id: str
    workflow_type: str
    fin_wf_source_context: str
    source_document_id: str
    assignee_id: str
    sla_hours: int

    @property
    def event_name(self) -> str:
        return "financial_kernel.workflow.started"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "workflow_id": self.workflow_id,
            "workflow_type": self.workflow_type,
            "source_context": self.fin_wf_source_context,
            "source_document_id": self.source_document_id,
            "assignee_id": self.assignee_id,
            "sla_hours": self.sla_hours,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialWorkflowApprovedIntegration(IntegrationEvent):
    workflow_id: str
    workflow_type: str
    approved_by: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.workflow.approved"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "workflow_id": self.workflow_id,
            "workflow_type": self.workflow_type,
            "approved_by": self.approved_by,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialWorkflowRejectedIntegration(IntegrationEvent):
    workflow_id: str
    workflow_type: str
    rejected_by: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.workflow.rejected"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "workflow_id": self.workflow_id,
            "workflow_type": self.workflow_type,
            "rejected_by": self.rejected_by,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialWorkflowEscalatedIntegration(IntegrationEvent):
    workflow_id: str
    workflow_type: str
    escalated_to: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.workflow.escalated"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "workflow_id": self.workflow_id,
            "workflow_type": self.workflow_type,
            "escalated_to": self.escalated_to,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialWorkflowSignedIntegration(IntegrationEvent):
    workflow_id: str
    workflow_type: str
    signer_id: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.workflow.signed"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "workflow_id": self.workflow_id,
            "workflow_type": self.workflow_type,
            "signer_id": self.signer_id,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialSecurityMakerCheckerSubmittedIntegration(IntegrationEvent):
    request_id: str
    control_type: str
    maker_id: str
    resource_type: str
    resource_id: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.security.maker_checker.submitted"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "request_id": self.request_id,
            "control_type": self.control_type,
            "maker_id": self.maker_id,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialSecurityMakerCheckerApprovedIntegration(IntegrationEvent):
    request_id: str
    control_type: str
    approved_by: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.security.maker_checker.approved"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "request_id": self.request_id,
            "control_type": self.control_type,
            "approved_by": self.approved_by,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialSecurityTransactionLockedIntegration(IntegrationEvent):
    lock_id: str
    resource_type: str
    resource_id: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.security.transaction.locked"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "lock_id": self.lock_id,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialSecurityPeriodClosedIntegration(IntegrationEvent):
    close_type: str
    target_id: str
    closed_by: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.security.period.closed"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "close_type": self.close_type,
            "target_id": self.target_id,
            "closed_by": self.closed_by,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialSecurityAuditRecordedIntegration(IntegrationEvent):
    audit_id: str
    action: str
    resource_type: str
    resource_id: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.security.audit.recorded"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "audit_id": self.audit_id,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialSecurityTamperDetectedIntegration(IntegrationEvent):
    audit_id: str
    resource_id: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.security.tamper.detected"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"audit_id": self.audit_id, "resource_id": self.resource_id}


@dataclass(frozen=True, kw_only=True)
class FinancialAIAnalysisCompletedIntegration(IntegrationEvent):
    job_id: str
    capability: str
    confidence: float

    @property
    def event_name(self) -> str:
        return "financial_kernel.ai.analysis.completed"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "job_id": self.job_id,
            "capability": self.capability,
            "confidence": self.confidence,
        }


@dataclass(frozen=True, kw_only=True)
class FinancialAIDashboardGeneratedIntegration(IntegrationEvent):
    job_id: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.ai.dashboard.generated"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"job_id": self.job_id}


@dataclass(frozen=True, kw_only=True)
class FinancialAIChatCompletedIntegration(IntegrationEvent):
    session_id: str
    session_type: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.ai.chat.completed"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"session_id": self.session_id, "session_type": self.session_type}


@dataclass(frozen=True, kw_only=True)
class GLAIAnalysisCompletedIntegration(IntegrationEvent):
    job_id: str
    capability: str
    confidence: float

    @property
    def event_name(self) -> str:
        return "financial_kernel.gl_ai.analysis.completed"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "job_id": self.job_id,
            "capability": self.capability,
            "confidence": self.confidence,
        }


@dataclass(frozen=True, kw_only=True)
class GLAICFODashboardGeneratedIntegration(IntegrationEvent):
    job_id: str

    @property
    def event_name(self) -> str:
        return "financial_kernel.gl_ai.cfo_dashboard.generated"

    @property
    def source_context(self) -> str:
        return "financial_kernel"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"job_id": self.job_id}
