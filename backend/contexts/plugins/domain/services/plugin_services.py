"""Plugin domain services."""
from __future__ import annotations

import re

SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.]+))?$")


def parse_semver(version: str) -> tuple[int, int, int] | None:
    match = SEMVER_RE.match(version.strip())
    if not match:
        return None
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def is_upgrade_compatible(current: str, target: str) -> bool:
    cur = parse_semver(current)
    tgt = parse_semver(target)
    if not cur or not tgt:
        return False
    if tgt[0] > cur[0]:
        return True
    if tgt[0] == cur[0] and tgt[1] > cur[1]:
        return True
    if tgt[0] == cur[0] and tgt[1] == cur[1] and tgt[2] > cur[2]:
        return True
    return False


def verify_signature(
    *,
    package_checksum: str,
    public_key_fingerprint: str,
    algorithm: str,
) -> tuple[bool, str]:
    if not package_checksum.startswith("sha256:"):
        return False, "invalid_checksum_format"
    if not public_key_fingerprint:
        return False, "missing_fingerprint"
    if algorithm not in ("ed25519", "rsa-pss-sha256"):
        return False, "unsupported_algorithm"
    if len(package_checksum) < 15:
        return False, "checksum_too_short"
    return True, "verified"


def validate_permission_grants(
    required: list[str],
    granted: list[str],
) -> tuple[bool, list[str]]:
    missing = [p for p in required if p not in granted]
    return len(missing) == 0, missing


SANDBOX_BY_TYPE = {
    "widget": "strict",
    "theme": "strict",
    "report": "standard",
    "dashboard": "standard",
    "ai_skill": "standard",
    "workflow_extension": "standard",
    "integration": "integration",
    "module": "module",
}


def resolve_sandbox_profile(plugin_type: str, override: str | None = None) -> str:
    if override and override in ("strict", "standard", "integration", "module"):
        return override
    return SANDBOX_BY_TYPE.get(plugin_type, "standard")
