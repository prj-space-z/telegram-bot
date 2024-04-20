from aiogram import F
from aiogram.enums import ChatType
from aiogram.filters import BaseFilter, MagicData
from typing import Union


ADMIN_ONLY = MagicData(F.event_from_user.id == F.settings.admin_id)
PRIVATE_ONLY = MagicData(F.event_chat.type == ChatType.PRIVATE)
