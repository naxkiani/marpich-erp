"""Enterprise Posting Rule Engine — all module postings flow through here."""
from __future__ import annotations

from dataclasses import dataclass

from contexts.financial_kernel.domain.aggregates.posting_rules import (
    PLATFORM_POSTING_RULES,
    AccountSlot,
    ConfigurablePostingRule,
    LineTemplate,
    PostingPattern,
    PostingRuleDefinition,
)
from contexts.financial_kernel.domain.services.double_entry_posting_engine import POSTING_RULES


def _line(side: str, account_slot: str, amount_field: str = "amount") -> LineTemplate:
    return LineTemplate(side=side, account_slot=account_slot, amount_field=amount_field)


@dataclass(frozen=True, slots=True)
class PostingExecutionContext:
    amount: float
    account_mappings: dict[str, str]
    description: str = ""
    dimensions: dict[str, str] | None = None
    tax_amount: float | None = None
    extra_amounts: dict[str, float] | None = None
    lines: list[dict] | None = None


@dataclass(frozen=True, slots=True)
class RuleBuilderInput:
    rule_id: str
    label: str
    module: str
    journal_type: str = "general"
    pattern: str = PostingPattern.DEBIT_CREDIT.value
    account_slots: dict | None = None
    line_templates: list[dict] | None = None
    approval_required: bool = False
    tax_amount_field: str | None = None
    tax_account_slot: str | None = None
    dimensions: list[str] | None = None
    description: str = ""


def get_platform_rule(rule_id: str) -> PostingRuleDefinition:
    rule = PLATFORM_POSTING_RULES.get(rule_id)
    if not rule:
        raise KeyError(f"unknown_posting_rule:{rule_id}")
    return rule


def resolve_rule(
    rule_id: str,
    *,
    tenant_rules: list[ConfigurablePostingRule] | None = None,
) -> PostingRuleDefinition:
    for custom in tenant_rules or []:
        if custom.rule_id == rule_id and custom.is_active:
            return custom.to_definition()
    if rule_id in PLATFORM_POSTING_RULES:
        return get_platform_rule(rule_id)
    if rule_id in POSTING_RULES:
        meta = POSTING_RULES[rule_id]
        return PostingRuleDefinition(
            rule_id=rule_id,
            label=meta["description"],
            module="legacy",
            journal_type="general",
            account_slots=(
                AccountSlot("debit", "Debit account", role=meta.get("debit_role")),
                AccountSlot("credit", "Credit account", role=meta.get("credit_role")),
            ),
            line_templates=(_line("debit", "debit"), _line("credit", "credit")),
            description=meta["description"],
        )
    raise KeyError(f"unknown_posting_rule:{rule_id}")


def list_platform_posting_rules() -> list[dict]:
    return [_rule_summary(rule) for rule in PLATFORM_POSTING_RULES.values()]


def list_all_posting_rules(
    *,
    tenant_rules: list[ConfigurablePostingRule] | None = None,
) -> list[dict]:
    platform = list_platform_posting_rules()
    custom = [r.to_dict() for r in (tenant_rules or []) if r.is_active]
    return platform + custom


def _rule_summary(rule: PostingRuleDefinition) -> dict:
    return {
        "rule_id": rule.rule_id,
        "label": rule.label,
        "module": rule.module,
        "journal_type": rule.journal_type,
        "pattern": rule.pattern,
        "approval_required": rule.approval_required,
        "account_slots": [
            {
                "slot": s.slot,
                "label": s.label,
                "account_key": s.account_key,
                "role": s.role,
                "required": s.required,
            }
            for s in rule.account_slots
        ],
        "line_templates": [
            {
                "side": t.side,
                "account_slot": t.account_slot,
                "amount_field": t.amount_field,
            }
            for t in rule.line_templates
        ],
        "dimensions": list(rule.dimensions),
        "description": rule.description,
        "is_platform": rule.is_platform,
    }


def get_rule_detail(rule: PostingRuleDefinition) -> dict:
    detail = _rule_summary(rule)
    detail["tax_amount_field"] = rule.tax_amount_field
    detail["tax_account_slot"] = rule.tax_account_slot
    return detail


def validate_rule_builder_input(data: RuleBuilderInput) -> tuple[bool, str]:
    if not data.rule_id or not data.label:
        return False, "rule_id_and_label_required"
    if data.pattern == PostingPattern.EXPLICIT_LINES.value:
        return True, ""
    if not data.account_slots:
        return False, "account_slots_required"
    if not data.line_templates:
        return False, "line_templates_required"
    slot_names = set(data.account_slots.keys())
    for template in data.line_templates:
        if template.get("account_slot") not in slot_names:
            return False, f"unknown_account_slot:{template.get('account_slot')}"
        if template.get("side") not in ("debit", "credit"):
            return False, "invalid_line_side"
    return True, ""


def build_rule_from_builder(
    tenant_id: str,
    data: RuleBuilderInput,
) -> ConfigurablePostingRule:
    ok, reason = validate_rule_builder_input(data)
    if not ok:
        raise ValueError(reason)
    return ConfigurablePostingRule.create(
        tenant_id=tenant_id,
        rule_id=data.rule_id,
        label=data.label,
        module=data.module,
        journal_type=data.journal_type,
        pattern=data.pattern,
        account_slots=data.account_slots or {},
        line_templates=data.line_templates or [],
        approval_required=data.approval_required,
        tax_amount_field=data.tax_amount_field,
        tax_account_slot=data.tax_account_slot,
        dimensions=data.dimensions,
        description=data.description,
    )


def validate_posting_context(
    rule: PostingRuleDefinition,
    context: PostingExecutionContext,
) -> tuple[bool, str]:
    if rule.pattern == PostingPattern.EXPLICIT_LINES.value:
        if not context.lines:
            return False, "explicit_lines_required"
        return True, ""

    if context.amount <= 0:
        return False, "amount_must_be_positive"

    for slot in rule.account_slots:
        if slot.required and slot.slot not in context.account_mappings:
            return False, f"missing_account_slot:{slot.slot}"

    if rule.tax_amount_field and context.tax_amount is not None:
        if context.tax_amount < 0:
            return False, "tax_amount_invalid"

    return True, ""


def _resolve_amount(
    field: str,
    context: PostingExecutionContext,
) -> float:
    if field == "amount":
        return round(context.amount, 2)
    if context.extra_amounts and field in context.extra_amounts:
        return round(float(context.extra_amounts[field]), 2)
    if field == "tax_amount" and context.tax_amount is not None:
        return round(context.tax_amount, 2)
    return round(context.amount, 2)


def build_lines_from_rule(
    rule: PostingRuleDefinition,
    context: PostingExecutionContext,
) -> list[dict]:
    ok, reason = validate_posting_context(rule, context)
    if not ok:
        raise ValueError(reason)

    if rule.pattern == PostingPattern.EXPLICIT_LINES.value:
        lines = [dict(line) for line in (context.lines or [])]
        for line in lines:
            line["posting_rule_id"] = rule.rule_id
        return lines

    dims = {
        k: v for k, v in (context.dimensions or {}).items() if k in rule.dimensions or not rule.dimensions
    }
    lines: list[dict] = []

    for template in rule.line_templates:
        account_code = context.account_mappings[template.account_slot]
        amt = _resolve_amount(template.amount_field, context)
        line = {
            "account_code": account_code,
            "debit": amt if template.side == "debit" else 0,
            "credit": amt if template.side == "credit" else 0,
            "description": context.description or template.description,
            "posting_rule_id": rule.rule_id,
            **dims,
        }
        lines.append(line)

    if rule.tax_amount_field and context.tax_amount and rule.tax_account_slot:
        tax_amt = round(context.tax_amount, 2)
        if tax_amt > 0:
            tax_account = context.account_mappings[rule.tax_account_slot]
            lines.append(
                {
                    "account_code": tax_account,
                    "debit": 0,
                    "credit": tax_amt,
                    "description": f"{context.description} (tax)".strip(),
                    "posting_rule_id": rule.rule_id,
                    **dims,
                }
            )
            debit_slot = next((s.slot for s in rule.account_slots if s.role == "expense"), "debit")
            if debit_slot in context.account_mappings:
                lines.append(
                    {
                        "account_code": context.account_mappings[debit_slot],
                        "debit": tax_amt,
                        "credit": 0,
                        "description": f"{context.description} (tax expense)".strip(),
                        "posting_rule_id": rule.rule_id,
                        **dims,
                    }
                )

    return lines


def preview_posting_rule(
    rule: PostingRuleDefinition,
    context: PostingExecutionContext,
) -> dict:
    try:
        lines = build_lines_from_rule(rule, context)
    except ValueError as exc:
        return {"valid": False, "error": str(exc), "lines": []}
    total_debit = round(sum(float(l.get("debit", 0)) for l in lines), 2)
    total_credit = round(sum(float(l.get("credit", 0)) for l in lines), 2)
    return {
        "valid": total_debit == total_credit,
        "rule_id": rule.rule_id,
        "journal_type": rule.journal_type,
        "lines": lines,
        "total_debit": total_debit,
        "total_credit": total_credit,
        "is_balanced": total_debit == total_credit,
    }


def resolve_default_account_mappings(
    rule: PostingRuleDefinition,
    *,
    account_key_resolver: dict[str, str],
) -> dict[str, str]:
    """Resolve slot -> account_code from COA account keys."""
    mappings: dict[str, str] = {}
    for slot in rule.account_slots:
        if slot.account_key and slot.account_key in account_key_resolver:
            mappings[slot.slot] = account_key_resolver[slot.account_key]
    return mappings
