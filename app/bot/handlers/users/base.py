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
from bot.keyboards.dynamic_keyboards import main_menu


base_router = Router()
db_methods = DBMethods()


async def is_user_allowed(event) -> bool:
    if getattr(event, "chat", None) and event.chat.type != "private":
        return False
    if await db_methods.user_is_muted(event.from_user.id):
        return False
    if hasattr(event, "text") and not await anti_spam_handler(event):
        return False
    return True


@base_router.message(Command("отмена"), ~StateFilter(UserStates.main_state))
async def cancel_report_as_command(message: types.Message, state: FSMContext):
    await message.answer(text=render_template("user/cancel_report.html"), parse_mode="HTML", reply_markup=main_menu)
    await state.set_state(UserStates.main_state)


@base_router.message(F.text, StateFilter(UserStates.main_state))
async def create_report_from_command(message: types.Message, state: FSMContext):

    if message.chat.type != "private" or await db_methods.user_is_muted(message.from_user.id) or not await anti_spam_handler(message):
        return

    await message.answer(text=render_template("user/welcome.html"), parse_mode="HTML", reply_markup=create_report_keyboard())


@base_router.callback_query(F.data == "create_report", StateFilter(UserStates.main_state))
async def create_report_from_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id) or not await anti_spam_handler(callback.message):
        return

    photo = FSInputFile("templates/images/fio_photo.jpg")
    bot_answer = await callback.message.answer_photo(photo=photo, caption=render_template("user/fio.html"), parse_mode="HTML")
    await state.update_data(id=callback.from_user.id, bot_answer_id=bot_answer.message_id)
    await state.update_data(username=callback.from_user.username)

    await state.set_state(Anketa.get_fio)
