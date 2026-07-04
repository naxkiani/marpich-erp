"""Repository ports — Search."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.search.domain.aggregates.index_document import IndexDocument
from contexts.search.domain.aggregates.search_index import SearchIndex
from contexts.search.domain.aggregates.search_query import SearchQuery


class ISearchIndexRepository(ABC):
    @abstractmethod
    async def save(self, index: SearchIndex) -> None: ...

    @abstractmethod
    async def find_by_type(self, tenant_id: str, entity_type: str) -> SearchIndex | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[SearchIndex]: ...


class IIndexDocumentRepository(ABC):
    @abstractmethod
    async def upsert(self, document: IndexDocument) -> None: ...

    @abstractmethod
    async def search(
        self,
        tenant_id: str,
        query: str,
        *,
        entity_types: list[str] | None = None,
        limit: int = 50,
    ) -> list[IndexDocument]: ...

    @abstractmethod
    async def suggest(self, tenant_id: str, prefix: str, *, limit: int = 10) -> list[str]: ...

    @abstractmethod
    async def count_by_tenant(self, tenant_id: str) -> int: ...

    @abstractmethod
    async def clear_tenant(self, tenant_id: str) -> int: ...


class ISearchQueryRepository(ABC):
    @abstractmethod
    async def append(self, query: SearchQuery) -> None: ...
