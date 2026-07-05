"""Enterprise Double Entry Validation Engine."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ValidationSeverity(StrEnum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    message: str
    severity: str = ValidationSeverity.ERROR.value
    field: str | None = None


@dataclass
class ValidationResult:
    valid: bool
    issues: list[ValidationIssue] = field(default_factory=list)
    total_debit: float = 0.0
    total_credit: float = 0.0
    balance_delta: float = 0.0
    line_count: int = 0
    is_balanced: bool = False
    is_compound: bool = False

    def add(self, code: str, message: str, *, severity: str = ValidationSeverity.ERROR.value, field: str | None = None) -> None:
        self.issues.append(ValidationIssue(code=code, message=message, severity=severity, field=field))
        if severity == ValidationSeverity.ERROR.value:
            self.valid = False

    def to_dict(self) -> dict:
        return {
            "valid": self.valid,
            "is_balanced": self.is_balanced,
            "is_compound": self.is_compound,
            "total_debit": self.total_debit,
            "total_credit": self.total_credit,
            "balance_delta": self.balance_delta,
            "line_count": self.line_count,
            "issues": [
                {"code": i.code, "message": i.message, "severity": i.severity, "field": i.field}
                for i in self.issues
            ],
        }


@dataclass(frozen=True, slots=True)
class PostingValidationContext:
    tenant_id: str
    period_status: str | None = None
    fiscal_year_status: str | None = None
    account_postable: dict[str, bool] | None = None
    account_categories: dict[str, str] | None = None
    locked_resources: set[str] | None = None
    resource_key: str | None = None
    journal_entry_type: str = "standard"
    intercompany_pair_id: str | None = None
    requires_approval: bool = False
    min_lines: int = 2


def compute_totals(lines: list[dict]) -> tuple[float, float]:
    total_debit = 0.0
    total_credit = 0.0
    for line in lines:
        total_debit += float(line.get("debit", 0))
        total_credit += float(line.get("credit", 0))
    return round(total_debit, 2), round(total_credit, 2)


def validate_double_entry_balance(lines: list[dict]) -> ValidationResult:
    """Core law: Debit Total must equal Credit Total."""
    result = ValidationResult(valid=True)
    if not lines:
        result.add("empty_lines", "Journal must contain at least one line")
        return result

    total_debit, total_credit = compute_totals(lines)
    result.total_debit = total_debit
    result.total_credit = total_credit
    result.balance_delta = round(total_debit - total_credit, 2)
    result.line_count = len(lines)
    result.is_compound = len(lines) > 2
    result.is_balanced = result.balance_delta == 0

    if total_debit == 0 and total_credit == 0:
        result.add("zero_amount", "Journal total must be greater than zero")

    if not result.is_balanced:
        result.add(
            "unbalanced",
            f"Debit total ({total_debit}) must equal credit total ({total_credit}); "
            f"delta={result.balance_delta}",
        )

    return result


def validate_line_structure(lines: list[dict], *, min_lines: int = 2) -> ValidationResult:
    result = ValidationResult(valid=True)
    if len(lines) < min_lines:
        result.add("insufficient_lines", f"Double entry requires at least {min_lines} lines")

    for idx, line in enumerate(lines):
        code = line.get("account_code", "")
        if not code:
            result.add("missing_account_code", f"Line {idx + 1} missing account_code", field=f"lines[{idx}]")
        debit = float(line.get("debit", 0))
        credit = float(line.get("credit", 0))
        if debit < 0 or credit < 0:
            result.add("negative_amount", f"Line {idx + 1} has negative amount", field=f"lines[{idx}]")
        if debit > 0 and credit > 0:
            result.add(
                "debit_and_credit_on_same_line",
                f"Line {idx + 1} cannot have both debit and credit",
                field=f"lines[{idx}]",
            )
        if debit == 0 and credit == 0:
            result.add("zero_line", f"Line {idx + 1} must have debit or credit", field=f"lines[{idx}]")

    return result


def validate_accounts(
    lines: list[dict],
    *,
    account_postable: dict[str, bool],
) -> ValidationResult:
    result = ValidationResult(valid=True)
    for idx, line in enumerate(lines):
        code = line.get("account_code", "")
        if not code:
            continue
        if code not in account_postable:
            result.add("unknown_account", f"Unknown account: {code}", field=f"lines[{idx}]")
            continue
        if not account_postable[code]:
            result.add("non_posting_account", f"Account {code} does not accept GL posting", field=f"lines[{idx}]")
    return result


def validate_period_open(
    *,
    period_status: str | None,
    fiscal_year_status: str | None = None,
    journal_entry_type: str = "standard",
    is_adjustment_period: bool = False,
) -> ValidationResult:
    from contexts.financial_kernel.domain.services.fiscal_calendar_engine import (
        validate_period_for_posting,
    )

    result = ValidationResult(valid=True)
    if period_status:
        ok, code = validate_period_for_posting(
            period_status=period_status,
            journal_entry_type=journal_entry_type,
            is_adjustment_period=is_adjustment_period,
        )
        if not ok:
            result.add(code, f"Posting forbidden: {code}")
    if fiscal_year_status == "closed":
        result.add("fiscal_year_closed", "Posting to closed fiscal year is forbidden")
    return result


def validate_financial_lock(
    *,
    locked_resources: set[str] | None,
    resource_key: str | None,
) -> ValidationResult:
    result = ValidationResult(valid=True)
    if locked_resources and resource_key and resource_key in locked_resources:
        result.add("resource_locked", f"Resource {resource_key} is financially locked")
    return result


def validate_journal_entry_type(
    lines: list[dict],
    *,
    journal_entry_type: str,
    account_categories: dict[str, str] | None = None,
) -> ValidationResult:
    result = ValidationResult(valid=True)
    categories = account_categories or {}

    if journal_entry_type == "closing":
        has_revenue_or_expense = any(
            categories.get(line.get("account_code", "")) in ("revenue", "expense")
            for line in lines
        )
        if not has_revenue_or_expense:
            result.add(
                "closing_missing_pl_accounts",
                "Closing entry must include revenue or expense accounts",
                severity=ValidationSeverity.WARNING.value,
            )

    if journal_entry_type == "opening_balance":
        for idx, line in enumerate(lines):
            if not line.get("opening_balance"):
                result.add(
                    "opening_balance_flag",
                    f"Line {idx + 1} should be flagged as opening balance",
                    severity=ValidationSeverity.WARNING.value,
                    field=f"lines[{idx}]",
                )

    if journal_entry_type == "intercompany":
        pair_ids = {line.get("intercompany_pair_id") for line in lines if line.get("intercompany_pair_id")}
        org_ids = {line.get("organization_id") for line in lines if line.get("organization_id")}
        if not pair_ids:
            result.add(
                "intercompany_missing_pair",
                "Intercompany entry must include intercompany_pair_id",
            )
        if not org_ids:
            result.add(
                "intercompany_missing_org",
                "Intercompany entry lines must include organization_id",
            )

    return result


def validate_posting_rules(
    lines: list[dict],
    *,
    rule_id: str | None,
    allowed_rules: set[str] | None = None,
) -> ValidationResult:
    result = ValidationResult(valid=True)
    if rule_id and allowed_rules and rule_id not in allowed_rules:
        result.add("unknown_posting_rule", f"Posting rule '{rule_id}' is not registered")
    return result


def merge_validation_results(*results: ValidationResult) -> ValidationResult:
    merged = ValidationResult(valid=True)
    for r in results:
        if not r.valid:
            merged.valid = False
        merged.issues.extend(r.issues)
        if r.total_debit or r.total_credit:
            merged.total_debit = r.total_debit
            merged.total_credit = r.total_credit
            merged.balance_delta = r.balance_delta
            merged.line_count = r.line_count
            merged.is_balanced = r.is_balanced
            merged.is_compound = r.is_compound
    if merged.total_debit != merged.total_credit:
        merged.is_balanced = False
    elif merged.total_debit > 0:
        merged.is_balanced = True
    return merged


def run_posting_validation(
    lines: list[dict],
    *,
    context: PostingValidationContext | None = None,
) -> ValidationResult:
    """Full automatic validation chain before posting."""
    ctx = context or PostingValidationContext(tenant_id="")
    min_lines = 1 if ctx.journal_entry_type == "single_entry" else ctx.min_lines

    results = [
        validate_line_structure(lines, min_lines=min_lines),
        validate_double_entry_balance(lines),
    ]

    if ctx.account_postable:
        results.append(validate_accounts(lines, account_postable=ctx.account_postable))

    if ctx.period_status or ctx.fiscal_year_status:
        results.append(
            validate_period_open(
                period_status=ctx.period_status,
                fiscal_year_status=ctx.fiscal_year_status,
                journal_entry_type=ctx.journal_entry_type,
            )
        )

    if ctx.locked_resources and ctx.resource_key:
        results.append(
            validate_financial_lock(
                locked_resources=ctx.locked_resources,
                resource_key=ctx.resource_key,
            )
        )

    results.append(
        validate_journal_entry_type(
            lines,
            journal_entry_type=ctx.journal_entry_type,
            account_categories=ctx.account_categories,
        )
    )

    return merge_validation_results(*results)


def validate_journal_lines(lines: list[dict]) -> tuple[bool, str]:
    """Backward-compatible balance check used by legacy callers."""
    result = validate_double_entry_balance(lines)
    if result.valid:
        return True, "valid"
    first = result.issues[0] if result.issues else ValidationIssue("invalid", "invalid")
    return False, first.code


def build_posting_preview(
    lines: list[dict],
    *,
    context: PostingValidationContext | None = None,
    currency: str = "USD",
    base_currency: str = "USD",
) -> dict:
    validation = run_posting_validation(lines, context=context)
    total_debit, total_credit = compute_totals(lines)
    return {
        "validation": validation.to_dict(),
        "preview": {
            "lines": lines,
            "currency": currency,
            "base_currency": base_currency,
            "total_debit": total_debit,
            "total_credit": total_credit,
            "is_balanced": total_debit == total_credit,
            "is_compound": len(lines) > 2,
            "journal_entry_type": context.journal_entry_type if context else "standard",
            "requires_approval": context.requires_approval if context else False,
        },
        "can_post": validation.valid,
    }
