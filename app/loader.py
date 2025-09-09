from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from settings.config import settings
from redis.asyncio import Redis

redis = Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

storage = RedisStorage(redis=redis)

bot = Bot(token=settings.bot_api_key, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)
