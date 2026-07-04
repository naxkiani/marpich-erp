"""Application-layer validation — no FastAPI imports."""
from __future__ import annotations

from contexts.module_id.application.commands.create_example import CreateExampleCommand


def validate_create_example(command: CreateExampleCommand) -> str | None:
    if not command.name.strip():
        return "name is required"
    return None
