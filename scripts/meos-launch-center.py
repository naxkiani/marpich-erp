#!/usr/bin/env python3
"""P395 Launch Center CLI snapshot. Same honesty as the UI."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_p395 import evaluate  # noqa: E402


def main() -> int:
    data = evaluate()
    print(json.dumps(data, indent=2, sort_keys=True, default=str))
    print(f"P395_STATUS={data['P395_STATUS']}")
    print("G26_READY=FALSE")
    print("PRODUCTION_READY=False")
    return 2


if __name__ == "__main__":
    sys.exit(main())
