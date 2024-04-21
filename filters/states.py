from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup


class PatternCreate(StatesGroup):
    image = State()
    title = State()


class StickersCreate(StatesGroup):
    image = State()


class AdminTelegramAD(StatesGroup):
    chat = State()
    url = State()


class AdminGetTemplate(StatesGroup):
    id_template = State()


NoneState = StateFilter(None)
AnyState = ~NoneState
