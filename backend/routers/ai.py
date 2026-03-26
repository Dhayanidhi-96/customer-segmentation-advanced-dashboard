from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from services.grok_service import build_context, chat


router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str


class ChatResponse(BaseModel):
    session_id: str
    response: str


@router.post("/chat", response_model=ChatResponse)
async def ai_chat(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    session_id = payload.session_id or str(uuid.uuid4())
    response = await chat(session_id=session_id, user_message=payload.message, db=db)
    return ChatResponse(session_id=session_id, response=response)


@router.get("/recommendations")
def recommendations(db: Session = Depends(get_db)) -> dict:
    context = build_context(db)
    prompts = [
        "Why are my VIP customers declining?",
        "What campaign should I run for at-risk customers?",
        "Summarize this week's segmentation changes",
    ]
    return {"context": context, "starter_prompts": prompts}
