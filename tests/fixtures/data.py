from typing import get_args

import pytest
from faker import Faker

from parsing_router.models import EntityType


@pytest.fixture(name="queues_binding")
def queues_binding_fixture(faker: Faker) -> dict[str, str]:
    return {faker.word(): faker.word() for _ in range(5)}


@pytest.fixture(name="entity_types_binding")
def entity_types_binding_fixture(faker: Faker) -> dict[str, str]:
    return {faker.random_element(get_args(EntityType)): faker.random_element(get_args(EntityType))}
