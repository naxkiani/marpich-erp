"""REST API — maps HTTP to commands/queries."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from contexts.module_id.application.commands.create_example import CreateExampleCommand
from contexts.module_id.application.queries.list_examples import ListExamplesQuery
from contexts.module_id.application.use_cases.example_use_case import ExampleUseCase
from contexts.module_id.container import get_example_use_case
from contexts.module_id.presentation.rest.schemas import (
    CreateExampleRequest,
    ExampleResponse,
)
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/module-id", tags=["ModuleId"])


@router.post("/examples", status_code=status.HTTP_201_CREATED)
async def create_example(
    body: CreateExampleRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("module_id.examples.write"))],
    use_case: Annotated[ExampleUseCase, Depends(get_example_use_case)],
):
    result = await use_case.create_example(
        CreateExampleCommand(
            tenant_id=tenant_id,
            name=body.name,
            correlation_id=correlation_id,
        )
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    dto = result.unwrap()
    return {
        "data": ExampleResponse(id=dto.id, name=dto.name),
        "meta": {"correlation_id": correlation_id},
    }


@router.get("/examples")
async def list_examples(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("module_id.examples.read"))],
    use_case: Annotated[ExampleUseCase, Depends(get_example_use_case)],
):
    result = await use_case.list_examples(ListExamplesQuery(tenant_id=tenant_id))
    return {"data": [ExampleResponse(id=r.id, name=r.name) for r in result.unwrap()]}
