from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards import for_index

router = Router(name=__name__)


@router.callback_query(F.data == "howWork")
async def create_stickers(callback: CallbackQuery):
    await callback.message.answer_photo(
        photo='https://i.imgur.com/ZRTZzvi.jpg',
        caption="""<b>😎 Работает всё очень просто:</b>

— Вы выбираете шаблон стикеров
— Отправляете фото с лицом
— Получаете кастомные стикеры 👑

<b>х Советы:</b>
1. На фото должно быть хорошо видно лицо
2. На фото не должно быть других лиц
3. Желательно без очков или головного убора (Если Вы носите очки, попробуйте без них)

<b>🙊 Дерзай!</b>""",
        reply_markup=for_index.go_home()
    )
    await callback.message.delete()
