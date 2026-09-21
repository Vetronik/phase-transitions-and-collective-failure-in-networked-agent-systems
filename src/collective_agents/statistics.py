"""Aggregate metrics with uncertainty intervals."""

from __future__ import annotations

import numpy as np
import pandas as pd


def bootstrap_mean(values, rng, reps=2000, alpha=0.05):
    x = np.asarray(values, dtype=float)
    if len(x) == 0:
        return {"estimate": np.nan, "low": np.nan, "high": np.nan}
    idx = rng.integers(0, len(x), size=(reps, len(x)))
    means = x[idx].mean(axis=1)
    return {"estimate": float(x.mean()), "low": float(np.quantile(means, alpha / 2)),
            "high": float(np.quantile(means, 1 - alpha / 2))}


def summarize(frame: pd.DataFrame, group_columns=None, *, seed=0, reps=2000):
    group_columns = group_columns or ["N", "J", "q", "rho_in", "horizon"]
    rng = np.random.default_rng(seed)
    rows = []
    for keys, group in frame.groupby(group_columns, dropna=False):
        if not isinstance(keys, tuple): keys = (keys,)
        row = dict(zip(group_columns, keys))
        for col in ["agent_accuracy", "majority_score", "agreement", "severe_failure", "loss", "signed_m"]:
            result = bootstrap_mean(group[col].astype(float).to_numpy(), rng, reps=reps)
            row.update({f"{col}_{k}": v for k, v in result.items()})
        rows.append(row)
    return pd.DataFrame(rows)
