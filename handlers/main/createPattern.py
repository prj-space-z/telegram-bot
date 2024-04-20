import logging
from PIL import Image
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from keyboards import for_index, for_createPattern
from filters.states import PatternCreate
from aiogram.fsm.context import FSMContext
import io

router = Router(name=__name__)


@router.callback_query(F.data == "createPattern")
async def create_pattern(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo='https://i.imgur.com/pqpa6qz.jpeg',
        caption='<b>🔥 Отправьте шаблон стикера на котором будет заменено лицо</b>\n\n❗️ Изображение должно быть больше или равно 512x512 пикс',
        reply_markup=for_index.go_home()
    )
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
            caption=f'<code>🖼 {len(data["images"])}/{settings.max_images_pattern}</code>\n\n❗️ Изображение должно быть больше или равно 512x512 пикс',
            reply_markup=for_createPattern.get_images()
        )


@router.callback_query(F.data == "createPattern|getName")
async def create_pattern(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo='https://i.imgur.com/mztr2yf.jpeg',
        caption='<b>⚡️ Придумайте название шаблона:</b>',
        reply_markup=for_index.go_home()
    )
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

    # TODO: Перенести в функцию
    logging.info('Downloading images')

    data = await state.get_data()
    images_buffer = []

    for image_id in data['images']:
        file = await bot.get_file(image_id)
        image_in_memory = io.BytesIO()
        await bot.download_file(file.file_path, destination=image_in_memory)
        images_buffer.append(image_in_memory)

    logging.info('Resizing images')

    for buffer in images_buffer:
        img = Image.open(buffer)
        img = img.convert('RGB')
        img = img.resize((512, 512))
        img.save(buffer, 'WEBP')
        img.save('tmp.WEBP', 'WEBP')

    logging.info('Sending images')



    await msg.delete()
    await message.answer_photo(
        photo='https://i.imgur.com/uF15JYE.jpeg',
        caption='<b>✅ Шаблон успешно создан</b>\n\nСсылка на ваш шаблон: t.me/MemeSwap_robot?pattern=98034',
        reply_markup=for_createPattern.successfully(share_url='t.me/MemeSwap_robot?pattern=98034')
    )
    await state.clear()
