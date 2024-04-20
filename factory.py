from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from redis.asyncio import Redis
from services import mjson
from handlers import admin, main
from settings import Settings


def create_dispatcher() -> Dispatcher:
    redis = Redis()

    dp = Dispatcher(
        name="main_dispatcher",
        storage=RedisStorage(redis=redis, json_loads=mjson.decode, json_dumps=mjson.encode),
        redis=redis,
    )
    dp["settings"] = settings = Settings()
    dp.include_routers(admin.router, main.router)

    dp.callback_query.middleware(CallbackAnswerMiddleware())

    return dp


def create_bot(settings: Settings) -> Bot:
    session = AiohttpSession(json_loads=mjson.decode, json_dumps=mjson.encode)
    return Bot(
        token=settings.api_token.get_secret_value(),
        parse_mode=ParseMode.HTML,
        session=session,
    )
