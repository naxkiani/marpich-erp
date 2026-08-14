"""P210-N Deploy / DevSecOps aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsDeployAutomatedPipelineRoot(AggregateRoot):
    tenant_id: str
    pipeline_ref: str
    automated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def start(
        cls, *, tenant_id: str, pipeline_ref: str, automated: bool = True
    ) -> CsDeployAutomatedPipelineRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.deploy.tenant_required")
        if not automated:
            raise ValueError(
                "cyber_security.deploy.deployment_is_not_automated"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            pipeline_ref=pipeline_ref.strip(),
            automated=True,
            status="running",
        )
        root.pending_events.append("DeploymentPipelineStarted")
        root.pending_events.append("NonAutomatedDeployRejected")
        root.history.append({"event": "PipelineAutomated"})
        return root

    def is_manual_only(self) -> bool:
        return not self.automated


@dataclass(eq=False, kw_only=True)
class CsDeployK8sSecurityRoot(AggregateRoot):
    tenant_id: str
    cluster_ref: str
    security_complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def harden(
        cls,
        *,
        tenant_id: str,
        cluster_ref: str,
        security_complete: bool = True,
    ) -> CsDeployK8sSecurityRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.deploy.k8s_tenant_required")
        if not security_complete:
            raise ValueError(
                "cyber_security.deploy.kubernetes_security_is_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            cluster_ref=cluster_ref.strip(),
            security_complete=True,
            status="hardened",
        )
        root.pending_events.append("KubernetesWorkloadDeployed")
        root.pending_events.append("IncompleteK8sSecurityRejected")
        root.history.append({"event": "K8sSecurityComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.security_complete


@dataclass(eq=False, kw_only=True)
class CsDeployReproducibleInfraRoot(AggregateRoot):
    tenant_id: str
    stack_ref: str
    reproducible: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def provision(
        cls, *, tenant_id: str, stack_ref: str, reproducible: bool = True
    ) -> CsDeployReproducibleInfraRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.deploy.iac_tenant_required")
        if not reproducible:
            raise ValueError(
                "cyber_security.deploy.infrastructure_cannot_be_reproduced"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            stack_ref=stack_ref.strip(),
            reproducible=True,
            status="provisioned",
        )
        root.pending_events.append("InfrastructureReproduced")
        root.pending_events.append("NonReproducibleInfraRejected")
        root.history.append({"event": "IaCApplied"})
        return root

    def is_non_reproducible(self) -> bool:
        return not self.reproducible


@dataclass(eq=False, kw_only=True)
class CsDeployObservabilityRoot(AggregateRoot):
    tenant_id: str
    service_ref: str
    observability_present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def attach(
        cls,
        *,
        tenant_id: str,
        service_ref: str,
        observability_present: bool = True,
    ) -> CsDeployObservabilityRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.deploy.obs_tenant_required")
        if not observability_present:
            raise ValueError(
                "cyber_security.deploy.observability_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            service_ref=service_ref.strip(),
            observability_present=True,
            status="instrumented",
        )
        root.pending_events.append("ObservabilityAttached")
        root.pending_events.append("MissingObservabilityRejected")
        root.history.append({"event": "OTelAttached"})
        return root

    def is_missing(self) -> bool:
        return not self.observability_present


@dataclass(eq=False, kw_only=True)
class CsDeployAutoScalingRoot(AggregateRoot):
    tenant_id: str
    service_ref: str
    auto_scaling: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, service_ref: str, auto_scaling: bool = True
    ) -> CsDeployAutoScalingRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.deploy.scale_tenant_required")
        if not auto_scaling:
            raise ValueError("cyber_security.deploy.scaling_is_manual")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            service_ref=service_ref.strip(),
            auto_scaling=True,
            status="autoscaled",
        )
        root.pending_events.append("ScalingPolicyApplied")
        root.pending_events.append("ManualOnlyScalingRejected")
        root.history.append({"event": "AutoScalingEnabled"})
        return root

    def is_manual_only(self) -> bool:
        return not self.auto_scaling


@dataclass(eq=False, kw_only=True)
class CsDeployDisasterRecoveryRoot(AggregateRoot):
    tenant_id: str
    plan_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls, *, tenant_id: str, plan_ref: str, defined: bool = True
    ) -> CsDeployDisasterRecoveryRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.deploy.dr_tenant_required")
        if not defined:
            raise ValueError(
                "cyber_security.deploy.disaster_recovery_is_undefined"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            plan_ref=plan_ref.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("DisasterRecoveryPlanDefined")
        root.pending_events.append("UndefinedDrRejected")
        root.history.append({"event": "DrPlanDeclared"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class CsDeploySecurityControlsRoot(AggregateRoot):
    tenant_id: str
    control_ref: str
    integrated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, control_ref: str, integrated: bool = True
    ) -> CsDeploySecurityControlsRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.deploy.ctrl_tenant_required")
        if not integrated:
            raise ValueError(
                "cyber_security.deploy.security_controls_are_not_integrated"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            control_ref=control_ref.strip(),
            integrated=True,
            status="integrated",
        )
        root.pending_events.append("SecurityValidationPassed")
        root.pending_events.append("UnintegratedControlsRejected")
        root.history.append({"event": "SecurityControlsIntegrated"})
        return root

    def is_unintegrated(self) -> bool:
        return not self.integrated


@dataclass(eq=False, kw_only=True)
class CsDeployPipelineValidationRoot(AggregateRoot):
    tenant_id: str
    pipeline_ref: str
    validated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def validate(
        cls, *, tenant_id: str, pipeline_ref: str, validated: bool = True
    ) -> CsDeployPipelineValidationRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.deploy.val_tenant_required")
        if not validated:
            raise ValueError(
                "cyber_security.deploy.devsecops_pipeline_lacks_validation"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            pipeline_ref=pipeline_ref.strip(),
            validated=True,
            status="validated",
        )
        root.pending_events.append("ContainerImageSigned")
        root.pending_events.append("UnvalidatedPipelineRejected")
        root.history.append({"event": "PipelineValidated"})
        return root

    def lacks_validation(self) -> bool:
        return not self.validated
