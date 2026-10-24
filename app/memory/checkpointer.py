from functools import lru_cache

from langgraph.checkpoint.memory import MemorySaver

"""
Checkpointer - механизм LangGraph для сохранения состояния графа.

MemorySaver хранит состояние в памяти процесса по thread_id.
Каждый graph.ainvoke с тем же thread_id подхватывает предыдущее состояние -
так работает память диалога: chat_agent видит всю историю, а не только
последнюю реплику.

lru_cache(maxsize=1) - один MemorySaver на процесс, иначе каждый build_graph()
создавал бы новый и память бы терялась.
"""

@lru_cache(maxsize=1)
def get_checkpointer() -> MemorySaver:
    return MemorySaver()