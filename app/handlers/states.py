from aiogram.dispatcher.filters.state import State, StatesGroup

class UserStates(StatesGroup):
    offset = State()
    spam = State()
    admin_actions = State()
