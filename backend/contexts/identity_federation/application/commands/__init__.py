"""CQRS write-side entry points for Identity Federation (P200-B2)."""
from __future__ import annotations

from contexts.identity_federation.application.commands.evaluate_trust import (
    EvaluateTrustCommand,
    handle_evaluate_trust,
)

__all__ = ["EvaluateTrustCommand", "handle_evaluate_trust"]
