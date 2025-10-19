import asyncio

from aiogram import Router, types, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from database.methods.queries import DBMethods
from templates import render_template

from bot.keyboards.keyboard_utils import (floor_1_cabs, floors_keyboard, reason_keyboard, 
                                          skip_report_description, floor_2_cabs, floor_3_cabs, 
                                          floor_4_cabs, create_report_keyboard)
from bot.keyboards.dynamic_keyboards import main_menu
from bot.states.users import UserStates, Anketa
from bot.utils.sender import send_report_to_admins
from bot.utils.filter import anti_spam_handler
from bot.utils.google_sync import append_report


report_description_router = Router()
db_methods = DBMethods()

@report_description_router.callback_query(F.data == 'skip_report_description', StateFilter(Anketa.description))
async def handle_skip_description_button(callback: CallbackQuery, state: FSMContext):
    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return
    
    await callback.message.delete()

    photo = FSInputFile("templates/images/done_photo.jpg")
    await callback.message.answer_photo(photo=photo, caption=render_template("user/report_created.html"), parse_mode="HTML", reply_markup=main_menu)
    await state.update_data(description="Комментарий отсутствует")

    data = await state.get_data()
    user_id = data.get('id')

    report = await db_methods.create_user_report(
        user_id=user_id,
        report_floor=data['floor'],
        report_cabinet=data['audi'],
        report_reason=data['trouble'],
        report_description=data['description'],
        report_fio=data['fio'],
        user_username=data['username']
    )

    asyncio.create_task(asyncio.to_thread(
        append_report,
        report.report_fio,
        str(report.report_cabinet),
        report.report_description or "Комментарий отсутствует"
    ))

    await state.set_state(UserStates.main_state)

    await state.set_state(UserStates.main_state)
    await send_report_to_admins(report.id)


@report_description_router.message(F.text, StateFilter(Anketa.description))
async def handle_adding_report_description(message: types.Message, state: FSMContext):
    if message.chat.type != "private" or await db_methods.user_is_muted(message.from_user.id) or not await anti_spam_handler(message):
        return

    message_len = len(message.text)
    if message_len > 400:
        await message.answer(render_template("user/report_length_warning.html"), parse_mode="HTML")
        await state.set_state(Anketa.description)
        return

    photo = FSInputFile("templates/images/done_photo.jpg")
    await message.answer_photo(photo=photo, caption=render_template("user/report_created.html"), parse_mode="HTML", reply_markup=main_menu)
    await state.update_data(description=message.text)

    data = await state.get_data()
    user_id = data.get('id')

    report = await db_methods.create_user_report(
        user_id=user_id,
        report_floor=data['floor'],
        report_cabinet=data['audi'],
        report_reason=data['trouble'],
        report_description=data['description'],
        report_fio=data['fio'],
        user_username=data['username']
    )


    asyncio.create_task(asyncio.to_thread(
        append_report,
        report.report_fio,
        str(report.report_cabinet),
        report.report_description or "Комментарий отсутствует"
    ))

    await state.set_state(UserStates.main_state)

    await state.set_state(UserStates.main_state)
    await send_report_to_admins(report.id)