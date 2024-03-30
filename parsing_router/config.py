from pydantic import AmqpDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    amqp_dsn: AmqpDsn
    queue_prefix: str = "parsing."

    ozon_id: int
    ozon_name: str = "ozon"

    @property
    def ozon_queue(self) -> str:
        return f"{self.queue_prefix}{self.ozon_id}"

    @property
    def ozon_routed_queue(self) -> str:
        return f"{self.queue_prefix}{self.ozon_name}"

    @property
    def amqp_dsn_str(self) -> str:
        return self.amqp_dsn.unicode_string()
