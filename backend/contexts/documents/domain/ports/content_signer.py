"""Port for Document Exchange content integrity signatures.

Private keys stay in infrastructure / future Secrets platform — never in aggregates.
"""
from __future__ import annotations

from typing import Protocol


class IDocumentContentSigner(Protocol):
    """RSA (or HSM-backed) signer for document version checksums."""

    @property
    def algorithm(self) -> str: ...

    @property
    def key_id(self) -> str: ...

    def sign(
        self,
        *,
        document_id: str,
        version_checksum: str,
        signer_id: str,
    ) -> dict:
        """Return evidence dict: algorithm, signature (b64), key_id, signed_at, …"""
        ...

    def verify(
        self,
        *,
        document_id: str,
        version_checksum: str,
        signer_id: str,
        signature: str,
        algorithm: str | None = None,
        key_id: str | None = None,
    ) -> bool:
        """Cryptographically verify a prior sign() evidence payload."""
        ...
