from __future__ import annotations

import questionary

from models import OptimizationMode


class ModeSelector:
    """
    Interactive optimization mode selector.
    """

    def __init__(self) -> None:

        self._choices = {
            OptimizationMode.CONSERVATIVE: questionary.Choice(
                title="Conservative",
                value=OptimizationMode.CONSERVATIVE,
            ),
            OptimizationMode.BALANCED: questionary.Choice(
                title="Balanced",
                value=OptimizationMode.BALANCED,
            ),
            OptimizationMode.AGGRESSIVE: questionary.Choice(
                title="Aggressive",
                value=OptimizationMode.AGGRESSIVE,
            ),
        }

    def select(
        self,
        default: OptimizationMode,
    ) -> OptimizationMode:

        ordered_choices = [
            self._choices[default],
            *[
                choice
                for mode, choice in self._choices.items()
                if mode != default
            ],
        ]

        result = questionary.select(
            "Select Optimization Mode",
            choices=ordered_choices,
            use_indicator=True,
        ).ask()

        if result is None:
            return default

        return result