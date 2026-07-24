"""ACL: Secrets Cryptographic Trust ↔ peers (P209)."""
from __future__ import annotations

from typing import Any


def to_pam_ref(*, tenant_id: str, secret_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "secret_ref": secret_ref,
        "pam_orchestrates_refs_only": True,
        "material_stays_in_secrets": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    return {
        "target": "audit",
        "tenant_id": tenant_id,
        "action": action,
        "resource_ref": resource_ref,
        "immutable_crypto_trail": True,
        "trust_relationships_audited": True,
    }


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    return {
        "target": "ai",
        "tenant_id": tenant_id,
        "surface": surface,
        "context": dict(context),
        "via_ai_platform": True,
        "advisor_not_authority": True,
        "embeds_llm_forbidden": True,
    }


def to_hsm(*, tenant_id: str, operation: str, key_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "operation": operation,
        "key_ref": key_ref,
        "hsm_required": True,
        "via_integration_connector": True,
        "fips_140_3": True,
        "peer_ids_only": True,
    }


def to_spiffe(*, tenant_id: str, workload_ref: str, spiffe_id: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "workload_ref": workload_ref,
        "spiffe_id": spiffe_id,
        "verifiable_workload_identity": True,
        "mtls_required": True,
        "peer_ids_only": True,
    }


def to_compliance(*, tenant_id: str, assessment_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "assessment_ref": assessment_ref,
        "via_compliance_framework": True,
        "peer_ids_only": True,
    }


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": [
            "pam",
            "audit",
            "ai",
            "hsm",
            "spiffe",
            "compliance",
            "integration",
        ],
        "plaintext_forbidden": True,
        "hsm_required": True,
        "pam_orchestrates_refs_only": True,
        "via_ai_platform": True,
        "via_audit_platform": True,
    }
