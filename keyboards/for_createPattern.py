import aiogram.types as types
from aiogram.utils.keyboard import InlineKeyboardMarkup
import urllib.parse


def get_images() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Создать шаблон ⚡️ ", callback_data="createPattern|getName")],
        [types.InlineKeyboardButton(text="◀️ В меню", callback_data="menu")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def successfully(share_url: str) -> InlineKeyboardMarkup:
    share_data = {'url': share_url, 'text': '\nХАХАХ Посмотри какие смешные мемы я создал'}
    buttons = [
        [types.InlineKeyboardButton(text="Воспользоваться шаблоном ⚡️", callback_data="createPattern|getName")],
        [types.InlineKeyboardButton(text="Поделиться 💎", url=f'https://t.me/share/url?{urllib.parse.urlencode(share_data)}')],
        [types.InlineKeyboardButton(text="◀️ В меню", callback_data="menu")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
