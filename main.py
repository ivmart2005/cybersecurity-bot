import asyncio

from app.ui.cli import run_simulator


if __name__ == "__main__":
    try:
        asyncio.run(run_simulator())
    except KeyboardInterrupt:
        print("\nВыход.")