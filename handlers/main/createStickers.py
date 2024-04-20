from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards import for_index

router = Router(name=__name__)


@router.callback_query(F.data == "createStickers")
async def create_stickers(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo='https://i.imgur.com/rX6mOEK.jpg',
        reply_markup=for_index.go_home()
    )


# @router.message(F.photo)
# async def process_photo(message: Message, bot: Bot):
#     file_name = f"photos/{message.photo[-1].file_id}.jpg"
#     await bot.download(message.photo[-1], destination=file_name)
