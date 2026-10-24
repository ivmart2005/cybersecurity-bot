import re
from functools import lru_cache

from rank_bm25 import BM25Okapi

from app.rag.indexer import RuleChunk, load_pattern_chunks


"""
BM25-поиск релевантных правил по тексту диалога.

BM25 - лексический алгоритм: ищет по совпадению слов, без эмбеддингов.
Для 22 коротких правил работает точнее и быстрее векторного поиска.

SYNONYMS - расширение запроса синонимами. BM25 ищет по буквальным словам,
а пользователь может написать "торопят" вместо "срочность". Синонимы
помогают найти нужное правило, даже если слова не совпадают буквально.

Пример: запрос "Просят код из СМС, торопят, грозят блокировкой"
         -> расширяется до "... срочность спешка давление угроза блокировка ..."
         -> BM25 находит правила про код из СМС, срочность и угрозы.
"""

SYNONYMS = {
    "торопят": "срочность срочно спешка давление",
    "торопит": "срочность срочно спешка давление",
    "срочно": "срочность спешка давление",
    "грозят": "угроза угрозы блокировка давление",
    "грозит": "угроза угрозы блокировка давление",
    "блокировк": "блокировка угроза давление",
    "код": "код смс подтверждение",
    "смс": "смс код подтверждение push",
    "перевод": "перевод деньги счёт средства",
    "деньг": "деньги средства счёт перевод",
    "ссылк": "ссылка домен сайт переход",
    "карт": "карта cvv данные реквизиты",
    "пароль": "пароль логин данные",
    "банк": "банк служба безопасность сотрудник",
    "директор": "директор руководитель начальник",
    "коллег": "коллега работа документ",
}


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def _expand_query(query: str) -> str:
    query_low = query.lower()
    extras: list[str] = []
    for key, syn in SYNONYMS.items():
        if key in query_low:
            extras.append(syn)
    if extras:
        return query + " " + " ".join(extras)
    return query


@lru_cache(maxsize=1)
def _get_index() -> tuple[BM25Okapi, list[RuleChunk]]:
    chunks = load_pattern_chunks()
    tokenized = [_tokenize(c.full_text) for c in chunks]
    bm25 = BM25Okapi(tokenized)
    return bm25, chunks


def retrieve_security_rules(query: str, k: int = 6) -> str:
    if not query.strip():
        return ""

    bm25, chunks = _get_index()
    expanded = _expand_query(query)
    tokens = _tokenize(expanded)
    if not tokens:
        return ""

    scores = bm25.get_scores(tokens)
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

    selected: list[RuleChunk] = []
    for i in ranked:
        if len(selected) >= k:
            break
        if scores[i] > 0:
            selected.append(chunks[i])

    if not selected:
        return ""

    return "\n".join(f"- {c.full_text}" for c in selected)