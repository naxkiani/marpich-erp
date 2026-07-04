#!/usr/bin/env python3
"""Marpich ERP — architecture validation hard gates (run before generating code)."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "backend"

# Mandatory folders per MODULE_ARCHITECTURE.md
MANDATORY_MODULE_FOLDERS: tuple[str, ...] = (
    "application/commands",
    "application/queries",
    "application/dto",
    "application/validators",
    "application/use_cases",
    "domain/aggregates",
    "domain/value_objects",
    "domain/services",
    "domain/ports",
    "domain/events",
    "domain/specifications",
    "infrastructure/persistence",
    "infrastructure/messaging",
    "infrastructure/caching",
    "infrastructure/storage",
    "infrastructure/external_apis",
    "presentation/rest",
    "presentation/websocket",
    "presentation/reports",
    "presentation/dashboard",
    "tests/unit",
    "tests/integration",
    "tests/performance",
    "docs/api",
    "docs/architecture",
)

CRITICAL_DIMENSIONS: tuple[str, ...] = (
    "Architecture",
    "DDD",
    "Security",
    "Audit",
)

ENTERPRISE_GRADE_MIN_DIMENSION = 3
ENTERPRISE_GRADE_MIN_CRITICAL = 4
ENTERPRISE_GRADE_MIN_AVERAGE = 4.0

DIMENSIONS: tuple[str, ...] = (
    "Architecture",
    "DDD",
    "Security",
    "Scalability",
    "Performance",
    "Testing",
    "AI Integration",
    "Documentation",
    "Accessibility",
    "Localization",
    "Observability",
    "Workflow",
    "Audit",
    "Policy Compliance",
    "Plugin Compatibility",
)


def _run_dependency_check() -> tuple[bool, str]:
    script = REPO_ROOT / "scripts" / "check-dependency-graph.py"
    if not script.is_file():
        return False, "Missing scripts/check-dependency-graph.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode == 0, output.strip()


def _check_module_structure(context_id: str) -> tuple[bool, list[str]]:
    context_root = BACKEND_ROOT / "contexts" / context_id
    if not context_root.is_dir():
        return False, [f"Context not found: backend/contexts/{context_id}/"]
    missing: list[str] = []
    for folder in MANDATORY_MODULE_FOLDERS:
        path = context_root / folder
        if not path.is_dir():
            missing.append(f"backend/contexts/{context_id}/{folder}/")
    required_files = ["container.py", "context.yaml"]
    for name in required_files:
        if not (context_root / name).is_file():
            missing.append(f"backend/contexts/{context_id}/{name}")
    return len(missing) == 0, missing


def _scorecard_template(context_id: str | None) -> str:
    lines = [
        "## Architecture validation scorecard",
        "",
        f"**Context / module:** {context_id or '(specify)'}",
        "",
        "### Hard gates",
        "- [ ] validate-architecture.py PASS",
        "- [ ] check-dependency-graph.py PASS",
        "",
        "### Dimension scores (1–5)",
        "",
        "| # | Dimension | Score | Notes |",
        "|---|-----------|-------|-------|",
    ]
    for i, dim in enumerate(DIMENSIONS, start=1):
        lines.append(f"| {i} | {dim} | | |")
    lines.extend(
        [
            "",
            "**Average:** _ / 5.0",
            f"**Critical ({', '.join(CRITICAL_DIMENSIONS)}):** all ≥ {ENTERPRISE_GRADE_MIN_CRITICAL}?",
            "",
            "### Verdict",
            "- [ ] ENTERPRISE_GRADE — proceed to production code",
            "- [ ] BELOW_THRESHOLD — STOP; improve architecture first",
            "",
        ]
    )
    return "\n".join(lines)


def _evaluate_scores(scores: dict[str, int]) -> tuple[bool, list[str]]:
    blockers: list[str] = []
    if not scores:
        blockers.append("No dimension scores provided — complete scorecard first")
        return False, blockers

    unknown = set(scores) - set(DIMENSIONS)
    if unknown:
        blockers.append(f"Unknown dimensions: {', '.join(sorted(unknown))}")

    for dim in DIMENSIONS:
        if dim not in scores:
            blockers.append(f"Missing score for: {dim}")
            continue
        score = scores[dim]
        if score < 1 or score > 5:
            blockers.append(f"{dim}: score must be 1–5 (got {score})")
        elif score < ENTERPRISE_GRADE_MIN_DIMENSION:
            blockers.append(f"{dim}: {score} < minimum {ENTERPRISE_GRADE_MIN_DIMENSION}")

    present = [scores[d] for d in DIMENSIONS if d in scores]
    if present:
        avg = sum(present) / len(present)
        if avg < ENTERPRISE_GRADE_MIN_AVERAGE:
            blockers.append(
                f"Average {avg:.2f} < {ENTERPRISE_GRADE_MIN_AVERAGE} (Enterprise Grade)"
            )

    for dim in CRITICAL_DIMENSIONS:
        if dim in scores and scores[dim] < ENTERPRISE_GRADE_MIN_CRITICAL:
            blockers.append(
                f"Critical dimension {dim}: {scores[dim]} < {ENTERPRISE_GRADE_MIN_CRITICAL}"
            )

    return len(blockers) == 0, blockers


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Marpich architecture hard gates before generating code"
    )
    parser.add_argument(
        "--context",
        help="Bounded context id to validate module folder structure (new modules)",
    )
    parser.add_argument(
        "--scores",
        help='JSON object of dimension scores, e.g. \'{"Modularity":4,"Security":5}\'',
    )
    parser.add_argument(
        "--scorecard",
        action="store_true",
        help="Print empty scorecard template",
    )
    args = parser.parse_args()

    if args.scorecard:
        print(_scorecard_template(args.context))
        return 0

    print("Marpich Architecture Validation — Hard Gates")
    print("=" * 48)

    all_pass = True

    dep_ok, dep_out = _run_dependency_check()
    print(f"\n[{'PASS' if dep_ok else 'FAIL'}] Dependency graph")
    print(dep_out or "(no output)")
    all_pass = all_pass and dep_ok

    if args.context:
        struct_ok, missing = _check_module_structure(args.context)
        print(f"\n[{'PASS' if struct_ok else 'FAIL'}] Module structure: {args.context}")
        if missing:
            for m in missing:
                print(f"  - missing: {m}")
        all_pass = all_pass and struct_ok

    if args.scores:
        try:
            scores = json.loads(args.scores)
            if not isinstance(scores, dict):
                raise ValueError("scores must be a JSON object")
            scores = {str(k): int(v) for k, v in scores.items()}
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"\n[FAIL] Score evaluation: {exc}")
            return 1
        grade_ok, blockers = _evaluate_scores(scores)
        print(f"\n[{'PASS' if grade_ok else 'FAIL'}] Enterprise Grade score evaluation")
        if blockers:
            for b in blockers:
                print(f"  - {b}")
        all_pass = all_pass and grade_ok
    else:
        print("\n[INFO] No --scores provided — complete manual scorecard before coding")
        print("       python3 scripts/validate-architecture.py --scorecard")

    print("\n" + "=" * 48)
    if all_pass:
        print("VERDICT: HARD GATES PASS")
        if not args.scores:
            print("NEXT: Score 15 dimensions (see docs/architecture/ARCHITECTURE_VALIDATION.md)")
            print("      If average ≥ 4.0 and critical ≥ 4 → ENTERPRISE_GRADE → then code")
        else:
            print("VERDICT: ENTERPRISE_GRADE — proceed to code")
        return 0

    print("VERDICT: BELOW_THRESHOLD — STOP — improve architecture before generating code")
    print("See: docs/architecture/ARCHITECTURE_VALIDATION.md")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
