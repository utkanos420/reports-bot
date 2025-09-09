from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    main_state = State()


class Anketa(StatesGroup):
    get_floor = State()
    get_auditory = State()
    get_trouble = State()
    description = State()
    result = State()