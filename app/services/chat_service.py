import asyncio

import httpx
from langchain_core.messages import BaseMessage

from app.llm.client import get_chat_llm

"""
Вызов chat-модели с retry и обработкой ошибок.
"""

class ModelUnavailableError(RuntimeError):
    """Модель недоступна текущему ключу (403)."""


async def get_bot_response(messages: list[BaseMessage], retries: int = 2) -> str:
    llm = get_chat_llm()
    last_err: Exception | None = None

    for attempt in range(retries + 1):
        try:
            response = await llm.ainvoke(messages)
            text = str(response.content).strip()

            if not text:
                if attempt < retries:
                    print(f"Пустой ответ, retry {attempt + 1}/{retries}...")
                    await asyncio.sleep(1)
                    continue
                return "Извините, связь прервалась. Повторите вопрос."

            return text

        except Exception as e:
            last_err = e
            err_str = str(e)
            if "403" in err_str or "Forbidden" in err_str:
                raise ModelUnavailableError(
                    "Модель недоступна (403). "
                ) from e

            is_timeout = isinstance(e, httpx.TimeoutException)
            is_rate = "429" in err_str

            if attempt < retries and (is_timeout or is_rate):
                print(f"{e.__class__.__name__}, retry {attempt + 1}/{retries}...")
                await asyncio.sleep(2 * (attempt + 1))
                continue
            raise

    raise last_err