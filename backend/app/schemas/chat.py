from pydantic import BaseModel, Field
from typing import Optional


class ChatMessageRequest(BaseModel):
    session_id: str
    message: str = Field(..., min_length=1)


class ChatMessageResponse(BaseModel):
    session_id: str
    reply: str
    is_final: bool = False
    crisis_detected: bool = False
    final_data: Optional[dict] = None
