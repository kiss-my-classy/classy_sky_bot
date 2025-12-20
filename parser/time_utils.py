from datetime import datetime, timedelta
import pytz

TZ = pytz.timezone("America/Los_Angeles")

MONTHS_RU = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
]

def start_of_day(dt: datetime) -> datetime:
    return TZ.localize(datetime(dt.year, dt.month, dt.day))


def format_delta_hm(delta: timedelta) -> tuple[int, int]:
    seconds = int(delta.total_seconds())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return hours, minutes