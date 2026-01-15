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

    chat_id = message.chat.id

    # проверяем, админ ли цель
    member = await bot.get_chat_member(chat_id, TARGET_ID)
    if member.is_chat_admin():
        await message.reply("Эй, @BUNKERKlNG слишком крут для бутылки, он админ 😎")
        return

    until_date = int(time.time()) + MUTE_TIME

    try:
        # мутим цель
        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=TARGET_ID,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        cooldowns[user_id] = now

        # первое сообщение с таймером
        timer_msg = await message.reply(f"@BUNKERKlNG отправлен в бутылку на 5 минут 🍼\nОсталось: 5:00 🕒")

        # таймер обновляем каждые 5 секунд
        interval = 5
        remaining = MUTE_TIME
        while remaining > 0:
            minutes, seconds = divmod(remaining, 60)
            await timer_msg.edit_text(f"@BUNKERKlNG в бутылке 🍼\nОсталось: {minutes}:{seconds:02d} 🕒")
            await asyncio.sleep(interval)
            remaining -= interval
            if remaining < 0:
                remaining = 0

        await timer_msg.edit_text(f"@BUNKERKlNG свободен, бутылка опустела 🎉")

    except Exception as e:
        await message.reply(f"Бот не админ или не может мутить. Я не бог, блин.\nОшибка: {e}")


if __name__ == "__main__":
    asyncio.run(dp.start_polling())