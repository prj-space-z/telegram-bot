import aiogram.types as types
from aiogram.utils.keyboard import InlineKeyboardMarkup, ReplyKeyboardMarkup


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


def social_network_menu(settings_social: dict) -> InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text=f'{"🟢" if settings_social["vk"]["active"] else "🔴"} ВКонтакте', callback_data="admin|socialNetwork|vk"),
            types.InlineKeyboardButton(text=f'{"🟢" if settings_social["telegram"]["active"] else "🔴"} Telegram', callback_data="admin|socialNetwork|telegram"),
        ],
        [
            types.InlineKeyboardButton(text="◀️ В меню", callback_data="admin|menu"),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def telegram_delete() -> InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text='✅ Да', callback_data="admin|socialNetwork|telegram|delete"),
            types.InlineKeyboardButton(text='❌ Нет', callback_data='admin|socialNetwork')
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_telegram() -> ReplyKeyboardMarkup:
    buttons = [
        [
            types.KeyboardButton(text='Выбрать чат',
                                 request_chat=types.KeyboardButtonRequestChat(request_id=26, chat_is_channel=True))
        ]
    ]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def go_menu() -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text="◀️ В меню", callback_data="admin|menu"),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
