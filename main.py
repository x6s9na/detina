from fastapi import FastAPI, Depends, Request, WebSocket
from routes import auth, ws_chat, chat
from database import engine, Base
from contextlib import asynccontextmanager
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Receive, Scope, Send
from copy import deepcopy


@asynccontextmanager
async def on_event(app: FastAPI):
    print("Торпеда пошла")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("ГООООООЛ")


app = FastAPI(lifespan=on_event)

app.include_router(auth.router)
app.include_router(ws_chat.router)
app.include_router(chat.router)

class AppLifetimeDependencyMiddleware(BaseHTTPMiddleware):

    def __init__(self, **kwargs):
        kwargs = dict(kwargs)
        new_kwargs = {}
        for key in ('app', 'dispatch'):
            if key in kwargs:
                new_kwargs[key] = kwargs.pop(key)

        self.__storage = {}
        self.__kwargs = kwargs or {}
        super().__init__(**new_kwargs)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope['app_lifetime_dependency'] = self.__storage
        scope['app_lifetime_dependency_kwargs'] = deepcopy(self.__kwargs)

        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        response = await self.dispatch_func(request, self.call_next)
        await response(scope, receive, send)

    async def dispatch(self, request, call_next):
        return await call_next(request)

async def lifespan(app: FastAPI):
    print("🚀 Lifespan start")
    async with engine.begin() as conn:
        print("🔌 Connected to DB")
        # инициализация базы
    yield