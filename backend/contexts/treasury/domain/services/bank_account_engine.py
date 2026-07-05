"""Enterprise Bank Account Management engine."""
from __future__ import annotations

import re

from contexts.treasury.domain.aggregates.bank_account import (
    BankAccountStatus,
    BankAccountType,
    BankDocumentType,
)

_IBAN_PATTERN = re.compile(r"^[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}$")
_SWIFT_PATTERN = re.compile(r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$")
_ROUTING_PATTERN = re.compile(r"^[0-9]{9}$")

BANK_ACCOUNT_CATALOG: dict[str, dict] = {
    "unlimited_banks": {"label": "Unlimited Banks", "limit": None},
    "unlimited_branches": {"label": "Unlimited Branches", "limit": None},
    "unlimited_accounts": {"label": "Unlimited Bank Accounts", "limit": None},
    "account_types": {
        "label": "Account Types",
        "values": [t.value for t in BankAccountType],
    },
    "identifiers": {
        "label": "Bank Identifiers",
        "fields": ["iban", "swift_bic", "routing_number"],
    },
    "multi_currency": {"label": "Multi Currency", "supported": True},
    "authorized_signatories": {"label": "Authorized Signatories", "supported": True},
    "approval_workflow": {"label": "Approval Workflow", "supported": True},
    "bank_documents": {"label": "Bank Documents", "types": [d.value for d in BankDocumentType]},
    "account_status": {
        "label": "Account Status",
        "values": [s.value for s in BankAccountStatus],
    },
    "multi_tenant": {"label": "Multi Tenant", "supported": True},
    "multi_organization": {"label": "Multi Organization", "supported": True},
    "secure_masking": {"label": "Secure Field Masking", "fields": ["iban", "account_number", "routing_number"]},
}


def list_bank_account_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in BANK_ACCOUNT_CATALOG.items()]


def validate_iban(iban: str | None) -> tuple[bool, str | None]:
    if not iban:
        return True, None
    normalized = iban.strip().upper().replace(" ", "")
    if not _IBAN_PATTERN.match(normalized):
        return False, "invalid_iban_format"
    return True, None


def validate_swift(swift: str | None) -> tuple[bool, str | None]:
    if not swift:
        return True, None
    normalized = swift.strip().upper()
    if not _SWIFT_PATTERN.match(normalized):
        return False, "invalid_swift_format"
    return True, None


def validate_routing_number(routing: str | None) -> tuple[bool, str | None]:
    if not routing:
        return True, None
    if not _ROUTING_PATTERN.match(routing.strip()):
        return False, "invalid_routing_number"
    return True, None


def validate_account_identifiers(
    *,
    iban: str | None = None,
    swift_bic: str | None = None,
    routing_number: str | None = None,
) -> list[str]:
    errors: list[str] = []
    ok, err = validate_iban(iban)
    if not ok and err:
        errors.append(err)
    ok, err = validate_swift(swift_bic)
    if not ok and err:
        errors.append(err)
    ok, err = validate_routing_number(routing_number)
    if not ok and err:
        errors.append(err)
    return errors


def assert_account_type(account_type: str) -> None:
    if account_type not in {t.value for t in BankAccountType}:
        raise ValueError("invalid_account_type")


def can_transition(current: str, action: str) -> bool:
    transitions: dict[str, set[str]] = {
        BankAccountStatus.DRAFT.value: {"submit", "approve"},
        BankAccountStatus.PENDING_APPROVAL.value: {"approve", "reject"},
        BankAccountStatus.ACTIVE.value: {"suspend", "freeze", "close"},
        BankAccountStatus.SUSPENDED.value: {"freeze", "close", "approve"},
        BankAccountStatus.FROZEN.value: {"close"},
    }
    return action in transitions.get(current, set())
