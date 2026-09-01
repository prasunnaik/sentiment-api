from __future__ import annotations

import sys

from .assistant import AegisAssistant
from .config import ConfigurationError, load_settings


def main() -> int:
    try:
        settings = load_settings()
        assistant = AegisAssistant(settings)
    except ConfigurationError as exc:
        print(f"Configuration error: {exc}")
        return 2
    except Exception as exc:
        print(f"Startup error: {exc}")
        return 2

    print("Aegis Research Assistant")
    print("Type 'exit' or 'quit' to save memory and leave.")

    try:
        while True:
            try:
                user_input = input("\nYou: ").strip()
            except EOFError:
                user_input = "exit"
            if user_input.lower() in {"exit", "quit"}:
                assistant.save()
                print("Memory persisted. Goodbye.")
                return 0
            try:
                print(f"Aegis: {assistant.handle(user_input)}")
            except Exception as exc:
                # FR-5/FR-8: readable failure instead of an unhandled exception.
                print(f"Aegis: I could not complete that request safely: {exc}")
    except KeyboardInterrupt:
        assistant.save()
        print("\nMemory persisted. Goodbye.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
