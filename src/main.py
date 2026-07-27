import sys
from pathlib import Path

import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

import utils.fastapi_warnings  # noqa
from api.app import create_fastapi_app
from ioc import create_container
from config import settings


container = create_container(settings)
app = create_fastapi_app(settings, container)


@app.get("/")
async def root():
    return {"name": settings.app.app_name, "developer": settings.app.developer}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
