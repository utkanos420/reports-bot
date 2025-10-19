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


report_reason_router = Router()
db_methods = DBMethods()

reasons = {
    "card": "Проходка",
    "devices": "Оборудование",
    "devices_soft": "Настройка оборудования",
    "other": "Другое"
}

@report_reason_router.callback_query(F.data.in_(reasons.keys()), StateFilter(Anketa.get_trouble))
async def handle_reason(callback: CallbackQuery, state: FSMContext):

    caption_text = render_template("user/problem_description.html")
    photo = FSInputFile("templates/images/description_photo.jpg")
    await callback.message.answer_photo(
        photo=photo,
        caption=caption_text,
        parse_mode="HTML",
        reply_markup=skip_report_description()
    )

    await state.update_data(trouble=callback.data)
    await state.set_state(Anketa.description)
