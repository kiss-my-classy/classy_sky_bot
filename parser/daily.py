import json
import os
from datetime import datetime
import logging
from datetime import datetime, timedelta
from .time_utils import TZ

logger = logging.getLogger(__name__)


def format_daily() -> list[str]:
    raw = os.getenv("DAILY_JSON")
    if not raw:
        return []

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []

    today = datetime.now(TZ).date().isoformat()
    logger.info("Sky today: %s", today.isoformat())
    logger.info("Sky yesterday: %s", yesterday.isoformat())
    logger.info("JSON date: %s", data.get("date"))

    if data.get("date") != today:
        return []

    return [
        task["text"]
        for task in data.get("tasks", [])
        if isinstance(task, dict) and "text" in task
    ]