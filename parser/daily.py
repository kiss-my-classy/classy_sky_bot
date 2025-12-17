from datetime import datetime
from .time_utils import TZ

def format_daily(data: dict) -> list[str]:
    """
    Возвращает ежедневные задания из переданного словаря data,
    если дата совпадает с текущей датой Sky (America/Los_Angeles).
    """
    if not data:
        return []

    today = datetime.now(TZ).date().isoformat()

    if data.get("date") != today:
        return []

    return [
        task["text"]
        for task in data.get("tasks", [])
        if isinstance(task, dict) and "text" in task
    ]