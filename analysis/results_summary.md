# Executed evidence summary

The fresh confirmation establishes two contrasting operational regimes. With independent inputs (`q=0.55`, `rho_in=0`), `J=3` gives mean individual accuracy 0.946, agreement 0.993, and severe-failure probability 0.05. With the same marginal quality and shared-input correlation (`rho_in=0.25`), `J=3` gives accuracy 0.401, agreement 0.994, majority score 0.40, and severe-failure probability 0.60. The Bayes oracle scores 0.90 for the correlated signals in this cell.

The retained-vector mechanism run measures the change in dependence directly. At `q=0.55`, `rho_in=0.25`, effective population size falls from 17.6 at `J=0` to 1.36 at `J=1.5`, 0.984 at `J=3`, and 0.975 at `J=4`. The high-coupling population therefore behaves, for terminal error aggregation, like a nearly single effective draw.

The reduced size/time and critical benchmark runs are diagnostic and underpowered for asymptotic claims. Their outputs and the exact sample counts are in `analysis/scaling/`, `analysis/critical/`, and the corresponding raw CSV files.
