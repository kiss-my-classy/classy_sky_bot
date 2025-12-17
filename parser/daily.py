from datetime import datetime
from .time_utils import TZ, MONTHS_RU


def format_daily(data: dict) -> list[str]:
    """
    Возвращает ежедневные задания из переданного словаря data,
    если дата совпадает с текущей датой Sky (America/Los_Angeles).
    """
    if not data:
        return []

    today_dt = datetime.now(TZ)
    today = today_dt.date().isoformat()

    if data.get("date") != today:
        return []

    day = today_dt.day
    month = MONTHS_RU[today_dt.month - 1]

    result = [f"🗓️ {day} {month}\n"]

    result.extend(
        task["text"]
        for task in data.get("tasks", [])
        if isinstance(task, dict) and "text" in task
    )

    return result