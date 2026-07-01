from rich.panel import Panel
from rich.align import Align

from .console import console


def show_header() -> None:

    console.print()

    console.print(
        Panel(
            Align.center(
                "[title]PromptForge v1.0[/title]\n"
                "[subtitle]AI Prompt Optimization Toolkit[/subtitle]"
            ),
            expand=False,
            border_style="cyan",
        )
    )

    console.print()