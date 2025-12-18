import os
import json


def load_json_from_env(env_name: str) -> dict:
    """
    Загружает JSON из переменной окружения.
    Если переменная не задана или содержит некорректный JSON,
    возвращает пустой словарь.
    """
    raw = os.getenv(env_name)
    if not raw:
        return {}

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}