from dataclasses import dataclass

from app.config import DATA_DIR

"""
Загрузка базы правил и разбивка на чанки.
"""

@dataclass(frozen=True)
class RuleChunk:
    section: str
    text: str

    @property
    def full_text(self) -> str:
        return f"[{self.section}] {self.text}"


def load_pattern_chunks() -> list[RuleChunk]:
    """Читает security_patterns.txt и режет на чанки-правила."""
    path = DATA_DIR / "security_patterns.txt"
    text = path.read_text(encoding="utf-8")

    chunks: list[RuleChunk] = []
    current_section = ""

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.endswith(":") and not line[0].isdigit():
            current_section = line.rstrip(":").strip()
            continue

        chunks.append(RuleChunk(section=current_section, text=line))

    return chunks