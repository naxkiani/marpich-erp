"""TOTP MFA service."""
from __future__ import annotations

import secrets

import pyotp


class TotpMfaService:
    def generate_secret(self) -> str:
        return pyotp.random_base32()

    def provisioning_uri(self, email: str, secret: str, issuer: str = "Marpich ERP") -> str:
        return pyotp.TOTP(secret).provisioning_uri(name=email, issuer_name=issuer)

    def verify(self, secret: str, code: str) -> bool:
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)

    def generate_backup_codes(self, count: int = 8) -> list[str]:
        return [secrets.token_hex(4) for _ in range(count)]
