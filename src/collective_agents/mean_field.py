"""Analytic mean-field reference calculations."""

from __future__ import annotations

import numpy as np


def F(m, J: float, H: float, q: float):
    m = np.asarray(m, dtype=float)
    return q * np.tanh(J * m + H) + (1.0 - q) * np.tanh(J * m - H)


def dF(m, J: float, H: float, q: float):
    return J * (q / np.cosh(J * m + H) ** 2 + (1.0 - q) / np.cosh(J * m - H) ** 2)


def fixed_points(J: float, H: float, q: float, grid=10001):
    xs = np.linspace(-1.0, 1.0, grid)
    ys = xs - F(xs, J, H, q)
    roots = []
    for i in range(grid - 1):
        if ys[i] == 0:
            roots.append(float(xs[i]))
        if ys[i] * ys[i + 1] < 0:
            lo, hi = xs[i], xs[i + 1]
            for _ in range(60):
                mid = (lo + hi) / 2
                if (mid - F(mid, J, H, q)) * (lo - F(lo, J, H, q)) <= 0:
                    hi = mid
                else:
                    lo = mid
            roots.append(float((lo + hi) / 2))
    if abs(ys[-1]) < 1e-12:
        roots.append(float(xs[-1]))
    return sorted(set(round(r, 12) for r in roots))


def free_energy(m, J: float, H: float, q: float):
    m = np.asarray(m, dtype=float)
    return J * m * m / 2.0 - q * np.log(2.0 * np.cosh(J * m + H)) - (1.0 - q) * np.log(2.0 * np.cosh(J * m - H))


def critical_coupling_zero_bias(H: float) -> float:
    return float(np.cosh(H) ** 2)
