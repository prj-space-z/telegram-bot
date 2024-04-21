from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from services import db
from keyboards import for_admin
from filters.states import AdminGetTemplate
from aiogram.fsm.context import FSMContext
from services.s3_storage import s3

router = Router(name=__name__)


@router.callback_query(F.data == "admin|template")
async def social_network_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer_photo(
        photo='https://i.imgur.com/oyqjNiu.jpeg',
        reply_markup=for_admin.go_menu(),
        caption='<b>⚡️ Введите ID шаблона:</b>'
    )
    await callback.message.delete()
    await state.set_state(AdminGetTemplate.id_template)


@router.message(AdminGetTemplate.id_template)
async def pattern_menu(message: Message, state: FSMContext, id_template: int = None):
    await state.clear()
    if id_template is None:
        id_template = int(message.text)

    pattern = await db.get_pattern(id_template)
    if pattern is None:
        await message.answer_photo(
            photo='https://i.imgur.com/oyqjNiu.jpeg',
            reply_markup=for_admin.go_menu(),
            caption=f'<b>❌ ОШИБКА:</b> Такого шаблона нет :('
        )
        return

    await message.answer_photo(
        photo='https://i.imgur.com/oyqjNiu.jpeg',
        reply_markup=for_admin.pattern_menu(pattern['is_share'], id_template),
        caption=f'⚡️ <b>Шаблон создан юзером</b> <code>#{pattern["user_id"]}</code>',
    )


@router.callback_query(F.data.startswith("admin|template|share|"))
async def go_menu(callback: CallbackQuery, state: FSMContext):
    id_template = int(callback.data.replace("admin|template|share|", ''))

    pattern = await db.get_pattern(id_template)
    await db.edit_pattern(id_template, {'is_share': not pattern['is_share']})

    await pattern_menu(callback.message, state, id_template)
    await callback.message.delete()


@router.callback_query(F.data.startswith("admin|template|delete|"))
async def go_menu(callback: CallbackQuery, state: FSMContext):
    id_template = int(callback.data.replace("admin|template|delete|", ''))

    await db.delete_pattern(id_template)
    await callback.message.delete()

    await callback.message.answer_photo(
        photo='https://i.imgur.com/oyqjNiu.jpeg',
        reply_markup=for_admin.go_menu(),
        caption=f'<b>✅ Успешно удалено</b>'
    )


@router.callback_query(F.data.startswith("admin|template|download|"))
async def go_menu(callback: CallbackQuery, state: FSMContext):
    id_template = int(callback.data.replace("admin|template|download|", ''))

    photos = await s3.get_patterns_photos(id_template)
    for photo in photos:
        await callback.message.answer_photo(
            photo=BufferedInputFile(
                photo.read(),
                'test.webp'
            ),
            reply_markup=for_admin.go_menu(),
        )
