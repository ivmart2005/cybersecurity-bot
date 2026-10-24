from langchain_core.messages import AIMessage, SystemMessage

from app.agents.state import SimulatorState
from app.services.chat_service import get_bot_response

"""
Узел диалога: бот отвечает пользователю в роли.

Узел только
1. Проверяет, не пора ли уходить в judge.
2. Комбинирует системный промпт + историю.
3. Вызывает сервис и кладёт ответ бота в state.
"""

async def chat_agent_node(state: SimulatorState) -> dict:
    if state.get("do_judge"):
        return {}
    messages = [SystemMessage(content=state["system_prompt"])] + state["messages"]
    bot_text = await get_bot_response(messages)
    return {"messages": [AIMessage(content=bot_text)]}