from __future__ import annotations

from statistics import mode
import time

from models import OptimizationMode

from service import PromptOptimizer

from .commands import CommandHandler
from .header import show_header
from .mode_selector import ModeSelector
from .prompt_editor import PromptEditor
from .result_view import ResultView
from .summary import SummaryView
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live

console = Console()

spinner = Spinner(
    "dots",
    text="[cyan]Optimizing Prompt[/cyan]",
)


class PromptForgeApp:
    """
    Main PromptForge CLI runtime.
    """

    def __init__(self) -> None:

        self._optimizer = PromptOptimizer()

        self._editor = PromptEditor()

        self._selector = ModeSelector()

        self._result = ResultView()

        self._summary = SummaryView()

        self._mode = OptimizationMode.BALANCED

    def run(self) -> None:

        show_header()
        

        while True:

            # ----------------------------
            # 1. Get prompt input
            # ----------------------------
            prompt = self._editor.get_prompt(self._mode)

            if CommandHandler.is_command(prompt):

                if not CommandHandler.execute(prompt):
                    break

                continue

            # ----------------------------
            # 2. Select mode
            # ----------------------------
            mode = self._selector.select(self._mode)

            self._mode = mode

            # ----------------------------
            # 3. Run optimization
            # ----------------------------
            console.print(
                "[cyan]▶[/cyan] "
                f"Mode: [bold]{mode.name.title()}[/bold]"
            )
            
            with Live(spinner, refresh_per_second=10):
                start = time.time()

                result = self._optimizer.optimize(prompt, mode)

                end = time.time()

            console.print(
                "[green]✔ Optimization Complete[/green]"
            )

            # ----------------------------
            # 4. Display results
            # ----------------------------
            self._result.show(result.current_prompt)

            self._summary.show(result)

            console.print(
                "[bright_black]"
                f"Completed in {end-start:.2f}s"
                "[/bright_black]"
            )

            console.print("\n")