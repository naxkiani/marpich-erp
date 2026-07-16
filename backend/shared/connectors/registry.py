"""Connector adapter registry — plugin-style registration."""
from __future__ import annotations

from typing import Callable, Type

from shared.connectors.base import IConnectorAdapter

_registry: dict[str, IConnectorAdapter] = {}
_factories: dict[str, Callable[[], IConnectorAdapter]] = {}


def register_connector(connector_type: str):
    """Decorator to register a connector adapter class or factory."""

    def decorator(cls_or_factory: Type[IConnectorAdapter] | Callable[[], IConnectorAdapter]):
        def factory() -> IConnectorAdapter:
            if isinstance(cls_or_factory, type):
                return cls_or_factory()
            return cls_or_factory()

        _factories[connector_type] = factory
        return cls_or_factory

    return decorator


def get_connector_adapter(connector_type: str) -> IConnectorAdapter | None:
    if connector_type in _registry:
        return _registry[connector_type]
    factory = _factories.get(connector_type)
    if factory is None:
        return None
    adapter = factory()
    _registry[connector_type] = adapter
    return adapter


def list_registered_connectors() -> list[str]:
    return sorted(set(_registry.keys()) | set(_factories.keys()))


def register_adapter_instance(connector_type: str, adapter: IConnectorAdapter) -> None:
    _registry[connector_type] = adapter


def reset_connector_registry() -> None:
    _registry.clear()
    _factories.clear()
