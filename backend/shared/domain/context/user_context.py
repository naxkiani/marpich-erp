"""Request-scoped user context."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class UserContext:
    user_id: str
    email: str
    permissions: tuple[str, ...] = field(default_factory=tuple)
    role_ids: tuple[str, ...] = field(default_factory=tuple)
    display_name: str | None = None

    def has_permission(self, required: str) -> bool:
        if "*" in self.permissions:
            return True
        return required in self.permissions

    @classmethod
    def from_token_claims(cls, claims: dict) -> UserContext:
        return cls(
            user_id=str(claims.get("sub", "")),
            email=str(claims.get("email", "")),
            permissions=tuple(claims.get("permissions", [])),
            role_ids=tuple(claims.get("role_ids", [])),
            display_name=claims.get("display_name"),
        )
