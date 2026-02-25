from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.session import SessionRecord
from app.schemas.session import (
    SessionEndResponse,
    SessionRecordOut,
    SessionStartRequest,
    SessionStartResponse,
)
from app.services import session_service

router = APIRouter()


@router.post("/start", response_model=SessionStartResponse, status_code=status.HTTP_201_CREATED)
async def start_session(body: SessionStartRequest):
    if not body.anonymous and body.user_profile is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="user_profile is required when anonymous is false.",
        )

    user_profile = None
    if not body.anonymous and body.user_profile:
        user_profile = body.user_profile.model_dump()

    session_id, greeting = await session_service.create_session(user_profile=user_profile)
    return SessionStartResponse(
        session_id=session_id,
        greeting=greeting,
        anonymous=body.anonymous,
    )


@router.post("/{session_id}/end", response_model=SessionEndResponse)
async def end_session(session_id: str, db: AsyncSession = Depends(get_db)):
    bot = await session_service.get_session(session_id)
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or already ended.",
        )

    summary = bot.generate_summary()

    user_data: dict = {}
    if bot.user_profile:
        user_data = {**bot.user_profile}
    user_data["summary"] = summary

    record = SessionRecord(
        session_id=session_id,
        user_data=user_data,
        ended_at=datetime.utcnow(),
    )
    db.add(record)
    await db.flush()

    await session_service.remove_session(session_id)

    return SessionEndResponse(
        session_id=session_id,
        summary=summary,
        user_data=user_data,
    )


@router.get("/history", response_model=list[SessionRecordOut])
async def list_sessions(
    skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(SessionRecord).offset(skip).limit(limit).order_by(SessionRecord.created_at.desc())
    )
    return result.scalars().all()
