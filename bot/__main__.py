import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from redis.asyncio import Redis

from bot.handlers import user, admin
from bot.config import TELEGRAM_BOT_TOKEN, REDIS_HOST, REDIS_PORT, REDIS_DB_FSM
from bot.database.session import async_session
from bot.middlewares.db import DbSessionMiddleware


async def main() -> None:
    redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_FSM)
    storage = RedisStorage(redis_client)

    dp = Dispatcher(storage=storage)

    dp.include_router(admin.router)
    dp.include_router(user.router)

    dp.update.middleware(DbSessionMiddleware(session_pool=async_session))

    bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
