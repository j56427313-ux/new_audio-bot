from aiogram.fsm.state import StatesGroup, State


class TarjimaState(StatesGroup):
    qaysi_tildan = State()
    qaysi_tilga = State()
    matn = State()