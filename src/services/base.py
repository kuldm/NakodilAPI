from infrastructure.api_connectors.internal.payment import PaymentConnector
from infrastructure.api_connectors.internal.protection import ProtectionConnector
from infrastructure.concurrency.singleflight import Singleflight
from infrastructure.postgres.db_manager import DatabaseManager
from infrastructure.redis.event_cache import EventCache
from infrastructure.redis.manager import RedisManager


class BaseService:
    db: DatabaseManager | None
    payment_connector: PaymentConnector | None
    protection_connector: ProtectionConnector | None
    event_cache: EventCache | None
    singleflight: Singleflight | None
    redis_client: RedisManager | None

    def __init__(
        self,
        db: DatabaseManager | None = None,
        payment_connector: PaymentConnector | None = None,
        protection_connector: ProtectionConnector | None = None,
        event_cache: EventCache | None = None,
        singleflight: Singleflight | None = None,
        redis_client: RedisManager | None = None,
    ) -> None:
        self.db = db
        self.payment_connector = payment_connector
        self.protection_connector = protection_connector
        self.event_cache = event_cache
        self.singleflight = singleflight
        self.redis_client = redis_client

