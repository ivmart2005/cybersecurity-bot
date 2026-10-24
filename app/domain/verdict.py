from dataclasses import dataclass, field

"""
Результат анализа диалога.

VerdictAnalysis - то, что возвращает judge после разбора:
правильно ли пользователь угадал, кем был бот, какие флаги нашёл, и обучающее объяснение.
"""

@dataclass
class VerdictAnalysis:
    user_was_correct: bool
    true_role: str
    red_flags_found: list[str] = field(default_factory=list)
    explanation: str = ""