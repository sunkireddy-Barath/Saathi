"""
Chat/Negotiation Service.
Manages WebSocket connections and real-time negotiation logic.
"""

from typing import Dict, List
from uuid import UUID

from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.negotiation import Negotiation, Message
from app.repository.negotiation_repository import NegotiationRepository, MessageRepository
from app.utils.constants import NegotiationStatus
from app.utils.exceptions import NotFoundException, BelowFairPriceException


class ConnectionManager:
    def __init__(self):
        # Room ID (Negotiation ID) -> List of WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast_to_room(self, message: str, room_id: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)

# Global singleton
manager = ConnectionManager()


class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.negotiation_repo = NegotiationRepository(db)
        self.message_repo = MessageRepository(db)

    async def save_message(
        self, negotiation_id: UUID, sender_id: UUID, content: str, msg_type: str = "text", offer_amount: float = None
    ) -> Message:
        negotiation = await self.negotiation_repo.get_by_id(negotiation_id)
        if not negotiation:
            raise NotFoundException("Negotiation not found")
            
        if msg_type in ["offer", "counter_offer"] and offer_amount:
            if offer_amount < negotiation.fair_price_floor:
                raise BelowFairPriceException()

        message_data = {
            "negotiation_id": negotiation_id,
            "sender_id": sender_id,
            "content": content,
            "msg_type": msg_type,
            "offer_amount": offer_amount
        }
        
        return await self.message_repo.create(message_data)
