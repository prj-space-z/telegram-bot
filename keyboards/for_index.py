import aiogram.types as types
from aiogram.utils.keyboard import InlineKeyboardMarkup


def menu() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Создать стикеры 🎉", callback_data="createStickers")],
        [types.InlineKeyboardButton(text="Добавить шаблон ⚡️", callback_data="createPattern")],
        [types.InlineKeyboardButton(text="Как это работает? 🔥", callback_data="howWork")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def go_home() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="◀️ В меню", callback_data="menu")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def subscription_check(callback_data: str, telegram: str = None, vk: str = None) -> InlineKeyboardMarkup:
    buttons = []

    if telegram is not None:
        buttons.append(
            [types.InlineKeyboardButton(text="🍏 Telegram", url=telegram)]
        )

    if vk is not None:
        buttons.append(
            [types.InlineKeyboardButton(text="🍎 ВКонтакте", url=vk)]
        )

    buttons.append([types.InlineKeyboardButton(text="✅ Готово", callback_data=callback_data)])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
