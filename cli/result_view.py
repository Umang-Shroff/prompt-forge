from __future__ import annotations

from rich.panel import Panel
from rich.syntax import Syntax

from .console import console


class ResultView:
    """
    Displays the optimized prompt.
    """

    def show(
        self,
        optimized_prompt: str,
    ) -> None:

        syntax = Syntax(
            optimized_prompt,
            "markdown",
            line_numbers=False,
            word_wrap=True,
        )

        console.print()

        console.print(
            Panel(
                syntax,
                title="[bold green]Optimized Prompt[/bold green]",
                border_style="green",
                expand=True,
            )
        )

        console.print()