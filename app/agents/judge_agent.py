from langchain_core.messages import AIMessage, BaseMessage

from app.agents.state import SimulatorState
from app.rag.retriever import retrieve_security_rules
from app.services.judge_service import analyze_dialogue
from app.mcp.client import read_security_patterns_via_mcp 


def _history_text(messages: list[BaseMessage]) -> str:
    return "\n".join(
        f"{'Собеседник' if isinstance(m, AIMessage) else 'Пользователь'}: {m.content}"
        for m in messages[1:]
    )

"""
Узел анализа: judge выносит вердикт по диалогу.

Порядок действий:
1. MCP - вызов существующего MCP-сервера (filesystem) для чтения базы правил.
2. RAG - BM25-поиск релевантных правил по истории диалога.
3. LLM - judge-модель анализирует диалог с учётом найденных правил.

"""

async def judge_agent_node(state: SimulatorState) -> dict:
    history = _history_text(state["messages"])

    # MCP
    try:
        full_rules = await read_security_patterns_via_mcp()
        print(f"MCP: security_patterns.txt прочитан ({len(full_rules)} символов)")
    except Exception as e:
        print(f"MCP недоступен ({e}), RAG работает без него")
        full_rules = ""

    # RAG
    try:
        security_db = retrieve_security_rules(history, k=6)
        if security_db:
            print(f"RAG: найдено {security_db.count('- ')} правил для judge")
    except Exception as e:
        print(f"RAG недоступен ({e})")
        security_db = ""

    analysis = await analyze_dialogue(
        messages=state["messages"],
        is_scam=state["is_scam"],
        user_verdict=state["user_verdict"],
        security_db=security_db,
    )
    return {
        "verdict_correct": analysis.user_was_correct,
        "verdict_role": analysis.true_role,
        "verdict_flags": analysis.red_flags_found,
        "verdict_explanation": analysis.explanation,
    }