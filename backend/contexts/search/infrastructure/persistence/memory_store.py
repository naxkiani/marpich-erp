"""In-memory search repositories."""
from __future__ import annotations

from contexts.search.domain.aggregates.index_document import IndexDocument
from contexts.search.domain.aggregates.search_index import SearchIndex
from contexts.search.domain.aggregates.search_query import SearchQuery
from contexts.search.domain.ports.repositories import (
    IIndexDocumentRepository,
    ISearchIndexRepository,
    ISearchQueryRepository,
)


class SearchMemoryStore:
    indices: dict[str, SearchIndex] = {}
    documents: dict[str, IndexDocument] = {}
    queries: list[SearchQuery] = []

    @classmethod
    def reset(cls) -> None:
        cls.indices.clear()
        cls.documents.clear()
        cls.queries.clear()


class InMemorySearchIndexRepository(ISearchIndexRepository):
    def _key(self, tenant_id: str, entity_type: str) -> str:
        return f"{tenant_id}:{entity_type.lower()}"

    async def save(self, index: SearchIndex) -> None:
        SearchMemoryStore.indices[self._key(index.tenant_id, index.entity_type)] = index

    async def find_by_type(self, tenant_id: str, entity_type: str) -> SearchIndex | None:
        return SearchMemoryStore.indices.get(self._key(tenant_id, entity_type))

    async def list_by_tenant(self, tenant_id: str) -> list[SearchIndex]:
        return [i for i in SearchMemoryStore.indices.values() if i.tenant_id == tenant_id]


class InMemoryIndexDocumentRepository(IIndexDocumentRepository):
    def _key(self, tenant_id: str, entity_type: str, entity_id: str) -> str:
        return f"{tenant_id}:{entity_type}:{entity_id}"

    async def upsert(self, document: IndexDocument) -> None:
        SearchMemoryStore.documents[
            self._key(document.tenant_id, document.entity_type, document.entity_id)
        ] = document

    async def search(
        self,
        tenant_id: str,
        query: str,
        *,
        entity_types: list[str] | None = None,
        limit: int = 50,
    ) -> list[IndexDocument]:
        results = [
            doc
            for doc in SearchMemoryStore.documents.values()
            if doc.tenant_id == tenant_id and doc.matches_query(query)
        ]
        if entity_types:
            allowed = {t.lower() for t in entity_types}
            results = [doc for doc in results if doc.entity_type in allowed]
        results.sort(key=lambda d: d.indexed_at, reverse=True)
        return results[:limit]

    async def suggest(self, tenant_id: str, prefix: str, *, limit: int = 10) -> list[str]:
        needle = prefix.lower().strip()
        titles: list[str] = []
        for doc in SearchMemoryStore.documents.values():
            if doc.tenant_id != tenant_id:
                continue
            if not needle or doc.title.lower().startswith(needle):
                titles.append(doc.title)
        return sorted(set(titles))[:limit]

    async def count_by_tenant(self, tenant_id: str) -> int:
        return sum(1 for doc in SearchMemoryStore.documents.values() if doc.tenant_id == tenant_id)

    async def clear_tenant(self, tenant_id: str) -> int:
        keys = [k for k, doc in SearchMemoryStore.documents.items() if doc.tenant_id == tenant_id]
        for key in keys:
            del SearchMemoryStore.documents[key]
        return len(keys)


class InMemorySearchQueryRepository(ISearchQueryRepository):
    async def append(self, query: SearchQuery) -> None:
        SearchMemoryStore.queries.append(query)
