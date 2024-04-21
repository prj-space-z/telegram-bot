from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup


class PatternCreate(StatesGroup):
    image = State()
    title = State()


class StickersCreate(StatesGroup):
    image = State()


class TelegramAD(StatesGroup):
    chat = State()
    url = State()


NoneState = StateFilter(None)
AnyState = ~NoneState
