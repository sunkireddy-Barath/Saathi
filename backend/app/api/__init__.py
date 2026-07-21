"""
API Routers package.
"""

from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.seller import router as seller_router
from app.api.buyer import router as buyer_router
from app.api.marketplace import router as marketplace_router
from app.api.negotiation import router as negotiation_router
from app.api.order import router as order_router
from app.api.dispute import router as dispute_router
from app.api.trust import router as trust_router
from app.api.forecast import pricing_router, forecast_router
from app.api.admin import router as admin_router
from app.api.chat import router as chat_router
from app.api.market import router as market_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(seller_router)
api_router.include_router(buyer_router)
api_router.include_router(marketplace_router)
api_router.include_router(negotiation_router)
api_router.include_router(order_router)
api_router.include_router(dispute_router)
api_router.include_router(trust_router)
api_router.include_router(pricing_router)
api_router.include_router(forecast_router)
api_router.include_router(admin_router)
api_router.include_router(chat_router)
api_router.include_router(market_router)
