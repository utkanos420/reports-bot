import asyncio

from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from database.methods.queries import DBMethods
from templates import render_template

from bot.keyboards.keyboard_utils import (floor_1_cabs, floors_keyboard, reason_keyboard, 
                                          skip_report_description, floor_2_cabs, floor_3_cabs, 
                                          floor_4_cabs, create_report_keyboard)
from bot.states.users import UserStates, Anketa
from bot.utils.sender import send_report_to_admins
from bot.utils.filter import anti_spam_handler
from bot.utils.google_sync import append_report


user_main_router = Router()
db_methods = DBMethods()

@user_main_router.message(Command("cancel"), ~StateFilter(UserStates.main_state))
async def cancel_report_as_command(message: types.Message, state: FSMContext):
    await message.answer("Вы вернулись в главное меню! Используйте /report для создания нового запроса.")
    await state.set_state(UserStates.main_state)


@user_main_router.message(F.text, StateFilter(UserStates.main_state))
async def create_report_from_command(message: types.Message, state: FSMContext):

    if message.chat.type != "private" or await db_methods.user_is_muted(message.from_user.id) or not await anti_spam_handler(message):
        return

    await message.answer(render_template("user/welcome.html"), parse_mode="HTML", reply_markup=create_report_keyboard())


@user_main_router.callback_query(F.data == "create_report", StateFilter(UserStates.main_state))
async def create_report_from_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id) or not await anti_spam_handler(callback.message):
        return

    await callback.message.answer(render_template("user/problem.html"), parse_mode="HTML")
    await state.update_data(id=callback.from_user.id)
    await state.update_data(username=callback.from_user.username)

    await state.set_state(Anketa.get_fio)


@user_main_router.message(F.text, StateFilter(Anketa.get_fio))
async def handle_fio(message: types.Message, state: FSMContext):

    if message.chat.type != "private" or await db_methods.user_is_muted(message.from_user.id) or not await anti_spam_handler(message):
        return

    message_len = len(message.text)
    if message_len > 70:
        await message.answer(render_template("user/report_length_warning.html"), parse_mode="HTML")
        await state.set_state(Anketa.get_fio)
        return
    
    await state.set_state(Anketa.get_floor)
    await message.answer(render_template("user/choose_floor.html"), parse_mode="HTML", reply_markup=floors_keyboard())

    await state.update_data(fio=message.text)


@user_main_router.callback_query(F.data.startswith("floor_"), StateFilter(Anketa.get_floor))
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

    await callback.message.answer(
        text=render_template("user/choose_cabinet.html"),
        reply_markup=floor_keyboards[floor](),
        parse_mode="HTML"
    )
    await state.update_data(floor=floor)
    await state.set_state(Anketa.get_auditory)
    await callback.message.delete()


@user_main_router.callback_query(F.data.startswith("cabinet_"), StateFilter(Anketa.get_auditory))
async def handle_cabinet_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    audience_number = callback.data.removeprefix("cabinet_")

    await callback.message.answer(text=render_template("user/choose_reason.html"), reply_markup=reason_keyboard(), parse_mode="HTML")
    await state.update_data(audi=audience_number)
    await state.set_state(Anketa.get_trouble)
    await callback.message.delete()


@user_main_router.callback_query(F.data == "card", StateFilter(Anketa.get_trouble))
async def handle_reason_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    await callback.message.answer(render_template("user/problem_description.html"), parse_mode="HTML", reply_markup=skip_report_description())
    await state.update_data(trouble="Проходка")
    await state.set_state(Anketa.description)
    await callback.message.delete()


@user_main_router.callback_query(F.data == 'devices', StateFilter(Anketa.get_trouble))
async def handle_reason_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    await callback.message.answer(render_template("user/problem_description.html"), parse_mode="HTML", reply_markup=skip_report_description())
    await state.update_data(trouble="Оборудование")
    await state.set_state(Anketa.description)
    await callback.message.delete()


@user_main_router.callback_query(F.data == 'devices_soft', StateFilter(Anketa.get_trouble))
async def handle_reason_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    await callback.message.answer(render_template("user/problem_description.html"), parse_mode="HTML", reply_markup=skip_report_description())
    await state.update_data(trouble="Настройка оборудования")
    await state.set_state(Anketa.description)
    await callback.message.delete()


@user_main_router.callback_query(F.data == "other", StateFilter(Anketa.get_trouble))
async def handle_reason_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    await callback.message.answer(render_template("user/problem_description.html"), parse_mode="HTML", reply_markup=skip_report_description())
    await state.update_data(trouble="другое")
    await state.set_state(Anketa.description)
    await callback.message.delete()


@user_main_router.callback_query(F.data == 'skip_report_description', StateFilter(Anketa.description))
async def handle_skip_description_button(callback: CallbackQuery, state: FSMContext):
    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    await callback.message.answer(render_template("user/report_created.html"), parse_mode="HTML")

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

    # ✅ Добавляем запись в Google Sheets (в отдельном потоке, чтобы не тормозило бота)
    asyncio.create_task(asyncio.to_thread(
        append_report,
        report.report_fio,
        str(report.report_cabinet),
        report.report_description or "Комментарий отсутствует"
    ))

    await state.set_state(UserStates.main_state)
    await send_report_to_admins(report.id)


@user_main_router.message(F.text, StateFilter(Anketa.description))
async def handle_adding_report_description(message: types.Message, state: FSMContext):
    if message.chat.type != "private" or await db_methods.user_is_muted(message.from_user.id) or not await anti_spam_handler(message):
        return

    message_len = len(message.text)
    if message_len > 400:
        await message.answer(render_template("user/report_length_warning.html"), parse_mode="HTML")
        await state.set_state(Anketa.description)
        return

    await message.answer(render_template("user/report_created.html"), parse_mode="HTML")

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
        report.report_description or ""
    ))

    await state.set_state(UserStates.main_state)
    await send_report_to_admins(report.id)
