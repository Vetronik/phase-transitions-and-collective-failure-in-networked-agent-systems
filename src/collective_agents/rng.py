"""Stable random-stream derivation.

The seed namespace is part of the data provenance.  Python's process-randomized
hash is intentionally not used.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

import numpy as np


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def seed_from(*parts: Any) -> int:
    payload = canonical_json(parts).encode("utf-8")
    digest = hashlib.blake2b(payload, digest_size=16).digest()
    return int.from_bytes(digest[:8], "little", signed=False)


def generator(*parts: Any) -> np.random.Generator:
    return np.random.default_rng(seed_from(*parts))
