from collections.abc import Sequence

from bakery import Bakery, Cake
from faststream.rabbit import RabbitBroker, RabbitQueue, RabbitRoute, RabbitRouter

from parsing_router.config import Settings
from parsing_router.handler import ParsingHandler
from parsing_router.models import EntityType
from parsing_router.router import ParsingRouter


class Container(Bakery):
    settings: Settings = Cake(Settings)  # type: ignore[assignment]
    broker: RabbitBroker = Cake(RabbitBroker, settings.amqp_dsn_str)

    _queues_binding: dict[str, str] = Cake(
        {
            settings.ozon_queue: settings.ozon_routed_queue,
        },
    )
    _entity_types_binding: dict[EntityType, EntityType] = Cake(
        {
            "CATEGORY": "SELLER",
            "PRODUCT": "PRODUCT",
            "BRAND": "BRAND",
            "SELLER": "SELLER",
        },
    )
    _parsing_router: ParsingRouter = Cake(ParsingRouter, broker, _queues_binding, _entity_types_binding)
    _parsing_handler: ParsingHandler = Cake(ParsingHandler, _parsing_router)
    _ozon_queue: RabbitQueue = Cake(RabbitQueue, settings.ozon_queue, durable=True)
    _ozon_route: RabbitRoute = Cake(RabbitRoute, _parsing_handler, _ozon_queue)

    _routes: Sequence[RabbitRoute] = (_ozon_route,)
    router: RabbitRouter = Cake(RabbitRouter, handlers=_routes)

    queues_to_declare: list[str] = Cake(
        [
            settings.ozon_routed_queue,
        ],
    )
