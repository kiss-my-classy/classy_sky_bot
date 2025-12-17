import json
import os
from datetime import datetime

from .time_utils import TZ


def format_daily() -> list[str]:
    raw = os.getenv("DAILY_JSON")
    if not raw:
        return []

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []

    today = datetime.now(TZ).date().isoformat()
    print("Sky today:", today.isoformat())
    print("JSON date:", data.get("date"))


    if data.get("date") != today:
        return []

    return [
        task["text"]
        for task in data.get("tasks", [])
        if isinstance(task, dict) and "text" in task
    ]