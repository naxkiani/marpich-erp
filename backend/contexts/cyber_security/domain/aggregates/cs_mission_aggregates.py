"""P210-B Cyber Security mission/vision/scope aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsMissionMeasurableRoot(AggregateRoot):
    tenant_id: str
    mission_ref: str
    measurable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, mission_ref: str, measurable: bool = True
    ) -> CsMissionMeasurableRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.mission.tenant_required")
        if not measurable:
            raise ValueError("cyber_security.mission.mission_not_measurable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            mission_ref=mission_ref.strip(),
            measurable=True,
            status="published",
        )
        root.pending_events.append("MissionPublished")
        root.history.append({"event": "MissionPublishedMeasurable"})
        return root

    def is_unmeasurable(self) -> bool:
        return not self.measurable


@dataclass(eq=False, kw_only=True)
class CsVisionEnterpriseScaleRoot(AggregateRoot):
    tenant_id: str
    vision_ref: str
    enterprise_scale: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, vision_ref: str, enterprise_scale: bool = True
    ) -> CsVisionEnterpriseScaleRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.mission.vision_tenant_required")
        if not enterprise_scale:
            raise ValueError(
                "cyber_security.mission.vision_not_enterprise_scale"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            vision_ref=vision_ref.strip(),
            enterprise_scale=True,
            status="published",
        )
        root.pending_events.append("VisionPublished")
        root.history.append({"event": "VisionPublishedEnterpriseScale"})
        return root

    def is_non_enterprise(self) -> bool:
        return not self.enterprise_scale


@dataclass(eq=False, kw_only=True)
class CsScopeCompleteRoot(AggregateRoot):
    tenant_id: str
    scope_ref: str
    complete: bool
    item_count: int
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls,
        *,
        tenant_id: str,
        scope_ref: str,
        complete: bool = True,
        item_count: int = 26,
    ) -> CsScopeCompleteRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.mission.scope_tenant_required")
        if not complete or item_count < 20:
            raise ValueError(
                "cyber_security.mission.enterprise_scope_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            scope_ref=scope_ref.strip(),
            complete=True,
            item_count=item_count,
            status="declared",
        )
        root.pending_events.append("ScopeDeclared")
        root.history.append({"event": "EnterpriseScopeComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete or self.item_count < 20


@dataclass(eq=False, kw_only=True)
class CsDomainsUnifiedRoot(AggregateRoot):
    tenant_id: str
    map_ref: str
    fragmented: bool
    domain_count: int
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        map_ref: str,
        fragmented: bool = False,
        domain_count: int = 19,
    ) -> CsDomainsUnifiedRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.mission.domain_tenant_required")
        if fragmented or domain_count < 15:
            raise ValueError(
                "cyber_security.mission.security_domains_fragmented"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            map_ref=map_ref.strip(),
            fragmented=False,
            domain_count=domain_count,
            status="unified",
        )
        root.pending_events.append("DomainRegistered")
        root.pending_events.append("FragmentedDomainsRejected")
        root.history.append({"event": "SecurityDomainsUnified"})
        return root

    def is_fragmented(self) -> bool:
        return self.fragmented or self.domain_count < 15


@dataclass(eq=False, kw_only=True)
class CsZeroTrustPresentRoot(AggregateRoot):
    tenant_id: str
    principle_ref: str
    zero_trust: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def adopt(
        cls, *, tenant_id: str, principle_ref: str, zero_trust: bool = True
    ) -> CsZeroTrustPresentRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.mission.zt_tenant_required")
        if not zero_trust:
            raise ValueError("cyber_security.mission.zero_trust_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            principle_ref=principle_ref.strip(),
            zero_trust=True,
            status="adopted",
        )
        root.pending_events.append("PrincipleAdopted")
        root.pending_events.append("ZeroTrustAbsenceRejected")
        root.history.append({"event": "ZeroTrustAdopted"})
        return root

    def is_absent(self) -> bool:
        return not self.zero_trust


@dataclass(eq=False, kw_only=True)
class CsAiSecurityPresentRoot(AggregateRoot):
    tenant_id: str
    surface_ref: str
    ai_security: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, surface_ref: str, ai_security: bool = True
    ) -> CsAiSecurityPresentRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.mission.ai_tenant_required")
        if not ai_security:
            raise ValueError("cyber_security.mission.ai_security_omitted")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            surface_ref=surface_ref.strip(),
            ai_security=True,
            status="enabled",
        )
        root.history.append({"event": "AiSecurityEnabled"})
        return root

    def is_omitted(self) -> bool:
        return not self.ai_security


@dataclass(eq=False, kw_only=True)
class CsObjectivesMeosAlignedRoot(AggregateRoot):
    tenant_id: str
    register_ref: str
    aligned: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def align(
        cls, *, tenant_id: str, register_ref: str, aligned: bool = True
    ) -> CsObjectivesMeosAlignedRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.mission.obj_tenant_required")
        if not aligned:
            raise ValueError(
                "cyber_security.mission.strategic_objectives_not_aligned_with_meos"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            register_ref=register_ref.strip(),
            aligned=True,
            status="aligned",
        )
        root.pending_events.append("ObjectiveAligned")
        root.history.append({"event": "ObjectivesMeosAligned"})
        return root

    def is_misaligned(self) -> bool:
        return not self.aligned


@dataclass(eq=False, kw_only=True)
class CsKpiRegisterRoot(AggregateRoot):
    tenant_id: str
    kpi_ref: str
    kpi_count: int
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls, *, tenant_id: str, kpi_ref: str, kpi_count: int = 12
    ) -> CsKpiRegisterRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.mission.kpi_tenant_required")
        if kpi_count < 6:
            raise ValueError("cyber_security.mission.mission_not_measurable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            kpi_ref=kpi_ref.strip(),
            kpi_count=kpi_count,
            status="registered",
        )
        root.pending_events.append("KpiRegistered")
        root.history.append({"event": "KpisRegistered"})
        return root
