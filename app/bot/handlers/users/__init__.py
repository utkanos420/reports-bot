from aiogram import Router
from .base import base_router
from .report import report_router

user_router = Router()
user_router.include_routers(base_router, report_router)

__all__ = ["user_router"]