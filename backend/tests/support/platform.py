"""Platform test helpers — unit (no app) vs integration (API smoke)."""
from __future__ import annotations

from httpx import AsyncClient


async def auth_headers(
    client: AsyncClient,
    *,
    tenant: str,
    email: str,
    display_name: str = "Test",
) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass123!", "display_name": display_name},
        headers={"X-Tenant-ID": tenant},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "SecurePass123!"},
        headers={"X-Tenant-ID": tenant},
    )
    token = login.json()["data"]["access_token"]
    return {"X-Tenant-ID": tenant, "Authorization": f"Bearer {token}"}


def reset_policy_stack() -> None:
    import contexts.identity.container as identity_container
    from contexts.identity.infrastructure.persistence.memory_store import InMemoryStore
    from contexts.policy.container import get_policy_service, reset_policy_service

    identity_container._container = None
    InMemoryStore.reset()
    reset_policy_service()
    get_policy_service()
