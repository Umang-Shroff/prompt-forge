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

    max_chunk_size = 350

    def chunk(
        self,
        text: str,
        max_chunk_size: int = 350,
    ) -> list[str]:
        
        self.max_chunk_size = max_chunk_size

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

                    chunks.extend(
                        self._split_large_chunk(
                            "\n".join(current).strip()
                        )
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

                    chunks.extend(
                        self._split_large_chunk(
                            "\n".join(current).strip()
                        )
                    )

                    current = []

                continue

            # -----------------------------
            # markdown heading
            # -----------------------------

            if re.match(r"^#{1,6}\s", stripped):

                if current:

                    chunks.extend(
                        self._split_large_chunk(
                            "\n".join(current).strip()
                        )
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

            if self._estimate_tokens("\n".join(current)) >= self.max_chunk_size:

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


    def _estimate_tokens(
        self,
        text: str,
    ) -> int:
        """
        Rough token estimation.

        English averages ~4 characters/token.
        """

        return max(
            1,
            len(text) // 4,
        )


    def _split_large_chunk(
        self,
        text: str,
    ) -> list[str]:

        if self._estimate_tokens(text) <= self.max_chunk_size:
            return [text]

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text,
        )

        chunks: list[str] = []

        current = ""

        for sentence in sentences:

            # -----------------------------------
            # Sentence itself too large
            # Split by words instead
            # -----------------------------------

            if (
                self._estimate_tokens(sentence)
                > self.max_chunk_size
            ):

                if current:

                    chunks.append(current.strip())
                    current = ""

                chunks.extend(
                    self._split_by_words(sentence)
                )

                continue

            candidate = current + sentence + " "

            if (
                self._estimate_tokens(candidate)
                <= self.max_chunk_size
            ):

                current = candidate

            else:

                if current:
                    chunks.append(current.strip())

                current = sentence + " "

        if current:
            chunks.append(current.strip())

        return chunks
    
    def _split_by_words(
        self,
        text: str,
    ) -> list[str]:
        """
        Final fallback for extremely long
        sentences without punctuation.
        """
    
        words = text.split()
    
        chunks: list[str] = []
    
        current = ""
    
        for word in words:
        
            candidate = current + word + " "
    
            if (
                self._estimate_tokens(candidate)
                <= self.max_chunk_size
            ):
    
                current = candidate
    
            else:
            
                if current:
                    chunks.append(current.strip())
    
                current = word + " "
    
        if current:
            chunks.append(current.strip())
    
        return chunks