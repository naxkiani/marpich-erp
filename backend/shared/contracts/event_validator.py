"""Integration event contract validation — JSON Schema registry."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft7Validator

EVENTS_DIR = Path(__file__).resolve().parents[3] / "docs" / "architecture" / "events"
ENVELOPE_SCHEMA = EVENTS_DIR / "_envelope.v1.json"


class ContractValidationError(Exception):
    def __init__(self, event_name: str, errors: list[str]) -> None:
        self.event_name = event_name
        self.errors = errors
        super().__init__(f"Contract violation for {event_name}: {'; '.join(errors)}")


@lru_cache(maxsize=64)
def _load_schema(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _validator_for(path: Path) -> Draft7Validator:
    from jsonschema import RefResolver

    schema = _load_schema(str(path))
    store = {schema_path.name: _load_schema(str(schema_path)) for schema_path in EVENTS_DIR.glob("*.json")}
    resolver = RefResolver(
        base_uri=f"{EVENTS_DIR.resolve().as_uri()}/",
        referrer=schema,
        store=store,
    )
    return Draft7Validator(schema, resolver=resolver)


def schema_path_for(event_name: str, event_version: int = 1) -> Path | None:
    candidate = EVENTS_DIR / f"{event_name}.v{event_version}.json"
    return candidate if candidate.is_file() else None


def list_registered_event_schemas() -> list[str]:
    return sorted(
        path.stem.rsplit(".v", 1)[0]
        for path in EVENTS_DIR.glob("*.v*.json")
        if not path.name.startswith("_")
    )


def validate_envelope(envelope: dict) -> None:
    _assert_valid(envelope, ENVELOPE_SCHEMA, envelope.get("event_name", "envelope"))


def validate_event(envelope: dict) -> None:
    """Validate base envelope + event-specific schema when registered."""
    validate_envelope(envelope)
    event_name = envelope.get("event_name", "")
    event_version = int(envelope.get("event_version", 1))
    specific = schema_path_for(event_name, event_version)
    if specific is not None:
        _assert_valid(envelope, specific, event_name)


def _assert_valid(instance: dict, schema_path: Path, label: str) -> None:
    validator = _validator_for(schema_path)
    errors = sorted({error.message for error in validator.iter_errors(instance)})
    if errors:
        raise ContractValidationError(label, errors)
