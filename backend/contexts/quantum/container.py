"""Quantum DI container."""
from __future__ import annotations

from contexts.quantum.application.service import QuantumApplicationService

_service: QuantumApplicationService | None = None


def get_quantum_service() -> QuantumApplicationService:
    global _service
    if _service is None:
        _service = QuantumApplicationService()
    return _service


def reset_quantum_service() -> None:
    global _service
    _service = None
