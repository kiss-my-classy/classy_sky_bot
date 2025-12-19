from datetime import datetime, timedelta
from .time_utils import TZ, start_of_day, MONTHS_RU, format_delta_hm
from .helper_fcn import load_json_from_env

# ================= константы =================

EVENT_TICKETS_PER_DAY = 5


# ================= загрузка =================

def load_event_config() -> dict:
    return load_json_from_env("EVENT_JSON")


# ================= даты =================

def parse_date(date_str: str) -> datetime:
    return start_of_day(TZ.localize(datetime.fromisoformat(date_str)))


def get_today() -> datetime:
    return start_of_day(datetime.now(TZ))


# ================= расчёт события =================

def calculate_event_progress() -> dict | None:
    config = load_event_config()
    events = config.get("events", [])

    if not events:
        return None

    now = datetime.now(TZ)
    today = get_today()

    for event in events:
        if not event.get("event_active", False):
            continue

        event_start = parse_date(event["event_start"])
        event_end = parse_date(event["event_end"])

        if today > event_end:
            continue

        # конец события — конец дня
        event_end_dt = TZ.localize(
            datetime(
                event_end.year,
                event_end.month,
                event_end.day,
                23, 59, 59
            )
        )

        time_left = event_end_dt - now
        if time_left.total_seconds() <= 0:
            continue

        days_left = time_left.days
        hours_left, _ = format_delta_hm(
            time_left - timedelta(days=days_left)
        )

        # считаем билеты
        tickets = 0
        current_day = max(today, event_start)

        while current_day <= event_end:
            tickets += EVENT_TICKETS_PER_DAY
            current_day += timedelta(days=1)

        return {
            "event_name": event.get("event_name", "Событие"),
            "days_left": days_left,
            "hours_left": hours_left,
            "tickets": tickets,
            "event_start": event_start,
            "event_end": event_end,
        }

    return None


# ================= форматирование =================

def format_ru_date(dt: datetime) -> str:
    day = f"{dt.day:02d}"
    month = MONTHS_RU[dt.month - 1]
    return f"{day} {month}"


def format_event_message(stats: dict | None) -> str:
    if stats is None:
        return ""

    return (
        f"🎉 {stats['event_name']}\n"
        f"📅 {format_ru_date(stats['event_start'])} — "
        f"{format_ru_date(stats['event_end'])}\n\n"
        f"До конца события осталось "
        f"{stats['days_left']} дней {stats['hours_left']} часов ⏳\n\n"
        f"🎟️ Билетов можно получить: {stats['tickets']}"
    )