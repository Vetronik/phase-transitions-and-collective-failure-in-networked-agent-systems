"""Asynchronous heat-bath dynamics and deterministic baselines."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .signals import stable_sigmoid


@dataclass
class Trajectory:
    terminal: np.ndarray
    checkpoints: dict[int, np.ndarray]
    fields: np.ndarray | None = None


def _complete_graph_weight(weights: np.ndarray):
    """Return the off-diagonal weight for a complete graph, or None."""
    w = np.asarray(weights, dtype=float)
    n = w.shape[0]
    if n < 2:
        return None
    expected = np.full((n, n), 1.0 / (n - 1))
    np.fill_diagonal(expected, 0.0)
    return float(expected[0, 1]) if np.allclose(w, expected, atol=1e-12) else None


def initial_decisions(signals: np.ndarray, H: float, rng: np.random.Generator) -> np.ndarray:
    p = stable_sigmoid(2.0 * H * signals)
    return np.where(rng.random(len(signals)) < p, 1, -1).astype(np.int8)


def run_async(signals: np.ndarray, weights: np.ndarray, J: float, H: float,
              sweeps: int, rng: np.random.Generator, *, checkpoints=(),
              initial: str = "natural", record_fields: bool = False) -> Trajectory:
    n = len(signals)
    # Convert once to adjacency-list form.  Sparse graph updates then cost
    # O(degree) per event instead of multiplying by a dense N-vector.
    neighbor_lists = []
    for row in np.asarray(weights):
        idx = np.flatnonzero(row)
        neighbor_lists.append((idx, row[idx]))
    if initial == "natural":
        decisions = initial_decisions(signals, H, rng)
    elif initial == "random":
        decisions = np.where(rng.random(n) < 0.5, 1, -1).astype(np.int8)
    elif initial == "signal":
        decisions = signals.astype(np.int8).copy()
    elif initial == "all_plus":
        decisions = np.ones(n, dtype=np.int8)
    elif initial == "all_minus":
        decisions = -np.ones(n, dtype=np.int8)
    else:
        raise ValueError(f"unknown initial condition: {initial}")
    checkpoints = set(int(x) for x in checkpoints)
    saved = {0: decisions.copy()} if 0 in checkpoints else {}
    fields = [] if record_fields else None
    for sweep in range(1, sweeps + 1):
        for i in rng.integers(0, n, size=n):
            idx, vals = neighbor_lists[int(i)]
            local = H * int(signals[i]) + J * float(vals @ decisions[idx])
            p = float(stable_sigmoid(2.0 * local))
            decisions[i] = 1 if rng.random() < p else -1
            if record_fields:
                fields.append(local)
        if sweep in checkpoints:
            saved[sweep] = decisions.copy()
    return Trajectory(decisions, saved, np.asarray(fields) if record_fields else None)


def run_equilibrium(signals: np.ndarray, weights: np.ndarray, J: float, H: float,
                    burnin: int, samples: int, thin: int,
                    rng: np.random.Generator, *, initial: str = "random") -> np.ndarray:
    """Draw approximately stationary states using asynchronous heat bath.

    ``burnin`` and ``thin`` are measured in sweeps. The returned array has
    shape (samples, N). For a complete graph the neighbor field is updated in
    O(1) time using the running magnetization; sparse graphs use adjacency lists.
    """
    n = len(signals)
    if initial == "random":
        decisions = np.where(rng.random(n) < 0.5, 1, -1).astype(np.int8)
    elif initial == "signal":
        decisions = signals.astype(np.int8).copy()
    elif initial == "all_plus":
        decisions = np.ones(n, dtype=np.int8)
    elif initial == "all_minus":
        decisions = -np.ones(n, dtype=np.int8)
    else:
        raise ValueError(f"unknown initial condition: {initial}")
    complete_weight = _complete_graph_weight(weights)
    neighbor_lists = [] if complete_weight is not None else [(np.flatnonzero(row), row[np.flatnonzero(row)]) for row in np.asarray(weights)]
    total = int(decisions.sum())
    saved = []
    total_sweeps = int(burnin) + int(samples) * int(thin)
    for sweep in range(1, total_sweeps + 1):
        for i in rng.integers(0, n, size=n):
            i = int(i)
            if complete_weight is not None:
                social = complete_weight * (total - int(decisions[i]))
            else:
                idx, vals = neighbor_lists[i]
                social = float(vals @ decisions[idx])
            local = H * int(signals[i]) + J * social
            p = float(stable_sigmoid(2.0 * local))
            old = int(decisions[i])
            new = 1 if rng.random() < p else -1
            if new != old:
                decisions[i] = new
                total += new - old
        if sweep > burnin and (sweep - burnin) % thin == 0:
            saved.append(decisions.copy())
    return np.asarray(saved, dtype=np.int8)


def direct_signal_majority(signals: np.ndarray) -> int:
    s = int(np.sign(signals.sum()))
    return s if s else 0


def bayes_decision(signals: np.ndarray, q: float, rho_in: float) -> int:
    from .signals import bayes_truth_probability
    p = bayes_truth_probability(signals, q, rho_in)
    return 1 if p > 0.5 else (-1 if p < 0.5 else 0)
