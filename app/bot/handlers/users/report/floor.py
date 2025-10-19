import asyncio

from aiogram import Router, types, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from database.methods.queries import DBMethods
from templates import render_template

from bot.states.users import UserStates, Anketa
from bot.utils.filter import anti_spam_handler
from bot.keyboards.keyboard_utils import (floor_1_cabs, floors_keyboard, reason_keyboard, 
                                          skip_report_description, floor_2_cabs, floor_3_cabs, 
                                          floor_4_cabs, create_report_keyboard)


report_floor_router = Router()
db_methods = DBMethods()

@report_floor_router.callback_query(F.data.startswith("floor_"), StateFilter(Anketa.get_floor))
async def handle_floor_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    floor = int(callback.data.removeprefix("floor_"))

    floor_keyboards = {
        1: floor_1_cabs,
        2: floor_2_cabs,
        3: floor_3_cabs,
        4: floor_4_cabs,
    }

    photo = FSInputFile("templates/images/cabinets_photo.jpg")
    await callback.message.answer_photo(
        photo=photo,
        caption=render_template("user/choose_cabinet.html"),
        reply_markup=floor_keyboards[floor](),
        parse_mode="HTML"
    )
    await state.update_data(floor=floor)
    await state.set_state(Anketa.get_auditory)
    await callback.message.delete()
