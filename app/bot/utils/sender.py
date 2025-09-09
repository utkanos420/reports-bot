from loader import bot

from settings.config import settings

from bot.keyboards.dynamic_keyboards import show_report_by_id
from templates.template_engine import render_template


async def send_report_to_admins(report_id: int):
    await bot.send_message(text=f"Получен репорт №{report_id}", reply_markup=show_report_by_id(report_id), chat_id=settings.bot_admin_id)


async def notice_muted_user(user_id: int):
    await bot.send_message(render_template("mute-notice.html"), parse_mode="HTML", chat_id=user_id)


async def notice_user(user_id: int):
    user_id = int(user_id)
    await bot.send_message(chat_id=user_id, text=render_template("admin/notice_user.html"), parse_mode="HTML")


