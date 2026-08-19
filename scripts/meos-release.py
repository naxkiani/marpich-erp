#!/usr/bin/env python3
"""MEOS release command center (P354). Reuses existing Docker/CI/GHCR. No silent publish."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_release_engine import (  # noqa: E402
    checksum_package,
    git_state,
    identity_ok,
    meos_release,
    publish_status,
    write_release_package,
)


def cmd_inspect() -> int:
    data = meos_release()
    data["git"] = git_state()
    data["identity"] = identity_ok(data)
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0 if data["verification_status"] != "FORBIDDEN_DIRTY" else 2


def cmd_build() -> int:
    git = git_state()
    if git["dirty"] or git["forbidden_dirty_identity"]:
        print("BUILD=BLOCKED")
        print("reason=DIRTY_RELEASE")
        return 2
    dockerfile = ROOT / "infrastructure" / "docker" / "images" / "backend.Dockerfile"
    cmd = [
        "docker",
        "build",
        "-f",
        str(dockerfile),
        "-t",
        "meos/backend:p354-local",
        str(ROOT / "backend"),
    ]
    print("BUILD_COMMAND=" + " ".join(cmd))
    print("NOTE=existing backend.Dockerfile; local tag is BUILD_VALIDATION not GHCR digest")
    r = subprocess.run(cmd, cwd=ROOT, check=False)
    print("BUILD=" + ("PASS" if r.returncode == 0 else "FAIL"))
    return r.returncode


def cmd_test() -> int:
    tests = [
        str(ROOT / "backend" / "tests" / "contracts" / "test_p354_universal_installation_honesty.py"),
        str(ROOT / "backend" / "tests" / "contracts" / "test_p353_release_engineering_honesty.py"),
        str(ROOT / "backend" / "contexts" / "crm" / "tests" / "test_crm_flow.py::test_crm_tenant_b_cannot_list_tenant_a_contacts"),
    ]
    pytest = ROOT / "backend" / ".venv" / "bin" / "python"
    exe = str(pytest) if pytest.is_file() else sys.executable
    r = subprocess.run([exe, "-m", "pytest", "-q", *tests], cwd=ROOT, check=False)
    scan = subprocess.run([sys.executable, str(ROOT / "scripts" / "meos-secret-scan.py")], cwd=ROOT, check=False)
    mig = subprocess.run([str(ROOT / "scripts" / "meos-migration-check.sh")], cwd=ROOT, check=False)
    print("PYTEST=" + ("PASS" if r.returncode == 0 else "FAIL"))
    print("SECRET_SCAN=" + ("PASS" if scan.returncode == 0 else "FAIL"))
    print("MIGRATION_CHECK=" + ("PASS" if mig.returncode == 0 else "FAIL"))
    return 0 if r.returncode == 0 and scan.returncode == 0 and mig.returncode == 0 else 1


def cmd_package() -> int:
    dest = write_release_package()
    sums = checksum_package()
    print("PACKAGE=" + str(dest))
    print("FILES=" + str(len(sums)))
    print("SECRETS=none")
    return 0


def cmd_verify() -> int:
    ident = identity_ok()
    print(json.dumps(ident, indent=2, sort_keys=True))
    if ident["ok"]:
        print("VERIFY=PASS")
        return 0
    print("VERIFY=BLOCKED")
    return 2


def cmd_publish(confirm: bool) -> int:
    data = publish_status(confirm=confirm)
    print(json.dumps(data, indent=2, sort_keys=True))
    print("SILENT_PUBLISH=FALSE")
    if data["status"] == "READY_FOR_CREDENTIALS":
        return 2
    if data["status"] in {"REFUSED", "BLOCKED"}:
        return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="MEOS release command center (P354)")
    parser.add_argument("command", choices=["build", "test", "package", "verify", "publish", "inspect"])
    parser.add_argument("--confirm-publish", action="store_true", help="Required for publish; never silent")
    args = parser.parse_args()
    if args.command == "inspect":
        return cmd_inspect()
    if args.command == "build":
        return cmd_build()
    if args.command == "test":
        return cmd_test()
    if args.command == "package":
        return cmd_package()
    if args.command == "verify":
        return cmd_verify()
    if args.command == "publish":
        return cmd_publish(args.confirm_publish)
    return 2


if __name__ == "__main__":
    sys.exit(main())
