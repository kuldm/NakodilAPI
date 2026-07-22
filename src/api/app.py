from dishka import AsyncContainer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dishka.integrations.fastapi import setup_dishka

from api.lifespan import create_lifespan
# from samokat.api.exceptions import setup_exception_handlers
# from samokat.api.lifespan import create_lifespan
from src.api import main_router
from src.config import Settings, AppConfig


def create_fastapi_app(
    settings: Settings,
    container: AsyncContainer,
) -> FastAPI:
    app = FastAPI(
        title=settings.app.app_name,
        description=f"Разработчик: {settings.app.developer}",
        swagger_ui_parameters={"displayRequestDuration": True},
        lifespan=create_lifespan(container),
        # debug=False,
    )

    app.add_middleware(
        CORSMiddleware,
        # allow_origins=settings.cors.allowed_origins,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_dishka(
        container=container,
        app=app,
    )

    app.include_router(main_router)
    return app
