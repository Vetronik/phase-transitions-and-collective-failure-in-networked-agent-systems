"""Graph generation and normalized interaction matrices."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import numpy as np

from .rng import generator


@dataclass(frozen=True)
class GraphInstance:
    family: str
    n: int
    adjacency: np.ndarray
    weights: np.ndarray
    metadata: dict


def _array_from_graph(graph: nx.Graph) -> np.ndarray:
    return nx.to_numpy_array(graph, dtype=float, nodelist=range(len(graph)))


def make_graph(family: str, n: int, *, seed_parts=(), degree: int = 8,
               normalization: str = "symmetric", connected: bool = False,
               rewiring: float = 0.10) -> GraphInstance:
    rng = generator("graph", *seed_parts, family, n, degree, normalization, connected, rewiring)
    if family == "complete":
        graph = nx.complete_graph(n)
    elif family == "random_regular":
        if degree >= n or (n * degree) % 2:
            raise ValueError("random_regular requires degree < n and n*degree even")
        graph = nx.random_regular_graph(degree, n, seed=int(rng.integers(2**32)))
    elif family == "erdos_renyi":
        graph = nx.gnp_random_graph(n, degree / (n - 1), seed=int(rng.integers(2**32)))
    elif family == "watts_strogatz":
        if degree % 2:
            raise ValueError("watts_strogatz degree must be even")
        graph = nx.watts_strogatz_graph(n, degree, rewiring, seed=int(rng.integers(2**32)))
    elif family == "sbm":
        sizes = [n // 2, n - n // 2]
        p_in = min(1.0, (degree - 1) / max(1, sizes[0] - 1))
        p_out = min(1.0, 1.0 / max(1, sizes[1]))
        graph = nx.stochastic_block_model(sizes, [[p_in, p_out], [p_out, p_in]],
                                          seed=int(rng.integers(2**32)), directed=False)
    elif family == "preferential_attachment":
        m = max(1, min(degree // 2, n - 1))
        graph = nx.barabasi_albert_graph(n, m, seed=int(rng.integers(2**32)))
    else:
        raise ValueError(f"unknown graph family: {family}")

    if connected and not nx.is_connected(graph):
        # Preserve the requested population size.  Regenerate a finite number
        # of times rather than silently dropping disconnected nodes.
        for _ in range(100):
            if family == "erdos_renyi":
                graph = nx.gnp_random_graph(n, degree / (n - 1), seed=int(rng.integers(2**32)))
            elif family == "watts_strogatz":
                graph = nx.watts_strogatz_graph(n, degree, rewiring, seed=int(rng.integers(2**32)))
            elif family == "sbm":
                sizes = [n // 2, n - n // 2]
                p_in = min(1.0, (degree - 1) / max(1, sizes[0] - 1)); p_out = min(1.0, 1.0 / max(1, sizes[1]))
                graph = nx.stochastic_block_model(sizes, [[p_in, p_out], [p_out, p_in]], seed=int(rng.integers(2**32)), directed=False)
            elif family == "preferential_attachment":
                m = max(1, min(degree // 2, n - 1)); graph = nx.barabasi_albert_graph(n, m, seed=int(rng.integers(2**32)))
            if nx.is_connected(graph):
                break
        else:
            raise RuntimeError(f"could not generate connected {family} graph with n={n}")

    a = _array_from_graph(graph)
    if normalization == "symmetric":
        mean_degree = float(a.sum(axis=1).mean())
        w = a / mean_degree if mean_degree else a.copy()
    elif normalization == "row":
        degrees = a.sum(axis=1)
        w = np.divide(a, degrees[:, None], out=np.zeros_like(a), where=degrees[:, None] > 0)
    else:
        raise ValueError("normalization must be symmetric or row")
    metadata = {
        "family": family,
        "n": n,
        "requested_n": int(n),
        "degree_target": int(degree),
        "normalization": normalization,
        "connected_requested": connected,
        "connected": nx.is_connected(graph) if n else True,
        "edges": int(graph.number_of_edges()),
        "mean_degree": float(a.sum(axis=1).mean()) if n else 0.0,
        "min_degree": int(a.sum(axis=1).min()) if n else 0,
        "max_degree": int(a.sum(axis=1).max()) if n else 0,
        "components": int(nx.number_connected_components(graph)) if n else 0,
        "clustering": float(nx.average_clustering(graph)) if n else 0.0,
    }
    return GraphInstance(family, n, a, w, metadata)
