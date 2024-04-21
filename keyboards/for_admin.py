import aiogram.types as types
from aiogram.utils.keyboard import InlineKeyboardMarkup


def get_panel(technical_work: bool) -> InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text='🔴 Остановить тех-работы' if technical_work else '🟢 Запустить тех-работы',
                                       callback_data="admin|technicalWork")
        ],
        [
            types.InlineKeyboardButton(text="Соц-сети 🔥", callback_data="admin|socialNetwork"),
            types.InlineKeyboardButton(text="Шаблоны ⚡️", callback_data="menu")
         ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def social_network_menu() -> InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text='🍎 ВКонтакте', callback_data="admin|socialNetwork|vk"),
            types.InlineKeyboardButton(text='🍏 Telegram', callback_data="admin|socialNetwork|telegram"),
        ],
        [
            types.InlineKeyboardButton(text="◀️ В меню", callback_data="admin|menu"),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
