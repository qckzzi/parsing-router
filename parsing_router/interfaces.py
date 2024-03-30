from typing import Any, Protocol

from parsing_router.models import EntityType


class IPublisher(Protocol):
    async def publish(
        self,
        message: str,
        queue: str,
        *,
        headers: dict,
    ) -> Any: ...


class ILogger(Protocol):
    def debug(self, msg: str) -> None: ...


class IRouter(Protocol):
    async def send_route_message(
        self,
        *,
        message: str,
        queue: str,
        entity_type: EntityType,
        logger: ILogger | None = None,
    ) -> None: ...
