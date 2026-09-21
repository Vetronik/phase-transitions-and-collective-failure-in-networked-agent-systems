"""Equilibrium finite-size experiments for the criticality claim."""

from __future__ import annotations

import itertools
from pathlib import Path

import numpy as np
import pandas as pd

from .dynamics import run_equilibrium
from .graphs import make_graph
from .rng import canonical_json, generator
from .signals import generate_signals


def run_equilibrium_condition(config: dict) -> pd.DataFrame:
    n = int(config["N"]); J = float(config["J"]); q = float(config.get("q", 0.5))
    rho = float(config.get("rho_in", 0.0)); H = float(config.get("H", 0.0))
    graph_family = config.get("graph_family", "complete")
    graph_count = int(config.get("graph_count", 1)); signal_count = int(config.get("signal_count", 1))
    chains = int(config.get("chain_count", 10)); burnin = int(config.get("burnin", 200))
    samples = int(config.get("samples", 10)); thin = int(config.get("thin", 10))
    run_key = config.get("run_key", "equilibrium")
    stage = config.get("stage", "equilibrium")
    cfg_hash = __import__("hashlib").sha256(canonical_json(config).encode()).hexdigest()[:16]
    rows = []
    for graph_id in range(graph_count):
        graph = make_graph(graph_family, n, seed_parts=(run_key, graph_id), degree=int(config.get("degree", 8)), normalization=config.get("normalization", "symmetric"), connected=True)
        for signal_id in range(signal_count):
            truth, signals, _ = generate_signals(n, q, rho, seed_parts=(run_key, graph_id, signal_id))
            for chain_id in range(chains):
                rng = generator("equilibrium", run_key, graph_id, signal_id, chain_id, n, J, q, rho, H, burnin, samples, thin)
                states = run_equilibrium(signals, graph.weights, J, H, burnin, samples, thin, rng, initial=config.get("initial", "random"))
                for sample_id, state in enumerate(states):
                    m = float(state.mean())
                    rows.append({
                        "run_id": f"{run_key}-{graph_id}-{signal_id}-{chain_id}-{sample_id}",
                        "config_hash": cfg_hash, "stage": stage, "model": "binary_heat_bath",
                        "protocol": "equilibrium_heat_bath", "graph_family": graph_family,
                        "graph_id": graph_id, "signal_id": signal_id, "chain_id": chain_id,
                        "sample_id": sample_id, "N": n, "J": J, "q": q, "rho_in": rho,
                        "H": H, "burnin": burnin, "thin": thin, "truth": truth,
                        "m": m, "abs_m": abs(m), "m2": m*m, "m4": m**4,
                    })
    return pd.DataFrame(rows)


def run_equilibrium_grid(base: dict, grid: dict, output: str | Path) -> pd.DataFrame:
    keys = list(grid); values = [grid[k] for k in keys]; frames = []
    for combo in itertools.product(*values):
        config = dict(base); config.update(dict(zip(keys, combo)))
        frames.append(run_equilibrium_condition(config))
    frame = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    out = Path(output); out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp"); frame.to_csv(tmp, index=False); tmp.replace(out)
    return frame
