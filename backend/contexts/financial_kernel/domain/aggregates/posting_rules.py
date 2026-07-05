"""Enterprise posting rule definitions — configurable, never hardcoded in modules."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class EnterprisePostingRuleType(StrEnum):
    PURCHASE = "purchase"
    SALES = "sales"
    PAYROLL = "payroll"
    INVENTORY = "inventory"
    HOSPITAL_BILLING = "hospital_billing"
    UNIVERSITY_TUITION = "university_tuition"
    CONSTRUCTION_COST = "construction_cost"
    BANK_DEPOSIT = "bank_deposit"
    BANK_WITHDRAWAL = "bank_withdrawal"
    INTEREST_ACCRUAL = "interest_accrual"
    TREASURY_TRANSFER = "treasury_transfer"
    TREASURY_INTERNAL_TRANSFER = "treasury_internal_transfer"
    TREASURY_BANK_TRANSFER = "treasury_bank_transfer"
    TREASURY_WIRE_TRANSFER = "treasury_wire_transfer"
    TREASURY_CASH_MOVEMENT = "treasury_cash_movement"
    TREASURY_FUND_ALLOCATION = "treasury_fund_allocation"
    TREASURY_SETTLEMENT = "treasury_settlement"
    TREASURY_INVESTMENT_PURCHASE = "treasury_investment_purchase"
    TREASURY_INVESTMENT_SALE = "treasury_investment_sale"
    TREASURY_DEBT_PAYMENT = "treasury_debt_payment"
    TREASURY_INTEREST_PAYMENT = "treasury_interest_payment"
    TREASURY_LOAN_DISBURSEMENT = "treasury_loan_disbursement"
    TREASURY_LOAN_REPAYMENT = "treasury_loan_repayment"
    EXCHANGE_TRANSACTION = "exchange_transaction"
    TAX = "tax"
    ASSET = "asset"
    LOAN = "loan"
    INSURANCE = "insurance"
    GENERAL_MANUAL = "general_manual"


class PostingPattern(StrEnum):
    DEBIT_CREDIT = "debit_credit"
    EXPLICIT_LINES = "explicit_lines"
    MULTI_AMOUNT = "multi_amount"


@dataclass(frozen=True, slots=True)
class LineTemplate:
    side: str  # debit | credit
    account_slot: str
    amount_field: str = "amount"
    description: str = ""


@dataclass(frozen=True, slots=True)
class AccountSlot:
    slot: str
    label: str
    account_key: str | None = None
    role: str | None = None
    required: bool = True


@dataclass(frozen=True, slots=True)
class PostingRuleDefinition:
    rule_id: str
    label: str
    module: str
    journal_type: str
    pattern: str = PostingPattern.DEBIT_CREDIT.value
    account_slots: tuple[AccountSlot, ...] = ()
    line_templates: tuple[LineTemplate, ...] = ()
    approval_required: bool = False
    tax_amount_field: str | None = None
    tax_account_slot: str | None = None
    dimensions: tuple[str, ...] = ()
    description: str = ""
    is_platform: bool = True


def _slot(
    slot: str,
    label: str,
    *,
    account_key: str | None = None,
    role: str | None = None,
    required: bool = True,
) -> AccountSlot:
    return AccountSlot(
        slot=slot,
        label=label,
        account_key=account_key,
        role=role,
        required=required,
    )


def _line(side: str, account_slot: str, amount_field: str = "amount") -> LineTemplate:
    return LineTemplate(side=side, account_slot=account_slot, amount_field=amount_field)


PLATFORM_POSTING_RULES: dict[str, PostingRuleDefinition] = {
    EnterprisePostingRuleType.PURCHASE.value: PostingRuleDefinition(
        rule_id="purchase",
        label="Purchase Posting",
        module="procurement",
        journal_type="purchase",
        account_slots=(
            _slot("debit", "Expense or inventory", account_key="clinical_staff", role="expense"),
            _slot("credit", "Accounts payable", account_key="accounts_payable", role="liability"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        dimensions=("cost_center", "project"),
        description="Debit expense/inventory, credit accounts payable",
    ),
    EnterprisePostingRuleType.SALES.value: PostingRuleDefinition(
        rule_id="sales",
        label="Sales Posting",
        module="sales",
        journal_type="sales",
        account_slots=(
            _slot("debit", "Accounts receivable", account_key="accounts_receivable", role="asset"),
            _slot("credit", "Revenue", account_key="patient_service_revenue", role="revenue"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        dimensions=("profit_center",),
        description="Debit AR, credit revenue",
    ),
    EnterprisePostingRuleType.PAYROLL.value: PostingRuleDefinition(
        rule_id="payroll",
        label="Payroll Posting",
        module="hr",
        journal_type="payroll",
        account_slots=(
            _slot("debit", "Payroll expense", account_key="clinical_staff", role="expense"),
            _slot("credit", "Payroll payable", account_key="payroll_payable", role="liability"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Debit payroll expense, credit payroll payable",
    ),
    EnterprisePostingRuleType.INVENTORY.value: PostingRuleDefinition(
        rule_id="inventory",
        label="Inventory Posting",
        module="inventory",
        journal_type="inventory",
        account_slots=(
            _slot("debit", "Inventory asset", account_key="inventory", role="asset"),
            _slot("credit", "Inventory offset", account_key="inventory_clearing", role="asset"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        dimensions=("warehouse", "project"),
        description="Inventory receipt or issue posting",
    ),
    EnterprisePostingRuleType.HOSPITAL_BILLING.value: PostingRuleDefinition(
        rule_id="hospital_billing",
        label="Hospital Billing Posting",
        module="hospital",
        journal_type="sales",
        account_slots=(
            _slot("debit", "Patient receivables", account_key="patient_receivables", role="asset"),
            _slot("credit", "Patient service revenue", account_key="patient_service_revenue", role="revenue"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        dimensions=("cost_center", "department"),
        description="Hospital encounter billing to GL",
    ),
    EnterprisePostingRuleType.UNIVERSITY_TUITION.value: PostingRuleDefinition(
        rule_id="university_tuition",
        label="University Tuition Posting",
        module="university",
        journal_type="sales",
        account_slots=(
            _slot("debit", "Student receivables", account_key="student_receivables", role="asset"),
            _slot("credit", "Tuition revenue", account_key="tuition_revenue", role="revenue"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        dimensions=("faculty", "program"),
        description="Tuition billing to GL",
    ),
    EnterprisePostingRuleType.CONSTRUCTION_COST.value: PostingRuleDefinition(
        rule_id="construction_cost",
        label="Construction Cost Posting",
        module="construction",
        journal_type="purchase",
        account_slots=(
            _slot("debit", "Construction WIP", account_key="construction_wip", role="asset"),
            _slot("credit", "Construction payable", account_key="construction_payable", role="liability"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        dimensions=("project", "site"),
        description="Capitalize construction costs to WIP",
    ),
    EnterprisePostingRuleType.BANK_DEPOSIT.value: PostingRuleDefinition(
        rule_id="bank_deposit",
        label="Bank Deposit Posting",
        module="treasury",
        journal_type="bank",
        account_slots=(
            _slot("debit", "Bank account", account_key="bank", role="asset"),
            _slot("credit", "Cash account", account_key="cash", role="asset"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Transfer cash to bank",
    ),
    EnterprisePostingRuleType.BANK_WITHDRAWAL.value: PostingRuleDefinition(
        rule_id="bank_withdrawal",
        label="Bank Withdrawal Posting",
        module="banking",
        journal_type="bank",
        account_slots=(
            _slot("debit", "Cash account", account_key="cash", role="asset"),
            _slot("credit", "Customer deposits", account_key="customer_deposits", role="liability"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=False,
        description="Customer withdrawal from deposit account",
    ),
    EnterprisePostingRuleType.INTEREST_ACCRUAL.value: PostingRuleDefinition(
        rule_id="interest_accrual",
        label="Interest Accrual Posting",
        module="banking",
        journal_type="general",
        account_slots=(
            _slot("debit", "Interest expense", account_key="interest_expense", role="expense"),
            _slot("credit", "Interest income", account_key="interest_income", role="revenue"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=False,
        description="Deposit interest accrual",
    ),
    EnterprisePostingRuleType.TREASURY_TRANSFER.value: PostingRuleDefinition(
        rule_id="treasury_transfer",
        label="Treasury Transfer Posting",
        module="treasury",
        journal_type="cash",
        account_slots=(
            _slot("debit", "Destination account", account_key="cash", role="asset"),
            _slot("credit", "Source account", account_key="cash", role="asset"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=False,
        description="Inter-account treasury transfer",
    ),
    EnterprisePostingRuleType.TREASURY_INTERNAL_TRANSFER.value: PostingRuleDefinition(
        rule_id="treasury_internal_transfer",
        label="Internal Transfer Posting",
        module="treasury",
        journal_type="cash",
        account_slots=(
            _slot("debit", "Destination account", account_key="cash", role="asset"),
            _slot("credit", "Source account", account_key="cash", role="asset"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=False,
        description="Internal treasury account transfer",
    ),
    EnterprisePostingRuleType.TREASURY_BANK_TRANSFER.value: PostingRuleDefinition(
        rule_id="treasury_bank_transfer",
        label="Bank Transfer Posting",
        module="treasury",
        journal_type="bank",
        account_slots=(
            _slot("debit", "Destination bank", account_key="bank", role="asset"),
            _slot("credit", "Source bank", account_key="bank", role="asset"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Inter-bank treasury transfer",
    ),
    EnterprisePostingRuleType.TREASURY_WIRE_TRANSFER.value: PostingRuleDefinition(
        rule_id="treasury_wire_transfer",
        label="Wire Transfer Posting",
        module="treasury",
        journal_type="bank",
        account_slots=(
            _slot("debit", "Beneficiary bank", account_key="bank", role="asset"),
            _slot("credit", "Originating bank", account_key="bank", role="asset"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Wire transfer settlement",
    ),
    EnterprisePostingRuleType.TREASURY_CASH_MOVEMENT.value: PostingRuleDefinition(
        rule_id="treasury_cash_movement",
        label="Cash Movement Posting",
        module="treasury",
        journal_type="cash",
        account_slots=(
            _slot("debit", "Destination cash", account_key="cash", role="asset"),
            _slot("credit", "Source cash", account_key="cash", role="asset"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=False,
        description="Cash movement between locations",
    ),
    EnterprisePostingRuleType.TREASURY_FUND_ALLOCATION.value: PostingRuleDefinition(
        rule_id="treasury_fund_allocation",
        label="Fund Allocation Posting",
        module="treasury",
        journal_type="cash",
        account_slots=(
            _slot("debit", "Target pool", account_key="treasury_cash", role="asset"),
            _slot("credit", "Source pool", account_key="treasury_cash", role="asset"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Allocate funds between treasury pools",
    ),
    EnterprisePostingRuleType.TREASURY_SETTLEMENT.value: PostingRuleDefinition(
        rule_id="treasury_settlement",
        label="Treasury Settlement Posting",
        module="treasury",
        journal_type="cash",
        account_slots=(
            _slot("debit", "Settlement account", account_key="bank", role="asset"),
            _slot("credit", "Counterparty account", account_key="cash", role="asset"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Treasury settlement posting",
    ),
    EnterprisePostingRuleType.TREASURY_INVESTMENT_PURCHASE.value: PostingRuleDefinition(
        rule_id="treasury_investment_purchase",
        label="Investment Purchase Posting",
        module="treasury",
        journal_type="general",
        account_slots=(
            _slot("debit", "Investment asset", account_key="investments", role="asset"),
            _slot("credit", "Funding account", account_key="bank", role="asset"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Purchase treasury investment instrument",
    ),
    EnterprisePostingRuleType.TREASURY_INVESTMENT_SALE.value: PostingRuleDefinition(
        rule_id="treasury_investment_sale",
        label="Investment Sale Posting",
        module="treasury",
        journal_type="general",
        account_slots=(
            _slot("debit", "Proceeds account", account_key="bank", role="asset"),
            _slot("credit", "Investment asset", account_key="investments", role="asset"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Sell treasury investment instrument",
    ),
    EnterprisePostingRuleType.TREASURY_DEBT_PAYMENT.value: PostingRuleDefinition(
        rule_id="treasury_debt_payment",
        label="Debt Payment Posting",
        module="treasury",
        journal_type="general",
        account_slots=(
            _slot("debit", "Debt payable", account_key="loan_payable", role="liability"),
            _slot("credit", "Payment account", account_key="bank", role="asset"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Principal debt repayment",
    ),
    EnterprisePostingRuleType.TREASURY_INTEREST_PAYMENT.value: PostingRuleDefinition(
        rule_id="treasury_interest_payment",
        label="Interest Payment Posting",
        module="treasury",
        journal_type="general",
        account_slots=(
            _slot("debit", "Interest expense", account_key="interest_expense", role="expense"),
            _slot("credit", "Payment account", account_key="bank", role="asset"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Interest payment on borrowing",
    ),
    EnterprisePostingRuleType.TREASURY_LOAN_DISBURSEMENT.value: PostingRuleDefinition(
        rule_id="treasury_loan_disbursement",
        label="Loan Disbursement Posting",
        module="treasury",
        journal_type="general",
        account_slots=(
            _slot("debit", "Disbursement account", account_key="bank", role="asset"),
            _slot("credit", "Loan payable", account_key="loan_payable", role="liability"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Loan proceeds disbursement",
    ),
    EnterprisePostingRuleType.TREASURY_LOAN_REPAYMENT.value: PostingRuleDefinition(
        rule_id="treasury_loan_repayment",
        label="Loan Repayment Posting",
        module="treasury",
        journal_type="general",
        account_slots=(
            _slot("debit", "Loan payable", account_key="loan_payable", role="liability"),
            _slot("credit", "Payment account", account_key="bank", role="asset"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Loan principal repayment",
    ),
    EnterprisePostingRuleType.EXCHANGE_TRANSACTION.value: PostingRuleDefinition(
        rule_id="exchange_transaction",
        label="Exchange Transaction Posting",
        module="treasury",
        journal_type="foreign_currency",
        account_slots=(
            _slot("debit", "FX asset", account_key="fx_asset", role="asset"),
            _slot("credit", "FX liability", account_key="fx_liability", role="liability"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Foreign exchange transaction posting",
    ),
    EnterprisePostingRuleType.TAX.value: PostingRuleDefinition(
        rule_id="tax",
        label="Tax Posting",
        module="tax",
        journal_type="tax",
        account_slots=(
            _slot("debit", "Tax expense", account_key="tax_expense", role="expense"),
            _slot("credit", "Tax payable", account_key="tax_payable", role="liability"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        tax_amount_field="tax_amount",
        tax_account_slot="credit",
        description="Tax accrual posting",
    ),
    EnterprisePostingRuleType.ASSET.value: PostingRuleDefinition(
        rule_id="asset",
        label="Asset Posting",
        module="fixed_assets",
        journal_type="general",
        account_slots=(
            _slot("debit", "Fixed asset", account_key="fixed_assets", role="asset"),
            _slot("credit", "Asset payable", account_key="accounts_payable", role="liability"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Capital asset acquisition",
    ),
    EnterprisePostingRuleType.LOAN.value: PostingRuleDefinition(
        rule_id="loan",
        label="Loan Posting",
        module="treasury",
        journal_type="general",
        account_slots=(
            _slot("debit", "Cash received", account_key="cash", role="asset"),
            _slot("credit", "Loan payable", account_key="loan_payable", role="liability"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Loan proceeds receipt",
    ),
    EnterprisePostingRuleType.INSURANCE.value: PostingRuleDefinition(
        rule_id="insurance",
        label="Insurance Posting",
        module="insurance",
        journal_type="general",
        account_slots=(
            _slot("debit", "Insurance expense", account_key="insurance_expense", role="expense"),
            _slot("credit", "Insurance payable", account_key="insurance_payable", role="liability"),
        ),
        line_templates=(_line("debit", "debit"), _line("credit", "credit")),
        approval_required=True,
        description="Insurance premium accrual",
    ),
    EnterprisePostingRuleType.GENERAL_MANUAL.value: PostingRuleDefinition(
        rule_id="general_manual",
        label="General Manual Posting",
        module="financial_kernel",
        journal_type="general",
        pattern=PostingPattern.EXPLICIT_LINES.value,
        account_slots=(),
        line_templates=(),
        description="Explicit journal lines — kernel internal / legacy only",
    ),
}


@dataclass(eq=False, kw_only=True)
class ConfigurablePostingRule(AggregateRoot):
    """Tenant-built posting rule from Rule Builder."""

    tenant_id: str
    rule_id: str
    label: str
    module: str
    journal_type: str
    pattern: str
    account_slots: dict
    line_templates: list[dict]
    approval_required: bool = False
    tax_amount_field: str | None = None
    tax_account_slot: str | None = None
    dimensions: list[str] = field(default_factory=list)
    description: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        rule_id: str,
        label: str,
        module: str,
        journal_type: str,
        pattern: str,
        account_slots: dict,
        line_templates: list[dict],
        approval_required: bool = False,
        tax_amount_field: str | None = None,
        tax_account_slot: str | None = None,
        dimensions: list[str] | None = None,
        description: str = "",
    ) -> ConfigurablePostingRule:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            rule_id=rule_id,
            label=label,
            module=module,
            journal_type=journal_type,
            pattern=pattern,
            account_slots=account_slots,
            line_templates=line_templates,
            approval_required=approval_required,
            tax_amount_field=tax_amount_field,
            tax_account_slot=tax_account_slot,
            dimensions=dimensions or [],
            description=description,
        )

    def update(
        self,
        *,
        label: str | None = None,
        account_slots: dict | None = None,
        line_templates: list[dict] | None = None,
        approval_required: bool | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ) -> None:
        if label is not None:
            self.label = label
        if account_slots is not None:
            self.account_slots = account_slots
        if line_templates is not None:
            self.line_templates = line_templates
        if approval_required is not None:
            self.approval_required = approval_required
        if description is not None:
            self.description = description
        if is_active is not None:
            self.is_active = is_active
        self.updated_at = datetime.now(UTC)

    def to_definition(self) -> PostingRuleDefinition:
        slots = tuple(
            AccountSlot(
                slot=name,
                label=meta.get("label", name),
                account_key=meta.get("account_key"),
                role=meta.get("role"),
                required=meta.get("required", True),
            )
            for name, meta in self.account_slots.items()
        )
        templates = tuple(
            LineTemplate(
                side=t["side"],
                account_slot=t["account_slot"],
                amount_field=t.get("amount_field", "amount"),
                description=t.get("description", ""),
            )
            for t in self.line_templates
        )
        return PostingRuleDefinition(
            rule_id=self.rule_id,
            label=self.label,
            module=self.module,
            journal_type=self.journal_type,
            pattern=self.pattern,
            account_slots=slots,
            line_templates=templates,
            approval_required=self.approval_required,
            tax_amount_field=self.tax_amount_field,
            tax_account_slot=self.tax_account_slot,
            dimensions=tuple(self.dimensions),
            description=self.description,
            is_platform=False,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "rule_id": self.rule_id,
            "label": self.label,
            "module": self.module,
            "journal_type": self.journal_type,
            "pattern": self.pattern,
            "account_slots": self.account_slots,
            "line_templates": self.line_templates,
            "approval_required": self.approval_required,
            "tax_amount_field": self.tax_amount_field,
            "tax_account_slot": self.tax_account_slot,
            "dimensions": self.dimensions,
            "description": self.description,
            "is_active": self.is_active,
            "is_platform": False,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
