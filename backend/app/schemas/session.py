from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserProfile(BaseModel):
    name: str = Field(..., min_length=1)
    major: str = Field(..., min_length=1)
    quarter: str = Field(..., min_length=1)


class SessionStartRequest(BaseModel):
    anonymous: bool = True
    user_profile: Optional[UserProfile] = None


class SessionStartResponse(BaseModel):
    session_id: str
    greeting: str
    anonymous: bool


class SessionEndResponse(BaseModel):
    session_id: str
    summary: str
    user_data: dict


class SessionRecordOut(BaseModel):
    id: int
    session_id: str
    user_data: dict
    created_at: datetime
    ended_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
