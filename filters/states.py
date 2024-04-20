from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup


class PatternCreate(StatesGroup):
    image = State()
    title = State()


NoneState = StateFilter(None)
AnyState = ~NoneState
