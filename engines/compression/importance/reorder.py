from __future__ import annotations


def reorder_chunks(
    chunks: list[str],
    scores: list[float],
) -> tuple[list[str], list[float]]:
    """
    Reorder chunks by importance while preserving
    score alignment.
    """

    paired = sorted(
        zip(chunks, scores),
        key=lambda item: item[1],
        reverse=True,
    )

    ordered_chunks = [
        chunk
        for chunk, _ in paired
    ]

    ordered_scores = [
        score
        for _, score in paired
    ]

    return ordered_chunks, ordered_scores