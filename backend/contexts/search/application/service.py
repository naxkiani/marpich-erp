"""Search application service — event-driven indexing."""
from __future__ import annotations

from contexts.search.domain.aggregates.index_document import IndexDocument
from contexts.search.domain.aggregates.search_index import SearchIndex
from contexts.search.domain.aggregates.search_query import SearchQuery
from contexts.search.domain.events.integration_events import (
    IndexUpdatedIntegration,
    ReindexCompletedIntegration,
)
from contexts.search.domain.ports.repositories import (
    IIndexDocumentRepository,
    ISearchIndexRepository,
    ISearchQueryRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event

DEFAULT_ENTITY_TYPES = ("user", "document", "event", "workflow", "organization", "hospital")


class SearchApplicationService:
    def __init__(
        self,
        indices: ISearchIndexRepository,
        documents: IIndexDocumentRepository,
        queries: ISearchQueryRepository,
    ) -> None:
        self._indices = indices
        self._documents = documents
        self._queries = queries

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        for entity_type in DEFAULT_ENTITY_TYPES:
            existing = await self._indices.find_by_type(tenant_id, entity_type)
            if existing:
                continue
            await self._indices.save(SearchIndex.create(tenant_id=tenant_id, entity_type=entity_type))

    async def handle_module_activated(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        module_id = envelope.get("payload", {}).get("module_id", "module")
        entity_type = module_id.replace(".", "_").lower()
        if not await self._indices.find_by_type(tenant_id, entity_type):
            await self._indices.save(SearchIndex.create(tenant_id=tenant_id, entity_type=entity_type))

    async def handle_integration_event(self, envelope: dict) -> None:
        event_name = envelope.get("event_name", "")
        if event_name.startswith("search."):
            return
        tenant_id = envelope.get("tenant_id", "")
        if not tenant_id:
            return

        document = IndexDocument.from_event(tenant_id=tenant_id, envelope=envelope)
        await self._documents.upsert(document)

        index = await self._indices.find_by_type(tenant_id, document.entity_type)
        if index is None:
            index = SearchIndex.create(tenant_id=tenant_id, entity_type=document.entity_type)
        index.increment_count()
        await self._indices.save(index)

        await publish_integration_event(
            IndexUpdatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=envelope.get("correlation_id", ""),
                entity_type=document.entity_type,
                entity_id=document.entity_id,
                action="upsert",
            )
        )

    async def query(
        self,
        tenant_id: str,
        q: str,
        *,
        entity_types: list[str] | None = None,
        limit: int = 50,
    ) -> Result[dict]:
        results = await self._documents.search(
            tenant_id, q, entity_types=entity_types, limit=limit
        )
        await self._queries.append(
            SearchQuery.record(
                tenant_id=tenant_id,
                query_text=q,
                entity_types=entity_types or [],
                result_count=len(results),
            )
        )
        return Result.ok(
            {
                "query": q,
                "total": len(results),
                "items": [doc.to_dict() for doc in results],
            }
        )

    async def suggest(self, tenant_id: str, q: str, *, limit: int = 10) -> Result[dict]:
        items = await self._documents.suggest(tenant_id, q, limit=limit)
        return Result.ok({"prefix": q, "suggestions": items})

    async def list_indices(self, tenant_id: str) -> Result[list[dict]]:
        indices = await self._indices.list_by_tenant(tenant_id)
        return Result.ok([index.to_dict() for index in indices])

    async def reindex(self, tenant_id: str, correlation_id: str) -> Result[dict]:
        cleared = await self._documents.clear_tenant(tenant_id)
        for entity_type in DEFAULT_ENTITY_TYPES:
            await self._indices.save(SearchIndex.create(tenant_id=tenant_id, entity_type=entity_type))

        await publish_integration_event(
            ReindexCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_count=cleared,
            )
        )
        return Result.ok({"cleared": cleared, "status": "ready_for_replay"})
