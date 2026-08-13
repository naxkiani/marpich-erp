"""Unit — Banking money-path postgres document round-trip (no live DB)."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.banking.domain.aggregates.customer_account_engine import (
    BankingAccount,
    BankingAccountProduct,
    BankingCustomer,
)
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
from contexts.banking.domain.aggregates.payment_platform_engine import PaymentTransfer
from contexts.banking.infrastructure.persistence import postgres_store as pg


def test_customer_round_trip():
    customer = BankingCustomer.create(
        tenant_id="t1",
        customer_type="individual",
        display_name="Ada",
        legal_name="Ada Lovelace",
        email="ada@bank.test",
        phone="+10000000000",
    )
    restored = pg._customer_from_doc(customer.to_dict())
    assert restored.email == "ada@bank.test"
    assert str(restored.id) == str(customer.id)


def test_product_account_transfer_round_trip():
    product = BankingAccountProduct.create(
        tenant_id="t1",
        product_code="CHK",
        name="Checking",
        account_type="checking",
    )
    account = BankingAccount.create(
        tenant_id="t1",
        customer_id="cust-1",
        account_number="ACC00000001",
        account_type="checking",
        product_code="CHK",
        currency="USD",
    )
    transfer = PaymentTransfer.create(
        tenant_id="t1",
        transfer_ref="TXF00000001",
        transfer_type="internal",
        source_account_id=str(account.id),
        customer_id="cust-1",
        amount=25.5,
        currency="USD",
        destination_account_id="acc-2",
    )
    assert pg._product_from_doc(product.to_dict()).product_code == "CHK"
    assert pg._account_from_doc(account.to_dict()).account_number == "ACC00000001"
    assert pg._transfer_from_doc(transfer.to_dict()).amount == 25.5


def test_deposit_loan_round_trip():
    rule = ProfitDistributionRule.create(
        tenant_id="t1",
        rule_code="SAV1",
        name="Savings",
        deposit_type="savings",
        rate_annual=0.05,
    )
    deposit = DepositProfile.create(
        tenant_id="t1",
        account_id="acc-1",
        customer_id="cust-1",
        deposit_type="savings",
        currency="USD",
        principal=1000.0,
        interest_rate_annual=0.05,
        profit_rule_id=str(rule.id),
        requires_approval=False,
    )
    dtx = DepositTransaction.create(
        tenant_id="t1",
        deposit_id=str(deposit.id),
        account_id="acc-1",
        transaction_ref="DTX00000001",
        transaction_type="deposit",
        amount=1000.0,
        currency="USD",
        auto_approve=True,
    )
    now = datetime.now(UTC)
    accrual = DepositInterestAccrual.create(
        tenant_id="t1",
        deposit_id=str(deposit.id),
        accrual_ref="ACC00000001",
        period_start=now,
        period_end=now,
        principal_base=1000.0,
        rate_annual=0.05,
        accrued_amount=1.37,
    )
    loan = LoanProfile.create(
        tenant_id="t1",
        account_id="acc-2",
        customer_id="cust-1",
        loan_type="personal",
        loan_ref="LN00000001",
        currency="USD",
        principal=5000.0,
        interest_rate_annual=0.12,
        tenure_months=12,
        emi_amount=444.0,
    )
    ltx = LoanTransaction.create(
        tenant_id="t1",
        loan_id=str(loan.id),
        account_id="acc-2",
        transaction_ref="LTX00000001",
        transaction_type="disbursement",
        amount=5000.0,
        currency="USD",
        auto_approve=True,
    )
    installment = LoanInstallment.create(
        tenant_id="t1",
        loan_id=str(loan.id),
        installment_number=1,
        due_date=now,
        principal_due=400.0,
        interest_due=44.0,
    )
    collateral = LoanCollateral.create(
        tenant_id="t1",
        loan_id=str(loan.id),
        collateral_type="vehicle",
        description="Car",
        estimated_value=8000.0,
        currency="USD",
    )
    guarantor = LoanGuarantor.create(
        tenant_id="t1",
        loan_id=str(loan.id),
        guarantor_name="Bob",
        guarantor_id_ref="G-1",
        guaranteed_amount=5000.0,
    )
    risk = LoanCreditRiskAnalysis.create(
        tenant_id="t1",
        loan_id=str(loan.id),
        risk_score=72.5,
        risk_grade="B",
        recommendation="approve",
        factors=[{"name": "income", "weight": 0.4}],
    )
    assert pg._profit_rule_from_doc(rule.to_dict()).rule_code == "SAV1"
    assert pg._deposit_from_doc(deposit.to_dict()).principal == 1000.0
    assert pg._deposit_tx_from_doc(dtx.to_dict()).transaction_ref == "DTX00000001"
    assert pg._deposit_accrual_from_doc(accrual.to_dict()).accrued_amount == 1.37
    assert pg._loan_from_doc(loan.to_dict()).loan_ref == "LN00000001"
    assert pg._loan_tx_from_doc(ltx.to_dict()).amount == 5000.0
    assert pg._loan_installment_from_doc(installment.to_dict()).total_due == 444.0
    assert pg._loan_collateral_from_doc(collateral.to_dict()).estimated_value == 8000.0
    assert pg._loan_guarantor_from_doc(guarantor.to_dict()).guarantor_name == "Bob"
    assert pg._loan_credit_risk_from_doc(risk.to_dict()).risk_grade == "B"
