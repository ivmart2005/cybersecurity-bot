from langgraph.graph import END, START, StateGraph
from app.agents.chat_agent import chat_agent_node
from app.agents.judge_agent import judge_agent_node
from app.agents.state import SimulatorState
from app.memory.checkpointer import get_checkpointer


def _route(state: SimulatorState) -> str:
    if state.get("do_judge"):
        return "judge"
    return END

"""
Сборка LangGraph-графа симулятора.

Два узла: chat (диалог) и judge (анализ).
После chat граф либо завершается (диалог продолжается),
либо идёт в judge (пользователь ввёл /scam или /safe).

Граф завершается после каждого ответа, а не крутится в цикле.
Следующий ввод пользователя запускает новый graph.ainvoke с тем же
thread_id - MemorySaver берёт состояние.
"""

def build_graph():
    graph = StateGraph(SimulatorState)
    graph.add_node("chat", chat_agent_node)
    graph.add_node("judge", judge_agent_node)
    graph.add_edge(START, "chat")
    graph.add_conditional_edges("chat", _route, {"judge": "judge", END: END})
    graph.add_edge("judge", END)
    return graph.compile(checkpointer=get_checkpointer())