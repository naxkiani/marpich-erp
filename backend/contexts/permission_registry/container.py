"""Permission Registry DI + event subscriptions."""
from __future__ import annotations

from contexts.permission_registry.application.service import PermissionRegistryApplicationService
from contexts.permission_registry.infrastructure.adapters.identity_registry_adapter import IdentityRegistryAdapter
from contexts.permission_registry.infrastructure.persistence.permission_registry_memory_store import (
    InMemoryPermissionRepository,
    InMemoryPermissionSetRepository,
    InMemoryRegistryProfileRepository,
    InMemoryRegistryRoleRepository,
    InMemoryRoleBindingRepository,
)
from contexts.policy.container import get_policy_evaluator
from shared.infrastructure.messaging.event_bus import InProcessEventBus

_service: PermissionRegistryApplicationService | None = None
_registered = False


def get_permission_registry_service() -> PermissionRegistryApplicationService:
    global _service, _registered
    if _service is None:
        _service = PermissionRegistryApplicationService(
            profiles=InMemoryRegistryProfileRepository(),
            permissions=InMemoryPermissionRepository(),
            roles=InMemoryRegistryRoleRepository(),
            bindings=InMemoryRoleBindingRepository(),
            permission_sets=InMemoryPermissionSetRepository(),
            identity=IdentityRegistryAdapter(),
            policy_evaluator=get_policy_evaluator(),
        )
    if not _registered:
        InProcessEventBus.subscribe("platform.tenant.provisioned", _service.handle_tenant_provisioned)
        _registered = True
    return _service


def reset_permission_registry_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
    InMemoryRegistryProfileRepository.reset()
    InMemoryPermissionRepository.reset()
    InMemoryRegistryRoleRepository.reset()
    InMemoryRoleBindingRepository.reset()
    InMemoryPermissionSetRepository.reset()
