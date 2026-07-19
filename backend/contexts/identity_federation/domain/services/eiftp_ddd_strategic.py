"""EIFTP DDD Strategic Design (P200-B3) — catalog + model gates."""
from __future__ import annotations

from pathlib import Path

import yaml

from contexts.identity_federation.domain.strategic.context_map import has_circular_dependency
from contexts.identity_federation.domain.strategic.event_ownership import EVENT_OWNERSHIP
from contexts.identity_federation.domain.strategic.ubiquitous_language import CORE_DOMAINS

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/217-enterprise-identity-federation-trust-ddd-strategic.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_TRUST_DDD_STRATEGIC.md",
    "docs/architecture/identity/eiftp/DDD_DOMAIN_CATALOG.v1.yaml",
    "docs/architecture/identity/eiftp/DDD_BOUNDED_CONTEXT_MAP.v1.yaml",
    "docs/architecture/identity/eiftp/DDD_CONTEXT_MAPPING.v1.yaml",
    "docs/architecture/identity/eiftp/DDD_UBIQUITOUS_LANGUAGE.v1.yaml",
    "docs/architecture/identity/eiftp/DDD_AGGREGATE_CATALOG.v1.yaml",
    "docs/architecture/identity/eiftp/DDD_EVENT_MATRIX.v1.yaml",
    "docs/architecture/identity/eiftp/DDD_RESPONSIBILITY_MATRIX.v1.yaml",
    "docs/architecture/identity/eiftp/DDD_INTEGRATION_MATRIX.v1.yaml",
    "docs/architecture/identity/eiftp/DDD_GOVERNANCE_MODEL.v1.yaml",
    "backend/contexts/identity_federation/domain/strategic/ubiquitous_language.py",
    "backend/contexts/identity_federation/domain/strategic/event_ownership.py",
    "backend/contexts/identity_federation/domain/strategic/context_map.py",
    "backend/contexts/identity_federation/infrastructure/acl/__init__.py",
]

EXPECTED_DOMAIN_COUNT = 20
FORBIDDEN_SIBLING = "backend/contexts/eiftp"


def validate_ddd_strategic_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = (root / FORBIDDEN_SIBLING).exists()
    circular = has_circular_dependency()

    catalog_path = root / "docs/architecture/identity/eiftp/DDD_DOMAIN_CATALOG.v1.yaml"
    domain_count = 0
    core_ids: list[str] = []
    if catalog_path.exists():
        data = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
        domains = data.get("domains") or []
        domain_count = len(domains)
        core_ids = [d["id"] for d in domains if d.get("type") == "core"]

    authz_separate = True
    mapping_path = root / "docs/architecture/identity/eiftp/DDD_CONTEXT_MAPPING.v1.yaml"
    if mapping_path.exists():
        mapping = yaml.safe_load(mapping_path.read_text(encoding="utf-8"))
        types = {r.get("type") for r in mapping.get("relationships") or []}
        authz_separate = "separate_ways" in types

    passed = (
        not missing
        and not sibling
        and not circular
        and domain_count >= EXPECTED_DOMAIN_COUNT
        and set(core_ids) == set(CORE_DOMAINS)
        and authz_separate
        and len(EVENT_OWNERSHIP) >= 17
    )
    return {
        "prompt": "P200-B3",
        "adr": 217,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "circular_dependency": circular,
        "domain_count": domain_count,
        "core_domains": core_ids,
        "event_ownership_count": len(EVENT_OWNERSHIP),
        "foundation_for": "P200-B4",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
