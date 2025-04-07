from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ChatCreate(BaseModel):
    name: str
    type: str  # 'private' или 'group'

class ChatResponse(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    chat_id: int
    sender_id: int
    text: str

class MessageResponse(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    text: str
    timestamp: datetime
    is_read: bool

    class Config:
        from_attributes=True