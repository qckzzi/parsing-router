import pytest
from faker import Faker
from pydantic import AmqpDsn

from parsing_router.config import Settings


@pytest.fixture(name="settings")
def settings_mock(faker: Faker) -> Settings:
    settings: Settings = Settings(
        ozon_id=faker.pyint(),
        ozon_name=faker.word(),
        queue_prefix=faker.word(),
        amqp_dsn=AmqpDsn("amqp://guest:guest@localhost:5672/"),
    )

    return settings
