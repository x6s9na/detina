from fastapi import FastAPI
from routes import auth, ws_chat, chat
from database import engine, Base
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Торпеда пошла")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("ГООООООЛ")


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(ws_chat.router)
app.include_router(chat.router)
