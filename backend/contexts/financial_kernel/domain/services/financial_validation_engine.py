"""Enterprise financial validation engine — unified pre-posting validation chain."""
from __future__ import annotations

from dataclasses import dataclass, field

from contexts.financial_kernel.domain.aggregates.financial_validation import ValidationCheckType
from contexts.financial_kernel.domain.services.double_entry_validation_engine import (
    ValidationResult,
    ValidationSeverity,
    merge_validation_results,
    validate_accounts,
    validate_double_entry_balance,
    validate_financial_lock,
    validate_journal_entry_type,
    validate_line_structure,
    validate_period_open,
)
from contexts.financial_kernel.domain.services.financial_dimension_engine import (
    validate_line_dimensions,
)

VALIDATION_CATALOG: dict[str, dict] = {
    ValidationCheckType.BALANCED_JOURNALS.value: {
        "label": "Balanced Journals",
        "description": "Debit total must equal credit total; valid line structure",
        "required": True,
    },
    ValidationCheckType.POSTING_PERMISSIONS.value: {
        "label": "Posting Permissions",
        "description": "User must hold required posting permission for mode",
        "required": True,
    },
    ValidationCheckType.FISCAL_PERIOD.value: {
        "label": "Fiscal Period",
        "description": "Target period and fiscal year must be open for posting",
        "required": True,
    },
    ValidationCheckType.CURRENCY.value: {
        "label": "Currency",
        "description": "Currency code and exchange rate must be valid",
        "required": True,
    },
    ValidationCheckType.TAX.value: {
        "label": "Tax",
        "description": "Tax codes and amounts on lines must be consistent",
        "required": False,
    },
    ValidationCheckType.BUDGET.value: {
        "label": "Budget",
        "description": "Expense postings must not exceed available budget",
        "required": True,
    },
    ValidationCheckType.ACCOUNT_STATUS.value: {
        "label": "Account Status",
        "description": "Accounts must be active and accept GL posting",
        "required": True,
    },
    ValidationCheckType.DUPLICATE_POSTING.value: {
        "label": "Duplicate Posting",
        "description": "Idempotency key must not match an existing posted journal",
        "required": True,
    },
    ValidationCheckType.APPROVAL_STATUS.value: {
        "label": "Approval Status",
        "description": "Manual journals requiring approval must be approved before post",
        "required": True,
    },
    ValidationCheckType.DIMENSION_RULES.value: {
        "label": "Dimension Rules",
        "description": "Journal line dimensions must pass master-data rules",
        "required": True,
    },
    ValidationCheckType.BUSINESS_RULES.value: {
        "label": "Business Rules",
        "description": "Tenant business rules (min amount, blocked accounts, required dims)",
        "required": True,
    },
}


def list_validation_catalog() -> list[dict]:
    return [{"check_type": key, **meta} for key, meta in VALIDATION_CATALOG.items()]


@dataclass
class FinancialValidationContext:
    tenant_id: str
    period_status: str | None = None
    fiscal_year_status: str | None = None
    account_postable: dict[str, bool] | None = None
    account_active: dict[str, bool] | None = None
    account_status: dict[str, str] | None = None
    account_categories: dict[str, str] | None = None
    locked_resources: set[str] | None = None
    resource_key: str | None = None
    journal_entry_type: str = "standard"
    requires_approval: bool = False
    journal_status: str | None = None
    min_lines: int = 2
    currency: str = "USD"
    base_currency: str = "USD"
    exchange_rate: float = 1.0
    user_permissions: list[str] | None = None
    posting_mode: str = "automatic"
    idempotency_key: str | None = None
    duplicate_exists: bool = False
    dimension_lookup: dict[str, dict[str, dict]] | None = None
    budget_checks: list[dict] = field(default_factory=list)
    valid_tax_codes: set[str] | None = None
    business_rules: dict | None = None


def validate_balanced_journals(
    lines: list[dict], *, min_lines: int = 2, journal_entry_type: str = "standard"
) -> ValidationResult:
    effective_min = 1 if journal_entry_type == "single_entry" else min_lines
    return merge_validation_results(
        validate_line_structure(lines, min_lines=effective_min),
        validate_double_entry_balance(lines),
    )


def validate_posting_permissions(
    *,
    user_permissions: list[str] | None,
    posting_mode: str,
    requires_approval: bool,
) -> ValidationResult:
    result = ValidationResult(valid=True)
    perms = user_permissions or ["*"]
    if "*" in perms:
        return result
    if posting_mode == "manual" or requires_approval:
        required = "financial_kernel.journals.post"
        if not any(p in perms or p == "*" for p in [required, "financial_kernel.ledger.journals.manual"]):
            result.add(
                "missing_posting_permission",
                f"Manual posting requires {required} or financial_kernel.ledger.journals.manual",
            )
    else:
        required = "financial_kernel.journals.post"
        if required not in perms and "financial_kernel.ledger.journals.post" not in perms:
            result.add("missing_posting_permission", f"Automatic posting requires {required}")
    return result


def validate_fiscal_period(
    *,
    period_status: str | None,
    fiscal_year_status: str | None = None,
    journal_entry_type: str = "standard",
) -> ValidationResult:
    return validate_period_open(
        period_status=period_status,
        fiscal_year_status=fiscal_year_status,
        journal_entry_type=journal_entry_type,
    )


def validate_currency(
    *,
    currency: str,
    base_currency: str,
    exchange_rate: float,
) -> ValidationResult:
    result = ValidationResult(valid=True)
    if not currency or len(currency) < 3:
        result.add("invalid_currency", "Transaction currency must be a valid ISO code")
    if not base_currency or len(base_currency) < 3:
        result.add("invalid_base_currency", "Base currency must be a valid ISO code")
    if exchange_rate <= 0:
        result.add("invalid_exchange_rate", "Exchange rate must be greater than zero")
    if currency.upper() != base_currency.upper() and exchange_rate == 1.0:
        result.add(
            "stale_exchange_rate",
            "Cross-currency posting requires an explicit exchange rate",
            severity=ValidationSeverity.WARNING.value,
        )
    return result


def validate_tax_lines(
    lines: list[dict],
    *,
    valid_tax_codes: set[str] | None = None,
) -> ValidationResult:
    result = ValidationResult(valid=True)
    for idx, line in enumerate(lines):
        tax_code = line.get("tax_code")
        tax_amount = line.get("tax_amount")
        if not tax_code and tax_amount is None:
            continue
        if tax_code and valid_tax_codes and tax_code not in valid_tax_codes:
            result.add(
                "unknown_tax_code",
                f"Unknown tax code: {tax_code}",
                field=f"lines[{idx}].tax_code",
            )
        if tax_amount is not None:
            try:
                amt = float(tax_amount)
                if amt < 0:
                    result.add("negative_tax_amount", f"Line {idx + 1} has negative tax", field=f"lines[{idx}]")
            except (TypeError, ValueError):
                result.add("invalid_tax_amount", f"Line {idx + 1} has invalid tax_amount", field=f"lines[{idx}]")
    return result


def validate_budget_availability(
    lines: list[dict],
    *,
    budget_checks: list[dict],
) -> ValidationResult:
    result = ValidationResult(valid=True)
    if not budget_checks:
        return result
    lookup = {
        (b["account_code"], b.get("cost_center")): b for b in budget_checks
    }
    for idx, line in enumerate(lines):
        code = line.get("account_code", "")
        cost_center = line.get("cost_center")
        key = (code, cost_center)
        budget = lookup.get(key) or lookup.get((code, None))
        if not budget:
            continue
        amount = float(line.get("debit", 0))
        remaining = float(budget.get("remaining", 0))
        if amount > remaining:
            result.add(
                "budget_exceeded",
                f"Account {code} exceeds budget: requested {amount}, remaining {remaining}",
                field=f"lines[{idx}]",
            )
    return result


def validate_account_status(
    lines: list[dict],
    *,
    account_postable: dict[str, bool] | None,
    account_active: dict[str, bool] | None = None,
    account_status: dict[str, str] | None = None,
) -> ValidationResult:
    result = ValidationResult(valid=True)
    if account_postable:
        result = merge_validation_results(
            result, validate_accounts(lines, account_postable=account_postable)
        )
    active = account_active or {}
    status_map = account_status or {}
    for idx, line in enumerate(lines):
        code = line.get("account_code", "")
        if not code:
            continue
        if code in active and not active[code]:
            result.add("inactive_account", f"Account {code} is inactive", field=f"lines[{idx}]")
        if status_map.get(code) == "suspended":
            result.add("suspended_account", f"Account {code} is suspended", field=f"lines[{idx}]")
    return result


def validate_duplicate_posting(*, duplicate_exists: bool, idempotency_key: str | None) -> ValidationResult:
    result = ValidationResult(valid=True)
    if duplicate_exists:
        result.add(
            "duplicate_posting",
            f"Journal with idempotency key '{idempotency_key}' already exists",
        )
    return result


def validate_approval_status(
    *,
    requires_approval: bool,
    journal_status: str | None,
    posting_mode: str,
) -> ValidationResult:
    result = ValidationResult(valid=True)
    if journal_status == "rejected":
        result.add("journal_rejected", "Rejected journals cannot be posted")
    if journal_status == "posted":
        result.add("already_posted", "Journal is already posted")
    if requires_approval and posting_mode == "manual" and journal_status not in (
        "approved",
        "posted",
        None,
    ):
        if journal_status == "pending_approval":
            result.add(
                "approval_required",
                "Manual journal requires approval before posting",
            )
        elif journal_status == "draft":
            result.add(
                "approval_required",
                "Draft journal must be submitted and approved before posting",
            )
    return result


def validate_dimension_rules(
    lines: list[dict],
    *,
    dimension_lookup: dict[str, dict[str, dict]] | None,
) -> ValidationResult:
    result = ValidationResult(valid=True)
    if not dimension_lookup:
        return result
    valid, issues = validate_line_dimensions(lines, lookup=dimension_lookup)
    if not valid:
        for issue in issues:
            result.add(
                issue.get("error", "dimension_invalid"),
                f"Dimension {issue.get('dimension_type')}:{issue.get('code')} — {issue.get('error')}",
                field=f"lines[{issue.get('line_index', 0)}]",
            )
    return result


def validate_business_rules(
    lines: list[dict],
    *,
    business_rules: dict | None = None,
    account_categories: dict[str, str] | None = None,
) -> ValidationResult:
    result = ValidationResult(valid=True)
    rules = business_rules or {}
    categories = account_categories or {}
    min_amount = float(rules.get("min_transaction_amount", 0))
    blocked_accounts = set(rules.get("blocked_accounts", []))
    require_cost_center_on_expense = rules.get("require_cost_center_on_expense", False)

    total_debit = sum(float(l.get("debit", 0)) for l in lines)
    if min_amount > 0 and total_debit < min_amount:
        result.add(
            "below_min_amount",
            f"Transaction total {total_debit} is below minimum {min_amount}",
        )

    for idx, line in enumerate(lines):
        code = line.get("account_code", "")
        if code in blocked_accounts:
            result.add("blocked_account", f"Account {code} is blocked by business rule", field=f"lines[{idx}]")
        if require_cost_center_on_expense and categories.get(code) == "expense":
            dims = line.get("dimensions") or {}
            if not line.get("cost_center") and not dims.get("cost_center"):
                result.add(
                    "cost_center_required",
                    f"Expense line {idx + 1} requires cost_center dimension",
                    field=f"lines[{idx}]",
                )
    return result


def run_financial_validation(
    lines: list[dict],
    *,
    context: FinancialValidationContext,
) -> dict[str, ValidationResult]:
    ctx = context
    return {
        ValidationCheckType.BALANCED_JOURNALS.value: validate_balanced_journals(
            lines, min_lines=ctx.min_lines, journal_entry_type=ctx.journal_entry_type
        ),
        ValidationCheckType.POSTING_PERMISSIONS.value: validate_posting_permissions(
            user_permissions=ctx.user_permissions,
            posting_mode=ctx.posting_mode,
            requires_approval=ctx.requires_approval,
        ),
        ValidationCheckType.FISCAL_PERIOD.value: validate_fiscal_period(
            period_status=ctx.period_status,
            fiscal_year_status=ctx.fiscal_year_status,
            journal_entry_type=ctx.journal_entry_type,
        ),
        ValidationCheckType.CURRENCY.value: validate_currency(
            currency=ctx.currency,
            base_currency=ctx.base_currency,
            exchange_rate=ctx.exchange_rate,
        ),
        ValidationCheckType.TAX.value: validate_tax_lines(
            lines, valid_tax_codes=ctx.valid_tax_codes
        ),
        ValidationCheckType.BUDGET.value: validate_budget_availability(
            lines, budget_checks=ctx.budget_checks
        ),
        ValidationCheckType.ACCOUNT_STATUS.value: validate_account_status(
            lines,
            account_postable=ctx.account_postable,
            account_active=ctx.account_active,
            account_status=ctx.account_status,
        ),
        ValidationCheckType.DUPLICATE_POSTING.value: validate_duplicate_posting(
            duplicate_exists=ctx.duplicate_exists,
            idempotency_key=ctx.idempotency_key,
        ),
        ValidationCheckType.APPROVAL_STATUS.value: validate_approval_status(
            requires_approval=ctx.requires_approval,
            journal_status=ctx.journal_status,
            posting_mode=ctx.posting_mode,
        ),
        ValidationCheckType.DIMENSION_RULES.value: validate_dimension_rules(
            lines, dimension_lookup=ctx.dimension_lookup
        ),
        ValidationCheckType.BUSINESS_RULES.value: validate_business_rules(
            lines,
            business_rules=ctx.business_rules,
            account_categories=ctx.account_categories,
        ),
    }


def build_validation_report(check_results: dict[str, ValidationResult]) -> dict:
    checks: list[dict] = []
    all_issues: list[dict] = []
    valid = True
    error_count = 0
    warning_count = 0

    for check_type, result in check_results.items():
        passed = result.valid
        if not passed:
            valid = False
        issues = [
            {
                "code": i.code,
                "message": i.message,
                "severity": i.severity,
                "field": i.field,
                "check": check_type,
            }
            for i in result.issues
        ]
        checks.append(
            {
                "check": check_type,
                "label": VALIDATION_CATALOG.get(check_type, {}).get("label", check_type),
                "passed": passed,
                "issue_count": len(issues),
                "issues": issues,
            }
        )
        all_issues.extend(issues)
        error_count += sum(1 for i in issues if i["severity"] == ValidationSeverity.ERROR.value)
        warning_count += sum(1 for i in issues if i["severity"] == ValidationSeverity.WARNING.value)

    passed_checks = sum(1 for c in checks if c["passed"])
    return {
        "valid": valid,
        "can_post": valid and error_count == 0,
        "checks": checks,
        "issues": all_issues,
        "summary": {
            "total_checks": len(checks),
            "passed_checks": passed_checks,
            "failed_checks": len(checks) - passed_checks,
            "error_count": error_count,
            "warning_count": warning_count,
        },
    }


def reject_if_invalid(report: dict) -> tuple[bool, str]:
    if report.get("can_post"):
        return True, ""
    issues = report.get("issues", [])
    errors = [i for i in issues if i.get("severity") != ValidationSeverity.WARNING.value]
    if errors:
        first = errors[0]
        return False, f"financial_kernel.errors.validation.{first['check']}.{first['code']}"
    return False, "financial_kernel.errors.validation.failed"


def run_full_validation(
    lines: list[dict],
    *,
    context: FinancialValidationContext,
) -> dict:
    check_results = run_financial_validation(lines, context=context)
    if context.locked_resources and context.resource_key:
        lock_result = validate_financial_lock(
            locked_resources=context.locked_resources,
            resource_key=context.resource_key,
        )
        check_results[ValidationCheckType.BUSINESS_RULES.value] = merge_validation_results(
            check_results[ValidationCheckType.BUSINESS_RULES.value],
            lock_result,
        )
    entry_type_result = validate_journal_entry_type(
        lines,
        journal_entry_type=context.journal_entry_type,
        account_categories=context.account_categories,
    )
    check_results[ValidationCheckType.BUSINESS_RULES.value] = merge_validation_results(
        check_results[ValidationCheckType.BUSINESS_RULES.value],
        entry_type_result,
    )
    return build_validation_report(check_results)
