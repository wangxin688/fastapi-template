"""Main FastAPI app instance declaration."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.core import config
from app.db.redis_session import RedisClient, init_redis_pool
from app.register.exception_handler import exception_handlers
from app.utils.loggers import app_logger as logger

app = FastAPI(
    title=config.settings.PROJECT_NAME,
    version=config.settings.VERSION,
    description=config.settings.DESCRIPTION,
    openapi_url=f"api/v{config.settings.MAJAR_VERSION}/openapi.json",
    docs_url=f"/api/v{config.settings.MAJAR_VERSION}/docs",
    redoc_url=f"api/v{config.settings.MAJAR_VERSION}/redocs",
    exception_handlers=exception_handlers,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in config.settings.BACKEND_CORS_ORIGINS],
    # allow_origins=[*]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start_event():
    Instrumentator().instrument(app).expose(
        app, endpoint=f"/api/{config.settings.MAJAR_VERSION}/metrics", tags=["Monitor"]
    )
    app.state.database = await init_db_pool()
    app.state.redis = await init_redis_pool()
    app.state.r_client = RedisClient(app.state.redis)

    logger.info("init app logger success")


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.database.disconnect()
    await app.state.redis.close()
