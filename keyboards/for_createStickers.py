import aiogram.types as types
from aiogram.utils.keyboard import InlineKeyboardMarkup


def get_pack() -> InlineKeyboardMarkup:
    buttons = []

    buttons.append([types.InlineKeyboardButton(text="◀️ В меню", callback_data="menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
