from __future__ import annotations

from rich.table import Table

from models import PromptData

from .console import console


class SummaryView:
    """
    Displays optimization statistics.
    """

    def show(
        self,
        result: PromptData,
    ) -> None:

        table = Table(
            title="Optimization Summary",
            show_header=False,
            expand=False,
        )

        table.add_column(style="cyan")
        table.add_column(style="green")

        table.add_row(
            "Original Tokens",
            str(result.original_tokens),
        )

        table.add_row(
            "Optimized Tokens",
            str(result.optimized_tokens),
        )

        table.add_row(
            "Tokens Saved",
            str(result.tokens_saved),
        )

        table.add_row(
            "Reduction",
            f"{result.compression_ratio:.2f} %",
        )

        table.add_row(
            "Compression Engine",
            result.compression_engine,
        )

        table.add_row(
            "Compression Applied",
            "Yes" if result.compression_applied else "No",
        )

        console.print(table)
        console.print()