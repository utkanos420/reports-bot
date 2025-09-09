from typing import Callable, Any, Awaitable, Dict

from aiogram import Router, types, F, BaseMiddleware
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject

from database.methods.queries import DBMethods
from bot.states.users import UserStates
from bot.states.admins import AdminStates

from settings.config import admin_ids
from bot.keyboards.keyboard_utils import create_report_keyboard
from templates import render_template


class UserInternalIdMiddleware(BaseMiddleware):
    def __init__(self):
        self.db_methods = DBMethods()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        state: FSMContext = data.get("state")

        if user:
            user_id = user.id
            username = user.username

            existing_user = await self.db_methods.get_user(user_id)

            if not existing_user:
                created_user = await self.db_methods.create_user(user_id, username)

            data["user_id"] = user_id
            data["user_username"] = username

            if user_id in admin_ids:
                await state.set_state(AdminStates.main_state)
            else:
                await state.set_state(UserStates.main_state)
            
        return await handler(event, data)


start_router = Router()
start_router.message.middleware(UserInternalIdMiddleware())


@start_router.message(CommandStart(), StateFilter(None))
async def start_as_command(message: types.Message, state: FSMContext):

    if message.chat.type != "private":
        return

    if message.from_user.id in admin_ids:
        await message.answer(render_template("admin/welcome.html"), parse_mode="HTML")
    else:
        await message.answer(render_template("user/welcome.html"), parse_mode="HTML", reply_markup=create_report_keyboard())


@start_router.message(F.text, StateFilter(None))
async def start_as_message(message: types.Message, state: FSMContext):

    if message.chat.type != "private":
        return

    if message.from_user.id in admin_ids:
        await message.answer(render_template("admin/welcome.html"), parse_mode="HTML")
    else:
        await message.answer(render_template("user/welcome.html"), parse_mode="HTML", reply_markup=create_report_keyboard())
