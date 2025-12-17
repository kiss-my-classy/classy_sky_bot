from datetime import datetime
from .time_utils import TZ, MONTHS_RU
import os
import json

def list_daily() -> list[str]:
    """
    Возвращает ежедневные задания, если дата в DAILY_JSON совпадает с текущей датой Sky (TZ)
    """
    date = get_date()
    if date == "":
        return []

    today = datetime.now(TZ).date().isoformat()

    if date != today:
        return []
    
    return [
        task["text"]
        for task in get_tasks()
            if isinstance(task, dict) and "text" in task
    ]

def get_date() -> str:
    data = os.getenv("DAILY_JSON")
    if not data:
        return ""

    try:
        return data.get("date")
    except json.JSONDecodeError:
        return ""

    
def get_tasks() -> list[str]:
    data = os.getenv("DAILY_JSON")
    if not data:
        return []

    try:
        return data.get("tasks")
    except json.JSONDecodeError:
        return []