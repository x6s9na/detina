from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Chat, Message
from schemas import ChatCreate, ChatResponse, MessageCreate, MessageResponse

router = APIRouter()

@router.post("/chats", response_model=ChatResponse)
async def create_chat(chat: ChatCreate, db: AsyncSession = Depends(get_db)):
    new_chat = Chat(name=chat.name, type=chat.type)
    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)
    return new_chat


@router.post("/messages", response_model=MessageResponse)
async def send_message(msg: MessageCreate, db: AsyncSession = Depends(get_db)):
    new_msg = Message(
        chat_id=msg.chat_id,
        sender_id=msg.sender_id,
        text=msg.text,
    )
    db.add(new_msg)
    await db.commit()
    await db.refresh(new_msg)
    return new_msg


@router.get("/history/{chat_id}", response_model=list[MessageResponse])
async def get_message_history(chat_id: int, limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.timestamp.asc())
        .limit(limit)
        .offset(offset)
    )
    messages = result.scalars().all()
    return messages
