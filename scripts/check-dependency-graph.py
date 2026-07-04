#!/usr/bin/env python3
"""Detect Marpich ERP dependency graph violations."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1] / "backend"
BASELINE_PATH = BACKEND_ROOT / "tests" / "architecture" / "dependency_baseline.json"

sys.path.insert(0, str(BACKEND_ROOT))

from shared.kernel.dependency_graph import analyze_codebase  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Check dependency graph violations")
    parser.add_argument(
        "--update-baseline",
        action="store_true",
        help="Rewrite baseline with current violations (use after fixing debt)",
    )
    args = parser.parse_args()

    violations = analyze_codebase(BACKEND_ROOT)
    keys = sorted({v.key() for v in violations})

    if args.update_baseline:
        BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
        BASELINE_PATH.write_text(json.dumps(keys, indent=2) + "\n", encoding="utf-8")
        print(f"Updated baseline: {len(keys)} violation(s)")
        return 0

    if not BASELINE_PATH.is_file():
        print(f"Missing baseline: {BASELINE_PATH}", file=sys.stderr)
        return 2

    baseline = set(json.loads(BASELINE_PATH.read_text(encoding="utf-8")))
    current = set(keys)
    new_violations = current - baseline
    fixed = baseline - current

    if new_violations:
        print(f"FAIL: {len(new_violations)} new dependency violation(s):\n", file=sys.stderr)
        for key in sorted(new_violations):
            print(f"  + {key}", file=sys.stderr)
        if fixed:
            print(f"\n({len(fixed)} baseline violation(s) were fixed — run --update-baseline)", file=sys.stderr)
        return 1

    if fixed:
        print(
            f"PASS with note: {len(fixed)} violation(s) fixed — run --update-baseline to shrink baseline"
        )
    else:
        print(f"PASS: {len(current)} known violation(s) unchanged (baseline)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
