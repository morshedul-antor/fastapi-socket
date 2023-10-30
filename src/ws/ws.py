from fastapi import WebSocket, WebSocketDisconnect
from uuid import uuid4

active_connections = {}


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid4())
    active_connections[session_id] = websocket

    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"Received: {message}")
    except WebSocketDisconnect:
        del active_connections[session_id]


async def send_message_to_connections(message: str):
    for connection in active_connections.values():
        try:
            await connection.send_text(message)
        except WebSocketDisconnect:
            pass
