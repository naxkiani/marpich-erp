#!/usr/bin/env python3
"""MEOS secret scan (P353). Reports file paths and rule names only — never secret values."""
from __future__ import annotations

import re
import sys
from pathlib import Path

SKIP_DIR_NAMES = {
    ".git",
    ".venv",
    "node_modules",
    "dist",
    ".next",
    ".turbo",
    "__pycache__",
    ".pytest_cache",
    ".meos-backups",
    "certs",
    ".cursor",
}

# Placeholders and documented demo-local credentials are allowed.
ALLOW_SUBSTRINGS = (
    "CHANGE_ME",
    "change-me",
    "replace-with",
    "replace-meos",
    "NOT_AVAILABLE",
    "example",
    "placeholder",
    "marpich:marpich",  # documented LOCAL demo DSN only
    "postgresql://marpich:marpich@",
)

RULES: list[tuple[str, re.Pattern[str]]] = [
    ("PRIVATE_KEY_BLOCK", re.compile(r"BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY")),
    ("AWS_ACCESS_KEY_ID", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GITHUB_PAT", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("GITHUB_TOKEN", re.compile(r"\bghp_[A-Za-z0-9]{20,}\b")),
    ("SLACK_TOKEN", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("OPENAI_LIVE_KEY", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9]{20,}\b")),
    ("GOOGLE_API_KEY", re.compile(r"\bAIza[0-9A-Za-z\-_]{20,}\b")),
    ("PEM_RSA_MATERIAL", re.compile(r"-----BEGIN (?:RSA )?PRIVATE KEY-----")),
    ("KUBECONFIG_USER_TOKEN", re.compile(r"(?im)^[ \t]*token:[ \t]+\S{20,}")),
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _allowed(text: str) -> bool:
    lower = text.lower()
    return any(token.lower() in lower for token in ALLOW_SUBSTRINGS)


def iter_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.suffix in {".pyc", ".pyo", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".woff", ".woff2", ".gz", ".zip"}:
            continue
        if path.name == "meos-secret-scan.py":
            continue
        try:
            if path.stat().st_size > 1_500_000:
                continue
        except OSError:
            continue
        out.append(path)
    return out


def scan() -> list[dict[str, str]]:
    root = repo_root()
    hits: list[dict[str, str]] = []
    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if _allowed(text) and "BEGIN " not in text and "AKIA" not in text:
            # Placeholder env templates still get key-block checks below.
            pass
        rel = str(path.relative_to(root))
        example_like = (
            path.name.endswith(".example")
            or path.name.endswith(".example.yml")
            or "example" in path.name.lower()
        )
        for name, pattern in RULES:
            match = pattern.search(text)
            if not match:
                continue
            if example_like and name in {"PRIVATE_KEY_BLOCK", "PEM_RSA_MATERIAL"}:
                # Commented format samples such as -----BEGIN PRIVATE KEY-----\\n...
                snippet = text[max(0, match.start() - 80) : match.end() + 40]
                if snippet.strip().startswith("#") or "\\n..." in snippet or "\n..." in snippet:
                    continue
            if name in {"OPENAI_LIVE_KEY", "GOOGLE_API_KEY"} and _allowed(text):
                continue
            if name == "KUBECONFIG_USER_TOKEN" and _allowed(text):
                continue
            hits.append({"path": rel, "rule": name})
    # Deduplicate path+rule
    uniq: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for hit in hits:
        key = (hit["path"], hit["rule"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(hit)
    return uniq


def main() -> int:
    hits = scan()
    if hits:
        print("SECRET_SCAN_STATUS=FAIL")
        print("BLOCK_RELEASE=TRUE")
        print("hits=%s" % len(hits))
        for hit in hits:
            print("PATH=%s RULE=%s" % (hit["path"], hit["rule"]))
        return 2
    print("SECRET_SCAN_STATUS=PASS")
    print("BLOCK_RELEASE=FALSE")
    print("hits=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
