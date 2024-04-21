from filters.states import AdminTelegramAD
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from services import db
from keyboards import for_admin

router = Router(name=__name__)


@router.callback_query(F.data == "admin|socialNetwork")
async def social_network_menu(callback: CallbackQuery, db_settings: dict):
    await callback.message.answer_photo(
        photo='https://i.imgur.com/oyqjNiu.jpeg',
        reply_markup=for_admin.social_network_menu(db_settings['social'])
    )
    await callback.message.delete()


@router.callback_query(F.data == "admin|socialNetwork|telegram|delete")
async def go_menu(callback: CallbackQuery, state: FSMContext, db_settings: dict):
    db_settings['social']['telegram'] = {
        'active': False,
    }
    await db.edit_settings(db_settings)
    await social_network_menu(callback, db_settings)


@router.callback_query(F.data == "admin|socialNetwork|telegram")
async def go_menu(callback: CallbackQuery, state: FSMContext, db_settings: dict):
    # TODO: ALL Edit name func and add comment

    await callback.message.delete()

    if db_settings['social']['telegram']['active']:
        await callback.message.answer_photo(
            photo='https://i.imgur.com/oyqjNiu.jpeg',
            caption='<b>⚡️ Вы уверены что хотите удалить привязку Telegram?</b>',
            reply_markup=for_admin.telegram_delete()
        )
        return

    await callback.message.answer('⚡️', reply_markup=for_admin.get_telegram())
    await callback.message.answer_photo(
        photo='https://i.imgur.com/oyqjNiu.jpeg',
        caption="""<b>⚡️ Что-бы подключить проверку следуйте настурциям:</b>\n\n1. Добавьте бота в канал\n2. Отправьте мне канал\n3. Готово! Теперь бот будет проверять наличие""",
        reply_markup=for_admin.go_menu()
    )
    # TODO: Сделать сброс клавы
    await state.set_state(AdminTelegramAD.chat)


@router.message(F.chat_shared, AdminTelegramAD.chat)
async def go_menu(message: Message, state: FSMContext):
    await message.answer_photo(
        photo='https://i.imgur.com/oyqjNiu.jpeg',
        caption="""<b>⚡️ Супер! А теперь отправьте ссылку на канал</b>""",
        reply_markup=for_admin.go_menu()
    )
    await state.set_state(AdminTelegramAD.url)
    await state.update_data({'chat_id': message.chat_shared.chat_id})


@router.message(AdminTelegramAD.url)
async def go_menu(message: Message, state: FSMContext, db_settings: dict):
    state_data = await state.get_data()
    await state.clear()

    db_settings['social']['telegram'] = {
        'active': True,
        'url': message.text,
        'channel_id': state_data['chat_id']
    }
    await db.edit_settings(db_settings)

    await message.answer_photo(
        photo='https://i.imgur.com/oyqjNiu.jpeg',
        caption="""<b>⚡️ Успешно!</b>""",
        reply_markup=for_admin.go_menu()
    )

