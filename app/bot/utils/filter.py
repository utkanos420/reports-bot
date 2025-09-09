import time
from aiogram.types import Message

POST_COOLDOWN = 5
WARNING_THRESHOLD = 3
INITIAL_BAN_TIME = 30
BAN_MULTIPLIER = 2

user_post_timestamps = {}
user_warnings = {}
user_bans = {}
user_ban_count = {}


async def anti_spam_handler(message: Message) -> bool:

    user_id = message.from_user.id
    current_time = time.time()

    if user_id in user_bans and current_time < user_bans[user_id]:
        return False

    if user_id in user_post_timestamps:
        last_post_time = user_post_timestamps[user_id]
        if current_time - last_post_time < POST_COOLDOWN:
            user_warnings[user_id] = user_warnings.get(user_id, 0) + 1

            if user_warnings[user_id] >= WARNING_THRESHOLD:
                user_ban_count[user_id] = user_ban_count.get(user_id, 0) + 1

                ban_duration = INITIAL_BAN_TIME * (BAN_MULTIPLIER ** user_ban_count[user_id])


                user_bans[user_id] = current_time + ban_duration
                user_warnings[user_id] = 0

                await message.answer(
                    f"{message.from_user.full_name.capitalize()}, вы временно заблокированы за частые попытки отправки постов. Подождите {int(ban_duration)} секунд"
                )
            else:
                await message.answer(
                    "Не так быстро!"
                )
            return False

    user_post_timestamps[user_id] = current_time
    user_warnings[user_id] = 0
    return True


def cleanup_old_data():
    current_time = time.time()
    for user_id in list(user_post_timestamps):
        if current_time - user_post_timestamps[user_id] > POST_COOLDOWN:
            del user_post_timestamps[user_id]
    for user_id in list(user_bans):
        if current_time > user_bans[user_id]:
            del user_bans[user_id]
            del user_ban_count[user_id]
