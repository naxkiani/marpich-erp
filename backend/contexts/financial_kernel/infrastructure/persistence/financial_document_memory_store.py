"""In-memory Financial Document persistence."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.financial_document import (
    FinancialDocument,
    FinancialDocumentVersion,
)
from contexts.financial_kernel.domain.ports.financial_document_repositories import (
    IFinancialDocumentRepository,
    IFinancialDocumentVersionRepository,
)


class InMemoryFinancialDocumentRepository(IFinancialDocumentRepository):
    _documents: dict[str, FinancialDocument] = {}
    _sequences: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls._documents = {}
        cls._sequences = {}

    async def save(self, document: FinancialDocument) -> None:
        self._documents[str(document.id)] = document
        self._documents[f"idemp:{document.tenant_id}:{document.idempotency_key}"] = document

    async def find_by_id(self, document_id: str) -> FinancialDocument | None:
        doc = self._documents.get(document_id)
        return doc if isinstance(doc, FinancialDocument) else None

    async def find_by_idempotency(self, tenant_id: str, key: str) -> FinancialDocument | None:
        doc = self._documents.get(f"idemp:{tenant_id}:{key}")
        return doc if isinstance(doc, FinancialDocument) else None

    async def list_by_tenant(self, tenant_id: str) -> list[FinancialDocument]:
        seen: set[str] = set()
        result = []
        for doc in self._documents.values():
            if isinstance(doc, FinancialDocument) and doc.tenant_id == tenant_id and str(doc.id) not in seen:
                seen.add(str(doc.id))
                result.append(doc)
        return result

    async def next_sequence(self, tenant_id: str, document_type: str) -> int:
        key = f"{tenant_id}:{document_type}"
        self._sequences[key] = self._sequences.get(key, 0) + 1
        return self._sequences[key]


class InMemoryFinancialDocumentVersionRepository(IFinancialDocumentVersionRepository):
    _versions: dict[str, FinancialDocumentVersion] = {}

    @classmethod
    def reset(cls) -> None:
        cls._versions = {}

    async def save(self, version: FinancialDocumentVersion) -> None:
        self._versions[str(version.id)] = version

    async def find_by_id(self, version_id: str) -> FinancialDocumentVersion | None:
        return self._versions.get(version_id)

    async def list_by_document(self, tenant_id: str, document_id: str) -> list[FinancialDocumentVersion]:
        return sorted(
            [
                v
                for v in self._versions.values()
                if v.tenant_id == tenant_id and str(v.document_id) == document_id
            ],
            key=lambda v: v.version_number,
        )

    async def next_version_number(self, tenant_id: str, document_id: str) -> int:
        versions = await self.list_by_document(tenant_id, document_id)
        return (versions[-1].version_number + 1) if versions else 1
