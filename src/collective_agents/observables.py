"""Episode metrics and covariance summaries."""

from __future__ import annotations

import numpy as np


def episode_metrics(decisions: np.ndarray, truth: int, *, severe_threshold=0.9) -> dict:
    n = len(decisions)
    n_wrong = int(np.count_nonzero(decisions != truth))
    m = float(np.mean(decisions))
    signed = float(truth * m)
    majority_score = 1.0 if signed > 0 else (0.5 if signed == 0 else 0.0)
    return {
        "n": n,
        "n_wrong": n_wrong,
        "loss": n_wrong / n,
        "agent_accuracy": 1.0 - n_wrong / n,
        "m": m,
        "signed_m": signed,
        "agreement": abs(m),
        "majority_score": majority_score,
        "majority_correct": bool(signed > 0),
        "tie": bool(signed == 0),
        "severe_failure": bool(n_wrong >= int(np.ceil(severe_threshold * n))),
    }


def covariance_summary(error_matrix: np.ndarray) -> dict:
    """Return covariance and effective-size summaries from rows=episodes, cols=agents."""
    x = np.asarray(error_matrix, dtype=float)
    if x.ndim != 2 or x.shape[0] < 2:
        raise ValueError("error_matrix must have at least two episode rows")
    p = x.mean(axis=0)
    vbar = float(np.mean(p * (1.0 - p)))
    losses = x.mean(axis=1)
    var_loss = float(np.var(losses, ddof=1))
    n = x.shape[1]
    cbar = float((n * var_loss - vbar) / max(1, n - 1))
    rho_eff = cbar / vbar if vbar > 0 else float("nan")
    n_eff = vbar / var_loss if var_loss > 0 else float("inf")
    return {"vbar": vbar, "var_loss": var_loss, "cbar": cbar,
            "rho_eff": rho_eff, "n_eff": n_eff}
