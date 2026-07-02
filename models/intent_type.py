from __future__ import annotations

from enum import Enum


class IntentType(str, Enum):
    """
    Supported prompt intents.
    """

    ROLE = "role"

    EXPLAIN = "explain"

    PLAN = "plan"

    GENERATE_CODE = "generate_code"

    DEBUG = "debug"

    SUMMARIZE = "summarize"

    COMPARE = "compare"

    TRANSLATE = "translate"

    BRAINSTORM = "brainstorm"

    EXTRACT = "extract"

    UNKNOWN = "unknown"