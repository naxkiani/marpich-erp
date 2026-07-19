"""Federation ops read queries (P200-B11)."""
from __future__ import annotations

from contexts.identity_federation.domain.services.federation_ops_platform import (
    get_federation_ops_platform,
)


def handle_get_ops_surface() -> dict:
    return get_federation_ops_platform().surface()


def handle_get_deployment_profile() -> dict:
    return get_federation_ops_platform().deployment_profile()


def handle_get_pipeline_profile() -> dict:
    return get_federation_ops_platform().pipeline_profile()


def handle_get_observability_profile() -> dict:
    return get_federation_ops_platform().observability_profile()


def handle_get_slo_status(*, availability_ratio: float | None = None) -> dict:
    return get_federation_ops_platform().slo_status(
        availability_ratio=availability_ratio
    )


def handle_get_dr_profile() -> dict:
    return get_federation_ops_platform().dr_profile()


def handle_get_ops_health() -> dict:
    return get_federation_ops_platform().health()


def handle_get_ops_metrics() -> dict:
    return get_federation_ops_platform().metrics_snapshot()
