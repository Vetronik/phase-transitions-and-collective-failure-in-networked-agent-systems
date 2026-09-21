"""Paired contrasts, covariance reconstruction, and a compact results ledger."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .observables import covariance_summary
from .rng import generator
from .statistics import bootstrap_mean
from .uncertainty import hierarchical_summary


def paired_contrasts(frame: pd.DataFrame, baseline_j=0.0) -> pd.DataFrame:
    keys = ["N", "q", "rho_in", "horizon", "graph_family", "normalization", "initial", "graph_id", "signal_id", "trajectory_id"]
    if "protocol" in frame.columns:
        keys.insert(3, "protocol")
    base = frame[np.isclose(frame.J, baseline_j)].copy()
    out = []
    for j in sorted(float(x) for x in frame.J.unique() if not np.isclose(x, baseline_j)):
        treated = frame[np.isclose(frame.J, j)].copy()
        merged = treated.merge(base, on=keys, suffixes=("_t", "_b"), how="inner")
        if merged.empty:
            continue
        for metric in ["agent_accuracy", "majority_score", "agreement", "severe_failure", "loss", "bayes_oracle_score", "raw_signal_majority_score"]:
            # Boolean outcome columns need numeric coercion before subtraction.
            merged[f"delta_{metric}"] = merged[f"{metric}_t"].astype(float) - merged[f"{metric}_b"].astype(float)
        out.append(merged[["N", "q", "rho_in", "horizon", "graph_family", "normalization", "initial", "graph_id", "signal_id", "trajectory_id", "J_t", *[f"delta_{x}" for x in ["agent_accuracy", "majority_score", "agreement", "severe_failure", "loss", "bayes_oracle_score", "raw_signal_majority_score"]]]].rename(columns={"J_t":"J"}))
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()


def covariance_rows(frame: pd.DataFrame) -> pd.DataFrame:
    if "error_bits" not in frame.columns:
        return pd.DataFrame([{"status": "missing_error_bits", "reason": "run predates terminal-vector storage"}])
    rows = []
    group_cols = ["N", "J", "q", "rho_in", "horizon"]
    for keys, group in frame.groupby(group_cols, dropna=False):
        bits = []
        for value, n in zip(group.error_bits.dropna(), group.loc[group.error_bits.notna(), "N"]):
            text = str(value)
            if text.startswith("x"):
                text = text[1:]
            # Older CSVs allowed pandas to infer all-numeric bit strings as
            # integers; recover their fixed width from N when possible.
            text = text.zfill(int(n))
            if set(text) <= {"0", "1"} and len(text) == int(n):
                bits.append([int(x) for x in text])
        if not bits or len(bits) < 2:
            row = dict(zip(group_cols, keys)); row.update({"status":"insufficient_rows", "samples":len(bits)}); rows.append(row); continue
        matrix = np.asarray(bits, dtype=float)
        summary = covariance_summary(matrix)
        row = dict(zip(group_cols, keys)); row.update(summary); row.update({"status":"ok", "samples":len(bits)}); rows.append(row)
    return pd.DataFrame(rows)


def write_results_report(frame: pd.DataFrame, outdir: str | Path, *, label="results"):
    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    contrasts = paired_contrasts(frame)
    cov = covariance_rows(frame)
    group_cols = [c for c in ["N", "J", "q", "rho_in", "horizon", "graph_family", "protocol"] if c in frame.columns]
    metrics = [c for c in ["agent_accuracy", "majority_score", "agreement", "severe_failure", "loss"] if c in frame.columns]
    hierarchical = hierarchical_summary(frame, group_cols, metrics, reps=1000, seed=11) if group_cols and metrics else pd.DataFrame()
    contrasts.to_csv(out / f"{label}_contrasts.csv", index=False)
    cov.to_csv(out / f"{label}_covariance.csv", index=False)
    hierarchical.to_csv(out / f"{label}_hierarchical_uncertainty.csv", index=False)
    lines = [f"# {label} results ledger", "", "This file is generated from immutable run output. It is descriptive; it does not replace the preregistered analysis.", ""]
    lines.append(f"Rows: {len(frame)}. Conditions: {frame[['J','q','rho_in']].drop_duplicates().shape[0] if len(frame) else 0}.")
    if len(contrasts):
        lines += ["", "## Paired treatment contrasts", "", "| J | q | rho_in | delta agent accuracy | delta majority score | delta severe failure |", "|---:|---:|---:|---:|---:|---:|"]
        for keys, g in contrasts.groupby(["J", "q", "rho_in"], dropna=False):
            lines.append("| %g | %g | %g | %.4f | %.4f | %.4f |" % (keys[0], keys[1], keys[2], g.delta_agent_accuracy.mean(), g.delta_majority_score.mean(), g.delta_severe_failure.mean()))
    if len(cov):
        cov_text = cov.to_csv(index=False).strip()
    else:
        cov_text = "No covariance rows produced."
    lines += ["", "## Covariance status", "", "```csv", cov_text, "```", "", "Hierarchical uncertainty intervals are written to the accompanying CSV and resample graph clusters with signal instances nested within graphs.", "", "Interpretation rules: agreement is not accuracy; severe-failure effects are terminal risk changes; covariance must be estimated from repeated terminal error vectors and is not inferred from agreement alone."]
    (out / f"{label}_results_summary.md").write_text("\n".join(lines), encoding="utf-8")
    return contrasts, cov
