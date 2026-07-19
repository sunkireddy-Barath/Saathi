"""
Chat / WebSocket API Router.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.services.chat_service import ChatService, manager
from app.utils.logger import logger
from app.core.security import extract_user_id

router = APIRouter(prefix="/api/v1/ws", tags=["Chat"])


@router.websocket("/chat/{negotiation_id}")
async def websocket_chat(websocket: WebSocket, negotiation_id: str, token: str, db: AsyncSession = Depends(get_db)):
    """
    WebSocket endpoint for real-time negotiation chat.
    Authentication is passed via the 'token' query parameter since browsers
    don't support custom headers in WebSocket connections.
    """
    user_id_str = extract_user_id(token)
    if not user_id_str:
        await websocket.close(code=1008, reason="Invalid token")
        return

    try:
        user_id = UUID(user_id_str)
        # Verify user exists in db
        from app.repository.user_repository import UserRepository
        repo = UserRepository(db)
        user = await repo.get_by_id(user_id)
        if not user:
             await websocket.close(code=1008, reason="User not found")
             return
    except ValueError:
        await websocket.close(code=1008, reason="Invalid token payload")
        return

    await manager.connect(websocket, negotiation_id)
    chat_service = ChatService(db)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Expected format: {"type": "text", "content": "Hello", "offer_amount": null}
            msg_type = data.get("type", "text")
            content = data.get("content", "")
            offer_amount = data.get("offer_amount")

            try:
                # Save to DB
                saved_message = await chat_service.save_message(
                    negotiation_id=UUID(negotiation_id),
                    sender_id=user_id,
                    content=content,
                    msg_type=msg_type,
                    offer_amount=offer_amount
                )
                
                # Broadcast back to room
                response = {
                    "id": str(saved_message.id),
                    "sender_id": str(user_id),
                    "content": content,
                    "type": msg_type,
                    "offer_amount": offer_amount,
                    "created_at": saved_message.created_at.isoformat()
                }
                await manager.broadcast_to_room(str(response), negotiation_id)
                
            except Exception as e:
                # Send error back to sender only
                await websocket.send_json({"error": str(e)})

    except WebSocketDisconnect:
        manager.disconnect(websocket, negotiation_id)
        # Optional: Broadcast a system message that user left
