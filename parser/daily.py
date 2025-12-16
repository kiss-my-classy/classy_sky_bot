import json
from pathlib import Path

from .time_utils import TZ
from datetime import datetime

# путь к data/daily.json относительно ЭТОГО файла
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "daily.json"


def format_daily() -> list[str]:
    """
    Возвращает ежедневные задания,
    если дата в daily.json совпадает с текущей датой Sky
    (America/Los_Angeles)
    """
    if not DATA_PATH.exists():
        return []

    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return []

    # текущая дата в America/Los_Angeles
    today = datetime.now(TZ).date().isoformat()

    if data.get("date") != today:
        return []

    return [task["text"] for task in data.get("tasks", []) if "text" in task]
