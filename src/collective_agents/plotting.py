"""Minimal publication-oriented plots generated from processed tables."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def pilot_heatmaps(summary: pd.DataFrame, outdir: str | Path):
    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    for metric in ["agent_accuracy_estimate", "majority_score_estimate", "agreement_estimate", "severe_failure_estimate"]:
        for rho, sub in summary.groupby("rho_in"):
            pivot = sub.pivot(index="q", columns="J", values=metric).sort_index()
            fig, ax = plt.subplots(figsize=(8, 4.5), constrained_layout=True)
            im = ax.imshow(pivot.to_numpy(), aspect="auto", origin="lower", cmap="viridis", vmin=0, vmax=1)
            ax.set_xticks(range(len(pivot.columns)), [f"{x:g}" for x in pivot.columns])
            ax.set_yticks(range(len(pivot.index)), [f"{x:g}" for x in pivot.index])
            ax.set_xlabel("communication strength J"); ax.set_ylabel("signal quality q")
            ax.set_title(f"{metric.replace('_estimate','')}; input correlation rho={rho:g}")
            fig.colorbar(im, ax=ax)
            fig.savefig(out / f"pilot_{metric}_rho{rho:g}.png", dpi=180)
            plt.close(fig)


def confirmation_curves(frame: pd.DataFrame, outdir: str | Path):
    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    for q in sorted(frame.q.unique()):
        for rho in sorted(frame.rho_in.unique()):
            s = frame[(frame.q == q) & (frame.rho_in == rho)].groupby("J", as_index=False).agg(
                agent_accuracy=("agent_accuracy", "mean"), agreement=("agreement", "mean"),
                severe_failure=("severe_failure", "mean"), majority_score=("majority_score", "mean"))
            fig, axes = plt.subplots(1, 3, figsize=(12, 3.6), constrained_layout=True)
            axes[0].plot(s.J, s.agent_accuracy, "o-", label="agent accuracy")
            axes[0].plot(s.J, s.majority_score, "s--", label="majority score")
            axes[0].set_ylim(0, 1); axes[0].set_xlabel("J"); axes[0].set_ylabel("accuracy")
            axes[1].plot(s.J, s.agreement, "o-"); axes[1].set_ylim(0, 1); axes[1].set_xlabel("J"); axes[1].set_ylabel("agreement")
            axes[2].plot(s.J, s.severe_failure, "o-"); axes[2].set_ylim(0, 1); axes[2].set_xlabel("J"); axes[2].set_ylabel("severe failure")
            axes[0].legend(frameon=False)
            fig.suptitle(f"q={q:g}, input correlation rho={rho:g}")
            fig.savefig(out / f"confirmation_q{q:g}_rho{rho:g}.png", dpi=180)
            plt.close(fig)


def scaling_curves(frame: pd.DataFrame, outdir: str | Path):
    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    for q, rho, j in [(0.55, 0.25, 3.0), (0.65, 0.0, 3.0)]:
        s = frame[(frame.q == q) & (frame.rho_in == rho) & (frame.J == j)].groupby(["N", "horizon"], as_index=False).agg(
            accuracy=("agent_accuracy", "mean"), agreement=("agreement", "mean"), failure=("severe_failure", "mean"))
        fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), constrained_layout=True)
        for horizon, g in s.groupby("horizon"):
            axes[0].plot(g.N, g.accuracy, "o-", label=f"T={horizon}")
            axes[1].plot(g.N, g.failure, "o-", label=f"T={horizon}")
        axes[0].set_xlabel("N"); axes[0].set_ylabel("agent accuracy"); axes[1].set_xlabel("N"); axes[1].set_ylabel("severe failure")
        axes[0].set_ylim(0, 1); axes[1].set_ylim(0, 1); axes[0].legend(frameon=False)
        fig.suptitle(f"J={j:g}, q={q:g}, rho={rho:g}")
        fig.savefig(out / f"scaling_q{q:g}_rho{rho:g}_J{j:g}.png", dpi=180)
        plt.close(fig)
