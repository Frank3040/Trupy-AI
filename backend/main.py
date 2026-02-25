import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import get_settings
from app.core.database import init_db
from app.core.limiter import limiter
from app.core.redis_client import close_redis
from app.services import session_service
from app.api.v1.router import api_router
from app.utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(name="main")

SWEEP_INTERVAL = 300


async def _redis_sweep():
    while True:
        try:
            await asyncio.sleep(SWEEP_INTERVAL)
            count = await session_service.count_active_sessions()
            logger.info(f"[sweep] Active Redis sessions: {count}")
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"[sweep] Error during session sweep: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    sweep_task = asyncio.create_task(_redis_sweep())
    logger.info("Background session sweep started.")
    try:
        yield
    finally:
        sweep_task.cancel()
        try:
            await sweep_task
        except asyncio.CancelledError:
            pass
        await close_redis()
        logger.info("Redis connection closed.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.APP_NAME}
