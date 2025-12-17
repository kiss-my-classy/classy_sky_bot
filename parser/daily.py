from datetime import datetime
from .time_utils import TZ
import os
import json

def get_data() -> dict:
    raw = os.getenv("DAILY_JSON")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}

def get_date() -> str:
    return get_data().get("date", "")

def get_tasks() -> list[dict]:
    return get_data().get("tasks", [])

def list_daily() -> list[str]:
    """
    Возвращает ежедневные задания, если дата в DAILY_JSON совпадает с текущей датой Sky (TZ)
    """
    date = get_date()
    if not date:
        return []

    today = datetime.now(TZ).date().isoformat()

    if date != today:
        return []

    return [
        task["text"]
        for task in get_tasks()
        if isinstance(task, dict) and "text" in task
    ]