"""Enterprise trust levels 0–5 (P200-B6)."""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class EnterpriseTrustLevel(IntEnum):
    UNKNOWN = 0
    LIMITED = 1
    VERIFIED = 2
    ENTERPRISE = 3
    STRATEGIC = 4
    CONTINUOUS_ADAPTIVE = 5


LEVEL_NAMES = {
    0: "unknown_trust",
    1: "limited_trust",
    2: "verified_trust",
    3: "enterprise_trust",
    4: "strategic_trust",
    5: "continuous_adaptive_trust",
}


@dataclass(frozen=True, slots=True)
class TrustLevelBand:
    level: int
    name: str
    min_score: int
    max_score: int


BANDS: tuple[TrustLevelBand, ...] = (
    TrustLevelBand(0, "unknown_trust", 0, 19),
    TrustLevelBand(1, "limited_trust", 20, 39),
    TrustLevelBand(2, "verified_trust", 40, 59),
    TrustLevelBand(3, "enterprise_trust", 60, 74),
    TrustLevelBand(4, "strategic_trust", 75, 89),
    TrustLevelBand(5, "continuous_adaptive_trust", 90, 100),
)


def level_from_score(score: int) -> int:
    score = max(0, min(100, int(score)))
    for band in BANDS:
        if band.min_score <= score <= band.max_score:
            return band.level
    return 0


def level_name(level: int) -> str:
    return LEVEL_NAMES.get(int(level), "unknown_trust")


def can_transition(*, from_level: int, to_level: int, score: int, evidence_types: set[str]) -> dict:
    """Policy-lite transition gate — always explainable."""
    if to_level < from_level and to_level == 0:
        return {"allowed": True, "reason": "downgrade_to_unknown"}
    if to_level == from_level:
        return {"allowed": True, "reason": "unchanged"}
    if to_level > from_level + 1:
        return {"allowed": False, "reason": "skip_level_forbidden"}
    required = {
        1: {"authn"},
        2: {"authn", "assurance"},
        3: {"authn", "assurance", "org"},
        4: {"authn", "assurance", "org", "agreement"},
        5: {"authn", "assurance", "org", "agreement", "continuous"},
    }.get(to_level, set())
    missing = sorted(required - evidence_types)
    expected = level_from_score(score)
    if expected < to_level:
        return {"allowed": False, "reason": "score_below_target_band", "expected_level": expected}
    if missing:
        return {"allowed": False, "reason": "missing_evidence", "missing": missing}
    return {"allowed": True, "reason": "transition_ok", "to_level": to_level}
