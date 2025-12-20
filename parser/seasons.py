from datetime import datetime, timedelta
from .time_utils import TZ, start_of_day, MONTHS_RU, format_delta_hm
from .helper_fcn import load_json_from_env


CANDLES_NO_PASS = 5
CANDLES_WITH_PASS = 6

CANDLES_NO_PASS_DOUBLE = 6
CANDLES_WITH_PASS_DOUBLE = 7


def load_season_config() -> dict:
    return load_json_from_env("SEASON_JSON")

# ================= даты =================

def parse_date(date_str: str) -> datetime:
    return start_of_day(TZ.localize(datetime.fromisoformat(date_str)))


def get_today() -> datetime:
    return start_of_day(datetime.now(TZ))


# ================= удвоения =================

def build_double_days(double_events: list[dict]) -> set[datetime]:
    double_days = set()

    for event in double_events:
        start = parse_date(event["start"])
        end = parse_date(event["end"])

        current = start
        while current <= end:
            double_days.add(current)
            current += timedelta(days=1)

    return double_days


def get_next_double_event(
    double_events: list[dict],
    today: datetime
) -> tuple[datetime, datetime] | None:
    future_events = []

    for event in double_events:
        start = parse_date(event["start"])
        end = parse_date(event["end"])

        if end >= today:
            future_events.append((start, end))

    if not future_events:
        return None

    future_events.sort(key=lambda e: e[0])
    return future_events[0]


# ================= расчёт сезона =================

def calculate_season_progress() -> dict | None:
    config = load_season_config()

    if not config.get("season_active", False):
        return None

    now = datetime.now(TZ)
    today = start_of_day(now)

    season_start = parse_date(config["season_start"])
    season_end = parse_date(config["season_end"])

    if today > season_end:
        return None

    # конец сезона — конец дня
    season_end_dt = TZ.localize(
        datetime(
            season_end.year,
            season_end.month,
            season_end.day,
            23, 59, 59
        )
    )

    time_left = season_end_dt - now
    if time_left.total_seconds() <= 0:
        return None

    days_left = time_left.days
    hours_left, _ = format_delta_hm(
        time_left - timedelta(days=days_left)
    )

    double_events = config.get("double_events", [])
    double_days = build_double_days(double_events)

    candles_no_pass = 0
    candles_with_pass = 0

    current_day = max(today, season_start)

    while current_day <= season_end:
        if current_day in double_days:
            candles_no_pass += CANDLES_NO_PASS_DOUBLE
            candles_with_pass += CANDLES_WITH_PASS_DOUBLE
        else:
            candles_no_pass += CANDLES_NO_PASS
            candles_with_pass += CANDLES_WITH_PASS

        current_day += timedelta(days=1)

    next_double = get_next_double_event(double_events, today)

    return {
        "season_name": config.get("season_name", "Без названия"),
        "days_left": days_left,
        "hours_left": hours_left,
        "candles_no_pass": candles_no_pass,
        "candles_with_pass": candles_with_pass,
        "next_double": next_double,
    }


# ================= форматирование =================

def format_ru_date(dt: datetime) -> str:
    day = f"{dt.day:02d}"
    month = MONTHS_RU[dt.month - 1]
    return f"{day} {month}"


def format_season_message(stats: dict | None) -> str:
    if stats is None:
        return ""

    text = (
        f"{stats['season_name']}\n"
        f"До конца сезона осталось "
        f"{stats['days_left']} дней {stats['hours_left']} часов 🗓️\n\n"
        f"Сезонных свечей осталось:\n"
        f"🔹 {stats['candles_no_pass']} без сезонного пропуска\n"
        f"🔸 {stats['candles_with_pass']} с сезонным пропуском\n"
    )

    next_double = stats.get("next_double")
    if next_double:
        start, end = next_double
        text += (
            f"\n🔥 Ближайшее удвоение:\n"
            f"с {format_ru_date(start)} по {format_ru_date(end)}"
        )

    return text