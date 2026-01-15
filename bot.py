import asyncio
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions
import os

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN не найден! Проверь Shared Variable в Railway")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

TARGET_ID = 800734488  # BUNKERKlNG
MUTE_TIME = 5 * 60      # 5 минут
COOLDOWN = 60 * 60      # 1 час

TARGET_USERNAME = "@BUNKERKlNG"
MUTE_TIME = 5 * 60        # 5 минут
COOLDOWN = 60 * 60        # 1 час

bot = Bot(token=TOKEN)
dp = Dispatcher()

cooldowns = {}  # user_id : last_use_time


@dp.message_handler(commands=["butilka"])
async def butilka(message: types.Message):
    user_id = message.from_user.id
    now = time.time()

    # проверка кулдауна
    if user_id in cooldowns and now - cooldowns[user_id] < COOLDOWN:
        remaining = int((COOLDOWN - (now - cooldowns[user_id])) / 60)
        await message.reply(f"Кулдаун, терпила. Жди ещё {remaining} мин.")
        return

    chat = message.chat

    # ищем BUNKERKlNG среди участников
    target_id = None
    async for member in bot.get_chat_administrators(chat.id):
        if member.user.username == TARGET_USERNAME:
            target_id = member.user.id
            break
    if not target_id:
        async for member in bot.get_chat(chat.id).get_members():
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
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        cooldowns[user_id] = now

        # первое сообщение
        timer_msg = await message.reply(f"@{TARGET_USERNAME} отправлен в бутылку на 5 минут 🍼\nОсталось: 5:00 🕒")

        # цикл таймера
        for remaining in range(MUTE_TIME - 1, -1, -1):
            minutes, seconds = divmod(remaining, 60)
            await timer_msg.edit_text(f"@{TARGET_USERNAME} в бутылке 🍼\nОсталось: {minutes}:{seconds:02d} 🕒")
            await asyncio.sleep(1)

        await timer_msg.edit_text(f"@{TARGET_USERNAME} свободен, бутылка опустела 🎉")

    except Exception as e:
        await message.reply(f"Бот не админ или не может мутить. Я не бог, блин.\nОшибка: {e}")


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))