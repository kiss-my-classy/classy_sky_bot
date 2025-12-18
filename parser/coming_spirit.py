from datetime import datetime
from .time_utils import TZ, format_delta_hm
from .helper_fcn import load_json_from_env


def load_spirit_config() -> dict:
    return load_json_from_env("SPIRIT_JSON")


def get_spirits() -> list[dict]:
    return load_spirit_config().get("spirits", [])


def format_spirits_message() -> str:
    """
    Формирует сообщение о странствующих духах:
    - имя и даты прихода
    - если дух уже пришёл — сколько времени осталось до ухода
    - если информации нет — пустая строка
    """
    spirits = get_spirits()
    if not spirits:
        return ""

    now = datetime.now(TZ)

    for spirit in spirits:
        if not isinstance(spirit, dict):
            continue

        name = spirit.get("name")
        start_raw = spirit.get("start")
        end_raw = spirit.get("end")

        if not name or not start_raw or not end_raw:
            continue

        try:
            start = TZ.localize(datetime.fromisoformat(start_raw))
            end = TZ.localize(datetime.fromisoformat(end_raw))
        except ValueError:
            continue

        # дух ещё не пришёл
        if now < start:
            return (
                f"🕺 **{name}**\n"
                f"📅 {start.strftime('%d.%m %H:%M')} — {end.strftime('%d.%m %H:%M')}"
            )

        # дух уже активен
        if start <= now < end:
            delta = end - now
            hours, minutes = format_delta_hm(delta)

            return (
                f"🕺 **{name}**\n"
                f"⏳ Осталось: {hours} ч {minutes} мин"
            )

    return ""