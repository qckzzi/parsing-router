from typing import Any, get_args

import pytest
from faker import Faker
from pydantic import HttpUrl
from pytest_mock import MockFixture

from parsing_router.handler import ParsingHandler
from parsing_router.models import EntityType


@pytest.mark.asyncio()
async def test_parsing_handle(mocker: MockFixture, faker: Faker) -> None:
    router_mock: Any = mocker.AsyncMock()
    logger_mock: Any = mocker.Mock()
    parsing_handler: ParsingHandler = ParsingHandler(router=router_mock)
    url: HttpUrl = HttpUrl(faker.url())
    queue: str = faker.word()
    entity_type: EntityType = faker.random_element(get_args(EntityType))

    await parsing_handler(
        url=url,
        queue=queue,
        entity_type=entity_type,
        logger=logger_mock,
    )

    assert router_mock.send_route_message.mock_calls == [
        mocker.call(
            message=url.unicode_string(),
            queue=queue,
            entity_type=entity_type,
            logger=logger_mock,
        ),
    ]
