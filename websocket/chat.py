from fastapi import WebSocket, WebSocketDisconnect
from typing import List

# менеджер соединений
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: int):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, websocket: WebSocket, chat_id: int):
        self.active_connections[chat_id].remove(websocket)
        if not self.active_connections[chat_id]:
            del self.active_connections[chat_id]

    async def broadcast(self, chat_id: int, message: str):
        for connection in self.active_connections.get(chat_id, []):
            await connection.send_text(message)

manager = ConnectionManager()
