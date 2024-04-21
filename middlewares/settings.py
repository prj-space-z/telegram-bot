from typing import Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware, Dispatcher, Bot
from aiogram.types import TelegramObject, User
from services.database import db


class SettingsMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Optional[Any]:
        data['db_settings'] = await db.get_settings()

        if data['db_settings']['technical_work']:
            user: Optional[User] = data.get("event_from_user")
            if user.id != data['settings'].admin_id:
                await data['bot'].send_message(user.id, '<b>🙊 Извините! Бот на тех-работах</b>')
                return
            else:
                await data['bot'].send_message(user.id, '❗️ Бот на тех работах\n❗️ Пользователи не могут им пользоваться')

        return await handler(event, data)
