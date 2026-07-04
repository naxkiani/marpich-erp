"""Enterprise financial security engine."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import UTC, datetime

ENCRYPTION_SECRET = "marpich-fin-security-enc-v1"
SIGNING_SECRET = "marpich-fin-security-sign-v1"
TAMPER_SECRET = "marpich-fin-security-tamper-v1"


def checksum_payload(payload: dict) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode()).hexdigest()


def encrypt_payload(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True).encode()
    key = hashlib.sha256(ENCRYPTION_SECRET.encode()).digest()
    encrypted = bytes(b ^ key[i % len(key)] for i, b in enumerate(raw))
    return base64.b64encode(encrypted).decode("ascii")


def decrypt_payload(encrypted_b64: str) -> dict:
    key = hashlib.sha256(ENCRYPTION_SECRET.encode()).digest()
    encrypted = base64.b64decode(encrypted_b64.encode())
    raw = bytes(b ^ key[i % len(key)] for i, b in enumerate(encrypted))
    return json.loads(raw.decode())


def sign_operation(*, resource_id: str, checksum: str, signer_id: str, algorithm: str = "RS256") -> dict:
    payload = f"{resource_id}:{checksum}:{signer_id}"
    signature = hmac.new(SIGNING_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return {
        "signer_id": signer_id,
        "algorithm": algorithm,
        "signature": signature,
        "signed_at": datetime.now(UTC).isoformat(),
    }


def compute_tamper_hash(
    *,
    action: str,
    actor_id: str,
    resource_id: str,
    payload_checksum: str,
    previous_hash: str | None = None,
) -> str:
    chain = previous_hash or "genesis"
    payload = f"{chain}:{action}:{actor_id}:{resource_id}:{payload_checksum}"
    return hmac.new(TAMPER_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()


def verify_tamper(
    *,
    tamper_hash: str,
    action: str,
    actor_id: str,
    resource_id: str,
    payload_checksum: str,
    previous_hash: str | None = None,
) -> bool:
    expected = compute_tamper_hash(
        action=action,
        actor_id=actor_id,
        resource_id=resource_id,
        payload_checksum=payload_checksum,
        previous_hash=previous_hash,
    )
    return hmac.compare_digest(tamper_hash, expected)


def evaluate_rbac_policy(*, rules: dict, permission: str, role: str) -> bool:
    allowed_roles = rules.get("allowed_roles", [])
    allowed_permissions = rules.get("allowed_permissions", [])
    if permission in allowed_permissions:
        return True
    return role in allowed_roles and permission in rules.get("role_permissions", {}).get(role, [])


def evaluate_abac_policy(*, rules: dict, attributes: dict) -> bool:
    required = rules.get("required_attributes", {})
    for key, expected in required.items():
        actual = attributes.get(key)
        if isinstance(expected, list):
            if actual not in expected:
                return False
        elif actual != expected:
            return False
    denied = rules.get("deny_if", {})
    for key, blocked in denied.items():
        if attributes.get(key) == blocked:
            return False
    return True


def validate_maker_checker(maker_id: str, checker_id: str) -> None:
    if maker_id == checker_id:
        raise ValueError("maker_checker_same_user")


def validate_four_eyes(approver_ids: list[str]) -> None:
    if len(approver_ids) != len(set(approver_ids)):
        raise ValueError("four_eyes_duplicate_approver")
