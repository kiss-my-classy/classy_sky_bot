from datetime import datetime
from .time_utils import TZ, start_of_day, MONTHS_RU


MIN_CANDLES_PER_DAY = 1
MAX_CANDLES_PER_DAY = 21


def parse_date(date_str: str) -> datetime:
    """
    Парсит дату формата YYYY-MM-DD и приводит к началу дня в TZ Sky
    """
    return start_of_day(TZ.localize(datetime.fromisoformat(date_str)))


def calculate_candles(
    start_candles: int,
    target_date_str: str,
    candles_per_day: int
) -> dict | None:
    """
    Подсчёт свечей до указанной даты

    :param start_candles: текущее количество свечей
    :param target_date_str: конечная дата (YYYY-MM-DD)
    :param candles_per_day: сбор в день (1–21)
    """
    if not (MIN_CANDLES_PER_DAY <= candles_per_day <= MAX_CANDLES_PER_DAY):
        raise ValueError("candles_per_day_out_of_range")

    today = start_of_day(datetime.now(TZ))
    target_date = parse_date(target_date_str)

    if target_date < today:
        return None

    days = (target_date - today).days + 1
    total_candles = start_candles + days * candles_per_day

    return {
        "start_candles": start_candles,
        "candles_per_day": candles_per_day,
        "days": days,
        "total_candles": total_candles,
        "target_date": target_date,
    }


def format_candle_message(data: dict | None) -> str:
    """
    Форматирование ответа для пользователя
    """
    if data is None:
        return "❌ Указанная дата уже прошла"

    dt = data["target_date"]
    day = dt.day
    month = MONTHS_RU[dt.month - 1]

    return (
        "🕯️ Подсчёт свечей\n\n"
        f"📅 Дата: {day} {month}\n"
        f"🔥 Свечей сейчас: {data['start_candles']}\n"
        f"📈 Сбор в день: {data['candles_per_day']}\n"
        f"⏳ Дней фарма: {data['days']}\n\n"
        f"✨ К {day} {month} у вас будет "
        f"{data['total_candles']} свечей"
    )