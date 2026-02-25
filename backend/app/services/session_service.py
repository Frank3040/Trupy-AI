import json
import uuid
from typing import Dict, Optional

from app.core.redis_client import get_redis
from app.core.config import get_settings
from app.services.trupy_chat import TrupyOpenAI
from app.utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(name="session_service")

SESSION_PREFIX = "session:"


def _key(session_id: str) -> str:
    return f"{SESSION_PREFIX}{session_id}"


async def create_session(user_profile: Optional[Dict[str, str]] = None) -> tuple[str, str]:
    session_id = str(uuid.uuid4())
    bot = TrupyOpenAI(user_profile=user_profile)
    greeting = bot.start_conversation()

    redis = await get_redis()
    await redis.setex(
        _key(session_id),
        settings.SESSION_TTL,
        json.dumps(bot.to_dict()),
    )

    logger.info(f"Session created: {session_id} | anonymous={user_profile is None}")
    return session_id, greeting


async def get_session(session_id: str) -> Optional[TrupyOpenAI]:
    redis = await get_redis()
    raw = await redis.get(_key(session_id))
    if raw is None:
        return None
    
    logger.info(f"Session retrieved: {session_id}")

    return TrupyOpenAI.from_dict(json.loads(raw))


async def save_session(session_id: str, bot: TrupyOpenAI) -> None:
    redis = await get_redis()
    await redis.setex(
        _key(session_id),
        settings.SESSION_TTL,
        json.dumps(bot.to_dict()),
    )
    logger.info(f"Session saved: {session_id}")


async def remove_session(session_id: str) -> None:
    redis = await get_redis()
    await redis.delete(_key(session_id))
    logger.info(f"Session removed: {session_id}")


async def count_active_sessions() -> int:
    redis = await get_redis()
    keys = [k async for k in redis.scan_iter(f"{SESSION_PREFIX}*")]
    return len(keys)
