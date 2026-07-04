from __future__ import annotations

from enum import Enum, auto


class RegionType(Enum):
    TEXT = auto()

    CODE = auto()

    JSON = auto()

    YAML = auto()

    XML = auto()

    SQL = auto()

    LOG = auto()

    MARKDOWN = auto()