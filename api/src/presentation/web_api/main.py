import logging
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import (
    setup_dishka,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import configure_mappers

from core.di.container import container
from infrastructure.gunicorn.app_options import get_app_options
from infrastructure.gunicorn.application import Application
import core.db.logs  # noqa: F401
from infrastructure.gunicorn.config import app_settings

configure_mappers()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    yield
    await app.state.dishka_container.close()


app = FastAPI(lifespan=lifespan, root_path="/api")

setup_dishka(container=container, app=app)

logger = logging.getLogger("fastapi")
logger.setLevel(logging.INFO)

# logstash_handler = TCPLogstashHandler("logstash", 50000)
# logger.addHandler(logstash_handler)

app.include_router(reg_router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


def main():
    Application(
        application=app,
        options=get_app_options(
            host=app_settings.gunicorn.host,
            port=app_settings.gunicorn.port,
            timeout=app_settings.gunicorn.timeout,
            workers=app_settings.gunicorn.workers,
            log_level=app_settings.logging.log_level,
        ),
    ).run()


# if __name__ == "__main__":
#     main()
