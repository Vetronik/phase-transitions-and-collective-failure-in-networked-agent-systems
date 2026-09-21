"""Cluster-aware uncertainty intervals for graph and signal replication."""

from __future__ import annotations

import numpy as np
import pandas as pd


def hierarchical_bootstrap(values: pd.DataFrame, metric: str, *, graph_col="graph_id", signal_col="signal_id", reps=2000, seed=0):
    """Bootstrap graph clusters and signal instances nested within graphs.

    The returned interval reflects the graph/signal sampling hierarchy. Rows
    with repeated trajectories are averaged within each graph-signal unit
    before resampling, so trajectories do not masquerade as new graphs.
    """
    required = {graph_col, signal_col, metric}
    missing = required - set(values.columns)
    if missing:
        raise ValueError(f"missing columns for hierarchical bootstrap: {sorted(missing)}")
    units = values.groupby([graph_col, signal_col], dropna=False)[metric].mean().reset_index()
    if units.empty:
        return {"estimate": np.nan, "low": np.nan, "high": np.nan, "graphs": 0, "units": 0}
    grouped = [g[metric].to_numpy(dtype=float) for _, g in units.groupby(graph_col, sort=False)]
    graph_ids = units[graph_col].unique()
    rng = np.random.default_rng(seed)
    if len({len(x) for x in grouped}) == 1:
        matrix = np.vstack(grouped)
        graph_index = rng.integers(0, len(grouped), size=(int(reps), len(grouped)))
        signal_index = rng.integers(0, matrix.shape[1], size=(int(reps), len(grouped)))
        boot = matrix[graph_index, signal_index].mean(axis=1)
    else:
        boot = np.empty(int(reps), dtype=float)
        for b in range(int(reps)):
            chosen = rng.integers(0, len(grouped), size=len(grouped))
            boot[b] = np.mean([grouped[g][rng.integers(0, len(grouped[g]))] for g in chosen])
    return {"estimate": float(units[metric].mean()), "low": float(np.quantile(boot, 0.025)),
            "high": float(np.quantile(boot, 0.975)), "graphs": int(len(graph_ids)), "units": int(len(units))}


def hierarchical_summary(frame: pd.DataFrame, group_columns, metrics, *, reps=2000, seed=0) -> pd.DataFrame:
    rows = []
    for keys, group in frame.groupby(group_columns, dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        row = dict(zip(group_columns, keys))
        for offset, metric in enumerate(metrics):
            result = hierarchical_bootstrap(group, metric, reps=reps, seed=seed + offset)
            row.update({f"{metric}_{key}": value for key, value in result.items()})
        rows.append(row)
    return pd.DataFrame(rows)
