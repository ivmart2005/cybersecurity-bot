from dataclasses import dataclass
from enum import Enum

"""
Модели сценариев.

ScenarioType - тип сценария: SCAM (мошенник) или SAFE (безопасный).
Scenario - один сценарий: тема, роль бота, цель, тип.
"""

class ScenarioType(str, Enum):
    SCAM = "SCAM"
    SAFE = "SAFE"


@dataclass(frozen=True)
class Scenario:
    type: ScenarioType
    topic: str
    role: str
    goal: str

    @property
    def is_scam(self) -> bool:
        return self.type is ScenarioType.SCAM