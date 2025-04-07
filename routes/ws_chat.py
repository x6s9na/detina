from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websocket.chat import manager

router = APIRouter()

# маршрут ws-чата
@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    await manager.connect(websocket, chat_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(chat_id, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)
