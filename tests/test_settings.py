from parsing_router.config import Settings


def test_ozon_queue_property(settings: Settings) -> None:
    ozon_id: int = settings.ozon_id
    queue_prefix: str = settings.queue_prefix

    assert settings.ozon_queue == f"{queue_prefix}{ozon_id}"


def test_ozon_routed_queue_property(settings: Settings) -> None:
    ozon_name: str = settings.ozon_name
    queue_prefix: str = settings.queue_prefix

    assert settings.ozon_routed_queue == f"{queue_prefix}{ozon_name}"


def test_amqp_dsn_str_property(settings: Settings) -> None:
    assert settings.amqp_dsn_str == settings.amqp_dsn.unicode_string()
