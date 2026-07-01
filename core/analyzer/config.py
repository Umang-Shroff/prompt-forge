"""
Analyzer configuration.

All analyzer thresholds and tuning parameters live here.
"""

from __future__ import annotations

# ==========================================================
# General
# ==========================================================

MAX_CONFIDENCE = 1.0

# ==========================================================
# Detector Thresholds
# ==========================================================

MIN_CODE_CONFIDENCE = 0.20

MIN_MARKDOWN_CONFIDENCE = 0.15

MIN_SQL_CONFIDENCE = 0.20

MIN_LOG_CONFIDENCE = 0.15

# ==========================================================
# Scoring
# ==========================================================

CODE_MATCH_WEIGHT = 0.20

MARKDOWN_MATCH_WEIGHT = 1.0

SQL_MATCH_WEIGHT = 1.0

LOG_MATCH_WEIGHT = 1.0