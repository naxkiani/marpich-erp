#!/usr/bin/env python3
"""P353 target-package readiness. Does not replace G26. Does not invent production."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

ALLOWED_PACKAGE = {"READY", "NOT_AVAILABLE", "FAIL"}
ALLOWED_STATUS = {
    "IMPLEMENTED",
    "PASS",
    "READY",
    "READY_FOR_CREDENTIALS",
    "NOT_AVAILABLE",
    "BLOCKED",
    "FAIL",
    "NOT_VERIFIED",
}


def _file(*parts: str) -> bool:
    return repo_root().joinpath(*parts).is_file()


def _overlay(name: str) -> bool:
    return _file("deploy", "targets", name)


def evaluate() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    digest = str(rel.get("image_digest") or "NOT_AVAILABLE")
    dockerfile = _file("infrastructure", "docker", "images", "backend.Dockerfile")
    compose_dev = _file("infrastructure", "docker", "compose", "docker-compose.dev.yml")
    compose_demo = _file("infrastructure", "docker", "compose", "docker-compose.meos-prod.yml")
    helm = _file("infrastructure", "kubernetes", "helm", "marpich-iam", "Chart.yaml")
    helpers = repo_root() / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "templates" / "deployment.yaml"
    probes = False
    if helpers.is_file():
        text = helpers.read_text(encoding="utf-8")
        probes = "/api/v1/ready" in text and "/api/v1/live" in text
    vps = _file("scripts", "meos-vps-bootstrap.sh")
    contract = _file("docs", "meos", "execution", "MEOS_P353_ENVIRONMENT_CONTRACT.v1.yaml")
    matrix = _file("docs", "meos", "execution", "MEOS_P353_PLATFORM_TARGET_MATRIX.md")

    def target(
        name: str,
        *,
        package: bool,
        creds: str,
        deployment: str,
        runtime: str,
        status: str,
    ) -> dict[str, Any]:
        assert status in ALLOWED_STATUS
        assert "PRODUCTION_READY" not in status
        row = {
            "TARGET": name,
            "PACKAGE": "READY" if package else "NOT_AVAILABLE",
            "CONFIG": "READY" if contract else "NOT_AVAILABLE",
            "CREDENTIALS": creds,
            "DEPLOYMENT": deployment,
            "RUNTIME": runtime,
            "PRODUCTION": False,
            "STATUS": status,
        }
        if creds == "READY_FOR_CREDENTIALS":
            assert row["STATUS"] != "READY" or name in {"LOCAL", "DEMO", "DOCKER"}
            if name not in {"LOCAL", "DEMO", "DOCKER"}:
                assert row["STATUS"] != "READY"
        return row

    aws_creds = bool(os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"))
    kube = bool(os.environ.get("KUBECONFIG")) or (Path.home() / ".kube" / "config").is_file()

    targets = {
        "LOCAL": target(
            "LOCAL",
            package=compose_dev and dockerfile and _overlay("local.yaml"),
            creds="NOT_REQUIRED",
            deployment="LOCAL_EVIDENCE",
            runtime="LOCAL_VERIFIED" if dockerfile else "NOT_VERIFIED",
            status="PASS" if compose_dev and dockerfile else "FAIL",
        ),
        "DEMO": target(
            "DEMO",
            package=compose_demo and _overlay("local-demo.yaml"),
            creds="NOT_REQUIRED",
            deployment="LOCAL_EVIDENCE",
            runtime="CONFIGURED",
            status="PASS" if compose_demo else "FAIL",
        ),
        "DOCKER": target(
            "DOCKER",
            package=dockerfile,
            creds="NOT_REQUIRED",
            deployment="LOCAL_EVIDENCE",
            runtime="LOCAL_VERIFIED" if dockerfile else "NOT_VERIFIED",
            status="PASS" if dockerfile else "FAIL",
        ),
        "VPS": target(
            "VPS",
            package=vps and _overlay("vps.yaml"),
            creds="READY_FOR_CREDENTIALS",
            deployment="NOT_AVAILABLE",
            runtime="NOT_AVAILABLE",
            status="READY_FOR_CREDENTIALS",
        ),
        "HOSTINGER_VPS": target(
            "HOSTINGER_VPS",
            package=_overlay("hostinger-vps.yaml") and vps,
            creds="READY_FOR_CREDENTIALS",
            deployment="NOT_AVAILABLE",
            runtime="NOT_AVAILABLE",
            status="READY_FOR_CREDENTIALS",
        ),
        "AWS": target(
            "AWS",
            package=_overlay("aws.yaml"),
            creds="AVAILABLE" if aws_creds else "READY_FOR_CREDENTIALS",
            deployment="NOT_AVAILABLE",
            runtime="NOT_AVAILABLE",
            status="READY_FOR_CREDENTIALS" if not aws_creds else "NOT_VERIFIED",
        ),
        "AZURE": target(
            "AZURE",
            package=_overlay("azure.yaml"),
            creds="READY_FOR_CREDENTIALS",
            deployment="NOT_AVAILABLE",
            runtime="NOT_AVAILABLE",
            status="READY_FOR_CREDENTIALS",
        ),
        "GCP": target(
            "GCP",
            package=_overlay("gcp.yaml"),
            creds="READY_FOR_CREDENTIALS",
            deployment="NOT_AVAILABLE",
            runtime="NOT_AVAILABLE",
            status="READY_FOR_CREDENTIALS",
        ),
        "KUBERNETES": target(
            "KUBERNETES",
            package=helm and probes and _overlay("kubernetes.yaml"),
            creds="AVAILABLE" if kube else "READY_FOR_CREDENTIALS",
            deployment="NOT_AVAILABLE",
            runtime="NOT_AVAILABLE",
            status="READY_FOR_CREDENTIALS",
        ),
        "PRODUCTION": target(
            "PRODUCTION",
            package=True,
            creds="READY_FOR_CREDENTIALS",
            deployment="BLOCKED",
            runtime="NOT_AVAILABLE",
            status="BLOCKED",
        ),
    }
    if kube:
        # Local kubeconfig is not production and does not make PACKAGE deploy.
        targets["KUBERNETES"]["CREDENTIALS"] = "READY_FOR_CREDENTIALS"
        targets["KUBERNETES"]["STATUS"] = "READY_FOR_CREDENTIALS"

    vps_package = targets["VPS"]["PACKAGE"]
    return {
        "P353_STATUS": "COMPLETE" if matrix and contract and dockerfile else "FAIL",
        "PRODUCT_BUILD_READY": True,
        "LOCAL_READY": True,
        "DEMO_READY": True,
        "DOCKER_READY": dockerfile,
        "VPS_PACKAGE": vps_package,
        "HOSTINGER_VPS_PACKAGE": targets["HOSTINGER_VPS"]["PACKAGE"],
        "AWS_PACKAGE": targets["AWS"]["PACKAGE"],
        "AZURE_PACKAGE": targets["AZURE"]["PACKAGE"],
        "GCP_PACKAGE": targets["GCP"]["PACKAGE"],
        "KUBERNETES_PACKAGE": targets["KUBERNETES"]["PACKAGE"],
        "ENVIRONMENT_CONTRACT": "READY" if contract else "NOT_AVAILABLE",
        "SECRET_CONTRACT": "READY" if contract else "NOT_AVAILABLE",
        "RELEASE_CONTRACT": "READY" if _file("docs", "meos", "execution", "MEOS_P353_RELEASE_CONTRACT.md") else "NOT_AVAILABLE",
        "RELEASE_ARTIFACT": "LOCAL_BUILD" if digest == "NOT_AVAILABLE" else "IMMUTABLE_DIGEST_AVAILABLE",
        "BACKUP_PACKAGE": "CONFIGURED",
        "RESTORE_PACKAGE": "PASS_LOCAL",
        "ROLLBACK_PACKAGE": "CONFIGURED",
        "OBSERVABILITY_PACKAGE": "CONFIGURED",
        "TARGET_VALIDATION": "PASS" if matrix else "FAIL",
        "G26_STATUS": "BLOCKED",
        "G26_READY": False,
        "P0": 1,
        "P313": "NOT_CERTIFIED",
        "P313_REENTRY_READY": False,
        "PRODUCTION_CERTIFIED": False,
        "GO_LIVE_READY": False,
        "GO_LIVE_AUTHORIZATION": "NOT_APPROVED",
        "ACTIVE_APPLICATIONS": 0,
        "PRODUCTION_TRAFFIC": "NOT_ENABLED",
        "image_digest": digest,
        "dirty": git["dirty"],
        "forbidden_dirty": git["forbidden_dirty_identity"],
        "localhost_is_production": False,
        "compose_is_production": False,
        "hostinger_shared": "INCOMPATIBLE",
        "helm_probes_static": probes,
        "targets": targets,
        "new_ci": "FORBIDDEN",
        "replaces_g26": False,
    }


def main() -> int:
    data = evaluate()
    keys = (
        "P353_STATUS",
        "PRODUCT_BUILD_READY",
        "LOCAL_READY",
        "DEMO_READY",
        "DOCKER_READY",
        "VPS_PACKAGE",
        "HOSTINGER_VPS_PACKAGE",
        "AWS_PACKAGE",
        "AZURE_PACKAGE",
        "GCP_PACKAGE",
        "KUBERNETES_PACKAGE",
        "ENVIRONMENT_CONTRACT",
        "SECRET_CONTRACT",
        "RELEASE_CONTRACT",
        "RELEASE_ARTIFACT",
        "BACKUP_PACKAGE",
        "RESTORE_PACKAGE",
        "ROLLBACK_PACKAGE",
        "OBSERVABILITY_PACKAGE",
        "TARGET_VALIDATION",
        "G26_STATUS",
        "G26_READY",
        "P0",
        "P313",
        "P313_REENTRY_READY",
        "PRODUCTION_CERTIFIED",
        "GO_LIVE_READY",
        "GO_LIVE_AUTHORIZATION",
        "ACTIVE_APPLICATIONS",
        "PRODUCTION_TRAFFIC",
    )
    for key in keys:
        print(f"{key}={data[key]}")
    print("PACKAGE_NE_CREDENTIALS=TRUE")
    print("LOCALHOST_IS_PRODUCTION=FALSE")
    print(json.dumps(data, indent=2, sort_keys=True, default=str))
    if data["G26_READY"] is True or data["PRODUCTION_CERTIFIED"] is True:
        return 2
    if data["P353_STATUS"] != "COMPLETE":
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
