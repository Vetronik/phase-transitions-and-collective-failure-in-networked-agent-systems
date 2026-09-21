import numpy as np

from collective_agents.exact import detailed_balance_residual, stationary_distribution
from collective_agents.dynamics import run_equilibrium
from collective_agents.graphs import make_graph
from collective_agents.mean_field import critical_coupling_zero_bias, fixed_points
from collective_agents.observables import covariance_summary, episode_metrics
from collective_agents.signals import generate_signals, signal_correct_probability, signal_pair_correlation
from collective_agents.uncertainty import hierarchical_bootstrap
from collective_agents.runner import run_condition


def test_signal_probability_formula():
    assert np.isclose(signal_correct_probability(0.7, 0.5), 0.5 * (1 + 0.4 * np.tanh(0.5)))


def test_graph_shape_and_normalization():
    g = make_graph("random_regular", 32, seed_parts=(1,), degree=8)
    assert g.adjacency.shape == (32, 32)
    assert np.allclose(g.adjacency, g.adjacency.T)
    assert np.allclose(g.weights.sum(axis=1), 1.0)


def test_exact_detailed_balance():
    g = make_graph("complete", 5, seed_parts=(2,))
    signals = np.array([1, -1, 1, -1, 1], dtype=np.int8)
    assert detailed_balance_residual(signals, g.weights, 0.8, 0.5) < 1e-12


def test_mean_field_known_critical_points():
    assert np.isclose(critical_coupling_zero_bias(0.0), 1.0)
    assert fixed_points(0.5, 0.0, 0.5) == [0.0]


def test_metrics_and_covariance_identity():
    x = np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1], [0, 0, 1]], dtype=float)
    result = covariance_summary(x)
    assert result["var_loss"] >= 0
    metrics = episode_metrics(np.array([1, -1, 1, -1], dtype=np.int8), 1)
    assert metrics["majority_score"] == 0.5


def test_shared_source_correlation_parameter():
    assert signal_pair_correlation(0.65, 0.25) == 0.25


def test_equilibrium_sampler_returns_requested_samples():
    g = make_graph("complete", 8, seed_parts=(3,))
    signals = np.ones(8, dtype=np.int8)
    draws = run_equilibrium(signals, g.weights, 0.8, 0.0, burnin=5, samples=4, thin=2,
                            rng=np.random.default_rng(4))
    assert draws.shape == (4, 8)
    assert set(np.unique(draws)).issubset({-1, 1})


def test_hierarchical_bootstrap_tracks_graph_units():
    frame = __import__("pandas").DataFrame({"graph_id": [0, 0, 1, 1], "signal_id": [0, 1, 0, 1], "x": [0.0, 1.0, 0.0, 1.0]})
    result = hierarchical_bootstrap(frame, "x", reps=50, seed=1)
    assert result["graphs"] == 2
    assert result["units"] == 4
    assert 0 <= result["estimate"] <= 1


def test_source_tagged_protocol_runs():
    frame = run_condition({"run_key": "test_source", "N": 16, "J": 3.0, "q": 0.55,
                            "rho_in": 0.25, "H": 0.5, "horizon": 2,
                            "graph_family": "random_regular", "degree": 4,
                            "connected": True, "graph_count": 1, "signal_count": 1,
                            "trajectory_count": 1, "checkpoints": [0, 2],
                            "protocol": "source_tagged_one_pass"})
    assert len(frame) == 1
    assert frame.iloc[0]["protocol"] == "source_tagged_one_pass"
