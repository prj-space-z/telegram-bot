from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards import for_index
from aiogram.fsm.context import FSMContext

router = Router(name=__name__)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Command: /start"""

    # TODO: Перенести в конфик текста
    await state.clear()
    await message.answer_photo(
        photo='https://i.imgur.com/ZRTZzvi.jpg',
        caption='<b>👋  Привет! Я могу сделать смешные стикеры-мемы с твоим лицом</b>\n\n'
                '<b>👑  А ещё ты можешь сделать свой собственный пак со своими мемами</b>',
        reply_markup=for_index.menu()
    )


@router.callback_query(F.data == "menu")
async def go_menu(callback: CallbackQuery, state: FSMContext):
    """Go menu"""

    await cmd_start(callback.message, state)
    await callback.message.delete()
