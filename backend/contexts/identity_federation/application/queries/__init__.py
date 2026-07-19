"""CQRS read-side entry points for Identity Federation (P200-B2)."""
from __future__ import annotations

from contexts.identity_federation.application.queries.get_trust_facts import (
    GetTrustFactsQuery,
    handle_get_trust_facts,
)

__all__ = ["GetTrustFactsQuery", "handle_get_trust_facts"]
