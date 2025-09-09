import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from sqlmodel import SQLModel
from database.core import db_helper

from loader import bot, dp
from app.bot.handlers.routing.start import start_router
from app.bot.handlers.users.user import user_main_router
from app.bot.handlers.admins.admin import admin_router


async def main():

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_router(start_router)
    dp.include_router(user_main_router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
