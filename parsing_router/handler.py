from typing import Annotated, Final

from faststream import Context, Header, Logger
from pydantic import HttpUrl

from parsing_router.interfaces import IRouter
from parsing_router.models import EntityType


_Queue = Annotated[str, Context("message.raw_message.routing_key")]
_HeaderEntityType = Annotated[EntityType, Header("ENTITY_TYPE")]


class ParsingHandler:
    def __init__(
        self,
        router: IRouter,
    ) -> None:
        self.router: Final[IRouter] = router

    async def __call__(
        self,
        url: HttpUrl,
        queue: _Queue,
        entity_type: _HeaderEntityType,
        logger: Logger,
    ) -> None:
        logger.debug(f"{url=}, {queue=}, {entity_type=}")
        await self.router.send_route_message(
            message=url.unicode_string(),
            queue=queue,
            entity_type=entity_type,
            logger=logger,
        )
