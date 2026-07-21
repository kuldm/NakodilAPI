from infrustructure.api_connectors.base import BaseHTTPConnector
from infrustructure.api_connectors.schemas import (
    ProtectionCalculateItemData,
    ProtectionQuote,
)


class ProtectionConnector(BaseHTTPConnector):
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

    async def protection_calculate(
        self,
        data: ProtectionCalculateItemData,
    ) -> ProtectionQuote:
        response = await self._request(
            "POST", "/protection/calculate", json=data.model_dump(), retry=False
        )
        response.raise_for_status()
        return ProtectionQuote.model_validate(response.json())
