"""Provider-centric identity mapping pipeline (P200-B7)."""
from __future__ import annotations

from contexts.identity_federation.domain.services import claims_transformation_engine


def apply_mapping_pipeline(
    *,
    source_claims: dict,
    rules: list[dict],
    validate: bool = True,
) -> dict:
    """Transform → validate → explain. No peer-domain imports."""
    mapped = claims_transformation_engine.transform_claims(
        raw_claims=source_claims, mappings=rules
    )
    errors: list[str] = []
    if validate:
        for rule in rules:
            source = rule.get("source") or rule.get("source_claim")
            target = rule.get("target") or rule.get("target_claim")
            if not source or not target:
                errors.append("mapping.rule_incomplete")
            elif source not in source_claims and source not in mapped:
                errors.append(f"mapping.missing_source:{source}")
    return {
        "mapped_claims": mapped if isinstance(mapped, dict) else {"result": mapped},
        "rule_count": len(rules),
        "validation_errors": errors,
        "valid": not errors,
        "auditable": True,
    }


def catalog() -> dict:
    return {
        "pipeline": ["normalize", "transform", "validate", "audit"],
        "rules": ["direct", "rename", "concat", "constant", "regex"],
        "duplicate_resolution": "prefer_existing_link",
    }
