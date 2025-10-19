import asyncio

from aiogram import Router, types, F
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from database.methods.queries import DBMethods
from templates import render_template

from bot.states.users import Anketa
from bot.utils.filter import anti_spam_handler
from bot.keyboards.keyboard_utils import floors_keyboard


report_fio_router = Router()
db_methods = DBMethods()

@report_fio_router.message(F.text & (F.text != "/отмена"), StateFilter(Anketa.get_fio))
async def handle_fio(message: types.Message, state: FSMContext):

    if message.chat.type != "private" or await db_methods.user_is_muted(message.from_user.id) or not await anti_spam_handler(message):
        return

    state_data = await state.get_data()
    bot_message_id = state_data.get("bot_answer_id")

    if bot_message_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        except Exception as e:
            print(f"Не удалось удалить сообщение бота: {e}")

    message_len = len(message.text)
    if message_len > 70:
        await message.answer(render_template("user/report_length_warning.html"), parse_mode="HTML")
        await state.set_state(Anketa.get_fio)
        return
    


    await state.set_state(Anketa.get_floor)
    photo = FSInputFile("templates/images/floor_photo.jpg")
    await message.answer_photo(photo=photo, caption=render_template("user/choose_floor.html"), parse_mode="HTML", reply_markup=floors_keyboard())

    await state.update_data(fio=message.text)