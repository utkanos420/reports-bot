from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from database.methods.queries import DBMethods
from templates import render_template

from bot.keyboards.keyboard_utils import (floor_1_audiences, floors_keyboard, reason_keyboard, 
                                          skip_report_description, floor_2_audiences, floor_3_audiences, 
                                          floor_4_audiences, create_report_keyboard)
from bot.states.users import UserStates, Anketa
from bot.utils.sender import send_report_to_admins
from bot.utils.filter import anti_spam_handler


user_main_router = Router()
db_methods = DBMethods()

@user_main_router.message(Command("report"), StateFilter(UserStates.main_state))
async def create_report_from_command(message: types.Message, state: FSMContext):

    if message.chat.type != "private" or await db_methods.user_is_muted(message.from_user.id) or not await anti_spam_handler(message):
        return

    await message.answer(render_template("user/problem.html"), parse_mode="HTML")
    await message.answer("<b>Выберите ваш этаж:</b>", reply_markup=floors_keyboard(), parse_mode="HTML")
    await state.set_state(Anketa.get_floor)


@user_main_router.message(Command("admin"), StateFilter(UserStates.main_state))
async def admin_login_by_password(message: types.Message, state: FSMContext):
    await message.answer(render_template("user/admin_login_by_password.html"), parse_mode="HTML")
    await state.set_state(UserStates.get_password)


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
    await callback.message.answer("<b>Выберите ваш этаж:</b>", reply_markup=floors_keyboard(), parse_mode="HTML")
    await state.update_data(id=callback.from_user.id)

    await state.set_state(Anketa.get_floor)


@user_main_router.callback_query(F.data.startswith("floor_"), StateFilter(Anketa.get_floor))
async def handle_floor_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    floor = int(callback.data.removeprefix("floor_"))

    floor_keyboards = {
        1: floor_1_audiences,
        2: floor_2_audiences,
        3: floor_3_audiences,
        4: floor_4_audiences,
    }

    if floor not in floor_keyboards:
        await callback.answer("Неизвестный этаж.")
        return

    await callback.message.answer(
        "<b>Выберите кабинет:</b>",
        reply_markup=floor_keyboards[floor](),
        parse_mode="HTML"
    )
    await state.update_data(floor=floor)
    await state.set_state(Anketa.get_auditory)
    await callback.message.delete()


@user_main_router.callback_query(F.data.startswith("audience_"), StateFilter(Anketa.get_auditory))
async def handle_cabinet_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    audience_number = callback.data.removeprefix("audience_")

    await callback.message.answer("<b>Выберите вашу проблему из списка:</b>", reply_markup=reason_keyboard(), parse_mode="HTML")
    await state.update_data(audi=audience_number)
    await state.set_state(Anketa.get_trouble)
    await callback.message.delete()


@user_main_router.callback_query(F.data == 'sound', StateFilter(Anketa.get_trouble))
async def handle_reason_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    await callback.message.answer(render_template("user/problem_description.html"), parse_mode="HTML", reply_markup=skip_report_description())
    await state.update_data(trouble="sound")
    await state.set_state(Anketa.description)
    await callback.message.delete()


@user_main_router.callback_query(F.data == 'pc', StateFilter(Anketa.get_trouble))
async def handle_reason_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    await callback.message.answer(render_template("user/problem_description.html"), parse_mode="HTML", reply_markup=skip_report_description())
    await state.update_data(trouble="pc")
    await state.set_state(Anketa.description)
    await callback.message.delete()


@user_main_router.callback_query(F.data == 'projector', StateFilter(Anketa.get_trouble))
async def handle_reason_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    await callback.message.answer(render_template("user/problem_description.html"), parse_mode="HTML", reply_markup=skip_report_description())
    await state.update_data(trouble="проектор")
    await state.set_state(Anketa.description)
    await callback.message.delete()


@user_main_router.callback_query(F.data == 'другое', StateFilter(Anketa.get_trouble))
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

    await state.update_data(desc="Комментарий отсутсвует")

    data = await state.get_data()
    user_id = data.get('id')

    report = await db_methods.create_user_report(
        user_id=user_id,
        report_floor=data['floor'],
        report_cabinet=data['audi'],
        report_reason=data['trouble'],
        report_description=data['desc']
    )

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

    await state.update_data(desc=message.text)

    data = await state.get_data()
    user_id = data.get('id')

    report = await db_methods.create_user_report(
        user_id=user_id,
        report_floor=data['floor'],
        report_cabinet=data['audi'],
        report_reason=data['trouble'],
        report_description=data['desc']
    )

    await state.set_state(UserStates.main_state)

    await send_report_to_admins(report.id)
