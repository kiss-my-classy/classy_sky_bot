from datetime import datetime, timedelta
from .time_utils import TZ, format_delta_hm

EVENTS = {
    "🌋 Гейзер": (5, 15),
    "👵 Бабушка": (35, 45),
    "🐢 Черепаха": (50, 60),
}


def get_next_event_time(start_min: int, end_min: int):
    now = datetime.now(TZ)
    hour = now.hour
    minute = now.minute

    def make_time(base, hour_offset, minute):
        t = base.replace(
            hour=(base.hour + hour_offset) % 24,
            minute=minute % 60,
            second=0,
            microsecond=0
        )
        if base.hour + hour_offset >= 24:
            t += timedelta(days=1)
        return t

    # чётный час — возможен ивент
    if hour % 2 == 0:
        # активен
        if start_min <= minute < end_min:
            if end_min == 60:
                end_time = make_time(now, 1, 0)
            else:
                end_time = now.replace(minute=end_min, second=0, microsecond=0)

            return "active", end_time - now

        # ещё не начался
        if minute < start_min:
            start_time = now.replace(minute=start_min, second=0, microsecond=0)
            return "future", start_time - now

    # ищем следующий чётный час
    next_hour = hour + 1
    while next_hour % 2 != 0:
        next_hour += 1

    start_time = now.replace(
        hour=next_hour % 24,
        minute=start_min,
        second=0,
        microsecond=0
    )

    if next_hour >= 24:
        start_time += timedelta(days=1)

    return "future", start_time - now


def get_events():
    result = []

    for name, (start, end) in EVENTS.items():
        status, delta = get_next_event_time(start, end)
        h, m = format_delta_hm(delta)

        if status == "active":
            result.append(f"{name} закончится через 🕐 {m} мин")
        else:
            result.append(f"{name} через 🕐 {h} ч {m} мин")

    return result