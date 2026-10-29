# Тренажёр кибербезопасности

## Стек:
- Python
- фреймворк LangGraph
- модель обеих агентов GigaChat-3-Pro
- RAG, лексический поиск - BM25
- вызов готового MCP-сервера от Anthropic

## Демонстрация:
https://drive.google.com/file/d/1oituicyINw3jPUvrq3R1ciQuuy2mzXHf/view?usp=sharing




При желании запуска - создать .env файл:
GIGACHAT_CREDENTIALS=<base64 от client_id:client_secret>   -  айди и секрет на https://developers.sber.ru/studio
GIGACHAT_SCOPE=GIGACHAT_API_PERS
GIGACHAT_MODEL=GigaChat-3-Pro

Порядок команд:
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Запуск:
python main.py
