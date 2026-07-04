from __future__ import annotations

import re


class InlineCodeSplitter:
    """
    Splits mixed text into alternating text/code regions.
    """

    _START_PATTERNS = (
        r"^\s*(def|class)\b",
        r"^\s*(public|private|protected)\b",
        r"^\s*(const|let|var)\b",
        r"^\s*function\b",
        r"^\s*import\b",
        r"^\s*from\b",
        r"^\s*export\b",
        r"^\s*async\b",
        r"^\s*SELECT\b",
        r"^\s*INSERT\b",
        r"^\s*UPDATE\b",
        r"^\s*DELETE\b",
        r"^\s*<[^>]+>",
    )

    def split(
        self,
        text: str,
    ) -> list[tuple[bool, str]]:

        result = []

        current = []

        current_is_code = False

        for line in text.splitlines():

            is_code = any(
                re.search(
                    pattern,
                    line,
                    re.IGNORECASE,
                )
                for pattern in self._START_PATTERNS
            )

            if (
                "(" in line
                and ")" in line
                and (
                    "=" in line
                    or "{" in line
                    or ";" in line
                )
            ):
                is_code = True

            if current and is_code != current_is_code:

                result.append(
                    (
                        current_is_code,
                        "\n".join(current),
                    )
                )

                current = []

            current_is_code = is_code

            current.append(line)

        if current:

            result.append(
                (
                    current_is_code,
                    "\n".join(current),
                )
            )

        return result