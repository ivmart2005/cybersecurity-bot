import random

from app.config import DATA_DIR
from app.constants import SCENARIOS
from app.domain.models import Scenario


_LAST_SCENARIO_FILE = DATA_DIR / ".last_scenario.txt"


def load_security_patterns() -> str:
    pattern_file = DATA_DIR / "security_patterns.txt"
    if pattern_file.exists():
        with open(pattern_file, "r", encoding="utf-8") as f:
            return f.read()
    return "Стандартные правила кибербезопасности."


def _read_last_topic() -> str | None:
    """Читает topic последнего выпавшего сценария (для защиты от повтора)."""
    if not _LAST_SCENARIO_FILE.exists():
        return None
    try:
        return _LAST_SCENARIO_FILE.read_text(encoding="utf-8").strip() or None
    except OSError:
        return None


def _write_last_topic(topic: str) -> None:
    try:
        _LAST_SCENARIO_FILE.write_text(topic, encoding="utf-8")
    except OSError:
        pass


def pick_random_scenario() -> Scenario:
    """
    Выбирает случайный сценарий, стараясь не повторять предыдущий.
    Если все сценарии кроме предыдущего исчерпаны — сбрасывает историю.
    """
    last_topic = _read_last_topic()

    candidates = [s for s in SCENARIOS if s.topic != last_topic]
    if not candidates:
        candidates = list(SCENARIOS)

    scenario = random.choice(candidates)
    _write_last_topic(scenario.topic)
    return scenario