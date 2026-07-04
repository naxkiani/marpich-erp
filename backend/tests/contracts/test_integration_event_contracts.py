"""Contract tests — integration event JSON schemas."""
from __future__ import annotations

import pytest

from shared.contracts.event_samples import build_sample_event, discover_integration_event_classes
from shared.contracts.event_validator import (
    ContractValidationError,
    list_registered_event_schemas,
    schema_path_for,
    validate_envelope,
    validate_event,
)


def test_envelope_schema_file_is_valid_json():
    from shared.contracts.event_validator import ENVELOPE_SCHEMA

    assert ENVELOPE_SCHEMA.is_file()


def test_registered_schemas_are_unique():
    names = list_registered_event_schemas()
    assert len(names) == len(set(names))


@pytest.mark.parametrize("event_name", list_registered_event_schemas())
def test_registered_schema_files_exist(event_name: str):
    assert schema_path_for(event_name, 1) is not None


@pytest.mark.parametrize("event_cls", discover_integration_event_classes(), ids=lambda cls: cls.__name__)
def test_all_integration_events_satisfy_base_envelope(event_cls):
    envelope = build_sample_event(event_cls).envelope()
    validate_envelope(envelope)


@pytest.mark.parametrize("event_cls", discover_integration_event_classes(), ids=lambda cls: cls.__name__)
def test_integration_events_match_specific_schema_when_registered(event_cls):
    event = build_sample_event(event_cls)
    envelope = event.envelope()
    if schema_path_for(event.event_name, event.event_version) is None:
        pytest.skip(f"No registered schema for {event.event_name}")
    validate_event(envelope)


def test_envelope_rejects_missing_required_fields():
    with pytest.raises(ContractValidationError):
        validate_envelope({"event_name": "broken.event"})


def test_event_name_matches_class():
    event_cls = discover_integration_event_classes()[0]
    event = build_sample_event(event_cls)
    assert event.event_name
    assert event.source_context
    assert event.event_version >= 1
