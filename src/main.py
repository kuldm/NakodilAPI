import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))


from api.reports import router as reports_router
from api.system import router_ping
from config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description=f"Разработчик: {settings.DEVELOPER}",
    swagger_ui_parameters={"displayRequestDuration": True},
)

app.include_router(reports_router)
app.include_router(router_ping)


@app.get("/")
async def root():
    return {"name": settings.APP_NAME, "developer": settings.DEVELOPER}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
