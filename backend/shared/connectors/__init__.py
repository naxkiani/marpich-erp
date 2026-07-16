"""Connector SDK public API."""
from shared.connectors.base import IConnectorAdapter
from shared.connectors.builtins import register_builtin_connectors
from shared.connectors.registry import (
    get_connector_adapter,
    list_registered_connectors,
    register_adapter_instance,
    register_connector,
    reset_connector_registry,
)
from shared.connectors.stub_adapter import BaseConnectorAdapter
from shared.connectors.types import ConnectorAuthMethod, ConnectorCategory, ConnectorDirection

__all__ = [
    "BaseConnectorAdapter",
    "ConnectorAuthMethod",
    "ConnectorCategory",
    "ConnectorDirection",
    "IConnectorAdapter",
    "get_connector_adapter",
    "list_registered_connectors",
    "register_adapter_instance",
    "register_builtin_connectors",
    "register_connector",
    "reset_connector_registry",
]
