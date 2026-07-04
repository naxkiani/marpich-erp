"""Use case handler — transaction boundary."""
from __future__ import annotations

from contexts.module_id.application.commands.create_example import CreateExampleCommand
from contexts.module_id.application.dto.example_dto import ExampleDto
from contexts.module_id.application.queries.list_examples import ListExamplesQuery
from contexts.module_id.application.validators.create_example_validator import (
    validate_create_example,
)
from contexts.module_id.domain.aggregates.example import ExampleAggregate
from contexts.module_id.domain.ports.example_repository import IExampleRepository
from shared.application.result import Result


class ExampleUseCase:
    def __init__(self, repository: IExampleRepository) -> None:
        self._repository = repository

    async def create_example(self, command: CreateExampleCommand) -> Result[ExampleDto]:
        if error := validate_create_example(command):
            return Result.fail(error)
        aggregate = ExampleAggregate.create(
            tenant_id=command.tenant_id,
            name=command.name,
        )
        await self._repository.save(aggregate)
        return Result.ok(
            ExampleDto(
                id=aggregate.id,
                name=aggregate.name,
                tenant_id=aggregate.tenant_id,
            )
        )

    async def list_examples(self, query: ListExamplesQuery) -> Result[list[ExampleDto]]:
        rows = await self._repository.list_by_tenant(
            tenant_id=query.tenant_id,
            limit=query.limit,
            offset=query.offset,
        )
        return Result.ok(
            [
                ExampleDto(id=r.id, name=r.name, tenant_id=r.tenant_id)
                for r in rows
            ]
        )
