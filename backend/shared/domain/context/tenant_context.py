"""Request-scoped tenant context."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.value_objects.language import Language
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.timezone import TimeZone
from shared.kernel.localization import text_direction


@dataclass(frozen=True, slots=True)
class TenantContext:
    tenant_id: TenantId
    locale: Language
    timezone: TimeZone

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        locale: str = "en",
        timezone: str = "UTC",
    ) -> TenantContext:
        return cls(
            tenant_id=TenantId.create(tenant_id),
            locale=Language(locale),
            timezone=TimeZone(timezone),
        )

    @property
    def direction(self) -> str:
        return text_direction(str(self.locale))
