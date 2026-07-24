"""Architecture surface discovery — P200-B2 (read-only)."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from contexts.identity.presentation.dependencies import require_permissions
from contexts.identity_federation.domain.services.eiftp_architecture import (
    validate_architecture_foundation,
)

architecture_router = APIRouter(prefix="/federation/architecture", tags=["federation-architecture"])


@architecture_router.get(
    "/surface",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def architecture_surface() -> dict:
    result = validate_architecture_foundation()
    return {
        "prompt": "P200-B2",
        "adr": 216,
        "sor": "identity_federation",
        "deliverables": 50,
        "law": "ENTERPRISE_IDENTITY_FEDERATION_TRUST_ARCHITECTURE.md",
        "index": "docs/architecture/identity/eiftp/ARCH_DELIVERABLES_INDEX.v1.yaml",
        "shared_port": "IFederationTrustFacts",
        "validation": result,
    }
