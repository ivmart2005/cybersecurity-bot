import re

from langchain_core.messages import AIMessage, BaseMessage

from app.domain.verdict import VerdictAnalysis
from app.llm.client import get_judge_llm
from app.llm.prompts import build_judge_prompt


def _format_history(messages: list[BaseMessage]) -> str:
    return "\n".join(
        f"{'Собеседник' if isinstance(m, AIMessage) else 'Пользователь'}: {m.content}"
        for m in messages[1:]
    )


def _parse_verdict(text: str) -> VerdictAnalysis | None:
    """Парсит ответ модели в формате CORRECT / ROLE / FLAGS / EXPLANATION."""
    correct_match = re.search(r"CORRECT\s*:\s*(true|false)", text, re.IGNORECASE)
    role_match = re.search(r"ROLE\s*:\s*(МОШЕННИК|БЕЗОПАСНО)", text, re.IGNORECASE)
    if not correct_match or not role_match:
        return None

    user_was_correct = correct_match.group(1).lower() == "true"
    true_role = role_match.group(1).upper()

    flags: list[str] = []
    flags_block = re.search(
        r"FLAGS\s*:\s*(.*?)(?:EXPLANATION\s*:|$)",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if flags_block:
        for line in flags_block.group(1).splitlines():
            line = line.strip().lstrip("-•*").strip()
            if not line:
                continue
            low = line.lower()
            if low in ("нет", "нет флагов", "отсутствуют", "не обнаружено"):
                continue
            if re.fullmatch(r"флаг\s*\d+", low):
                continue
            if "найденные красные флаги" in low:
                continue
            flags.append(line)

    explanation = ""
    explanation_block = re.search(
        r"EXPLANATION\s*:\s*(.*)$", text, re.DOTALL | re.IGNORECASE
    )
    if explanation_block:
        raw_explanation = explanation_block.group(1).strip()
        for stop_marker in (
            "\nНайденные красные флаги",
            "\nFLAGS:",
            "\nROLE:",
            "\nCORRECT:",
        ):
            idx = raw_explanation.find(stop_marker)
            if idx != -1:
                raw_explanation = raw_explanation[:idx]
        raw_explanation = re.sub(r"\n\s*НЕТ\s*$", "", raw_explanation, flags=re.IGNORECASE)
        explanation = raw_explanation.strip()

    return VerdictAnalysis(
        user_was_correct=user_was_correct,
        true_role=true_role,
        red_flags_found=flags,
        explanation=explanation,
    )

async def analyze_dialogue(
    messages: list[BaseMessage],
    is_scam: bool,
    user_verdict: str,
    security_db: str,
    retries: int = 2,
) -> VerdictAnalysis:
    history_text = _format_history(messages)
    judge_prompt = build_judge_prompt(
        history_text=history_text,
        is_scam=is_scam,
        user_verdict=user_verdict,
        security_db=security_db,
    )

    llm = get_judge_llm()
    last_error: Exception | None = None

    for attempt in range(retries + 1):
        try:
            response = await llm.ainvoke(judge_prompt)
            text = str(response.content).strip()

            parsed = _parse_verdict(text)
            if parsed is not None:
                return parsed

            last_error = ValueError(
                f"Не удалось распарсить ответ судьи:\n{text[:300]}"
            )
        except Exception as e:
            last_error = e

        if attempt < retries:
            print(f"Судья ответил не по формату, retry {attempt + 1}/{retries}...")

    raise RuntimeError(
        f"Судья не смог вернуть корректный результат: {last_error}"
    )