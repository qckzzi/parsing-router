from typing import Final

from parsing_router.exceptions import EntityTypeNotMatchError, QueueNotMatchError
from parsing_router.interfaces import ILogger, IPublisher
from parsing_router.models import EntityType


class ParsingRouter:
    def __init__(
        self,
        publisher: IPublisher,
        queues_binding: dict[str, str],
        entity_types_binding: dict[EntityType, EntityType],
    ) -> None:
        self.publisher: Final[IPublisher] = publisher
        self.queues_binding: Final[dict[str, str]] = queues_binding
        self.entity_types_binding: Final[dict[EntityType, EntityType]] = entity_types_binding

    async def send_route_message(
        self,
        *,
        message: str,
        queue: str,
        entity_type: EntityType,
        logger: ILogger | None = None,
    ) -> None:
        try:
            routed_queue: str = self.queues_binding[queue]
        except KeyError as e:
            raise QueueNotMatchError(not_matched_queue=queue) from e

        try:
            new_entity_type: str = self.entity_types_binding[entity_type]
        except KeyError as e:
            raise EntityTypeNotMatchError(not_matched_entity_type=entity_type) from e

        await self.publisher.publish(
            message,
            routed_queue,
            headers={"ENTITY_TYPE": new_entity_type},
        )

        if logger is not None:
            logger.debug(f"Router sent {message=} to the {routed_queue=} with {new_entity_type=}")
