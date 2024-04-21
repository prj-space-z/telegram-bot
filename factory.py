from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from services import mjson, redis
from handlers import admin, main
from settings import Settings
from middlewares import UserMiddleware, SettingsMiddleware


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher(
        name="main_dispatcher",
        storage=RedisStorage(redis=redis, json_loads=mjson.decode, json_dumps=mjson.encode),
        redis=redis,
    )
    dp["settings"] = settings = Settings()
    dp.include_routers(admin.router, main.router)

    dp.update.outer_middleware(UserMiddleware())
    dp.update.outer_middleware(SettingsMiddleware())

    dp.callback_query.middleware(CallbackAnswerMiddleware())

    return dp


def create_bot(settings: Settings) -> Bot:
    session = AiohttpSession(json_loads=mjson.decode, json_dumps=mjson.encode)
    return Bot(
        token=settings.api_token.get_secret_value(),
        parse_mode=ParseMode.HTML,
        session=session,
    )
