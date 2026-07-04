from __future__ import annotations

from typing import Protocol


class IEventCountStore(Protocol):
    def increment(self, tenant_id: str, event_name: str) -> None: ...

    def summary(self, tenant_id: str) -> dict[str, int]: ...
