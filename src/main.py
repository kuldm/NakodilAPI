import sys
from pathlib import Path
from contextlib import asynccontextmanager

import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from services.add_event_data import add_event_data_to_db

sys.path.append(str(Path(__file__).parent.parent))


from api.reports import router as reports_router
from api.routes import router
from api.events import router as router_events
from api.system import router_ping
from api.seats import router as router_seats
from api.seats import router_events_seats
from config import settings
from di import AppProvider

container = make_async_container(AppProvider(), FastapiProvider())


@asynccontextmanager
async def lifespan(app: FastAPI):
    await add_event_data_to_db()
    yield
    await app.state.dishka_container.close()


app = FastAPI(
    title=settings.APP_NAME,
    description=f"Разработчик: {settings.DEVELOPER}",
    swagger_ui_parameters={"displayRequestDuration": True},
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(reports_router)
app.include_router(router_ping)
app.include_router(router)
app.include_router(router_events)
app.include_router(router_seats)
app.include_router(router_events_seats)

setup_dishka(container=container, app=app)


@app.get("/")
async def root():
    return {"name": settings.APP_NAME, "developer": settings.DEVELOPER}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
