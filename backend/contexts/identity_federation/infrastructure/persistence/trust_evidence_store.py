"""Append-only trust evidence + history (tenant-scoped) — P200-B6."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


class TrustEvidenceStore:
    def __init__(self) -> None:
        self._evidence: dict[str, list[dict]] = {}
        self._history: dict[str, list[dict]] = {}

    @staticmethod
    def _key(tenant_id: str, trust_ref: str) -> str:
        return f"{tenant_id}:{trust_ref}"

    def add_evidence(
        self,
        *,
        tenant_id: str,
        trust_ref: str,
        evidence_type: str,
        payload: dict[str, Any] | None = None,
        actor_id: str | None = None,
    ) -> dict:
        entry = {
            "evidence_id": str(uuid4()),
            "tenant_id": tenant_id,
            "trust_ref": trust_ref,
            "evidence_type": evidence_type,
            "payload": payload or {},
            "actor_id": actor_id,
            "recorded_at": datetime.now(UTC).isoformat(),
        }
        key = self._key(tenant_id, trust_ref)
        self._evidence.setdefault(key, []).append(entry)
        return entry

    def list_evidence(self, tenant_id: str, trust_ref: str, *, limit: int = 50) -> list[dict]:
        items = self._evidence.get(self._key(tenant_id, trust_ref), [])
        return items[-limit:]

    def evidence_types(self, tenant_id: str, trust_ref: str) -> set[str]:
        return {e["evidence_type"] for e in self.list_evidence(tenant_id, trust_ref, limit=500)}

    def append_history(
        self,
        *,
        tenant_id: str,
        trust_ref: str,
        trust_score: int,
        enterprise_level: int,
        reason: str,
        factors: list[str] | None = None,
    ) -> dict:
        entry = {
            "tenant_id": tenant_id,
            "trust_ref": trust_ref,
            "trust_score": trust_score,
            "enterprise_level": enterprise_level,
            "reason": reason,
            "factors": factors or [],
            "at": datetime.now(UTC).isoformat(),
        }
        key = self._key(tenant_id, trust_ref)
        hist = self._history.setdefault(key, [])
        hist.append(entry)
        self._history[key] = hist[-100:]
        return entry

    def list_history(self, tenant_id: str, trust_ref: str, *, limit: int = 50) -> list[dict]:
        return self._history.get(self._key(tenant_id, trust_ref), [])[-limit:]

    def reset(self) -> None:
        self._evidence.clear()
        self._history.clear()


_store = TrustEvidenceStore()


def get_trust_evidence_store() -> TrustEvidenceStore:
    return _store


def reset_trust_evidence_store() -> None:
    _store.reset()
