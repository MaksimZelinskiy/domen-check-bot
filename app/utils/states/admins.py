from aiogram.fsm.state import State, StatesGroup

class AddUserStates(StatesGroup):
    user_id = State()
    role = State()