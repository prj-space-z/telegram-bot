from typing import Any, Awaitable, Callable, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from services.database import db


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Optional[Any]:
        user: Optional[User] = data.get("event_from_user")
        if user:
            db_user = await db.create_user(user.id)
            if not db_user:
                db_user = await db.create_user(user.id)
            data["db_user"] = db_user
        return await handler(event, data)
