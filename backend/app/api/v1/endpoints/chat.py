from fastapi import APIRouter, HTTPException, Request, status

from app.core.limiter import limiter
from app.core.config import get_settings
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.services import session_service

settings = get_settings()
router = APIRouter()


@router.post("/message", response_model=ChatMessageResponse)
@limiter.limit(settings.RATE_LIMIT_CHAT)
async def send_message(request: Request, body: ChatMessageRequest):
    bot = await session_service.get_session(body.session_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or already ended.",
        )

    if bot.is_concluded:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Session is already concluded. Please end the session.",
        )

    result = bot.get_response(body.message)

    if isinstance(result, dict):
        if result.get("type") == "crisis":
            await session_service.remove_session(body.session_id)
            return ChatMessageResponse(
                session_id=body.session_id,
                reply=result["message"],
                is_final=True,
                crisis_detected=True,
            )
        if result.get("type") == "final_submission":
            await session_service.save_session(body.session_id, bot)
            return ChatMessageResponse(
                session_id=body.session_id,
                reply=result["message"],
                is_final=True,
                final_data=result.get("data"),
            )

    await session_service.save_session(body.session_id, bot)
    return ChatMessageResponse(
        session_id=body.session_id,
        reply=str(result),
    )


@router.get("/{session_id}/history")
async def get_chat_history(session_id: str):
    bot = await session_service.get_session(session_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or already ended.",
        )
    return {"session_id": session_id, "history": bot.get_history()}
