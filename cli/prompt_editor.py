from __future__ import annotations

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.processors import HighlightSelectionProcessor
from prompt_toolkit.styles import Style

from models import OptimizationMode


class PromptEditor:
    """
    Multiline prompt editor.

    Ctrl + Enter submits the prompt.
    """

    def __init__(self) -> None:

        self._bindings = KeyBindings()

        @self._bindings.add("c-m")
        def _(event) -> None:
            """
            Ctrl + Enter
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

    def get_prompt(
        self,
        mode: OptimizationMode,
    ) -> str:
        """
        Returns the prompt entered by the user.

        Parameters
        ----------
        mode:
            Current optimization mode.

        Returns
        -------
        str
            Prompt entered by the user.
        """

        print()

        print(f"Current Mode : {mode.name.title()}")

        print("Type 'exit' to quit.")

        print("Press Ctrl + Enter to optimize prompt.")

        print()

        while True:

            text = self._session.prompt(
                "$promptForge: ",
            )

            text = text.strip()

            if text:

                return text