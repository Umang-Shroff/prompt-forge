from __future__ import annotations

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.processors import HighlightSelectionProcessor
from prompt_toolkit.styles import Style

from models import OptimizationMode


class PromptEditor:
    """
    Multiline prompt editor.

    Ctrl + D submits the prompt.
    """

    def __init__(self) -> None:

        self._bindings = KeyBindings()

        @self._bindings.add("c-d")
        def _(event) -> None:
            """
            Ctrl + D
            """
            event.app.exit(
                result=event.app.current_buffer.text,
            )

        self._style = Style.from_dict(
            {
                "prompt": "#00d7ff bold",
            }
        )

        self._session = PromptSession(
            multiline=True,
            key_bindings=self._bindings,
            style=self._style,
            input_processors=[
                HighlightSelectionProcessor(),
            ],
        )

    def get_prompt(self, mode: OptimizationMode) -> str:
        print()

        print(f"Current Mode : {mode.name.title()}")
        print("Type 'exit' to quit.")
        print("Press Ctrl + D to optimize prompt.")
        print()

        while True:

            text = self._session.prompt(
                "$promptForge: ",
            ).strip()

            if text.lower() == "exit":
                raise SystemExit

            if text.lower() == "clear":
                import os
                os.system("cls" if os.name == "nt" else "clear")
                continue

            if text.lower() == "help":
                print()
                print("Available Commands")
                print("------------------")
                print("help  - Show this help")
                print("clear - Clear terminal")
                print("exit  - Exit PromptForge")
                print()
                continue

            if text:
                return text