from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command

from database.methods.queries import DBMethods

from bot.keyboards.dynamic_keyboards import mute_user_by_id, mark_as_reacted
from bot.utils.sender import notice_muted_user, notice_user
from bot.states.admins import AdminStates

from templates.template_engine import render_template




db_methods = DBMethods()
admin_router = Router()


@admin_router.callback_query(lambda c: c.data.startswith("show_report_by_id_"), StateFilter(AdminStates.main_state))
async def return_the_report_by_id(callback: CallbackQuery, state: FSMContext):
    post_id_str = callback.data.removeprefix("show_report_by_id_")
    post_id = int(post_id_str)

    db = DBMethods()
    report = await db.get_user_report_by_id(post_id)
    print(report.report_description)

    if report:

        await callback.message.answer(
            f"<b>📝Запрос №{report.id}</b>\n"
            f"Причина: {report.report_reason}\n"
            f"Этаж: {report.report_floor}, кабинет: {report.report_cabinet}\n"
            f"\n"
            f"Описание:"
            f"\n"
            f"{report.report_description}",
            parse_mode="HTML",
            reply_markup=mark_as_reacted(user_id=report.user_id)            
        )

    else:

        await callback.message.answer("Репорт не найден.")


@admin_router.callback_query(lambda c: c.data.startswith("mute_user_by_id_"), StateFilter(AdminStates.main_state))
async def mute_user_from_button(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.removeprefix("mute_user_by_id_")
    db = DBMethods()
    await db.mute_user_by_id(user_id=user_id)
    await callback.message.answer(f"Пользователь с id {user_id} заблокирован")
    await notice_muted_user(user_id)


@admin_router.callback_query(lambda c: c.data.startswith("notice_user_by_id_"), StateFilter(AdminStates.main_state))
async def notify_user_from_button(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.removeprefix("notice_user_by_id_")
    await notice_user(user_id=user_id)
    await callback.message.answer(text="Уведомление отправлено пользователю")


@admin_router.message(Command("unmute"), StateFilter(AdminStates.main_state))
async def create_report_from_command(message: types.Message, state: FSMContext):

    if message.chat.type != "private" or await db_methods.user_is_muted(message.from_user.id):
        return

    await message.answer(render_template("admin/unmute.html"), parse_mode="HTML")
    await state.set_state(AdminStates.get_user_id)


@admin_router.message(F.text, StateFilter(AdminStates.get_user_id))
async def create_report_from_command(message: types.Message, state: FSMContext):

    if message.chat.type != "private" or await db_methods.user_is_muted(message.from_user.id):
        return

    await db_methods.unmute_user_by_id(user_id=message.text)
    await message.answer("Пользователь разблокирован")
    await state.set_state(AdminStates.main_state)
