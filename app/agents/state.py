from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

"""
Состояние графа симулятора.

SimulatorState - единый словарь, который LangGraph передаёт между узлами.
Каждый узел читает из него нужные поля и возвращает dict с обновлениями.

Поле messages с редьюсером add_messages: LangGraph не перезаписывает список,
а ДОБАВЛЯЕТ в него новые сообщения - так копится история диалога.
"""

class SimulatorState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    system_prompt: str
    is_scam: bool
    user_verdict: str
    do_judge: bool
    verdict_correct: bool
    verdict_role: str
    verdict_flags: list[str]
    verdict_explanation: str