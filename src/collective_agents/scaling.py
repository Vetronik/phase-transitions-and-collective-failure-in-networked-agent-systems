"""Finite-size scaling and transition diagnostics."""

from __future__ import annotations

import numpy as np
import pandas as pd


def binder_cumulant(values: np.ndarray) -> float:
    x = np.asarray(values, dtype=float)
    m2 = np.mean(x ** 2); m4 = np.mean(x ** 4)
    return float(1.0 - m4 / (3.0 * m2 * m2)) if m2 > 0 else np.nan


def susceptibility(values: np.ndarray, n: int) -> float:
    x = np.asarray(values, dtype=float)
    return float(n * np.var(x, ddof=1)) if len(x) > 1 else np.nan


def transition_table(frame: pd.DataFrame, value_col="signed_m") -> pd.DataFrame:
    rows = []
    for keys, group in frame.groupby(["N", "J", "q", "rho_in"], dropna=False):
        n, j, q, rho = keys
        x = group[value_col].to_numpy(float)
        rows.append({"N": n, "J": j, "q": q, "rho_in": rho,
                     "mean": float(x.mean()), "abs_mean": float(np.mean(np.abs(x))),
                     "susceptibility": susceptibility(x, int(n)),
                     "binder": binder_cumulant(x), "samples": len(x)})
    return pd.DataFrame(rows)
