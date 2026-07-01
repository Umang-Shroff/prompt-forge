from __future__ import annotations

import questionary

from models import OptimizationMode


class ModeSelector:
    """
    Interactive optimization mode selector.

    Uses arrow keys for navigation and Enter to confirm.
    """

    _CHOICES = [
        questionary.Choice(
            title="Conservative",
            value=OptimizationMode.CONSERVATIVE,
        ),
        questionary.Choice(
            title="Balanced",
            value=OptimizationMode.BALANCED,
        ),
        questionary.Choice(
            title="Aggressive",
            value=OptimizationMode.AGGRESSIVE,
        ),
    ]

    def select(
        self,
        default: OptimizationMode,
    ) -> OptimizationMode:
        """
        Display the optimization mode selector.

        Parameters
        ----------
        default:
            Previously selected mode.

        Returns
        -------
        OptimizationMode
        """

        result = questionary.select(
            "Select Optimization Mode",
            choices=self._CHOICES,
            default=default.name.capitalize(),
            use_indicator=True,
        ).ask()

        if result is None:
            return default

        return result