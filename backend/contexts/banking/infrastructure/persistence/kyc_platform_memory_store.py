"""In-memory Enterprise KYC Platform repositories."""
from __future__ import annotations

from contexts.banking.domain.aggregates.kyc_platform_engine import (
    KycAddressVerification,
    KycAuditEntry,
    KycBiometricHook,
    KycCase,
    KycDocument,
    KycPeriodicReview,
    KycScreeningResult,
    KycWorkflowRequest,
)


class InMemoryKycCaseRepository:
    _store: dict[str, KycCase] = {}
    _counter: dict[str, int] = {}

    async def save(self, case: KycCase) -> None:
        self._store[str(case.id)] = case

    async def find_by_id(self, case_id: str) -> KycCase | None:
        return self._store.get(case_id)

    async def find_by_ref(self, tenant_id: str, case_ref: str) -> KycCase | None:
        for c in self._store.values():
            if c.tenant_id == tenant_id and c.case_ref == case_ref.upper():
                return c
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[KycCase]:
        return [c for c in self._store.values() if c.tenant_id == tenant_id]

    async def list_by_customer(self, customer_id: str) -> list[KycCase]:
        return [c for c in self._store.values() if c.customer_id == customer_id]

    def next_case_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"KYC{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryKycDocumentRepository:
    _store: dict[str, KycDocument] = {}

    async def save(self, document: KycDocument) -> None:
        self._store[str(document.id)] = document

    async def find_by_id(self, document_id: str) -> KycDocument | None:
        return self._store.get(document_id)

    async def list_by_case(self, case_id: str) -> list[KycDocument]:
        return [d for d in self._store.values() if d.case_id == case_id]

    async def list_by_tenant(self, tenant_id: str) -> list[KycDocument]:
        return [d for d in self._store.values() if d.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryKycAddressRepository:
    _store: dict[str, KycAddressVerification] = {}

    async def save(self, address: KycAddressVerification) -> None:
        self._store[str(address.id)] = address

    async def find_by_id(self, address_id: str) -> KycAddressVerification | None:
        return self._store.get(address_id)

    async def list_by_case(self, case_id: str) -> list[KycAddressVerification]:
        return [a for a in self._store.values() if a.case_id == case_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryKycScreeningRepository:
    _store: dict[str, KycScreeningResult] = {}

    async def save(self, result: KycScreeningResult) -> None:
        self._store[str(result.id)] = result

    async def list_by_case(self, case_id: str) -> list[KycScreeningResult]:
        return [s for s in self._store.values() if s.case_id == case_id]

    async def list_by_tenant(self, tenant_id: str) -> list[KycScreeningResult]:
        return [s for s in self._store.values() if s.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryKycReviewRepository:
    _store: dict[str, KycPeriodicReview] = {}
    _counter: dict[str, int] = {}

    async def save(self, review: KycPeriodicReview) -> None:
        self._store[str(review.id)] = review

    async def find_by_id(self, review_id: str) -> KycPeriodicReview | None:
        return self._store.get(review_id)

    async def list_by_case(self, case_id: str) -> list[KycPeriodicReview]:
        return [r for r in self._store.values() if r.case_id == case_id]

    async def list_by_tenant(self, tenant_id: str) -> list[KycPeriodicReview]:
        return [r for r in self._store.values() if r.tenant_id == tenant_id]

    def next_review_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"REV{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryKycWorkflowRepository:
    _store: dict[str, KycWorkflowRequest] = {}

    async def save(self, request: KycWorkflowRequest) -> None:
        self._store[str(request.id)] = request

    async def list_by_case(self, case_id: str) -> list[KycWorkflowRequest]:
        return [w for w in self._store.values() if w.case_id == case_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryKycBiometricRepository:
    _store: dict[str, KycBiometricHook] = {}

    async def save(self, hook: KycBiometricHook) -> None:
        self._store[str(hook.id)] = hook

    async def find_by_id(self, hook_id: str) -> KycBiometricHook | None:
        return self._store.get(hook_id)

    async def list_by_case(self, case_id: str) -> list[KycBiometricHook]:
        return [h for h in self._store.values() if h.case_id == case_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryKycAuditRepository:
    _store: dict[str, KycAuditEntry] = {}

    async def save(self, entry: KycAuditEntry) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_case(self, case_id: str) -> list[KycAuditEntry]:
        return sorted(
            [e for e in self._store.values() if e.case_id == case_id],
            key=lambda e: e.occurred_at,
            reverse=True,
        )

    async def list_by_tenant(self, tenant_id: str) -> list[KycAuditEntry]:
        return sorted(
            [e for e in self._store.values() if e.tenant_id == tenant_id],
            key=lambda e: e.occurred_at,
            reverse=True,
        )

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
