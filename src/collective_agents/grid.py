"""Small, resumable grid runner used for pilot and confirmation batches."""

from __future__ import annotations

import itertools
from pathlib import Path

import pandas as pd

from .runner import run_condition


def run_grid(base: dict, grid: dict, output: str | Path) -> pd.DataFrame:
    """Run a Cartesian grid and write one immutable CSV.

    The base ``run_key`` is shared across J/q/rho arms so graph, signal, and
    trajectory random streams are paired whenever their IDs match.
    """
    keys = list(grid)
    values = [grid[k] for k in keys]
    frames = []
    for combo in itertools.product(*values):
        config = dict(base)
        config.update(dict(zip(keys, combo)))
        frames.append(run_condition(config))
    frame = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    out = Path(output); out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    frame.to_csv(tmp, index=False)
    tmp.replace(out)
    return frame
