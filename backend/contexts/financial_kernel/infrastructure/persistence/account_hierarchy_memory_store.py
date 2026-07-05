"""In-memory account hierarchy repositories."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.account_hierarchy import (
    AccountTree,
    AccountTreeVersion,
)
from contexts.financial_kernel.domain.ports.account_hierarchy_repositories import (
    IAccountTreeRepository,
    IAccountTreeVersionRepository,
)


class InMemoryAccountTreeRepository(IAccountTreeRepository):
    _trees: dict[str, AccountTree] = {}

    @classmethod
    def reset(cls) -> None:
        cls._trees = {}

    async def save(self, tree: AccountTree) -> None:
        self._trees[str(tree.id)] = tree

    async def find_by_id(self, tree_id: str) -> AccountTree | None:
        return self._trees.get(tree_id)

    async def list_by_tenant(self, tenant_id: str) -> list[AccountTree]:
        return [t for t in self._trees.values() if t.tenant_id == tenant_id]

    async def find_default(self, tenant_id: str) -> AccountTree | None:
        for tree in self._trees.values():
            if tree.tenant_id == tenant_id and tree.is_default:
                return tree
        return None


class InMemoryAccountTreeVersionRepository(IAccountTreeVersionRepository):
    _versions: dict[str, AccountTreeVersion] = {}

    @classmethod
    def reset(cls) -> None:
        cls._versions = {}

    async def save(self, version: AccountTreeVersion) -> None:
        self._versions[str(version.id)] = version

    async def find_by_id(self, version_id: str) -> AccountTreeVersion | None:
        return self._versions.get(version_id)

    async def list_by_tree(self, tree_id: str) -> list[AccountTreeVersion]:
        items = [v for v in self._versions.values() if v.tree_id == tree_id]
        return sorted(items, key=lambda v: v.version_number, reverse=True)

    async def find_by_version_number(
        self, tree_id: str, version_number: int
    ) -> AccountTreeVersion | None:
        for version in self._versions.values():
            if version.tree_id == tree_id and version.version_number == version_number:
                return version
        return None
