"""Analytics FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.analytics.container import get_analytics_service
from contexts.analytics.presentation.schemas import CreateAlertRequest
from contexts.identity.presentation.dependencies import (
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/metrics")
async def list_metrics(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("analytics.metrics.read"))],
):
    result = await get_analytics_service().list_metrics(tenant_id)
    return {"data": result.unwrap()}


@router.get("/metrics/{metric_key}/timeseries")
async def get_timeseries(
    metric_key: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("analytics.metrics.read"))],
):
    result = await get_analytics_service().get_timeseries(tenant_id, metric_key)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.get("/dashboards")
async def list_dashboards(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
):
    result = await get_analytics_service().list_dashboards(tenant_id)
    return {"data": result.unwrap()}


@router.get("/dashboards/{dashboard_id}")
async def get_dashboard(
    dashboard_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
):
    result = await get_analytics_service().get_dashboard(tenant_id, dashboard_id)
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}


@router.post("/alerts", status_code=status.HTTP_201_CREATED)
async def create_alert(
    body: CreateAlertRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("analytics.alerts.write"))],
):
    result = await get_analytics_service().create_alert(
        tenant_id=tenant_id,
        metric_key=body.metric_key,
        name=body.name,
        threshold=body.threshold,
        operator=body.operator,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap()}


@router.get("/alerts")
async def list_alerts(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("analytics.alerts.write"))],
):
    result = await get_analytics_service().list_alerts(tenant_id)
    return {"data": result.unwrap()}


@router.get("/events/summary")
async def get_events_summary(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("analytics.events.read"))],
):
    result = await get_analytics_service().get_events_summary(tenant_id)
    return {"data": result.unwrap()}


# --- P213 Enterprise BI Fabric ---


@router.get("/catalog")
async def bi_catalog(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {
        "data": (await get_analytics_service().list_catalog()).unwrap()
    }


@router.get("/strategy")
async def bi_strategy(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_strategy()}


@router.get("/strategy/readiness")
async def bi_strategy_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().strategy_readiness()}


@router.get("/mission")
async def bi_mission(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_mission()}


@router.get("/mission/readiness")
async def bi_mission_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().mission_readiness()}


@router.get("/domain")
async def bi_domain(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_domain()}


@router.get("/domain/map")
async def bi_domain_map(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_map()}


@router.get("/domain/bounded-contexts")
async def bi_domain_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_bounded_contexts()}


@router.get("/domain/aggregates")
async def bi_domain_aggregates(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_aggregates()}


@router.get("/domain/entities")
async def bi_domain_entities(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_entities()}


@router.get("/domain/value-objects")
async def bi_domain_value_objects(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_value_objects()}


@router.get("/domain/ownership")
async def bi_domain_ownership(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_ownership()}


@router.get("/domain/services")
async def bi_domain_services(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_services_catalog()}


@router.get("/domain/events")
async def bi_domain_events(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_events()}


@router.get("/domain/microservices")
async def bi_domain_microservices(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_microservices()}


@router.get("/domain/integrations")
async def bi_domain_integrations(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_integrations()}


@router.get("/domain/cqrs")
async def bi_domain_cqrs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_cqrs()}


@router.get("/domain/apis")
async def bi_domain_apis(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_apis()}


@router.get("/domain/deployment")
async def bi_domain_deployment(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_deployment()}


@router.get("/domain/outputs")
async def bi_domain_outputs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_outputs()}


@router.get("/domain/production-readiness")
async def bi_domain_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_production_readiness()}


@router.get("/domain/readiness")
async def bi_domain_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().domain_readiness()}

# --- P213-D reporting / experience fabric ---

@router.get("/reporting")
async def bi_reporting(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_reporting()}


@router.get("/reporting/vision")
async def bi_reporting_vision(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_vision()}


@router.get("/reporting/domain")
async def bi_reporting_domain(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_domain()}


@router.get("/reporting/bounded-contexts")
async def bi_reporting_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_bounded_contexts()}


@router.get("/reporting/layers")
async def bi_reporting_layers(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_layers()}


@router.get("/reporting/engine")
async def bi_reporting_engine(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_engine()}


@router.get("/reporting/dashboards")
async def bi_reporting_dashboards(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_dashboards()}


@router.get("/reporting/visualizations")
async def bi_reporting_visualizations(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_visualizations()}


@router.get("/reporting/self-service")
async def bi_reporting_self_service(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_self_service()}


@router.get("/reporting/real-time")
async def bi_reporting_real_time(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_real_time()}


@router.get("/reporting/ai")
async def bi_reporting_ai(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_ai()}


@router.get("/reporting/knowledge-graph")
async def bi_reporting_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_knowledge_graph()}


@router.get("/reporting/digital-twin")
async def bi_reporting_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_digital_twin()}


@router.get("/reporting/cqrs")
async def bi_reporting_cqrs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_cqrs()}


@router.get("/reporting/events")
async def bi_reporting_events(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_events()}


@router.get("/reporting/microservices")
async def bi_reporting_microservices(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_microservices()}


@router.get("/reporting/apis")
async def bi_reporting_apis(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_apis()}


@router.get("/reporting/security")
async def bi_reporting_security(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_security()}


@router.get("/reporting/deployment")
async def bi_reporting_deployment(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_deployment()}


@router.get("/reporting/testing")
async def bi_reporting_testing(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_testing()}


@router.get("/reporting/outputs")
async def bi_reporting_outputs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_outputs()}


@router.get("/reporting/production-readiness")
async def bi_reporting_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_production_readiness()}


@router.get("/reporting/readiness")
async def bi_reporting_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().reporting_readiness()}


# --- P213-E warehouse / analytical data fabric ---

@router.get("/warehouse")
async def bi_warehouse(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_warehouse()}


@router.get("/warehouse/vision")
async def bi_warehouse_vision(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_vision()}


@router.get("/warehouse/domain")
async def bi_warehouse_domain(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_domain()}


@router.get("/warehouse/bounded-contexts")
async def bi_warehouse_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_bounded_contexts()}


@router.get("/warehouse/layers")
async def bi_warehouse_layers(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_layers()}


@router.get("/warehouse/dimensional-model")
async def bi_warehouse_dimensional_model(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_dimensional_model()}


@router.get("/warehouse/subject-areas")
async def bi_warehouse_subject_areas(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_subject_areas()}


@router.get("/warehouse/ingestion")
async def bi_warehouse_ingestion(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_ingestion()}


@router.get("/warehouse/transformation")
async def bi_warehouse_transformation(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_transformation()}


@router.get("/warehouse/governance")
async def bi_warehouse_governance(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_governance()}


@router.get("/warehouse/semantic-layer")
async def bi_warehouse_semantic_layer(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_semantic_layer()}


@router.get("/warehouse/knowledge-graph")
async def bi_warehouse_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_knowledge_graph()}


@router.get("/warehouse/ai-foundation")
async def bi_warehouse_ai_foundation(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_ai_foundation()}


@router.get("/warehouse/digital-twin")
async def bi_warehouse_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_digital_twin()}


@router.get("/warehouse/cqrs")
async def bi_warehouse_cqrs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_cqrs()}


@router.get("/warehouse/events")
async def bi_warehouse_events(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_events()}


@router.get("/warehouse/microservices")
async def bi_warehouse_microservices(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_microservices()}


@router.get("/warehouse/apis")
async def bi_warehouse_apis(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_apis()}


@router.get("/warehouse/security")
async def bi_warehouse_security(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_security()}


@router.get("/warehouse/deployment")
async def bi_warehouse_deployment(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_deployment()}


@router.get("/warehouse/testing")
async def bi_warehouse_testing(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_testing()}


@router.get("/warehouse/outputs")
async def bi_warehouse_outputs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_outputs()}


@router.get("/warehouse/production-readiness")
async def bi_warehouse_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_production_readiness()}


@router.get("/warehouse/readiness")
async def bi_warehouse_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().warehouse_readiness()}


# --- P213-F lakehouse intelligence fabric ---

@router.get("/lakehouse")
async def bi_lakehouse(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_lakehouse()}


@router.get("/lakehouse/vision")
async def bi_lakehouse_vision(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_vision()}


@router.get("/lakehouse/domain")
async def bi_lakehouse_domain(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_domain()}


@router.get("/lakehouse/bounded-contexts")
async def bi_lakehouse_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_bounded_contexts()}


@router.get("/lakehouse/layers")
async def bi_lakehouse_layers(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_layers()}


@router.get("/lakehouse/storage")
async def bi_lakehouse_storage(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_storage()}


@router.get("/lakehouse/processing")
async def bi_lakehouse_processing(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_processing()}


@router.get("/lakehouse/data-products")
async def bi_lakehouse_data_products(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_data_products()}


@router.get("/lakehouse/governance")
async def bi_lakehouse_governance(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_governance()}


@router.get("/lakehouse/semantic-layer")
async def bi_lakehouse_semantic_layer(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_semantic_layer()}


@router.get("/lakehouse/ai")
async def bi_lakehouse_ai(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_ai()}


@router.get("/lakehouse/knowledge-graph")
async def bi_lakehouse_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_knowledge_graph()}


@router.get("/lakehouse/digital-twin")
async def bi_lakehouse_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_digital_twin()}


@router.get("/lakehouse/cqrs")
async def bi_lakehouse_cqrs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_cqrs()}


@router.get("/lakehouse/events")
async def bi_lakehouse_events(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_events()}


@router.get("/lakehouse/microservices")
async def bi_lakehouse_microservices(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_microservices()}


@router.get("/lakehouse/apis")
async def bi_lakehouse_apis(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_apis()}


@router.get("/lakehouse/security")
async def bi_lakehouse_security(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_security()}


@router.get("/lakehouse/deployment")
async def bi_lakehouse_deployment(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_deployment()}


@router.get("/lakehouse/testing")
async def bi_lakehouse_testing(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_testing()}


@router.get("/lakehouse/outputs")
async def bi_lakehouse_outputs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_outputs()}


@router.get("/lakehouse/production-readiness")
async def bi_lakehouse_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_production_readiness()}


@router.get("/lakehouse/readiness")
async def bi_lakehouse_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().lakehouse_readiness()}


# --- P213-G OLAP / semantic intelligence fabric ---

@router.get("/olap")
async def bi_olap(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_olap()}


@router.get("/olap/vision")
async def bi_olap_vision(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_vision()}


@router.get("/olap/domain")
async def bi_olap_domain(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_domain()}


@router.get("/olap/bounded-contexts")
async def bi_olap_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_bounded_contexts()}


@router.get("/olap/metrics")
async def bi_olap_metrics(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_metrics()}


@router.get("/olap/kpi-governance")
async def bi_olap_kpi_governance(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_kpi_governance()}


@router.get("/olap/semantic-layer")
async def bi_olap_semantic_layer(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_semantic_layer()}


@router.get("/olap/modes")
async def bi_olap_modes(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_modes()}


@router.get("/olap/dimensions")
async def bi_olap_dimensions(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_dimensions()}


@router.get("/olap/calculation-engine")
async def bi_olap_calculation_engine(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_calculation_engine()}


@router.get("/olap/semantic-query")
async def bi_olap_semantic_query(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_semantic_query()}


@router.get("/olap/knowledge-graph")
async def bi_olap_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_knowledge_graph()}


@router.get("/olap/ai")
async def bi_olap_ai(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_ai()}


@router.get("/olap/digital-twin")
async def bi_olap_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_digital_twin()}


@router.get("/olap/cqrs")
async def bi_olap_cqrs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_cqrs()}


@router.get("/olap/events")
async def bi_olap_events(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_events()}


@router.get("/olap/microservices")
async def bi_olap_microservices(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_microservices()}


@router.get("/olap/apis")
async def bi_olap_apis(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_apis()}


@router.get("/olap/security")
async def bi_olap_security(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_security()}


@router.get("/olap/deployment")
async def bi_olap_deployment(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_deployment()}


@router.get("/olap/testing")
async def bi_olap_testing(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_testing()}


@router.get("/olap/outputs")
async def bi_olap_outputs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_outputs()}


@router.get("/olap/production-readiness")
async def bi_olap_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_production_readiness()}


@router.get("/olap/readiness")
async def bi_olap_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().olap_readiness()}


# --- P213-H self-service analytics experience fabric ---

@router.get("/self-service")
async def bi_self_service(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_self_service()}


@router.get("/self-service/vision")
async def bi_self_service_vision(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_vision()}


@router.get("/self-service/domain")
async def bi_self_service_domain(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_domain()}


@router.get("/self-service/bounded-contexts")
async def bi_self_service_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_bounded_contexts()}


@router.get("/self-service/workspaces")
async def bi_self_service_workspaces(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_workspaces()}


@router.get("/self-service/discovery")
async def bi_self_service_discovery(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_discovery()}


@router.get("/self-service/no-code")
async def bi_self_service_no_code(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_no_code()}


@router.get("/self-service/ad-hoc")
async def bi_self_service_ad_hoc(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_ad_hoc()}


@router.get("/self-service/collaboration")
async def bi_self_service_collaboration(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_collaboration()}


@router.get("/self-service/ai")
async def bi_self_service_ai(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_ai()}


@router.get("/self-service/natural-language")
async def bi_self_service_natural_language(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_natural_language()}


@router.get("/self-service/semantic")
async def bi_self_service_semantic(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_semantic()}


@router.get("/self-service/knowledge-graph")
async def bi_self_service_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_knowledge_graph()}


@router.get("/self-service/digital-twin")
async def bi_self_service_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_digital_twin()}


@router.get("/self-service/cqrs")
async def bi_self_service_cqrs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_cqrs()}


@router.get("/self-service/events")
async def bi_self_service_events(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_events()}


@router.get("/self-service/microservices")
async def bi_self_service_microservices(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_microservices()}


@router.get("/self-service/apis")
async def bi_self_service_apis(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_apis()}


@router.get("/self-service/security")
async def bi_self_service_security(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_security()}


@router.get("/self-service/deployment")
async def bi_self_service_deployment(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_deployment()}


@router.get("/self-service/testing")
async def bi_self_service_testing(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_testing()}


@router.get("/self-service/outputs")
async def bi_self_service_outputs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_outputs()}


@router.get("/self-service/production-readiness")
async def bi_self_service_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_production_readiness()}


@router.get("/self-service/readiness")
async def bi_self_service_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().self_service_readiness()}


# --- P213-I advanced analytics fabric ---

@router.get("/advanced")
async def bi_advanced(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_advanced()}


@router.get("/advanced/vision")
async def bi_advanced_vision(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_vision()}


@router.get("/advanced/domain")
async def bi_advanced_domain(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_domain()}


@router.get("/advanced/bounded-contexts")
async def bi_advanced_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_bounded_contexts()}


@router.get("/advanced/workbench")
async def bi_advanced_workbench(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_workbench()}


@router.get("/advanced/statistical")
async def bi_advanced_statistical(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_statistical()}


@router.get("/advanced/patterns")
async def bi_advanced_patterns(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_patterns()}


@router.get("/advanced/root-cause")
async def bi_advanced_root_cause(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_root_cause()}


@router.get("/advanced/experiments")
async def bi_advanced_experiments(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_experiments()}


@router.get("/advanced/visual")
async def bi_advanced_visual(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_visual()}


@router.get("/advanced/ai")
async def bi_advanced_ai(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_ai()}


@router.get("/advanced/knowledge-graph")
async def bi_advanced_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_knowledge_graph()}


@router.get("/advanced/digital-twin")
async def bi_advanced_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_digital_twin()}


@router.get("/advanced/cqrs")
async def bi_advanced_cqrs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_cqrs()}


@router.get("/advanced/events")
async def bi_advanced_events(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_events()}


@router.get("/advanced/microservices")
async def bi_advanced_microservices(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_microservices()}


@router.get("/advanced/apis")
async def bi_advanced_apis(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_apis()}


@router.get("/advanced/security")
async def bi_advanced_security(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_security()}


@router.get("/advanced/deployment")
async def bi_advanced_deployment(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_deployment()}


@router.get("/advanced/testing")
async def bi_advanced_testing(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_testing()}


@router.get("/advanced/outputs")
async def bi_advanced_outputs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_outputs()}


@router.get("/advanced/production-readiness")
async def bi_advanced_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_production_readiness()}


@router.get("/advanced/readiness")
async def bi_advanced_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().advanced_readiness()}


# --- P213-J predictive intelligence fabric ---

@router.get("/predictive")
async def bi_predictive(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_predictive()}


@router.get("/predictive/vision")
async def bi_predictive_vision(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_vision()}


@router.get("/predictive/domain")
async def bi_predictive_domain(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_domain()}


@router.get("/predictive/bounded-contexts")
async def bi_predictive_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_bounded_contexts()}


@router.get("/predictive/forecast-management")
async def bi_predictive_forecast_management(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_forecast_management()}


@router.get("/predictive/models")
async def bi_predictive_models(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_models()}


@router.get("/predictive/engine")
async def bi_predictive_engine(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_engine()}


@router.get("/predictive/scenarios")
async def bi_predictive_scenarios(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_scenarios()}


@router.get("/predictive/time-series")
async def bi_predictive_time_series(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_time_series()}


@router.get("/predictive/ai")
async def bi_predictive_ai(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_ai()}


@router.get("/predictive/explainability")
async def bi_predictive_explainability(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_explainability()}


@router.get("/predictive/knowledge-graph")
async def bi_predictive_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_knowledge_graph()}


@router.get("/predictive/digital-twin")
async def bi_predictive_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_digital_twin()}


@router.get("/predictive/cqrs")
async def bi_predictive_cqrs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_cqrs()}


@router.get("/predictive/events")
async def bi_predictive_events(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_events()}


@router.get("/predictive/microservices")
async def bi_predictive_microservices(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_microservices()}


@router.get("/predictive/apis")
async def bi_predictive_apis(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_apis()}


@router.get("/predictive/security")
async def bi_predictive_security(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_security()}


@router.get("/predictive/deployment")
async def bi_predictive_deployment(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_deployment()}


@router.get("/predictive/testing")
async def bi_predictive_testing(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_testing()}


@router.get("/predictive/outputs")
async def bi_predictive_outputs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_outputs()}


@router.get("/predictive/production-readiness")
async def bi_predictive_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_production_readiness()}


@router.get("/predictive/readiness")
async def bi_predictive_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().predictive_readiness()}


# --- P213-K decision optimization fabric ---

@router.get("/prescriptive")
async def bi_prescriptive(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_prescriptive()}


@router.get("/prescriptive/vision")
async def bi_prescriptive_vision(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_vision()}


@router.get("/prescriptive/domain")
async def bi_prescriptive_domain(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_domain()}


@router.get("/prescriptive/bounded-contexts")
async def bi_prescriptive_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_bounded_contexts()}


@router.get("/prescriptive/optimization")
async def bi_prescriptive_optimization(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_optimization()}


@router.get("/prescriptive/engine")
async def bi_prescriptive_engine(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_engine()}


@router.get("/prescriptive/recommendations")
async def bi_prescriptive_recommendations(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_recommendations()}


@router.get("/prescriptive/objectives")
async def bi_prescriptive_objectives(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_objectives()}


@router.get("/prescriptive/constraints")
async def bi_prescriptive_constraints(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_constraints()}


@router.get("/prescriptive/ai")
async def bi_prescriptive_ai(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_ai()}


@router.get("/prescriptive/explainability")
async def bi_prescriptive_explainability(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_explainability()}


@router.get("/prescriptive/knowledge-graph")
async def bi_prescriptive_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_knowledge_graph()}


@router.get("/prescriptive/digital-twin")
async def bi_prescriptive_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_digital_twin()}


@router.get("/prescriptive/cqrs")
async def bi_prescriptive_cqrs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_cqrs()}


@router.get("/prescriptive/events")
async def bi_prescriptive_events(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_events()}


@router.get("/prescriptive/microservices")
async def bi_prescriptive_microservices(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_microservices()}


@router.get("/prescriptive/apis")
async def bi_prescriptive_apis(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_apis()}


@router.get("/prescriptive/security")
async def bi_prescriptive_security(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_security()}


@router.get("/prescriptive/deployment")
async def bi_prescriptive_deployment(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_deployment()}


@router.get("/prescriptive/testing")
async def bi_prescriptive_testing(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_testing()}


@router.get("/prescriptive/outputs")
async def bi_prescriptive_outputs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_outputs()}


@router.get("/prescriptive/production-readiness")
async def bi_prescriptive_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_production_readiness()}


@router.get("/prescriptive/readiness")
async def bi_prescriptive_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().prescriptive_readiness()}


# --- P213-L decision knowledge fabric ---

@router.get("/graph")
async def bi_graph(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_graph()}


@router.get("/graph/vision")
async def bi_graph_vision(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_vision()}


@router.get("/graph/domain")
async def bi_graph_domain(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_domain()}


@router.get("/graph/bounded-contexts")
async def bi_graph_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_bounded_contexts()}


@router.get("/graph/model")
async def bi_graph_model(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_model()}


@router.get("/graph/ontology")
async def bi_graph_ontology(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_ontology()}


@router.get("/graph/lineage")
async def bi_graph_lineage(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_lineage()}


@router.get("/graph/analytics")
async def bi_graph_analytics(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_analytics()}


@router.get("/graph/ai")
async def bi_graph_ai(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_ai()}


@router.get("/graph/federation")
async def bi_graph_federation(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_federation()}


@router.get("/graph/digital-twin")
async def bi_graph_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_digital_twin()}


@router.get("/graph/query")
async def bi_graph_query(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_query()}


@router.get("/graph/cqrs")
async def bi_graph_cqrs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_cqrs()}


@router.get("/graph/events")
async def bi_graph_events(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_events()}


@router.get("/graph/microservices")
async def bi_graph_microservices(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_microservices()}


@router.get("/graph/apis")
async def bi_graph_apis(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_apis()}


@router.get("/graph/security")
async def bi_graph_security(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_security()}


@router.get("/graph/deployment")
async def bi_graph_deployment(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_deployment()}


@router.get("/graph/testing")
async def bi_graph_testing(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_testing()}


@router.get("/graph/outputs")
async def bi_graph_outputs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_outputs()}


@router.get("/graph/production-readiness")
async def bi_graph_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_production_readiness()}


@router.get("/graph/readiness")
async def bi_graph_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().graph_readiness()}


# --- P213-M autonomous decision intelligence fabric ---

@router.get("/ai")
async def bi_ai(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_ai()}


@router.get("/ai/vision")
async def bi_ai_vision(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_vision()}


@router.get("/ai/domain")
async def bi_ai_domain(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_domain()}


@router.get("/ai/bounded-contexts")
async def bi_ai_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_bounded_contexts()}


@router.get("/ai/agents")
async def bi_ai_agents(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_agents()}


@router.get("/ai/multi-agent")
async def bi_ai_multi_agent(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_multi_agent()}


@router.get("/ai/reasoning")
async def bi_ai_reasoning(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_reasoning()}


@router.get("/ai/autonomy")
async def bi_ai_autonomy(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_autonomy()}


@router.get("/ai/copilot")
async def bi_ai_copilot(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_copilot()}


@router.get("/ai/governance")
async def bi_ai_governance(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_governance()}


@router.get("/ai/knowledge-graph")
async def bi_ai_knowledge_graph(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_knowledge_graph()}


@router.get("/ai/digital-twin")
async def bi_ai_digital_twin(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_digital_twin()}


@router.get("/ai/cqrs")
async def bi_ai_cqrs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_cqrs()}


@router.get("/ai/events")
async def bi_ai_events(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_events()}


@router.get("/ai/microservices")
async def bi_ai_microservices(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_microservices()}


@router.get("/ai/apis")
async def bi_ai_apis(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_apis()}


@router.get("/ai/security")
async def bi_ai_security(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_security()}


@router.get("/ai/deployment")
async def bi_ai_deployment(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_deployment()}


@router.get("/ai/testing")
async def bi_ai_testing(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_testing()}


@router.get("/ai/outputs")
async def bi_ai_outputs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_outputs()}


@router.get("/ai/production-readiness")
async def bi_ai_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_production_readiness()}


@router.get("/ai/readiness")
async def bi_ai_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ai_readiness()}


# --- P213-N..P BI fabric surfaces ---

@router.get("/ops")
async def bi_ops(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_ops()}


@router.get("/ops/vision")
async def bi_ops_vision(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_vision()}


@router.get("/ops/domain")
async def bi_ops_domain(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_domain()}


@router.get("/ops/bounded-contexts")
async def bi_ops_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_bounded_contexts()}


@router.get("/ops/cqrs")
async def bi_ops_cqrs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_cqrs()}


@router.get("/ops/event-sourcing")
async def bi_ops_event_sourcing(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_event_sourcing()}


@router.get("/ops/streaming")
async def bi_ops_streaming(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_streaming()}


@router.get("/ops/apis")
async def bi_ops_apis(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_apis()}


@router.get("/ops/events")
async def bi_ops_events(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_events()}


@router.get("/ops/microservices")
async def bi_ops_microservices(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_microservices()}


@router.get("/ops/communication")
async def bi_ops_communication(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_communication()}


@router.get("/ops/read-models")
async def bi_ops_read_models(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_read_models()}


@router.get("/ops/security")
async def bi_ops_security(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_security()}


@router.get("/ops/observability")
async def bi_ops_observability(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_observability()}


@router.get("/ops/resilience")
async def bi_ops_resilience(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_resilience()}


@router.get("/ops/deployment")
async def bi_ops_deployment(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_deployment()}


@router.get("/ops/cicd")
async def bi_ops_cicd(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_cicd()}


@router.get("/ops/testing")
async def bi_ops_testing(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_testing()}


@router.get("/ops/outputs")
async def bi_ops_outputs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_outputs()}


@router.get("/ops/production-readiness")
async def bi_ops_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_production_readiness()}


@router.get("/ops/readiness")
async def bi_ops_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().ops_readiness()}


# --- P213-O BI operations fabric ---

@router.get("/deploy")
async def bi_deploy(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_deploy()}


@router.get("/deploy/vision")
async def bi_deploy_vision(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_vision()}


@router.get("/deploy/domain")
async def bi_deploy_domain(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_domain()}


@router.get("/deploy/bounded-contexts")
async def bi_deploy_bounded_contexts(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_bounded_contexts()}


@router.get("/deploy/environments")
async def bi_deploy_environments(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_environments()}


@router.get("/deploy/kubernetes")
async def bi_deploy_kubernetes(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_kubernetes()}


@router.get("/deploy/gitops")
async def bi_deploy_gitops(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_gitops()}


@router.get("/deploy/cicd")
async def bi_deploy_cicd(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_cicd()}


@router.get("/deploy/devsecops")
async def bi_deploy_devsecops(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_devsecops()}


@router.get("/deploy/observability")
async def bi_deploy_observability(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_observability()}


@router.get("/deploy/sre")
async def bi_deploy_sre(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_sre()}


@router.get("/deploy/scalability")
async def bi_deploy_scalability(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_scalability()}


@router.get("/deploy/disaster-recovery")
async def bi_deploy_disaster_recovery(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_disaster_recovery()}


@router.get("/deploy/platform-engineering")
async def bi_deploy_platform_engineering(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_platform_engineering()}


@router.get("/deploy/aiops")
async def bi_deploy_aiops(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_aiops()}


@router.get("/deploy/definition-of-done")
async def bi_deploy_definition_of_done(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_definition_of_done()}


@router.get("/deploy/quality-gates")
async def bi_deploy_quality_gates(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_quality_gates()}


@router.get("/deploy/security")
async def bi_deploy_security(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_security()}


@router.get("/deploy/testing")
async def bi_deploy_testing(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_testing()}


@router.get("/deploy/outputs")
async def bi_deploy_outputs(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_outputs()}


@router.get("/deploy/production-readiness")
async def bi_deploy_production_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_production_readiness()}


@router.get("/deploy/readiness")
async def bi_deploy_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().deploy_readiness()}


# --- P213-P QA / validation surfaces ---

@router.get("/qa")
async def bi_qa(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().platform_qa()}


@router.get("/qa/readiness")
async def bi_qa_readiness(
    _user: Annotated[dict, Depends(require_permissions("analytics.dashboards.read"))],
) -> dict:
    return {"data": get_analytics_service().qa_readiness()}
