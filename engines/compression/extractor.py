from __future__ import annotations


class CompressionResultExtractor:
    """
    Extracts the compressed prompt from LLMLingua's output.

    Different versions of LLMLingua may return slightly
    different structures. This class normalizes them.
    """

    def extract(
        self,
        result,
        fallback: str,
    ) -> str:

        if result is None:
            return fallback

        if isinstance(result, str):
            return result

        if isinstance(result, dict):

            for key in (
                "compressed_prompt",
                "compressed_text",
                "prompt",
            ):
                value = result.get(key)

                if isinstance(value, str):
                    return value

        return fallback