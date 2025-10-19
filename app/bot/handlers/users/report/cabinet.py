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


report_cabinet_router = Router()
db_methods = DBMethods()

@report_cabinet_router.callback_query(F.data.startswith("cabinet_"), StateFilter(Anketa.get_auditory))
async def handle_cabinet_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    audience_number = callback.data.removeprefix("cabinet_")

    photo = FSInputFile("templates/images/reason_photo.jpg")
    await callback.message.answer_photo(photo=photo, caption=render_template("user/choose_reason.html"), reply_markup=reason_keyboard(), parse_mode="HTML")
    await state.update_data(audi=audience_number)
    await state.set_state(Anketa.get_trouble)
    await callback.message.delete()