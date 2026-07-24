"""Strategic DDD package — P200-B3."""
from __future__ import annotations

from contexts.identity_federation.domain.strategic.context_map import (
    COUPLING_EDGES,
    has_circular_dependency,
)
from contexts.identity_federation.domain.strategic.event_ownership import (
    EVENT_OWNERSHIP,
    federation_may_publish,
)
from contexts.identity_federation.domain.strategic.ubiquitous_language import (
    CORE_DOMAINS,
    FederatedSubjectKind,
    TrustLevel,
    TrustStatus,
)

__all__ = [
    "COUPLING_EDGES",
    "CORE_DOMAINS",
    "EVENT_OWNERSHIP",
    "FederatedSubjectKind",
    "TrustLevel",
    "TrustStatus",
    "federation_may_publish",
    "has_circular_dependency",
]
