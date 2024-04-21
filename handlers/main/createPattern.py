import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from keyboards import for_index, for_createPattern
from filters.states import PatternCreate
from aiogram.fsm.context import FSMContext
import io
from services import db, s3, images

router = Router(name=__name__)


@router.callback_query(F.data == "createPattern")
async def create_pattern(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer_photo(
        photo='https://i.imgur.com/pqpa6qz.jpeg',
        caption='<b>🔥 Отправьте шаблон стикера на котором будет заменено лицо</b>\n\n'
                '❗️ Изображение должно быть больше или равно 512x512 пикс',
        reply_markup=for_index.go_home()
    )
    await callback.message.delete()
    await state.set_state(PatternCreate.image)
    await state.update_data({'images': []})


@router.message(PatternCreate.image, F.photo)
async def account_get_username(message: Message, state: FSMContext, settings: dict):
    if message.photo[-1].width < 512 or message.photo[-1].height < 512:
        await message.answer_photo(
            photo='https://imgur.com/ULa3EE5',
            caption='<b>❌ ОШИБКА:</b> Ваше фото меньше чем 512x512 пикс!\n\nПопробуйте снова',
            reply_markup=for_index.go_home()
        )
        return

    data = await state.get_data()
    data['images'] += [message.photo[-1].file_id]
    await state.update_data(data)

    if len(data['images']) >= settings.max_images_pattern:
        await message.answer_photo(
            photo='https://i.imgur.com/mztr2yf.jpeg',
            caption='<b>⚡️ Придумайте название шаблона:</b>',
            reply_markup=for_index.go_home()
        )
        await state.set_state(PatternCreate.title)
    else:
        await message.answer_photo(
            photo='https://i.imgur.com/4yGp1T4.jpeg',
            caption=f'<code>🖼 {len(data["images"])}/{settings.max_images_pattern}</code>\n\n'
                    f'❗️ Изображение должно быть больше или равно 512x512 пикс',
            reply_markup=for_createPattern.get_images()
        )


@router.callback_query(F.data == "createPattern|getName")
async def create_pattern(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer_photo(
        photo='https://i.imgur.com/mztr2yf.jpeg',
        caption='<b>⚡️ Придумайте название шаблона:</b>',
        reply_markup=for_index.go_home()
    )
    await callback.message.delete()
    await state.set_state(PatternCreate.title)


@router.message(PatternCreate.title)
async def account_get_username(message: Message, state: FSMContext, bot: Bot):
    if len(message.text) > 50:
        await message.answer('<b>❌ Ошибка:</b> Максимальная длина названия 50 символов')
        return

    msg = await message.answer_photo(
        photo='https://i.imgur.com/8epdsdY.png',
        caption='<b>🐑 Идёт обработка вашего шаблона</b>',
    )

    pattern_db = await db.create_patterns(
        name=message.text,
        user_id=message.from_user.id
    )

    logging.info('Downloading images')

    data = await state.get_data()
    images_buffer = []

    for image_id in data['images']:
        image_in_memory = await images.downloading_image(bot, image_id)
        images_buffer.append(image_in_memory)

    logging.info('Resizing images')

    images_buffer_temp = []

    for buffer in images_buffer:
        image_io = await images.resizing_image(buffer)
        images_buffer_temp.append(image_io)

    logging.info('Sending images')

    await s3.add_patterns_photo([io.BytesIO(image.getbuffer()) for image in images_buffer_temp],
                                pattern_db['id'])

    await msg.delete()

    bot_me = await bot.get_me()
    pattern_url = f't.me/{bot_me.username}?pattern={pattern_db["id"]}_{pattern_db["translit"]}'
    await message.answer_photo(
        photo='https://i.imgur.com/uF15JYE.jpeg',
        caption=f'<b>✅ Шаблон успешно создан</b>\n\nСсылка на ваш шаблон: {pattern_url}',
        reply_markup=for_createPattern.successfully(share_url=pattern_url)
    )
    # TODO: Сделать переход
    await state.clear()
