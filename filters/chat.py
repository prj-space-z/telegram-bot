from aiogram import F, Bot
from aiogram.enums import ChatType
from aiogram.filters import BaseFilter, MagicData
from typing import Union
from aiogram.types import CallbackQuery
from keyboards import for_index


ADMIN_ONLY = MagicData(F.event_from_user.id == F.settings.admin_id)
PRIVATE_ONLY = MagicData(F.event_chat.type == ChatType.PRIVATE)


class CheckSubFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery, db_settings: dict, bot: Bot) -> bool:
        if db_settings['social']['telegram']['active']:
            user_channel_status = await bot.get_chat_member(chat_id=db_settings['social']['telegram']['channel_id'],
                                                            user_id=callback.from_user.id)

            if user_channel_status.status == 'left':
                await callback.message.delete()
                await callback.message.answer_photo(
                    photo='https://i.imgur.com/029y90p.jpeg',
                    caption='⚡️ Прежде чем начать, пожалуйста подпишитесь на каналы',
                    reply_markup=for_index.subscription_check(telegram=db_settings['social']['telegram']['url'],
                                                              callback_data=callback.data)
                )
                return False

        return True
