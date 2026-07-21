from infrustructure.api_connectors.base import BaseHTTPConnector
from infrustructure.api_connectors.schemas import (
    PaymentCalculateItemData,
    PaymentQuote,
)


class PaymentConnector(BaseHTTPConnector):
    def __init__(
        self,
        base_url: str,
        timeout: float,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            timeout=timeout,
            headers=headers,
            rate_limit_requests=None,
            rate_limit_interval=None,
        )

    async def payment_calculate(
        self,
        data: PaymentCalculateItemData,
    ) -> PaymentQuote:
        response = await self._request(
            "POST",
            "/payment/calculate",
            json=data.model_dump(),
            retry=True,
            retry_count=2,
        )
        response.raise_for_status()
        return PaymentQuote.model_validate(response.json())
