"""Robotics DI container."""
from __future__ import annotations

from contexts.robotics.application.service import RoboticsApplicationService

_service: RoboticsApplicationService | None = None


def get_robotics_service() -> RoboticsApplicationService:
    global _service
    if _service is None:
        _service = RoboticsApplicationService()
    return _service


def reset_robotics_service() -> None:
    global _service
    _service = None
