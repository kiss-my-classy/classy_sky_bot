from datetime import datetime
from .time_utils import TZ
from .helper_fcn import load_json_from_env

def load_daily_config() -> dict:
    return load_json_from_env("DAILY_JSON")

def get_date() -> str:
    return load_daily_config().get("date", "")

def get_tasks() -> list[dict]:
    return load_daily_config().get("tasks", [])

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