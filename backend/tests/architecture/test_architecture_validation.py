"""Architecture tests — validation gate helpers."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_validate_architecture_hard_gates_pass() -> None:
    script = REPO_ROOT / "scripts" / "validate-architecture.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
