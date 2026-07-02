from __future__ import annotations

from .registry import ReconstructorRegistry
from .sentence_reconstructor import SentenceReconstructor
from .list_reconstructor import ListReconstructor
from .markdown_reconstructor import MarkdownReconstructor
from .code_block_reconstructor import CodeBlockReconstructor


def create_default_registry() -> ReconstructorRegistry:

    registry = ReconstructorRegistry()

    registry.register(
        SentenceReconstructor(),
    )
    registry.register(
        ListReconstructor(),
    )
    registry.register(
        MarkdownReconstructor(),
    )
    registry.register(
        CodeBlockReconstructor(),
    )

    return registry