import aiogram.types as types
from aiogram.utils.keyboard import InlineKeyboardMarkup


def menu() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Создать стикеры 🎉", callback_data="createStickers")],
        [types.InlineKeyboardButton(text="Добавить шаблон ⚡️", callback_data="accountsMenu")],
        [types.InlineKeyboardButton(text="Как это работает? 🔥", callback_data="howWork")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def go_home() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="◀️ В меню", callback_data="menu")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
