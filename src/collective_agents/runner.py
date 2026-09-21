"""Experiment execution and flat, provenance-rich result rows."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from .dynamics import bayes_decision, direct_signal_majority, initial_decisions, run_async
from .graphs import make_graph
from .observables import episode_metrics
from .rng import canonical_json, generator, seed_from
from .signals import generate_signals, stable_sigmoid


def run_condition(config: dict, *, output_path: str | Path | None = None) -> pd.DataFrame:
    n = int(config["N"])
    graph_family = config.get("graph_family", "random_regular")
    degree = int(config.get("degree", 8))
    normalization = config.get("normalization", "symmetric")
    graph_count = int(config.get("graph_count", 1))
    signal_count = int(config.get("signal_count", 1))
    trajectory_count = int(config.get("trajectory_count", 1))
    q = float(config["q"]); rho = float(config.get("rho_in", 0.0))
    J = float(config["J"]); H = float(config.get("H", 0.5))
    horizon = int(config.get("horizon", 20))
    checkpoints = config.get("checkpoints", [horizon])
    initial = config.get("initial", "natural")
    protocol = config.get("protocol", "heat_bath")
    stage = config.get("stage", "smoke")
    rows = []
    run_key = config.get("run_key", "default")
    cfg_hash = __import__("hashlib").sha256(canonical_json(config).encode()).hexdigest()[:16]
    for graph_id in range(graph_count):
        graph = make_graph(graph_family, n, seed_parts=(run_key, graph_id), degree=degree,
                           normalization=normalization, connected=bool(config.get("connected", False)),
                           rewiring=float(config.get("rewiring", 0.10)))
        for signal_id in range(signal_count):
            truth, signals, signal_meta = generate_signals(n, q, rho, seed_parts=(run_key, graph_id, signal_id))
            for trajectory_id in range(trajectory_count):
                # Exclude varied treatment values from this stream so grid
                # arms share initial decisions, update indices, and uniforms.
                rng = generator("trajectory", run_key, graph_id, signal_id, trajectory_id,
                                n, q, rho, H, horizon, initial)
                if protocol == "heat_bath":
                    trajectory = run_async(signals, graph.weights, J, H, horizon, rng,
                                           checkpoints=checkpoints, initial=initial)
                elif protocol == "source_tagged_one_pass":
                    # Each agent reads each neighbor's private signal once.
                    # Source IDs are retained conceptually; no decision is
                    # repeatedly copied through the network.
                    fields = H * signals + J * (graph.weights @ signals)
                    p = stable_sigmoid(2.0 * fields)
                    terminal = np.where(rng.random(n) < p, 1, -1).astype(np.int8)
                    saved = {int(t): terminal.copy() for t in checkpoints}
                    trajectory = type("OnePassTrajectory", (), {"terminal": terminal, "checkpoints": saved})()
                else:
                    raise ValueError(f"unknown protocol: {protocol}")
                metric = episode_metrics(trajectory.terminal, truth)
                raw_vote = direct_signal_majority(signals)
                oracle = bayes_decision(signals, q, rho)
                rows.append({
                    "run_id": f"{run_key}-{protocol}-{graph_id}-{signal_id}-{trajectory_id}",
                    "config_hash": cfg_hash, "stage": stage, "model": "binary_heat_bath", "protocol": protocol,
                    "graph_family": graph_family, "graph_id": graph_id, "signal_id": signal_id,
                    "trajectory_id": trajectory_id, "pair_id": f"{run_key}-{graph_id}-{signal_id}",
                    "seed_namespace": run_key, "N": n, "J": J, "q": q, "H": H,
                    "rho_in": rho, "normalization": normalization, "initial": initial,
                    "horizon": horizon, "truth": truth,
                    "shared_signal": signal_meta["shared_signal"],
                    "copy_count": signal_meta["copy_count"],
                    "graph_mean_degree": graph.metadata["mean_degree"],
                    "graph_min_degree": graph.metadata["min_degree"],
                    "graph_max_degree": graph.metadata["max_degree"],
                    "graph_edges": graph.metadata["edges"],
                    "graph_components": graph.metadata["components"],
                    "graph_clustering": graph.metadata["clustering"],
                    "n_correct_signals": int((signals == truth).sum()),
                    "n_wrong": metric["n_wrong"], "loss": metric["loss"],
                    "agent_accuracy": metric["agent_accuracy"], "m": metric["m"],
                    "signed_m": metric["signed_m"], "agreement": metric["agreement"],
                    "majority_score": metric["majority_score"],
                    "majority_correct": metric["majority_correct"],
                    "severe_failure": metric["severe_failure"],
                    "raw_signal_majority": raw_vote,
                    "raw_signal_majority_score": 1.0 if raw_vote == truth else (0.5 if raw_vote == 0 else 0.0),
                    "bayes_oracle": oracle,
                    "bayes_oracle_score": 1.0 if oracle == truth else (0.5 if oracle == 0 else 0.0),
                    # Compact per-agent terminal errors permit covariance and
                    # effective-population-size reconstruction without keeping
                    # a dense N x N matrix.
                    "error_bits": "x" + "".join("1" if x != truth else "0" for x in trajectory.terminal),
                    **{f"m_t{t}": float((truth * state).mean()) for t, state in trajectory.checkpoints.items()},
                    **{f"loss_t{t}": float((state != truth).mean()) for t, state in trajectory.checkpoints.items()},
                })
    frame = pd.DataFrame(rows)
    if output_path is not None:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_suffix(out.suffix + ".tmp")
        if out.suffix.lower() == ".parquet":
            frame.to_parquet(tmp, index=False)
        else:
            frame.to_csv(tmp, index=False)
        tmp.replace(out)
    return frame
