"""PEM-backed RSA-PSS-SHA256 content signer (P5.1).

Loads keys from settings; generates an ephemeral 2048-bit keypair when PEMs
are unset (memory/dev/tests). Production must set DOCUMENT_SIGNING_*_KEY_PEM;
HSM/Secrets platform can replace this adapter without changing the port.
"""
from __future__ import annotations

import base64
import logging
from datetime import UTC, datetime
from functools import lru_cache

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from shared.infrastructure.settings import settings

logger = logging.getLogger("marpich.documents.crypto")

ALGORITHM = "RSA-PSS-SHA256"
_PSS = padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.DIGEST_LENGTH,
)


def _payload(*, document_id: str, version_checksum: str, signer_id: str) -> bytes:
    return f"{document_id}:{version_checksum}:{signer_id}".encode()


@lru_cache(maxsize=1)
def _load_keys() -> tuple[RSAPrivateKey, RSAPublicKey, str, bool]:
    priv_pem = (settings.document_signing_private_key_pem or "").strip()
    pub_pem = (settings.document_signing_public_key_pem or "").strip()
    key_id = (settings.document_signing_key_id or "").strip() or "documents-signing-v1"

    if priv_pem:
        private_key = serialization.load_pem_private_key(
            priv_pem.encode(),
            password=None,
        )
        if not isinstance(private_key, RSAPrivateKey):
            raise TypeError("DOCUMENT_SIGNING_PRIVATE_KEY_PEM must be an RSA private key")
        if pub_pem:
            public_key = serialization.load_pem_public_key(pub_pem.encode())
            if not isinstance(public_key, RSAPublicKey):
                raise TypeError("DOCUMENT_SIGNING_PUBLIC_KEY_PEM must be an RSA public key")
        else:
            public_key = private_key.public_key()
        logger.info("documents.signing.keys_loaded key_id=%s source=env", key_id)
        return private_key, public_key, key_id, False

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    ephemeral_id = f"ephemeral-dev-{key_id}"
    logger.warning(
        "documents.signing.ephemeral_keypair key_id=%s — set DOCUMENT_SIGNING_PRIVATE_KEY_PEM for production",
        ephemeral_id,
    )
    return private_key, public_key, ephemeral_id, False


def reset_signer_cache() -> None:
    """Test helper — clear cached keypair after settings overrides."""
    _load_keys.cache_clear()


class PemRsaPssContentSigner:
    """IDocumentContentSigner adapter — RSA-PSS with SHA-256."""

    @property
    def algorithm(self) -> str:
        return ALGORITHM

    @property
    def key_id(self) -> str:
        return _load_keys()[2]

    def sign(
        self,
        *,
        document_id: str,
        version_checksum: str,
        signer_id: str,
    ) -> dict:
        private_key, _public_key, key_id, hsm = _load_keys()
        signature = private_key.sign(
            _payload(
                document_id=document_id,
                version_checksum=version_checksum,
                signer_id=signer_id,
            ),
            _PSS,
            hashes.SHA256(),
        )
        return {
            "signer_id": signer_id,
            "algorithm": ALGORITHM,
            "signature": base64.urlsafe_b64encode(signature).decode().rstrip("="),
            "signed_at": datetime.now(UTC).isoformat(),
            "document_id": document_id,
            "version_checksum": version_checksum,
            "key_id": key_id,
            "hsm": hsm,
            "note": "RSA-PSS-SHA256 via documents infrastructure; HSM via Secrets platform later",
        }

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
        if algorithm and algorithm != ALGORITHM:
            return False
        _private_key, public_key, loaded_key_id, _hsm = _load_keys()
        if key_id is not None and key_id != loaded_key_id:
            return False
        try:
            padded = signature + "=" * (-len(signature) % 4)
            raw = base64.urlsafe_b64decode(padded.encode())
            public_key.verify(
                raw,
                _payload(
                    document_id=document_id,
                    version_checksum=version_checksum,
                    signer_id=signer_id,
                ),
                _PSS,
                hashes.SHA256(),
            )
            return True
        except (InvalidSignature, ValueError, TypeError):
            return False
