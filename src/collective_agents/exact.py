"""Small-system stationary-distribution and detailed-balance checks."""

from __future__ import annotations

from itertools import product

import numpy as np


def states(n: int):
    return np.asarray(list(product((-1, 1), repeat=n)), dtype=np.int8)


def energy_exponent(state, signals, weights, J, H):
    return float(H * np.dot(signals, state) + 0.5 * J * state @ weights @ state)


def stationary_distribution(signals, weights, J, H):
    ss = states(len(signals))
    exponents = np.asarray([energy_exponent(s, signals, weights, J, H) for s in ss])
    exponents -= exponents.max()
    p = np.exp(exponents)
    p /= p.sum()
    return ss, p


def transition_matrix(signals, weights, J, H):
    ss = states(len(signals))
    index = {tuple(s): i for i, s in enumerate(ss)}
    n = len(signals)
    p = np.zeros((len(ss), len(ss)))
    for r, state in enumerate(ss):
        for i in range(n):
            local = H * signals[i] + J * weights[i] @ state
            prob_plus = float(1.0 / (1.0 + np.exp(-2.0 * local)))
            plus = state.copy(); plus[i] = 1
            minus = state.copy(); minus[i] = -1
            p[r, index[tuple(plus)]] += prob_plus / n
            p[r, index[tuple(minus)]] += (1 - prob_plus) / n
    return ss, p


def detailed_balance_residual(signals, weights, J, H):
    ss, transition = transition_matrix(signals, weights, J, H)
    _, pi = stationary_distribution(signals, weights, J, H)
    flow = pi[:, None] * transition
    return float(np.max(np.abs(flow - flow.T)))
