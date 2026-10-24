from functools import lru_cache

from langchain_gigachat.chat_models import GigaChat

from app.config import (
    get_forced_model,
    get_gigachat_credentials,
    get_gigachat_scope,
)

"""
Создание клиентов GigaChat.

Два клиента:
- chat_llm  - для диалога (temperature 0.3, до 500 токенов);
- judge_llm - для анализа (temperature 0.1, до 1500 токенов).

lru_cache(maxsize=1) - клиент создаётся один раз и переиспользуется.
verify_ssl_certs=False - у GigaChat сертификат Минцифры, которого нет
в стандартном наборе Python (иначе SSLError).
"""

DEFAULT_MODEL = "GigaChat"


def select_model() -> str:
    return get_forced_model() or DEFAULT_MODEL


def _make_llm(temperature: float, max_tokens: int) -> GigaChat:
    return GigaChat(
        credentials=get_gigachat_credentials(),
        scope=get_gigachat_scope(),
        model=select_model(),
        temperature=temperature,
        max_tokens=max_tokens,
        verify_ssl_certs=False,
        timeout=200,
    )


@lru_cache(maxsize=1)
def get_chat_llm() -> GigaChat:
    return _make_llm(temperature=0.3, max_tokens=500)


@lru_cache(maxsize=1)
def get_judge_llm() -> GigaChat:
    return _make_llm(temperature=0.1, max_tokens=1500)