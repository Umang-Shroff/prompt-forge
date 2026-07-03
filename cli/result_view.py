from __future__ import annotations

import pyperclip

from .console import console


class ResultView:
    """
    Displays the optimized prompt and automatically copies it to the clipboard.
    """

    def show(
        self,
        optimized_prompt: str,
    ) -> None:

        copied = False

        try:
            pyperclip.copy(optimized_prompt)
            copied = True
        except pyperclip.PyperclipException:
            pass

        console.print()
        console.rule("[bold green]Optimized Prompt[/bold green]")
        console.print(optimized_prompt)
        console.rule(style="green")

        if copied:
            console.print(
                "[green]✓ Optimized prompt copied to clipboard.[/green]"
            )
        else:
            console.print(
                "[yellow]⚠ Clipboard unavailable. Copy the prompt manually.[/yellow]"
            )

        console.print()