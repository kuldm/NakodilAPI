from infrastructure.api_connectors.internal.payment import PaymentConnector
from infrastructure.api_connectors.internal.protection import ProtectionConnector
from infrastructure.postgres.db_manager import DatabaseManager


class BaseService:
    # db: DBManager | None
    db: DatabaseManager | None
    payment_connector: PaymentConnector | None
    protection_connector: ProtectionConnector | None

    def __init__(
        self,
        db: DatabaseManager | None = None,
        payment_connector: PaymentConnector | None = None,
        protection_connector: ProtectionConnector | None = None,
    ) -> None:
        self.db = db
        self.payment_connector = payment_connector
        self.protection_connector = protection_connector
