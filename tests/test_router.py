from typing import Any

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from parsing_router.exceptions import EntityTypeNotMatchError, QueueNotMatchError
from parsing_router.models import EntityType
from parsing_router.router import ParsingRouter


@pytest.mark.asyncio()
async def test_routing(
    queues_binding: dict[str, str],
    entity_types_binding: dict[EntityType, EntityType],
    mocker: MockerFixture,
    faker: Faker,
) -> None:
    publisher: Any = mocker.AsyncMock()
    parsing_router: ParsingRouter = ParsingRouter(
        publisher=publisher,
        queues_binding=queues_binding,
        entity_types_binding=entity_types_binding,
    )
    url: str = faker.url()
    queue: str = faker.random_element(queues_binding.keys())
    entity_type: str = faker.random_element(entity_types_binding.keys())
    await parsing_router.send_route_message(
        message=url,
        queue=queue,
        entity_type=entity_type,  # type: ignore[arg-type]
    )

    assert publisher.publish.mock_calls == [
        mocker.call(
            url,
            queues_binding[queue],
            headers={"ENTITY_TYPE": entity_types_binding[entity_type]},  # type: ignore[index]
        ),
    ]


@pytest.mark.asyncio()
async def test_queue_not_match_error(
    queues_binding: dict[str, str],
    entity_types_binding: dict[EntityType, EntityType],
    mocker: MockerFixture,
    faker: Faker,
) -> None:
    parsing_router: ParsingRouter = ParsingRouter(
        publisher=mocker.AsyncMock(),
        queues_binding=queues_binding,
        entity_types_binding=entity_types_binding,
    )

    with pytest.raises(QueueNotMatchError):
        await parsing_router.send_route_message(
            message=faker.url(),
            queue=faker.word(),
            entity_type=faker.random_element(entity_types_binding.keys()),
        )


@pytest.mark.asyncio()
async def test_entity_type_not_match_error(
    queues_binding: dict[str, str],
    entity_types_binding: dict[EntityType, EntityType],
    mocker: MockerFixture,
    faker: Faker,
) -> None:
    parsing_router: ParsingRouter = ParsingRouter(
        publisher=mocker.AsyncMock(),
        queues_binding=queues_binding,
        entity_types_binding=entity_types_binding,
    )

    with pytest.raises(EntityTypeNotMatchError):
        await parsing_router.send_route_message(
            message=faker.url(),
            queue=faker.random_element(queues_binding.keys()),
            entity_type=faker.word(),
        )
