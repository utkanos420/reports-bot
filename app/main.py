import asyncio

from sqlmodel import SQLModel
from database.core import db_helper

from loader import bot, dp


async def main():

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
