import asyncio
import os
import json
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from parser import (
    get_shard_status,
    get_next_shard_info,
    get_events,
    calculate_season_progress,
    format_season_message,
    calculate_candles,
    format_candle_message
)
from parser.time_utils import TZ

BOT_TOKEN = os.getenv("BOT_TOKEN")
DAILY_JSON = os.getenv("DAILY_JSON")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ================= вспомогательная функция =================
def format_daily() -> list[str]:
    """
    Возвращает ежедневные задания, если дата в DAILY_JSON совпадает с текущей датой Sky (TZ)
    """
    if not DAILY_JSON:
        return []

    try:
        data = json.loads(DAILY_JSON)
    except json.JSONDecodeError:
        return []

    today = datetime.now(TZ).date().isoformat()

    if data.get("date") != today:
        return []

    return [
        task["text"] + " " + format_daily()
        for task in data.get("tasks", [])
        if isinstance(task, dict) and "text" in task
    ]



# ================= команды =================
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет, путешественник! ✨\n"
        "Я помогу тебе не пропустить важное в игре Sky: Children of the Light\n\n"
        "✅ /daily — дейлики\n"
        "💠 /shards — когда падают осколки\n"
        "🔥 /schedule — время фарма\n"
        "🌸 /season — информация о сезоне\n"
        "🕯️ /candles — подсчёт свечей\n\n"
        "🔄 Информация об обновлениях - @classy_sky_dev"
    )


@dp.message(Command("daily"))
async def daily(message: Message):
    tasks = format_daily()

    if not tasks:
        await message.answer(
            "Создатель ещё спит и не обновил задания 💤\n"
            "Простите за неудобства :("
        )
        return

    text = ["✅ Ежедневные задания ✅\n"]
    for task in tasks:
        text.append(f"📌 {task}")

    await message.answer("\n".join(text))
    text = ["✅ Ежедневные задания ✅\n"]
    text.extend(f"📌 {task}" for task in format_daily())
    await message.answer("\n".join(text))



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


@dp.message(Command("schedule"))
async def schedule(message: Message):
    events = get_events()
    await message.answer("🕯️ Фарм:\n\n" + "\n".join(events))


@dp.message(Command("season"))
async def season(message: Message):
    stats = calculate_season_progress()
    text = format_season_message(stats)

    if not text:
        await message.answer("🌱 Сейчас активного сезона нет")
        return

    await message.answer(text)

@dp.message(Command("candles"))
async def candles(message: Message):
    args = message.text.split()

    # /candles без параметров
    if len(args) == 1:
        await message.answer(
            "🕯️ Подсчёт свечей\n\n"
            "Команда позволяет узнать, сколько свечей вы накопите "
            "к определённой дате.\n\n"
            "📌 Формат:\n"
            "/candles <сейчас> <дата> <в_день>\n\n"
            "📅 Дата указывается в формате YYYY-MM-DD\n"
            "🔥 Сбор в день — от 1 до 21 свечи\n\n"
            "✅ Пример:\n"
            "/candles 150 2025-02-28 18"
        )
        return

    # неверное количество аргументов
    if len(args) != 4:
        await message.answer(
            "❌ Неверный формат команды\n\n"
            "Используйте:\n"
            "/candles <сейчас> <дата> <в_день>\n\n"
            "Пример:\n"
            "/candles 150 2025-02-28 18"
        )
        return

    try:
        start_candles = int(args[1])
        target_date = args[2]
        candles_per_day = int(args[3])
    except ValueError:
        await message.answer(
            "❌ Ошибка ввода\n"
            "Количество свечей должно быть числом"
        )
        return

    try:
        result = calculate_candles(
            start_candles=start_candles,
            target_date_str=target_date,
            candles_per_day=candles_per_day
        )
    except ValueError:
        await message.answer(
            "❌ Количество свечей в день должно быть от 1 до 21"
        )
        return

    text = format_candle_message(result)
    await message.answer(text)

# ================= запуск =================
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())