import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from parser import format_daily, get_shard_status, get_next_shard_info, get_events

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет, путешественник! ✨\n"
        "Я помогу тебе не пропустить важное в игре Sky: Children of the Light\n"
        "✅ /daily — дейлики\n"
        "💠 /shards — когда падают осколки\n"
        "🔥 /schedule — время фарма\n"
    )


#=================дейлики=================
@dp.message(Command("daily"))
async def daily(message: Message):
    tasks = format_daily()

    if not tasks:
        await message.answer("Создатель ещё спит и не обновил задания💤 Простите за неудобства:(")
        return

    text = ["✅ Ежедневные задания ✅\n"]
    for task in tasks:
        text.append(f"📌 {task}")

    await message.answer("\n".join(text))

#=================осколки=================
@dp.message(Command("shards"))
async def shards(message: Message):
    status = get_shard_status()

    if status:
        await message.answer(status)
        return

    next_info = get_next_shard_info()
    if not next_info:
        await message.answer("Сегодня осколков нет ❌")
        return

    color, day_num, month = next_info
    await message.answer(
        f"Сегодня осколков нет ❌\n"
        f"Следующий осколок {color} цвета упадёт 🗓️ {day_num} {month}"
    )

#=================фарм-объекты=================
@dp.message(Command("schedule"))
async def schedule(message: Message):
    events = get_events()
    text = "🕯️ Фарм:\n\n" + "\n".join(events)
    await message.answer(text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())