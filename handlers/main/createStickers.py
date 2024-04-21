import traceback
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputSticker
from keyboards import for_createStickers, for_index
from services import db, s3
from filters.states import StickersCreate
from aiogram.fsm.context import FSMContext
from services.sheduler import create_stickers_task, app
import io
import time
from aiogram.types import BufferedInputFile
from filters import CheckSubFilter

router = Router(name=__name__)


@router.callback_query(F.data == "createStickers", CheckSubFilter())
async def create_stickers(callback: CallbackQuery):
    await callback.message.answer_photo(
        photo='https://i.imgur.com/rX6mOEK.jpg',
        reply_markup=for_createStickers.get_pattern(await db.get_patterns({'$or': [{'is_share': True}, {'user_id': callback.from_user.id}]}))
    )
    await callback.message.delete()


@router.callback_query(F.data.startswith("createStickers|"))
async def create_stickers(callback: CallbackQuery, state: FSMContext):
    pattern_id = int(callback.data.replace('createStickers|', ''))

    await state.set_state(StickersCreate.image)
    await state.update_data({'pattern_id': pattern_id})

    await callback.message.answer_photo(
        photo='https://i.imgur.com/pqpa6qz.jpeg',
        caption='<b>😎 Отправь своё фото</b>\n\n<b>х Советы:</b>\n1. На фото должно быть хорошо видно лицо\n2. На фото не должно быть других лиц\n3. Желательно без очков или головного убора (Если Вы носите очки, попробуйте без них)',
        reply_markup=for_index.go_home()
    )
    await callback.message.delete()


def await_task(task_id):
    result = app.AsyncResult(task_id).get()
    return result


@router.message(StickersCreate.image, F.photo)
async def account_get_username(message: Message, state: FSMContext, settings: dict, bot: Bot):
    data = await state.get_data()
    await state.clear()

    # task_set = app.AsyncResult.revision('face_swap').count()

    msg = await message.answer_photo(
        photo='https://i.imgur.com/8epdsdY.png',
        caption=f'<b>🐑 Идёт обработка вашего фото</b>\n\n<code>💎 Вы в очереди {1}</code>',
    )

    file = await bot.get_file(message.photo[-1].file_id)
    image_user = io.BytesIO()
    print(file.file_path)
    await bot.download_file(file.file_path, destination=image_user)

    photos = await s3.get_patterns_photos(data['pattern_id'])

    task = create_stickers_task.apply_async(args=([photo.read() for photo in photos], image_user.read(),))

    try:
        loop = asyncio.get_running_loop()
        photos = await loop.run_in_executor(None, await_task, task.id)
    except NotImplementedError:
        #TODO: ADD PHOTO
        traceback.print_exc()
        await message.answer('Произошла ошибка!')
        return

    stickers = []

    for id_, photo in enumerate(photos):
        stickers.append(
            InputSticker(
                sticker=BufferedInputFile(photo, filename='test.webp'),
                emoji_list=['✔️'],
                keywords=['мем']
            )
        )

    #     TODO: Add AD stickers

    bot_me = await bot.get_me()

    url = f't{int(time.time())}_by_{bot_me.username}'
    print(url)

    stickers_pack = await bot.create_new_sticker_set(
        user_id=6138338289,  # TODO: edit user_id
        name=url,
        title=f'Стикеры | By @{bot_me.username}',  # TODO: Go config
        stickers=stickers,
        sticker_format='static'
    )

    await message.answer(f'https://t.me/addstickers/{url}')




# @router.message(F.photo)
# async def process_photo(message: Message, bot: Bot):
#     file_name = f"photos/{message.photo[-1].file_id}.jpg"
#     await bot.download(message.photo[-1], destination=file_name)
