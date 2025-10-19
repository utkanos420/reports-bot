import asyncio
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel
from loguru import logger

from database.core import db_helper
from loader import bot, dp
from app.bot.handlers.routing.start import start_router
from app.bot.handlers.users import user_router
from app.bot.handlers.admins.admin import admin_router


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except Exception:
            level = record.levelno
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


async def main():

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_router(start_router)
    dp.include_router(user_router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
