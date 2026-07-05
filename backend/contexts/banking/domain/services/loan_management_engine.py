"""Enterprise Loan Platform engine — catalog, calculators, AI risk."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from contexts.banking.domain.aggregates.loan_management_engine import (
    LoanStatus,
    LoanType,
    RiskGrade,
)

LOAN_MANAGEMENT_CATALOG: dict[str, dict] = {
    LoanType.PERSONAL.value: {"label": "Personal Loans", "supported": True},
    LoanType.BUSINESS.value: {"label": "Business Loans", "supported": True},
    LoanType.EDUCATION.value: {"label": "Education Loans", "supported": True},
    LoanType.CONSTRUCTION.value: {"label": "Construction Loans", "supported": True},
    LoanType.MORTGAGE.value: {"label": "Mortgage", "supported": True},
    LoanType.MICROFINANCE.value: {"label": "Microfinance", "supported": True},
    LoanType.AGRICULTURE.value: {"label": "Agriculture Loans", "supported": True},
    "loan_origination": {"label": "Loan Origination", "supported": True},
    "approval_workflow": {"label": "Approval Workflow", "supported": True},
    "collateral": {"label": "Collateral", "supported": True},
    "guarantors": {"label": "Guarantors", "supported": True},
    "repayment_schedule": {"label": "Repayment Schedule", "supported": True},
    "installments": {"label": "Installments", "supported": True},
    "penalty_rules": {"label": "Penalty Rules", "policy_key": "loan.penalty.late_payment"},
    "restructuring": {"label": "Restructuring", "supported": True},
    "settlement": {"label": "Settlement", "supported": True},
    "early_closure": {"label": "Early Closure", "supported": True},
    "automatic_gl_posting": {"label": "Automatic Financial Posting", "supported": True},
    "ai_credit_risk_analysis": {"label": "AI Credit Risk Analysis", "supported": True},
    "audit_trail": {"label": "Audit Trail", "supported": True},
}

LOAN_POLICY_KEYS: list[dict] = [
    {"key": "loan.interest.rate", "description": "Loan interest rate by type and tenure"},
    {"key": "loan.approval.required_level", "description": "Approval levels for loan origination"},
    {"key": "loan.penalty.late_payment", "description": "Late payment penalty rules"},
    {"key": "loan.restructure.rules", "description": "Restructuring eligibility rules"},
    {"key": "loan.settlement.discount", "description": "Settlement discount parameters"},
    {"key": "loan.early_closure.penalty", "description": "Early closure penalty rules"},
    {"key": "loan.credit_risk.threshold", "description": "Credit risk score thresholds"},
    {"key": "lending.debt_to_income_ratio", "description": "DTI ceiling for approval"},
    {"key": "lending.collateral.haircut", "description": "Collateral valuation haircut"},
    {"key": "lending.single_exposure_limit", "description": "Maximum exposure per customer"},
]


def list_loan_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in LOAN_MANAGEMENT_CATALOG.items()]


def list_loan_policy_keys() -> list[dict]:
    return LOAN_POLICY_KEYS


def calculate_emi(*, principal: float, rate_annual: float, tenure_months: int) -> float:
    if principal <= 0 or tenure_months <= 0:
        return 0.0
    if rate_annual <= 0:
        return round(principal / tenure_months, 2)
    r = rate_annual / 12 / 100
    factor = (1 + r) ** tenure_months
    emi = principal * r * factor / (factor - 1)
    return round(emi, 2)


def build_amortization_schedule(
    *,
    principal: float,
    rate_annual: float,
    tenure_months: int,
    start_date: datetime | None = None,
) -> list[dict]:
    if principal <= 0 or tenure_months <= 0:
        return []
    start = start_date or datetime.now(UTC)
    emi = calculate_emi(principal=principal, rate_annual=rate_annual, tenure_months=tenure_months)
    monthly_rate = rate_annual / 12 / 100
    balance = principal
    schedule: list[dict] = []
    for n in range(1, tenure_months + 1):
        interest = round(balance * monthly_rate, 2) if monthly_rate > 0 else 0.0
        principal_part = round(emi - interest, 2) if n < tenure_months else round(balance, 2)
        if principal_part > balance:
            principal_part = round(balance, 2)
        total = round(principal_part + interest, 2)
        due = start + timedelta(days=30 * n)
        schedule.append(
            {
                "installment_number": n,
                "due_date": due.isoformat(),
                "principal_due": principal_part,
                "interest_due": interest,
                "total_due": total,
            }
        )
        balance = round(max(0, balance - principal_part), 2)
    return schedule


def calculate_late_penalty(
    *, amount: float, days_overdue: int, penalty_pct: float, policy_outcome: str | None
) -> float:
    if policy_outcome == "waive_penalty" or days_overdue <= 0 or penalty_pct <= 0:
        return 0.0
    return round(amount * (penalty_pct / 100), 2)


def calculate_dti_ratio(*, monthly_income: float, existing_obligations: float, new_emi: float) -> float:
    if monthly_income <= 0:
        return 999.0
    return round((existing_obligations + new_emi) / monthly_income, 4)


def calculate_collateral_coverage(*, collateral_value: float, loan_amount: float, haircut_pct: float) -> float:
    if loan_amount <= 0:
        return 0.0
    net_collateral = collateral_value * (1 - haircut_pct / 100)
    return round((net_collateral / loan_amount) * 100, 2)


def analyze_credit_risk(
    *,
    loan_amount: float,
    emi_amount: float,
    monthly_income: float,
    existing_obligations: float,
    collateral_value: float,
    haircut_pct: float,
    kyc_risk_rating: str = "low",
    policy_thresholds: dict | None = None,
) -> dict:
    """Deterministic credit risk scoring with AI-ready factor breakdown."""
    thresholds = policy_thresholds or {}
    max_dti = float(thresholds.get("max_dti_ratio", 0.45))
    min_coverage = float(thresholds.get("min_collateral_coverage_pct", 100))

    dti = calculate_dti_ratio(
        monthly_income=monthly_income,
        existing_obligations=existing_obligations,
        new_emi=emi_amount,
    )
    coverage = calculate_collateral_coverage(
        collateral_value=collateral_value, loan_amount=loan_amount, haircut_pct=haircut_pct
    )

    score = 100.0
    factors: list[dict] = []

    if dti > max_dti:
        penalty = min(40, (dti - max_dti) * 100)
        score -= penalty
        factors.append({"factor": "dti_ratio", "value": dti, "impact": -penalty, "status": "elevated"})
    else:
        factors.append({"factor": "dti_ratio", "value": dti, "impact": 0, "status": "ok"})

    if collateral_value > 0 and coverage < min_coverage:
        penalty = min(25, (min_coverage - coverage) / 2)
        score -= penalty
        factors.append({"factor": "collateral_coverage", "value": coverage, "impact": -penalty, "status": "weak"})
    elif collateral_value > 0:
        factors.append({"factor": "collateral_coverage", "value": coverage, "impact": 5, "status": "strong"})
        score += 5

    if kyc_risk_rating == "high":
        score -= 20
        factors.append({"factor": "kyc_risk", "value": kyc_risk_rating, "impact": -20, "status": "high"})
    elif kyc_risk_rating == "medium":
        score -= 10
        factors.append({"factor": "kyc_risk", "value": kyc_risk_rating, "impact": -10, "status": "medium"})
    else:
        factors.append({"factor": "kyc_risk", "value": kyc_risk_rating, "impact": 0, "status": "low"})

    if loan_amount > float(thresholds.get("large_loan_threshold", 100000)):
        score -= 10
        factors.append({"factor": "exposure_size", "value": loan_amount, "impact": -10, "status": "large"})

    score = max(0, min(100, round(score, 2)))

    if score >= 75:
        grade = RiskGrade.LOW.value
        recommendation = "approve"
    elif score >= 55:
        grade = RiskGrade.MEDIUM.value
        recommendation = "approve_with_conditions"
    elif score >= 35:
        grade = RiskGrade.HIGH.value
        recommendation = "enhanced_review"
    else:
        grade = RiskGrade.CRITICAL.value
        recommendation = "decline"

    return {
        "risk_score": score,
        "risk_grade": grade,
        "recommendation": recommendation,
        "factors": factors,
        "dti_ratio": dti,
        "collateral_coverage_pct": coverage,
    }


def resolve_loan_approval_levels(*, loan_type: str, amount: float) -> int:
    if loan_type in {LoanType.MORTGAGE.value, LoanType.CONSTRUCTION.value} or amount >= 100000:
        return 2
    if loan_type == LoanType.MICROFINANCE.value and amount < 5000:
        return 1
    if amount >= 500000:
        return 3
    return 1


def build_loan_dashboard(
    *,
    loans: list[dict],
    transactions: list[dict],
    installments: list[dict],
    risk_analyses: list[dict],
) -> dict:
    by_type: dict[str, int] = {}
    by_status: dict[str, int] = {}
    total_outstanding = 0.0
    total_disbursed = 0.0
    overdue_count = 0

    for loan in loans:
        by_type[loan.get("loan_type", "unknown")] = by_type.get(loan.get("loan_type", "unknown"), 0) + 1
        by_status[loan.get("status", "unknown")] = by_status.get(loan.get("status", "unknown"), 0) + 1
        if loan.get("status") in {LoanStatus.ACTIVE.value, LoanStatus.RESTRUCTURED.value}:
            total_outstanding += loan.get("outstanding_principal", 0)
        if loan.get("disbursed_at"):
            total_disbursed += loan.get("principal", 0)

    for inst in installments:
        if inst.get("status") == "overdue":
            overdue_count += 1

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "summary": {
            "loan_count": len(loans),
            "active_loans": by_status.get(LoanStatus.ACTIVE.value, 0),
            "pending_approval": by_status.get(LoanStatus.PENDING_APPROVAL.value, 0),
            "total_outstanding": round(total_outstanding, 2),
            "total_disbursed": round(total_disbursed, 2),
            "overdue_installments": overdue_count,
            "risk_analyses_count": len(risk_analyses),
        },
        "by_loan_type": by_type,
        "by_status": by_status,
        "policy_keys": list_loan_policy_keys(),
    }
