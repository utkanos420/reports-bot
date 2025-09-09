from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    main_state = State()
    get_user_id = State()