from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from services import db
from keyboards import for_admin

router = Router(name=__name__)


@router.message(Command("admin"))
async def cmd_admin(message: Message, db_settings: dict):
    """Command: /admin"""

    await message.answer_photo(
        photo='https://i.imgur.com/oyqjNiu.jpeg',
        caption=f"""📊 Статистика:

х Новых пользователей:
<b>➖ Сегодня:</b> <code>{await db.get_user_count(24)}</code>
<b>➖ За неделю:</b> <code>{await db.get_user_count(168)}</code>
<b>➖ За месяц:</b> <code>{await db.get_user_count(744)}</code>
<b>➖ Всего:</b> <code>{await db.get_user_count()}</code>

<b>➖ Всего генераций:</b> <code>0</code>
<b>➖ Всего шаблонов:</b> <code>{await db.get_patterns_count()}</code>""",
    reply_markup=for_admin.get_panel(db_settings['technical_work']))
    # TODO: Add Всего генераций


@router.callback_query(F.data == "admin|menu")
async def go_menu(callback: CallbackQuery, db_settings: dict):
    await cmd_admin(callback.message, db_settings)
    await callback.message.delete()


@router.callback_query(F.data == "admin|technicalWork")
async def go_menu(callback: CallbackQuery, db_settings: dict):
    db_settings['technical_work'] = not db_settings['technical_work']

    await db.edit_settings(db_settings)
    await cmd_admin(callback.message, db_settings)
    await callback.message.delete()
