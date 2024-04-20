import aiogram.types as types
from aiogram.utils.keyboard import InlineKeyboardMarkup


def get_pattern(packs: list[dict]) -> InlineKeyboardMarkup:
    buttons = []

    for pack in packs:
        buttons.append([types.InlineKeyboardButton(text=pack['name'], callback_data=f'createStickers|{pack["id"]}')])

    buttons.append([types.InlineKeyboardButton(text="◀️ В меню", callback_data="menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
