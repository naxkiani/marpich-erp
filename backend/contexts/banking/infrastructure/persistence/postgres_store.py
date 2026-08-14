"""PostgreSQL repositories — Banking money-path (customer / product / account / transfer)."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import select

from contexts.banking.domain.aggregates.customer_account_engine import (
    BankingAccount,
    BankingAccountProduct,
    BankingCustomer,
)
from contexts.banking.domain.aggregates.payment_platform_engine import (
    PaymentTransfer,
    TransferStatus,
)
from contexts.banking.domain.ports.customer_account_repositories import (
    IAccountProductRepository,
    IAccountRepository,
    ICustomerRepository,
)
from contexts.banking.domain.ports.payment_platform_repositories import IPaymentTransferRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    BankingAccountProductRow,
    BankingAccountRow,
    BankingCustomerRow,
    BankingPaymentTransferRow,
)


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _customer_from_doc(doc: dict) -> BankingCustomer:
    return BankingCustomer(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        customer_type=str(doc.get("customer_type") or "individual"),
        display_name=str(doc.get("display_name") or ""),
        legal_name=str(doc.get("legal_name") or ""),
        email=str(doc.get("email") or ""),
        phone=str(doc.get("phone") or ""),
        organization_id=doc.get("organization_id"),
        branch_id=doc.get("branch_id"),
        kyc_status=str(doc.get("kyc_status") or "pending"),
        risk_rating=str(doc.get("risk_rating") or "low"),
        approval_status=str(doc.get("approval_status") or "draft"),
        registration_number=doc.get("registration_number"),
        tax_id=doc.get("tax_id"),
        is_active=bool(doc.get("is_active", True)),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
        updated_at=_parse_dt(doc.get("updated_at")) or datetime.now(UTC),
    )


def _product_from_doc(doc: dict) -> BankingAccountProduct:
    return BankingAccountProduct(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        product_code=str(doc["product_code"]),
        name=str(doc.get("name") or ""),
        account_type=str(doc.get("account_type") or "checking"),
        currency=str(doc.get("currency") or "USD"),
        interest_rate_annual=float(doc.get("interest_rate_annual") or 0.0),
        minimum_balance=float(doc.get("minimum_balance") or 0.0),
        overdraft_limit=float(doc.get("overdraft_limit") or 0.0),
        overdraft_enabled=bool(doc.get("overdraft_enabled") or False),
        is_active=bool(doc.get("is_active", True)),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _account_from_doc(doc: dict) -> BankingAccount:
    return BankingAccount(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        customer_id=str(doc["customer_id"]),
        account_number=str(doc["account_number"]),
        account_type=str(doc.get("account_type") or "checking"),
        product_code=str(doc.get("product_code") or ""),
        currency=str(doc.get("currency") or "USD"),
        status=str(doc.get("status") or "pending"),
        balance=float(doc.get("balance") or 0.0),
        available_balance=float(doc.get("available_balance") or 0.0),
        organization_id=doc.get("organization_id"),
        branch_id=doc.get("branch_id"),
        is_joint=bool(doc.get("is_joint") or False),
        joint_holders=list(doc.get("joint_holders") or []),
        interest_rate_annual=float(doc.get("interest_rate_annual") or 0.0),
        minimum_balance=float(doc.get("minimum_balance") or 0.0),
        overdraft_limit=float(doc.get("overdraft_limit") or 0.0),
        overdraft_enabled=bool(doc.get("overdraft_enabled") or False),
        approval_status=str(doc.get("approval_status") or "draft"),
        gl_account_code=doc.get("gl_account_code"),
        kernel_account_key=doc.get("kernel_account_key"),
        kernel_linked=bool(doc.get("kernel_linked") or False),
        kernel_journal_id=doc.get("kernel_journal_id"),
        kernel_subledger_ref=doc.get("kernel_subledger_ref"),
        parent_account_id=doc.get("parent_account_id"),
        opened_at=_parse_dt(doc.get("opened_at")),
        closed_at=_parse_dt(doc.get("closed_at")),
        last_activity_at=_parse_dt(doc.get("last_activity_at")),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
        updated_at=_parse_dt(doc.get("updated_at")) or datetime.now(UTC),
    )


def _transfer_from_doc(doc: dict) -> PaymentTransfer:
    return PaymentTransfer(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        transfer_ref=str(doc["transfer_ref"]),
        transfer_type=str(doc.get("transfer_type") or "internal"),
        status=str(doc.get("status") or "draft"),
        source_account_id=str(doc["source_account_id"]),
        destination_account_id=doc.get("destination_account_id"),
        beneficiary_id=doc.get("beneficiary_id"),
        customer_id=str(doc["customer_id"]),
        amount=float(doc.get("amount") or 0.0),
        currency=str(doc.get("currency") or "USD"),
        channel=str(doc.get("channel") or "digital"),
        branch_id=str(doc.get("branch_id") or ""),
        destination_branch_id=str(doc.get("destination_branch_id") or ""),
        batch_id=doc.get("batch_id"),
        standing_order_id=doc.get("standing_order_id"),
        scheduled_at=_parse_dt(doc.get("scheduled_at")),
        qr_payload=str(doc.get("qr_payload") or ""),
        merchant_ref=str(doc.get("merchant_ref") or ""),
        bill_ref=str(doc.get("bill_ref") or ""),
        government_ref=str(doc.get("government_ref") or ""),
        salary_ref=str(doc.get("salary_ref") or ""),
        narrative=str(doc.get("narrative") or ""),
        fraud_status=str(doc.get("fraud_status") or "clear"),
        fraud_score=float(doc.get("fraud_score") or 0.0),
        journal_id=doc.get("journal_id"),
        executed_at=_parse_dt(doc.get("executed_at")),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
        updated_at=_parse_dt(doc.get("updated_at")) or datetime.now(UTC),
    )


class PostgresCustomerRepository(ICustomerRepository):
    async def save(self, customer: BankingCustomer) -> None:
        doc = customer.to_dict()
        async with session_scope() as session:
            row = await session.get(BankingCustomerRow, UUID(str(customer.id)))
            if row is None:
                session.add(
                    BankingCustomerRow(
                        id=UUID(str(customer.id)),
                        tenant_id=customer.tenant_id,
                        email=customer.email,
                        document=doc,
                        updated_at=customer.updated_at,
                    )
                )
            else:
                row.email = customer.email
                row.document = doc
                row.updated_at = customer.updated_at

    async def find_by_id(self, customer_id: str) -> BankingCustomer | None:
        async with session_scope() as session:
            row = await session.get(BankingCustomerRow, UUID(customer_id))
            return _customer_from_doc(row.document) if row else None

    async def find_by_email(self, tenant_id: str, email: str) -> BankingCustomer | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(BankingCustomerRow).where(
                    BankingCustomerRow.tenant_id == tenant_id,
                    BankingCustomerRow.email == email.lower(),
                )
            )
            return _customer_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[BankingCustomer]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingCustomerRow).where(BankingCustomerRow.tenant_id == tenant_id)
                )
            ).all()
        return [_customer_from_doc(r.document) for r in rows]


class PostgresAccountProductRepository(IAccountProductRepository):
    async def save(self, product: BankingAccountProduct) -> None:
        doc = product.to_dict()
        async with session_scope() as session:
            row = await session.get(BankingAccountProductRow, UUID(str(product.id)))
            if row is None:
                session.add(
                    BankingAccountProductRow(
                        id=UUID(str(product.id)),
                        tenant_id=product.tenant_id,
                        product_code=product.product_code,
                        document=doc,
                    )
                )
            else:
                row.product_code = product.product_code
                row.document = doc

    async def find_by_code(self, tenant_id: str, product_code: str) -> BankingAccountProduct | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(BankingAccountProductRow).where(
                    BankingAccountProductRow.tenant_id == tenant_id,
                    BankingAccountProductRow.product_code == product_code.upper(),
                )
            )
            return _product_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[BankingAccountProduct]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingAccountProductRow).where(
                        BankingAccountProductRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_product_from_doc(r.document) for r in rows]


class PostgresAccountRepository(IAccountRepository):
    _counter: dict[str, int] = {}

    async def save(self, account: BankingAccount) -> None:
        doc = account.to_dict()
        async with session_scope() as session:
            row = await session.get(BankingAccountRow, UUID(str(account.id)))
            if row is None:
                session.add(
                    BankingAccountRow(
                        id=UUID(str(account.id)),
                        tenant_id=account.tenant_id,
                        customer_id=account.customer_id,
                        account_number=account.account_number,
                        status=account.status,
                        document=doc,
                        updated_at=account.updated_at,
                    )
                )
            else:
                row.customer_id = account.customer_id
                row.account_number = account.account_number
                row.status = account.status
                row.document = doc
                row.updated_at = account.updated_at

    async def find_by_id(self, account_id: str) -> BankingAccount | None:
        async with session_scope() as session:
            row = await session.get(BankingAccountRow, UUID(account_id))
            return _account_from_doc(row.document) if row else None

    async def find_by_number(self, tenant_id: str, account_number: str) -> BankingAccount | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(BankingAccountRow).where(
                    BankingAccountRow.tenant_id == tenant_id,
                    BankingAccountRow.account_number == account_number.upper(),
                )
            )
            return _account_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[BankingAccount]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingAccountRow).where(BankingAccountRow.tenant_id == tenant_id)
                )
            ).all()
        return [_account_from_doc(r.document) for r in rows]

    async def list_by_customer(self, customer_id: str) -> list[BankingAccount]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingAccountRow).where(BankingAccountRow.customer_id == customer_id)
                )
            ).all()
        return [_account_from_doc(r.document) for r in rows]

    def next_account_number(self, tenant_id: str, prefix: str = "ACC") -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"{prefix}{self._counter[tenant_id]:08d}"

    @classmethod
    def reset_counters(cls) -> None:
        cls._counter = {}


class PostgresPaymentTransferRepository(IPaymentTransferRepository):
    _counter: dict[str, int] = {}

    async def save(self, transfer: PaymentTransfer) -> None:
        doc = transfer.to_dict()
        async with session_scope() as session:
            row = await session.get(BankingPaymentTransferRow, UUID(str(transfer.id)))
            if row is None:
                session.add(
                    BankingPaymentTransferRow(
                        id=UUID(str(transfer.id)),
                        tenant_id=transfer.tenant_id,
                        transfer_ref=transfer.transfer_ref,
                        status=transfer.status,
                        source_account_id=transfer.source_account_id,
                        customer_id=transfer.customer_id,
                        batch_id=transfer.batch_id,
                        document=doc,
                        created_at=transfer.created_at,
                    )
                )
            else:
                row.status = transfer.status
                row.source_account_id = transfer.source_account_id
                row.customer_id = transfer.customer_id
                row.batch_id = transfer.batch_id
                row.document = doc

    async def find_by_id(self, transfer_id: str) -> PaymentTransfer | None:
        async with session_scope() as session:
            row = await session.get(BankingPaymentTransferRow, UUID(transfer_id))
            return _transfer_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[PaymentTransfer]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingPaymentTransferRow).where(
                        BankingPaymentTransferRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_transfer_from_doc(r.document) for r in rows]

    async def list_by_batch(self, batch_id: str) -> list[PaymentTransfer]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingPaymentTransferRow).where(
                        BankingPaymentTransferRow.batch_id == batch_id
                    )
                )
            ).all()
        return [_transfer_from_doc(r.document) for r in rows]

    async def daily_total_by_account(self, tenant_id: str, account_id: str) -> float:
        today = datetime.now(UTC).date()
        total = 0.0
        for t in await self.list_by_tenant(tenant_id):
            if t.source_account_id != account_id:
                continue
            if t.status not in {TransferStatus.COMPLETED.value, TransferStatus.PROCESSING.value}:
                continue
            if t.created_at.date() == today:
                total += t.amount
        return round(total, 2)

    async def velocity_count(self, tenant_id: str, customer_id: str, hours: int = 24) -> int:
        cutoff = datetime.now(UTC) - timedelta(hours=hours)
        return sum(
            1
            for t in await self.list_by_tenant(tenant_id)
            if t.customer_id == customer_id
            and t.created_at >= cutoff
            and t.status != TransferStatus.CANCELLED.value
        )

    def next_transfer_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"TXF{self._counter[tenant_id]:08d}"

    @classmethod
    def reset_counters(cls) -> None:
        cls._counter = {}


# --- Deposit / Loan money-path (044) ---

from contexts.banking.domain.aggregates.deposit_management_engine import (
    DepositInterestAccrual,
    DepositProfile,
    DepositTransaction,
    ProfitDistributionRule,
)
from contexts.banking.domain.aggregates.loan_management_engine import (
    LoanCollateral,
    LoanCreditRiskAnalysis,
    LoanGuarantor,
    LoanInstallment,
    LoanProfile,
    LoanTransaction,
)
from contexts.banking.domain.ports.deposit_management_repositories import (
    IDepositAccrualRepository,
    IDepositProfileRepository,
    IDepositTransactionRepository,
    IProfitRuleRepository,
)
from contexts.banking.domain.ports.loan_management_repositories import (
    ILoanCollateralRepository,
    ILoanCreditRiskRepository,
    ILoanGuarantorRepository,
    ILoanInstallmentRepository,
    ILoanProfileRepository,
    ILoanTransactionRepository,
)
from shared.infrastructure.database.orm import (
    BankingDepositAccrualRow,
    BankingDepositProfileRow,
    BankingDepositTransactionRow,
    BankingLoanCollateralRow,
    BankingLoanCreditRiskRow,
    BankingLoanGuarantorRow,
    BankingLoanInstallmentRow,
    BankingLoanProfileRow,
    BankingLoanTransactionRow,
    BankingProfitRuleRow,
)


def _profit_rule_from_doc(doc: dict) -> ProfitDistributionRule:
    return ProfitDistributionRule(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        rule_code=str(doc["rule_code"]),
        name=str(doc.get("name") or ""),
        deposit_type=str(doc.get("deposit_type") or "savings"),
        method=str(doc.get("method") or "interest"),
        rate_annual=float(doc.get("rate_annual") or 0.0),
        profit_share_pct=float(doc.get("profit_share_pct") or 0.0),
        is_active=bool(doc.get("is_active", True)),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _deposit_from_doc(doc: dict) -> DepositProfile:
    return DepositProfile(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        account_id=str(doc["account_id"]),
        customer_id=str(doc["customer_id"]),
        deposit_type=str(doc.get("deposit_type") or "savings"),
        status=str(doc.get("status") or "pending_approval"),
        currency=str(doc.get("currency") or "USD"),
        principal=float(doc.get("principal") or 0.0),
        interest_rate_annual=float(doc.get("interest_rate_annual") or 0.0),
        profit_rule_id=doc.get("profit_rule_id"),
        tenure_months=doc.get("tenure_months"),
        maturity_date=_parse_dt(doc.get("maturity_date")),
        auto_renew=bool(doc.get("auto_renew") or False),
        recurring_amount=float(doc.get("recurring_amount") or 0.0),
        recurring_day=int(doc.get("recurring_day") or 1),
        accrued_interest=float(doc.get("accrued_interest") or 0.0),
        total_interest_paid=float(doc.get("total_interest_paid") or 0.0),
        gl_account_code=doc.get("gl_account_code"),
        opened_at=_parse_dt(doc.get("opened_at")),
        closed_at=_parse_dt(doc.get("closed_at")),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
        updated_at=_parse_dt(doc.get("updated_at")) or datetime.now(UTC),
    )


def _deposit_tx_from_doc(doc: dict) -> DepositTransaction:
    return DepositTransaction(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        deposit_id=str(doc["deposit_id"]),
        account_id=str(doc["account_id"]),
        transaction_ref=str(doc["transaction_ref"]),
        transaction_type=str(doc.get("transaction_type") or "deposit"),
        amount=float(doc.get("amount") or 0.0),
        currency=str(doc.get("currency") or "USD"),
        status=str(doc.get("status") or "pending"),
        penalty_amount=float(doc.get("penalty_amount") or 0.0),
        net_amount=float(doc.get("net_amount") or 0.0),
        kernel_journal_id=doc.get("kernel_journal_id"),
        approved_by=doc.get("approved_by"),
        posted_at=_parse_dt(doc.get("posted_at")),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _deposit_accrual_from_doc(doc: dict) -> DepositInterestAccrual:
    return DepositInterestAccrual(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        deposit_id=str(doc["deposit_id"]),
        accrual_ref=str(doc["accrual_ref"]),
        period_start=_parse_dt(doc.get("period_start")) or datetime.now(UTC),
        period_end=_parse_dt(doc.get("period_end")) or datetime.now(UTC),
        principal_base=float(doc.get("principal_base") or 0.0),
        rate_annual=float(doc.get("rate_annual") or 0.0),
        accrued_amount=float(doc.get("accrued_amount") or 0.0),
        status=str(doc.get("status") or "accrued"),
        kernel_journal_id=doc.get("kernel_journal_id"),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _loan_from_doc(doc: dict) -> LoanProfile:
    return LoanProfile(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        account_id=str(doc["account_id"]),
        customer_id=str(doc["customer_id"]),
        loan_type=str(doc.get("loan_type") or "personal"),
        status=str(doc.get("status") or "draft"),
        loan_ref=str(doc["loan_ref"]),
        currency=str(doc.get("currency") or "USD"),
        principal=float(doc.get("principal") or 0.0),
        outstanding_principal=float(doc.get("outstanding_principal") or 0.0),
        interest_rate_annual=float(doc.get("interest_rate_annual") or 0.0),
        tenure_months=int(doc.get("tenure_months") or 12),
        emi_amount=float(doc.get("emi_amount") or 0.0),
        total_interest_paid=float(doc.get("total_interest_paid") or 0.0),
        total_penalties_paid=float(doc.get("total_penalties_paid") or 0.0),
        gl_account_code=doc.get("gl_account_code"),
        disbursed_at=_parse_dt(doc.get("disbursed_at")),
        maturity_date=_parse_dt(doc.get("maturity_date")),
        closed_at=_parse_dt(doc.get("closed_at")),
        credit_risk_id=doc.get("credit_risk_id"),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
        updated_at=_parse_dt(doc.get("updated_at")) or datetime.now(UTC),
    )


def _loan_tx_from_doc(doc: dict) -> LoanTransaction:
    return LoanTransaction(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        loan_id=str(doc["loan_id"]),
        account_id=str(doc["account_id"]),
        transaction_ref=str(doc["transaction_ref"]),
        transaction_type=str(doc.get("transaction_type") or "disbursement"),
        amount=float(doc.get("amount") or 0.0),
        principal_part=float(doc.get("principal_part") or 0.0),
        interest_part=float(doc.get("interest_part") or 0.0),
        penalty_amount=float(doc.get("penalty_amount") or 0.0),
        currency=str(doc.get("currency") or "USD"),
        status=str(doc.get("status") or "pending"),
        kernel_journal_id=doc.get("kernel_journal_id"),
        approved_by=doc.get("approved_by"),
        posted_at=_parse_dt(doc.get("posted_at")),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _loan_installment_from_doc(doc: dict) -> LoanInstallment:
    return LoanInstallment(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        loan_id=str(doc["loan_id"]),
        installment_number=int(doc.get("installment_number") or 1),
        due_date=_parse_dt(doc.get("due_date")) or datetime.now(UTC),
        principal_due=float(doc.get("principal_due") or 0.0),
        interest_due=float(doc.get("interest_due") or 0.0),
        total_due=float(doc.get("total_due") or 0.0),
        status=str(doc.get("status") or "scheduled"),
        paid_at=_parse_dt(doc.get("paid_at")),
        penalty_amount=float(doc.get("penalty_amount") or 0.0),
    )


def _loan_collateral_from_doc(doc: dict) -> LoanCollateral:
    return LoanCollateral(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        loan_id=str(doc["loan_id"]),
        collateral_type=str(doc.get("collateral_type") or ""),
        description=str(doc.get("description") or ""),
        estimated_value=float(doc.get("estimated_value") or 0.0),
        currency=str(doc.get("currency") or "USD"),
        status=str(doc.get("status") or "pending"),
        lien_ref=str(doc.get("lien_ref") or ""),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _loan_guarantor_from_doc(doc: dict) -> LoanGuarantor:
    return LoanGuarantor(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        loan_id=str(doc["loan_id"]),
        guarantor_name=str(doc.get("guarantor_name") or ""),
        guarantor_id_ref=str(doc.get("guarantor_id_ref") or ""),
        relationship=str(doc.get("relationship") or ""),
        guaranteed_amount=float(doc.get("guaranteed_amount") or 0.0),
        currency=str(doc.get("currency") or "USD"),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _loan_credit_risk_from_doc(doc: dict) -> LoanCreditRiskAnalysis:
    return LoanCreditRiskAnalysis(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        loan_id=str(doc["loan_id"]),
        risk_score=float(doc.get("risk_score") or 0.0),
        risk_grade=str(doc.get("risk_grade") or "C"),
        recommendation=str(doc.get("recommendation") or ""),
        factors=list(doc.get("factors") or []),
        dti_ratio=float(doc.get("dti_ratio") or 0.0),
        collateral_coverage_pct=float(doc.get("collateral_coverage_pct") or 0.0),
        ai_provider_ref=doc.get("ai_provider_ref"),
        analyzed_at=_parse_dt(doc.get("analyzed_at")) or datetime.now(UTC),
    )


class PostgresProfitRuleRepository(IProfitRuleRepository):
    async def save(self, rule: ProfitDistributionRule) -> None:
        doc = rule.to_dict()
        async with session_scope() as session:
            row = await session.get(BankingProfitRuleRow, UUID(str(rule.id)))
            if row is None:
                session.add(
                    BankingProfitRuleRow(
                        id=UUID(str(rule.id)),
                        tenant_id=rule.tenant_id,
                        rule_code=rule.rule_code,
                        document=doc,
                    )
                )
            else:
                row.rule_code = rule.rule_code
                row.document = doc

    async def find_by_code(self, tenant_id: str, rule_code: str) -> ProfitDistributionRule | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(BankingProfitRuleRow).where(
                    BankingProfitRuleRow.tenant_id == tenant_id,
                    BankingProfitRuleRow.rule_code == rule_code.upper(),
                )
            )
            return _profit_rule_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[ProfitDistributionRule]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingProfitRuleRow).where(BankingProfitRuleRow.tenant_id == tenant_id)
                )
            ).all()
        return [_profit_rule_from_doc(r.document) for r in rows]


class PostgresDepositProfileRepository(IDepositProfileRepository):
    async def save(self, deposit: DepositProfile) -> None:
        doc = deposit.to_dict()
        async with session_scope() as session:
            row = await session.get(BankingDepositProfileRow, UUID(str(deposit.id)))
            if row is None:
                session.add(
                    BankingDepositProfileRow(
                        id=UUID(str(deposit.id)),
                        tenant_id=deposit.tenant_id,
                        account_id=deposit.account_id,
                        customer_id=deposit.customer_id,
                        status=deposit.status,
                        document=doc,
                        updated_at=deposit.updated_at,
                    )
                )
            else:
                row.account_id = deposit.account_id
                row.customer_id = deposit.customer_id
                row.status = deposit.status
                row.document = doc
                row.updated_at = deposit.updated_at

    async def find_by_id(self, deposit_id: str) -> DepositProfile | None:
        async with session_scope() as session:
            row = await session.get(BankingDepositProfileRow, UUID(deposit_id))
            return _deposit_from_doc(row.document) if row else None

    async def find_by_account(self, account_id: str) -> DepositProfile | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(BankingDepositProfileRow).where(
                    BankingDepositProfileRow.account_id == account_id
                )
            )
            return _deposit_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[DepositProfile]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingDepositProfileRow).where(
                        BankingDepositProfileRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_deposit_from_doc(r.document) for r in rows]


class PostgresDepositTransactionRepository(IDepositTransactionRepository):
    _counter: dict[str, int] = {}

    async def save(self, transaction: DepositTransaction) -> None:
        doc = transaction.to_dict()
        async with session_scope() as session:
            row = await session.get(BankingDepositTransactionRow, UUID(str(transaction.id)))
            if row is None:
                session.add(
                    BankingDepositTransactionRow(
                        id=UUID(str(transaction.id)),
                        tenant_id=transaction.tenant_id,
                        deposit_id=transaction.deposit_id,
                        transaction_ref=transaction.transaction_ref,
                        document=doc,
                    )
                )
            else:
                row.deposit_id = transaction.deposit_id
                row.transaction_ref = transaction.transaction_ref
                row.document = doc

    async def find_by_id(self, transaction_id: str) -> DepositTransaction | None:
        async with session_scope() as session:
            row = await session.get(BankingDepositTransactionRow, UUID(transaction_id))
            return _deposit_tx_from_doc(row.document) if row else None

    async def list_by_deposit(self, deposit_id: str) -> list[DepositTransaction]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingDepositTransactionRow).where(
                        BankingDepositTransactionRow.deposit_id == deposit_id
                    )
                )
            ).all()
        return [_deposit_tx_from_doc(r.document) for r in rows]

    async def list_by_tenant(self, tenant_id: str) -> list[DepositTransaction]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingDepositTransactionRow).where(
                        BankingDepositTransactionRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_deposit_tx_from_doc(r.document) for r in rows]

    def next_transaction_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"DTX{self._counter[tenant_id]:08d}"

    @classmethod
    def reset_counters(cls) -> None:
        cls._counter = {}


class PostgresDepositAccrualRepository(IDepositAccrualRepository):
    _counter: dict[str, int] = {}

    async def save(self, accrual: DepositInterestAccrual) -> None:
        doc = accrual.to_dict()
        async with session_scope() as session:
            row = await session.get(BankingDepositAccrualRow, UUID(str(accrual.id)))
            if row is None:
                session.add(
                    BankingDepositAccrualRow(
                        id=UUID(str(accrual.id)),
                        tenant_id=accrual.tenant_id,
                        deposit_id=accrual.deposit_id,
                        document=doc,
                    )
                )
            else:
                row.deposit_id = accrual.deposit_id
                row.document = doc

    async def list_by_deposit(self, deposit_id: str) -> list[DepositInterestAccrual]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingDepositAccrualRow).where(
                        BankingDepositAccrualRow.deposit_id == deposit_id
                    )
                )
            ).all()
        return [_deposit_accrual_from_doc(r.document) for r in rows]

    async def list_by_tenant(self, tenant_id: str) -> list[DepositInterestAccrual]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingDepositAccrualRow).where(
                        BankingDepositAccrualRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_deposit_accrual_from_doc(r.document) for r in rows]

    def next_accrual_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"ACC{self._counter[tenant_id]:08d}"

    @classmethod
    def reset_counters(cls) -> None:
        cls._counter = {}


class PostgresLoanProfileRepository(ILoanProfileRepository):
    _counter: dict[str, int] = {}

    async def save(self, loan: LoanProfile) -> None:
        doc = loan.to_dict()
        async with session_scope() as session:
            row = await session.get(BankingLoanProfileRow, UUID(str(loan.id)))
            if row is None:
                session.add(
                    BankingLoanProfileRow(
                        id=UUID(str(loan.id)),
                        tenant_id=loan.tenant_id,
                        account_id=loan.account_id,
                        loan_ref=loan.loan_ref,
                        status=loan.status,
                        document=doc,
                        updated_at=loan.updated_at,
                    )
                )
            else:
                row.account_id = loan.account_id
                row.loan_ref = loan.loan_ref
                row.status = loan.status
                row.document = doc
                row.updated_at = loan.updated_at

    async def find_by_id(self, loan_id: str) -> LoanProfile | None:
        async with session_scope() as session:
            row = await session.get(BankingLoanProfileRow, UUID(loan_id))
            return _loan_from_doc(row.document) if row else None

    async def find_by_account(self, account_id: str) -> LoanProfile | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(BankingLoanProfileRow).where(BankingLoanProfileRow.account_id == account_id)
            )
            return _loan_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[LoanProfile]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingLoanProfileRow).where(BankingLoanProfileRow.tenant_id == tenant_id)
                )
            ).all()
        return [_loan_from_doc(r.document) for r in rows]

    def next_loan_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"LN{self._counter[tenant_id]:08d}"

    @classmethod
    def reset_counters(cls) -> None:
        cls._counter = {}


class PostgresLoanTransactionRepository(ILoanTransactionRepository):
    _counter: dict[str, int] = {}

    async def save(self, transaction: LoanTransaction) -> None:
        doc = transaction.to_dict()
        async with session_scope() as session:
            row = await session.get(BankingLoanTransactionRow, UUID(str(transaction.id)))
            if row is None:
                session.add(
                    BankingLoanTransactionRow(
                        id=UUID(str(transaction.id)),
                        tenant_id=transaction.tenant_id,
                        loan_id=transaction.loan_id,
                        transaction_ref=transaction.transaction_ref,
                        document=doc,
                    )
                )
            else:
                row.loan_id = transaction.loan_id
                row.transaction_ref = transaction.transaction_ref
                row.document = doc

    async def find_by_id(self, transaction_id: str) -> LoanTransaction | None:
        async with session_scope() as session:
            row = await session.get(BankingLoanTransactionRow, UUID(transaction_id))
            return _loan_tx_from_doc(row.document) if row else None

    async def list_by_loan(self, loan_id: str) -> list[LoanTransaction]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingLoanTransactionRow).where(
                        BankingLoanTransactionRow.loan_id == loan_id
                    )
                )
            ).all()
        items = [_loan_tx_from_doc(r.document) for r in rows]
        return sorted(items, key=lambda t: t.created_at)

    async def list_by_tenant(self, tenant_id: str) -> list[LoanTransaction]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingLoanTransactionRow).where(
                        BankingLoanTransactionRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_loan_tx_from_doc(r.document) for r in rows]

    def next_transaction_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"LTX{self._counter[tenant_id]:08d}"

    @classmethod
    def reset_counters(cls) -> None:
        cls._counter = {}


class PostgresLoanInstallmentRepository(ILoanInstallmentRepository):
    async def save(self, installment: LoanInstallment) -> None:
        doc = installment.to_dict()
        async with session_scope() as session:
            row = await session.get(BankingLoanInstallmentRow, UUID(str(installment.id)))
            if row is None:
                session.add(
                    BankingLoanInstallmentRow(
                        id=UUID(str(installment.id)),
                        tenant_id=installment.tenant_id,
                        loan_id=installment.loan_id,
                        document=doc,
                    )
                )
            else:
                row.loan_id = installment.loan_id
                row.document = doc

    async def list_by_loan(self, loan_id: str) -> list[LoanInstallment]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingLoanInstallmentRow).where(
                        BankingLoanInstallmentRow.loan_id == loan_id
                    )
                )
            ).all()
        return sorted(
            [_loan_installment_from_doc(r.document) for r in rows],
            key=lambda i: i.installment_number,
        )

    async def find_by_id(self, installment_id: str) -> LoanInstallment | None:
        async with session_scope() as session:
            row = await session.get(BankingLoanInstallmentRow, UUID(installment_id))
            return _loan_installment_from_doc(row.document) if row else None


class PostgresLoanCollateralRepository(ILoanCollateralRepository):
    async def save(self, collateral: LoanCollateral) -> None:
        doc = collateral.to_dict()
        async with session_scope() as session:
            row = await session.get(BankingLoanCollateralRow, UUID(str(collateral.id)))
            if row is None:
                session.add(
                    BankingLoanCollateralRow(
                        id=UUID(str(collateral.id)),
                        tenant_id=collateral.tenant_id,
                        loan_id=collateral.loan_id,
                        document=doc,
                    )
                )
            else:
                row.loan_id = collateral.loan_id
                row.document = doc

    async def list_by_loan(self, loan_id: str) -> list[LoanCollateral]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingLoanCollateralRow).where(
                        BankingLoanCollateralRow.loan_id == loan_id
                    )
                )
            ).all()
        return [_loan_collateral_from_doc(r.document) for r in rows]


class PostgresLoanGuarantorRepository(ILoanGuarantorRepository):
    async def save(self, guarantor: LoanGuarantor) -> None:
        doc = guarantor.to_dict()
        async with session_scope() as session:
            row = await session.get(BankingLoanGuarantorRow, UUID(str(guarantor.id)))
            if row is None:
                session.add(
                    BankingLoanGuarantorRow(
                        id=UUID(str(guarantor.id)),
                        tenant_id=guarantor.tenant_id,
                        loan_id=guarantor.loan_id,
                        document=doc,
                    )
                )
            else:
                row.loan_id = guarantor.loan_id
                row.document = doc

    async def list_by_loan(self, loan_id: str) -> list[LoanGuarantor]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingLoanGuarantorRow).where(
                        BankingLoanGuarantorRow.loan_id == loan_id
                    )
                )
            ).all()
        return [_loan_guarantor_from_doc(r.document) for r in rows]


class PostgresLoanCreditRiskRepository(ILoanCreditRiskRepository):
    async def save(self, analysis: LoanCreditRiskAnalysis) -> None:
        doc = analysis.to_dict()
        async with session_scope() as session:
            row = await session.get(BankingLoanCreditRiskRow, UUID(str(analysis.id)))
            if row is None:
                session.add(
                    BankingLoanCreditRiskRow(
                        id=UUID(str(analysis.id)),
                        tenant_id=analysis.tenant_id,
                        loan_id=analysis.loan_id,
                        document=doc,
                    )
                )
            else:
                row.loan_id = analysis.loan_id
                row.document = doc

    async def find_by_loan(self, loan_id: str) -> LoanCreditRiskAnalysis | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(BankingLoanCreditRiskRow).where(
                    BankingLoanCreditRiskRow.loan_id == loan_id
                )
            )
            return _loan_credit_risk_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[LoanCreditRiskAnalysis]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BankingLoanCreditRiskRow).where(
                        BankingLoanCreditRiskRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_loan_credit_risk_from_doc(r.document) for r in rows]
