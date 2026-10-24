"""
Проект тренажёр кибербезопасности.

Папки:
    agents   - LangGraph-граф и узлы (chat, judge)
    services - бизнес-логика (чат, judge, сценарии)
    llm      - клиенты GigaChat и промпты
    rag      - BM25-поиск правил
    mcp      - подключение к MCP-серверу filesystem
    memory   - MemorySaver (краткосрочная память)
    domain   - доменные модели (Scenario, VerdictAnalysis)
    ui       - консольный интерфейс
    data     - security_patterns.txt и .last_scenario.txt
"""