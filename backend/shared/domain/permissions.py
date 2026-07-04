"""Permission evaluator — RBAC + wildcard admin."""
from __future__ import annotations


class PermissionEvaluator:
    def has_permission(self, user_permissions: list[str], required: str) -> bool:
        if "*" in user_permissions:
            return True
        return required in user_permissions

    def has_all(self, user_permissions: list[str], required: list[str]) -> bool:
        return all(self.has_permission(user_permissions, p) for p in required)
