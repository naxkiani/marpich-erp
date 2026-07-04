"""Build sample integration events for contract testing."""
from __future__ import annotations

import importlib
import inspect
import types
import typing
from dataclasses import MISSING, fields, is_dataclass
from enum import StrEnum
from types import EllipsisType

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

INTEGRATION_EVENT_MODULES = (
    "contexts.identity.domain.events.integration_events",
    "contexts.core_platform.domain.events.integration_events",
    "contexts.hospital.domain.events.integration_events",
    "contexts.accounting.domain.events.integration_events",
    "contexts.finance.domain.events.integration_events",
    "contexts.notifications.domain.events.integration_events",
    "contexts.settings.domain.events.integration_events",
    "contexts.organization.domain.events.integration_events",
    "contexts.audit.domain.events.integration_events",
    "contexts.documents.domain.events.integration_events",
    "contexts.workflow.domain.events.integration_events",
    "contexts.integration.domain.events.integration_events",
    "contexts.media.domain.events.integration_events",
    "contexts.analytics.domain.events.integration_events",
    "contexts.search.domain.events.integration_events",
)


def discover_integration_event_classes() -> list[type[IntegrationEvent]]:
    discovered: list[type[IntegrationEvent]] = []
    for module_name in INTEGRATION_EVENT_MODULES:
        module = importlib.import_module(module_name)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                is_dataclass(obj)
                and issubclass(obj, IntegrationEvent)
                and obj is not IntegrationEvent
            ):
                discovered.append(obj)
    return sorted(discovered, key=lambda cls: cls.__name__)


def build_sample_event(cls: type[IntegrationEvent]) -> IntegrationEvent:
    hints = typing.get_type_hints(cls)
    kwargs: dict = {}
    for field in fields(cls):
        if not _field_is_required(field):
            continue
        kwargs[field.name] = _sample_value(field.name, hints.get(field.name, field.type))
    return cls(**kwargs)


def _field_is_required(field) -> bool:
    if field.default_factory is not MISSING:
        return False
    if field.default is MISSING:
        return True
    if field.default is ...:
        return True
    return False


def _sample_value(name: str, annotation: object) -> object:
    if isinstance(annotation, str):
        if annotation == "TenantId":
            return TenantId.create("contract-tenant")
        if annotation == "UniqueId":
            return UniqueId.generate()
        return _sample_string(name)

    if annotation is TenantId:
        return TenantId.create("contract-tenant")
    if annotation is UniqueId:
        return UniqueId.generate()
    if annotation is str:
        return _sample_string(name)
    if annotation is int:
        return 1
    if annotation is float:
        return 1.0
    if annotation is bool:
        return True
    if annotation is dict:
        return {}
    if annotation is list:
        return []
    if annotation is tuple:
        return ()

    origin = typing.get_origin(annotation)
    if origin is typing.Union or origin is types.UnionType:
        args = [arg for arg in typing.get_args(annotation) if arg is not type(None)]
        return _sample_value(name, args[0]) if args else None
    if origin is tuple:
        args = typing.get_args(annotation)
        if args and args[-1] is Ellipsis:
            return ()
        return ()
    if origin is list:
        return []
    if origin is dict:
        return {}
    if isinstance(annotation, type) and issubclass(annotation, StrEnum):
        return next(iter(annotation))

    if annotation is object or annotation is typing.Any:
        return _sample_string(name)

    raise TypeError(f"Unsupported field type for contract sample: {name}={annotation!r}")


def _sample_string(name: str) -> str:
    if name == "correlation_id":
        return "contract-corr-id"
    if name == "tenant_slug":
        return "contract-tenant"
    if name == "email":
        return "user@contract.dev"
    if name == "currency":
        return "USD"
    if name == "job_type":
        return "full_sync"
    if name == "source_type":
        return "billing"
    if name.endswith("_url"):
        return "https://example.com/webhook"
    if name.endswith("_pattern"):
        return "*"
    if name == "operator":
        return "gte"
    return "sample"
