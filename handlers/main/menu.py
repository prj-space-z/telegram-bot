from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards import for_index

router = Router(name=__name__)


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Command: /start"""

    # TODO: Перенести в конфик текста
    await message.answer_photo(
        photo='https://i.imgur.com/ZRTZzvi.jpg',
        caption='<b>👋  Привет! Я могу сделать смешные стикеры-мемы с твоим лицом XD</b>\n\n<b>👑  А ещё ты можешь сделать свой собственный пак со своими мемами</b>',
        reply_markup=for_index.menu()
    )


@router.callback_query(F.data == "menu")
async def go_menu(callback: CallbackQuery):
    """Go menu"""

    await callback.message.delete()
    await cmd_start(callback.message)
