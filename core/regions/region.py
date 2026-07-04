from __future__ import annotations

from dataclasses import dataclass

from .region_type import RegionType


@dataclass(slots=True)
class Region:

    type: RegionType

    text: str

    compressible: bool = True

    confidence: float = 1.0

    is_code: bool = False