import uuid

from langchain_core.messages import HumanMessage

from app.agents.graph import build_graph
from app.config import ConfigError
from app.llm.client import get_chat_llm
from app.llm.prompts import build_system_prompt
from app.services.chat_service import ModelUnavailableError
from app.services.scenario_service import pick_random_scenario


def _print_banner() -> None:
    print("\n==================================================")
    print("ТРЕНАЖЁР КИБЕРБЕЗОПАСНОСТИ")
    print("==================================================")
    print("Инструкция:")
    print("1. Задавайте вопросы собеседнику.")
    print("2. Введите /scam (Мошенник) или /safe (Безопасно) для проверки.")
    print("3. Введите 'exit' для выхода.")
    print("==================================================\n")


def _print_analysis(
    verdict_correct: bool,
    role: str,
    flags: list[str],
    explanation: str,
) -> None:
    print("==================================================")
    print("РЕЗУЛЬТАТЫ РАЗБОРА")
    print("==================================================")
    print("ВЕРНО!" if verdict_correct else "ОШИБКА! Вы ошиблись.")
    print(f"\nКем являлся собеседник: {role}")
    print(f"Объяснение: {explanation}")
    if flags:
        print("\nНайденные красные флаги:")
        for flag in flags:
            print(f" - {flag}")
    print("==================================================\n")


async def run_simulator() -> None:
    try:
        llm = get_chat_llm()
        model_name = getattr(llm, "model", None) or getattr(llm, "model_name", "unknown")

        _print_banner()

        scenario = pick_random_scenario()
        print(f"Сценарий: {scenario.topic}")
        print(f"Роль бота: {scenario.role}\n")

        system_prompt = build_system_prompt(scenario)
        graph = build_graph()
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}

        init_state = {
            "messages": [
                HumanMessage(
                    content="(Начни диалог. Напиши первое короткое сообщение.)"
                )
            ],
            "system_prompt": system_prompt,
            "is_scam": scenario.is_scam,
            "user_verdict": "",
            "do_judge": False,
            "verdict_correct": False,
            "verdict_role": "",
            "verdict_flags": [],
            "verdict_explanation": "",
        }

        result = await graph.ainvoke(init_state, config=config)
        print(f"Собеседник: {result['messages'][-1].content}")

        while True:
            try:
                print("\nВы: ", end="")
                user_input = input().strip()
            except (KeyboardInterrupt, EOFError):
                break

            if not user_input:
                continue
            if user_input.lower() == "exit":
                break

            if user_input.lower() in ["/scam", "/safe"]:
                user_verdict = (
                    "МОШЕННИК" if user_input.lower() == "/scam" else "БЕЗОПАСНО"
                )
                print("\n[Анализ вердикта...]\n")
                result = await graph.ainvoke(
                    {"do_judge": True, "user_verdict": user_verdict},
                    config=config,
                )
                _print_analysis(
                    result["verdict_correct"],
                    result["verdict_role"],
                    result["verdict_flags"],
                    result["verdict_explanation"],
                )
                break

            result = await graph.ainvoke(
                {"messages": [HumanMessage(content=user_input)], "do_judge": False},
                config=config,
            )
            print(f"Собеседник: {result['messages'][-1].content}")

    except ConfigError as e:
        print(f"ОШИБКА КОНФИГУРАЦИИ: {e}")
    except ModelUnavailableError as e:
        print(f"МОДЕЛЬ НЕДОСТУПНА: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e.__class__.__name__}: {e}")
        raise