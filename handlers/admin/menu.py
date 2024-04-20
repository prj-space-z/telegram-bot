from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

router = Router(name=__name__)


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Command: /admin"""

    await message.answer('Я работаю!')
