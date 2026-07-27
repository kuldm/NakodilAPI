from fastapi import Request, FastAPI
from starlette.responses import JSONResponse

from exceptions import NakodilException


async def nakodil_exception_handler(
    request: Request,
    exc: NakodilException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


def setup_exception_handler(app: FastAPI) -> None:
    app.add_exception_handler(NakodilException, nakodil_exception_handler)
