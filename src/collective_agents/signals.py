"""Truth and private-information generation."""

from __future__ import annotations

import numpy as np

from .rng import generator


def stable_sigmoid(x):
    x = np.asarray(x, dtype=float)
    return np.where(x >= 0, 1.0 / (1.0 + np.exp(-x)), np.exp(x) / (1.0 + np.exp(x)))


def generate_signals(n: int, q: float, rho_in: float, *, seed_parts=()):
    if not 0 <= q <= 1:
        raise ValueError("q must lie in [0,1]")
    if not 0 <= rho_in <= 1:
        raise ValueError("rho_in must lie in [0,1]")
    rng = generator("signals", *seed_parts, n, q, rho_in)
    truth = 1 if rng.random() < 0.5 else -1
    # Keep the common source explicit for auditing but do not expose it to dynamics.
    z = truth if rng.random() < q else -truth
    u = np.where(rng.random(n) < q, truth, -truth).astype(np.int8)
    copy = rng.random(n) < np.sqrt(rho_in)
    signals = np.where(copy, z, u).astype(np.int8)
    return truth, signals, {"shared_signal": int(z), "copy_count": int(copy.sum())}


def signal_correct_probability(q: float, H: float) -> float:
    return 0.5 * (1.0 + (2.0 * q - 1.0) * np.tanh(H))


def signal_pair_correlation(q: float, rho_in: float) -> float:
    # With copy probability c=sqrt(rho), both agents share Z with probability
    # c^2.  Since Z^2=1, the conditional covariance is
    # c^2*(1-(2q-1)^2), while the marginal conditional variance is the same
    # factor without c^2.  Hence the correlation is exactly rho.
    if q in (0.0, 1.0):
        return float("nan")
    return float(rho_in)


def latent_signal_loglikelihood(signals: np.ndarray, q: float, rho_in: float, truth: int) -> float:
    """Log P(signals | truth) under the shared-source mixture."""
    if rho_in == 0:
        correct = (signals == truth).sum()
        wrong = len(signals) - correct
        return float(correct * np.log(q) + wrong * np.log1p(-q))
    c = np.sqrt(rho_in)
    log_terms = []
    for z in (truth, -truth):
        pz = q if z == truth else 1.0 - q
        # Each coordinate is a mixture of copied common evidence and private evidence.
        p = np.where(signals == z, c + (1 - c) * (q if z == truth else 1 - q),
                     (1 - c) * (1 - q if z == truth else q))
        if np.any(p <= 0) or pz <= 0:
            continue
        log_terms.append(np.log(pz) + np.log(p).sum())
    if not log_terms:
        return -np.inf
    a = max(log_terms)
    return float(a + np.log(np.exp(np.asarray(log_terms) - a).sum()))


def bayes_truth_probability(signals: np.ndarray, q: float, rho_in: float) -> float:
    lp = np.array([latent_signal_loglikelihood(signals, q, rho_in, y) for y in (-1, 1)])
    a = np.max(lp)
    p = np.exp(lp - a)
    return float(p[1] / p.sum())
