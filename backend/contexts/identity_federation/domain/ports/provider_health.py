"""Provider health probe port — protocol-agnostic (P200-B5)."""
from __future__ import annotations

from typing import Any, Protocol


class IProviderHealthProbe(Protocol):
    async def probe(
        self,
        *,
        tenant_id: str,
        provider_ref: str,
        protocol: str,
        endpoints: dict[str, Any] | None = None,
    ) -> dict: ...
