from fastapi import APIRouter

from schemas.reports import Ping

router_ping = APIRouter(prefix="/ping", tags=["Пинг"])


@router_ping.get(
    "",
    summary="Пингует API",
    description="<h3>Этот метод пингует API просто возвращая 'status: OK'<h3>",
    response_model=Ping,
)
async def get_ping():
    return {"status": "OK"}
