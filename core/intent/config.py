from __future__ import annotations

"""
Configuration for the intent detection pipeline.

These values control how intent detectors are interpreted
and filtered. They can be tuned without modifying the
detectors or scoring logic.
"""

# ---------------------------------------------------------
# Detection Thresholds
# ---------------------------------------------------------

# Minimum confidence required for an intent to be included
# in the final IntentResult.
MIN_INTENT_CONFIDENCE: float = 0.15

# Confidence above which an intent is considered "strong".
STRONG_INTENT_CONFIDENCE: float = 0.75

# ---------------------------------------------------------
# Output Limits
# ---------------------------------------------------------

# Maximum number of intents returned by the scorer.
MAX_INTENTS: int = 5

# ---------------------------------------------------------
# Evidence
# ---------------------------------------------------------

# Maximum evidence items retained per detected intent.
MAX_EVIDENCE_ITEMS: int = 10