from __future__ import annotations

import re


class PromptChunker:
    """
    Semantic chunker for LongLLMLingua.

    Preserves:

    • markdown headings
    • bullet lists
    • numbered lists
    • fenced code blocks
    • JSON/XML blocks
    • logical paragraphs

    while avoiding oversized chunks.
    """

    max_chunk_size = 900

    def chunk(
        self,
        text: str,
    ) -> list[str]:

        if not text.strip():
            return []

        text = text.replace("\r\n", "\n")

        chunks: list[str] = []

        current: list[str] = []

        inside_code = False

        lines = text.split("\n")

        for line in lines:

            stripped = line.strip()

            # -----------------------------
            # fenced code
            # -----------------------------

            if stripped.startswith("```"):

                current.append(line)

                inside_code = not inside_code

                if not inside_code:

                    chunks.append(
                        "\n".join(current).strip()
                    )

                    current = []

                continue

            if inside_code:

                current.append(line)

                continue

            # -----------------------------
            # blank line
            # -----------------------------

            if not stripped:

                if current:

                    chunks.append(
                        "\n".join(current).strip()
                    )

                    current = []

                continue

            # -----------------------------
            # markdown heading
            # -----------------------------

            if re.match(r"^#{1,6}\s", stripped):

                if current:

                    chunks.append(
                        "\n".join(current).strip()
                    )

                    current = []

                current.append(line)

                continue

            # -----------------------------
            # bullets
            # -----------------------------

            if re.match(r"^[-*+]\s", stripped):

                current.append(line)

                continue

            # -----------------------------
            # numbered list
            # -----------------------------

            if re.match(r"^\d+\.", stripped):

                current.append(line)

                continue

            # -----------------------------
            # normal paragraph
            # -----------------------------

            current.append(line)

            if len("\n".join(current)) >= self.max_chunk_size:

                chunks.extend(
                    self._split_large_chunk(
                        "\n".join(current)
                    )
                )

                current = []

        if current:

            chunks.extend(
                self._split_large_chunk(
                    "\n".join(current)
                )
            )

        return [
            c.strip()
            for c in chunks
            if c.strip()
        ]

    def _split_large_chunk(
        self,
        text: str,
    ) -> list[str]:

        if len(text) <= self.max_chunk_size:
            return [text]

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text,
        )

        chunks: list[str] = []

        current = ""

        for sentence in sentences:

            if (
                len(current)
                + len(sentence)
                + 1
                <= self.max_chunk_size
            ):

                current += (
                    sentence
                    + " "
                )

            else:

                if current:

                    chunks.append(
                        current.strip()
                    )

                current = sentence + " "

        if current:

            chunks.append(
                current.strip()
            )

        return chunks