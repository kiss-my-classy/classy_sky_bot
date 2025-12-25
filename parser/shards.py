from datetime import datetime, timedelta
from .time_utils import TZ, start_of_day, format_delta_hm, MONTHS_RU, LOCATIONS

LAND_OFFSET = timedelta(minutes=8, seconds=40)
END_OFFSET = timedelta(hours=4)

BLACK_INTERVAL = timedelta(hours=8)
RED_INTERVAL = timedelta(hours=6)

SHARDS_INFO = [
    {"no_days": [6, 7], "interval": BLACK_INTERVAL, "offset": timedelta(hours=1, minutes=50), "color": "черного ⚫️"},
    {"no_days": [7, 1], "interval": BLACK_INTERVAL, "offset": timedelta(hours=2, minutes=10), "color": "черного ⚫️"},
    {"no_days": [1, 2], "interval": RED_INTERVAL,   "offset": timedelta(hours=7, minutes=40), "color": "красного 🔴"},
    {"no_days": [2, 3], "interval": RED_INTERVAL,   "offset": timedelta(hours=2, minutes=20), "color": "красного 🔴"},
    {"no_days": [3, 4], "interval": RED_INTERVAL,   "offset": timedelta(hours=3, minutes=30), "color": "красного 🔴"},
]

def get_shard_location(date: datetime) -> str:
    index = (date.day - 1) % 5
    return LOCATIONS[index]

def get_shard_status(days_ahead: int = 0) -> str | None:
    now = datetime.now(TZ)
    target = now + timedelta(days=days_ahead)
    today = start_of_day(target)

    day = today.day
    weekday = today.isoweekday()

    is_red = day % 2 == 1
    info_index = ((day - 1) // 2) % 3 + 2 if is_red else (day // 2) % 2
    info = SHARDS_INFO[info_index]

    if weekday in info["no_days"]:
        return None

    first_start = today + info["offset"]

    # DST fix как в luxon
    if weekday == 7 and today.dst() != first_start.dst():
        first_start += timedelta(hours=-1 if first_start.dst() else 1)

    for i in range(3):
        start = first_start + info["interval"] * i
        land = start + LAND_OFFSET
        end = start + END_OFFSET

        if days_ahead == 0:
            if land <= now < end:
                h, m = format_delta_hm(end - now)
                location = get_shard_location(today)
                return (
                    f"Осколок {info['color']} цвета "
                    f"закончится через 🕐 {h} ч {m} мин\n"
                    f"📍 Локация: {location}"
                )

            if now < land:
                h, m = format_delta_hm(land - now)
                location = get_shard_location(today)
                return (
                    f"Осколок {info['color']} цвета "
                    f"упадёт через 🕐 {h} ч {m} мин\n"
                    f"📍 Локация: {location}"
                )
        else:
            h, m = format_delta_hm(land - now)
            location = get_shard_location(today)
            return (
                f"Осколок {info['color']} цвета "
                f"упадёт через 🕐 {h} ч {m} мин\n"
                f"📍 Локация: {location}"
            )

    return None


def get_next_shard_info():
    now = datetime.now(TZ)

    for days in range(1, 8):
        target = now + timedelta(days=days)
        today = start_of_day(target)

        day = today.day
        month = MONTHS_RU[today.month - 1]
        weekday = today.isoweekday()

        is_red = day % 2 == 1
        info_index = ((day - 1) // 2) % 3 + 2 if is_red else (day // 2) % 2
        info = SHARDS_INFO[info_index]

        if weekday in info["no_days"]:
            continue

        location = get_shard_location(today)
        return info["color"], day, month, location
    
    return None