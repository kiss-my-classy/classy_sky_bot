from datetime import datetime
from .time_utils import TZ, start_of_day, MONTHS_RU

CANDLES_PER_DAY = 20


def parse_date(date_str: str):
    return start_of_day(TZ.localize(datetime.fromisoformat(date_str)))


def calculate_candles(start_candles: int, target_date_str: str) -> dict | None:
    today = start_of_day(datetime.now(TZ))
    target_date = parse_date(target_date_str)

    if target_date < today:
        return None

    days = (target_date - today).days + 1
    total_candles = start_candles + days * CANDLES_PER_DAY

    return {
        "total_candles": total_candles,
        "target_date": target_date,
    }


def format_candle_message(data: dict | None) -> str:
    if data is None:
        return "Указанная дата уже прошла ❌"

    dt = data["target_date"]
    day = dt.day
    month = MONTHS_RU[dt.month - 1]

    return (
        f"К {day} {month} вы накопите "
        f"{data['total_candles']} свечей "
        f"(при учёте сбора {CANDLES_PER_DAY} в день)"
    )