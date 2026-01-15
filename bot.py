import asyncio
import time
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = "ВСТАВЬ_СЮДА_ТОКЕН"

TARGET_USERNAME = "BUNKERKlNG"
MUTE_TIME = 5 * 60        # 5 минут
COOLDOWN = 60 * 60        # 1 час

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

cooldowns = {}  # user_id : last_use_time


@dp.message_handler(commands=["butilka"])
async def butilka(message: types.Message):
    user_id = message.from_user.id
    now = time.time()

    # проверка кулдауна
    if user_id in cooldowns:
        if now - cooldowns[user_id] < COOLDOWN:
            remaining = int((COOLDOWN - (now - cooldowns[user_id])) / 60)
            await message.reply(f"Кулдаун, терпила. Жди ещё {remaining} мин.")
            return

    chat = message.chat

    # ищем BUNKERKlNG среди админов и участников
    target_id = None
    async for member in bot.iter_chat_members(chat.id):
        if member.user.username == TARGET_USERNAME:
            target_id = member.user.id
            break

    if not target_id:
        await message.reply("Цель не найдена. Он сбежал или сменил ник.")
        return

    until_date = int(time.time()) + MUTE_TIME

    try:
        await bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=target_id,
            permissions=types.ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        cooldowns[user_id] = now
        await message.reply(f"@{TARGET_USERNAME} отправлен в бутылку на 5 минут 🍼")
    except:
        await message.reply("Бот не админ или не может мутить. Я не бог, блин.")


if __name__ == "__main__":
    executor.start_polling(dp)
