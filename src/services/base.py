from infrustructure.api_connectors.internal.payment import PaymentConnector
from infrustructure.api_connectors.internal.protection import ProtectionConnector
from utils.db_manager import DBManager


class BaseService:
    db: DBManager | None
    payment_connector: PaymentConnector | None
    protection_connector: ProtectionConnector | None

    def __init__(
        self,
        db: DBManager | None = None,
        payment_connector: PaymentConnector | None = None,
        protection_connector: ProtectionConnector | None = None,
    ) -> None:
        self.db = db
        self.payment_connector = payment_connector
        self.protection_connector = protection_connector
