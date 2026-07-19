"""Federation quality / DoD read queries (P200-B12)."""
from __future__ import annotations

from contexts.identity_federation.domain.services.federation_quality_platform import (
    get_federation_quality_platform,
)


def handle_get_qa_surface() -> dict:
    return get_federation_quality_platform().surface()


def handle_get_quality_gates() -> dict:
    return get_federation_quality_platform().quality_gates()


def handle_get_dod_checklist() -> dict:
    return get_federation_quality_platform().dod_checklist()


def handle_get_traceability() -> dict:
    return get_federation_quality_platform().traceability()


def handle_get_testing_catalog() -> dict:
    return get_federation_quality_platform().testing_catalog()


def handle_get_governance() -> dict:
    return get_federation_quality_platform().governance()


def handle_get_compliance_validation() -> dict:
    return get_federation_quality_platform().compliance_validation()


def handle_get_production_readiness() -> dict:
    return get_federation_quality_platform().production_readiness()


def handle_get_qa_metrics() -> dict:
    return get_federation_quality_platform().metrics_snapshot()
