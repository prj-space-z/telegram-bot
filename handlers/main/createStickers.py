from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards import for_createStickers, for_index
from services import db, s3
from filters.states import StickersCreate
from aiogram.fsm.context import FSMContext
from services.face_swap_api import face_swap
import io
from aiogram.types import BufferedInputFile


router = Router(name=__name__)


@router.callback_query(F.data == "createStickers")
async def create_stickers(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo='https://i.imgur.com/rX6mOEK.jpg',
        reply_markup=for_createStickers.get_pattern(await db.get_patterns({'$or': [{'is_share': True}, {'user_id': callback.from_user.id}]}))
    )


@router.callback_query(F.data.startswith("createStickers|"))
async def create_stickers(callback: CallbackQuery, state: FSMContext):
    pattern_id = int(callback.data.replace('createStickers|', ''))

    await state.set_state(StickersCreate.image)
    await state.update_data({'pattern_id': pattern_id})

    await callback.message.delete()
    await callback.message.answer_photo(
        photo='https://i.imgur.com/pqpa6qz.jpeg',
        caption='<b>😎 Отправь своё фото</b>\n\n<b>х Советы:</b>\n1. На фото должно быть хорошо видно лицо\n2. На фото не должно быть других лиц\n3. Желательно без очков или головного убора (Если Вы носите очки, попробуйте без них)',
        reply_markup=for_index.go_home()
    )


@router.message(StickersCreate.image, F.photo)
async def account_get_username(message: Message, state: FSMContext, settings: dict, bot: Bot):
    data = await state.get_data()

    msg = await message.answer_photo(
        photo='https://i.imgur.com/8epdsdY.png',
        caption='<b>🐑 Идёт обработка вашего фото</b>\n\n<code>💎 Вы в очереди 1</code>',
    )

    photos = []

    for photo in await s3.get_patterns_photos(data['pattern_id']):
        file = await bot.get_file(message.photo[-1].file_id)
        image_in_memory = io.BytesIO()
        await bot.download_file(file.file_path, destination=image_in_memory)

        photos.append(await face_swap.face_swap(photo, image_in_memory))

    await msg.delete()

    for id_, photo in enumerate(photos):
        await message.answer_photo(
            photo=BufferedInputFile(photo.getbuffer(), filename='test.webp')
        )



# @router.message(F.photo)
# async def process_photo(message: Message, bot: Bot):
#     file_name = f"photos/{message.photo[-1].file_id}.jpg"
#     await bot.download(message.photo[-1], destination=file_name)
