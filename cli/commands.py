from __future__ import annotations

from enum import Enum


class Command(Enum):
    EXIT = "exit"
    HELP = "help"
    CLEAR = "clear"


class CommandHandler:
    """
    Handles built-in PromptForge commands.
    """

    @staticmethod
    def is_command(text: str) -> bool:

        return text.strip().lower() in {
            command.value
            for command in Command
        }

    @staticmethod
    def execute(command: str) -> bool:
        """
        Execute command.

        Returns
        -------
        bool
            True if CLI should continue.
            False if CLI should terminate.
        """

        command = command.strip().lower()

        if command == Command.EXIT.value:
            return False

        if command == Command.CLEAR.value:

            import os

            os.system(
                "cls" if os.name == "nt" else "clear"
            )

            return True

        if command == Command.HELP.value:

            print()

            print("Available Commands")
            print("------------------")
            print("help  - Show this help")
            print("clear - Clear terminal")
            print("exit  - Exit PromptForge")
            print()

            return True

        return True