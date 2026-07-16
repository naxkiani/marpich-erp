"""Permission Registry engine."""
from __future__ import annotations

import re

from contexts.permission_registry.domain.aggregates.permission_registry_platform import RegistryCapability

PERMISSION_CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*\.[a-z][a-z0-9_.]*$")

POLICY_KEYS = [
    "permission_registry.module_registration.enabled",
    "permission_registry.custom_roles.enabled",
    "permission_registry.binding.expiry.enabled",
]

CAPABILITY_LABELS = {
    RegistryCapability.PERMISSION_CATALOG.value: "Permission Catalog",
    RegistryCapability.MODULE_REGISTRATION.value: "Module Registration",
    RegistryCapability.ROLE_MANAGEMENT.value: "Role Management",
    RegistryCapability.ROLE_BINDING.value: "Role Binding",
    RegistryCapability.PERMISSION_SETS.value: "Permission Sets",
    RegistryCapability.PRINCIPAL_RESOLUTION.value: "Principal Resolution",
    RegistryCapability.NAMESPACE_GOVERNANCE.value: "Namespace Governance",
    RegistryCapability.POLICY_DRIVEN_REGISTRY.value: "Policy-Driven Registry",
    RegistryCapability.REGISTRY_DASHBOARD.value: "Registry Dashboard",
    RegistryCapability.REGISTRY_API.value: "Registry API",
}


def list_capability_catalog() -> list[dict]:
    return [
        {"capability": c.value, "label": CAPABILITY_LABELS.get(c.value, c.name.replace("_", " ").title())}
        for c in RegistryCapability
    ]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def dependency_map() -> dict:
    return {
        "nodes": [
            {"id": "permission_registry", "type": "platform", "label": "Permission Registry"},
            {"id": "identity", "type": "platform", "label": "Identity"},
            {"id": "authorization", "type": "platform", "label": "Authorization PDP"},
        ],
        "edges": [
            {"from": "permission_registry", "to": "identity", "type": "role_sync_delegate"},
            {"from": "authorization", "to": "permission_registry", "type": "catalog_delegate"},
        ],
    }


def parse_permission_code(code: str) -> tuple[str, str, str] | None:
    if not PERMISSION_CODE_PATTERN.match(code):
        return None
    module, resource, action = code.split(".", 2)
    return module, resource, action


def validate_permission_codes(codes: list[str]) -> tuple[list[str], list[str]]:
    valid: list[str] = []
    invalid: list[str] = []
    for code in codes:
        if parse_permission_code(code):
            valid.append(code.lower())
        else:
            invalid.append(code)
    return valid, invalid


def validate_role_permissions(
    permission_codes: list[str],
    catalog_codes: set[str],
) -> tuple[bool, list[str]]:
    missing = [c for c in permission_codes if c != "*" and c not in catalog_codes]
    return len(missing) == 0, missing


def build_dashboard(
    *,
    profile: dict | None,
    permissions: list[dict],
    roles: list[dict],
    bindings: list[dict],
    sets: list[dict],
) -> dict:
    modules = sorted({p.get("module") for p in permissions})
    return {
        "summary": {
            "capabilities": len(RegistryCapability),
            "permissions": len(permissions),
            "roles": len(roles),
            "bindings": len(bindings),
            "permission_sets": len(sets),
            "modules": len(modules),
        },
        "modules": modules,
        "profile": profile,
        "capabilities": list_capability_catalog(),
    }


def generate_seed_data() -> dict:
    return {
        "permissions": [
            {"code": "banking.accounts.read", "description": "Read bank accounts"},
            {"code": "banking.accounts.write", "description": "Manage bank accounts"},
            {"code": "banking.transfers.initiate", "description": "Initiate transfers"},
            {"code": "exchange.fx.read", "description": "Read FX rates"},
            {"code": "exchange.fx.trade", "description": "Execute FX trades"},
            {"code": "tax.returns.file", "description": "File tax returns"},
            {"code": "erp.inventory.read", "description": "Read inventory"},
            {"code": "hospital.patients.read", "description": "Read patient records"},
            {"code": "university.enrollment.manage", "description": "Manage enrollment"},
            {"code": "permissions.roles.write", "description": "Manage roles in registry"},
        ],
        "roles": [
            {
                "code": "treasury_operator",
                "name": "Treasury Operator",
                "description": "Banking and FX operations",
                "permission_codes": [
                    "banking.accounts.read",
                    "banking.transfers.initiate",
                    "exchange.fx.read",
                ],
            },
            {
                "code": "tax_analyst",
                "name": "Tax Analyst",
                "description": "Tax filing and reporting",
                "permission_codes": ["tax.returns.file"],
            },
        ],
        "permission_sets": [
            {
                "module": "banking",
                "name": "Banking Module Bundle",
                "description": "Default banking permissions",
                "permission_codes": [
                    "banking.accounts.read",
                    "banking.accounts.write",
                    "banking.transfers.initiate",
                ],
            },
        ],
    }
