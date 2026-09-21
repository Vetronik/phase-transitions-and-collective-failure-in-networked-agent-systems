"""Command-line entry points."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .exact import detailed_balance_residual
from .graphs import make_graph
from .mean_field import critical_coupling_zero_bias, fixed_points
from .runner import run_condition
from .statistics import summarize
from .grid import run_grid
from .report import write_results_report
from .equilibrium import run_equilibrium_grid


def validate_config(config):
    required = ["N", "J", "q"]
    missing = [k for k in required if k not in config]
    if missing: raise ValueError(f"missing required keys: {missing}")
    if int(config["N"]) < 2: raise ValueError("N must be >=2")
    if float(config["q"]) < 0 or float(config["q"]) > 1: raise ValueError("q must be in [0,1]")
    if float(config.get("rho_in", 0)) < 0 or float(config.get("rho_in", 0)) > 1: raise ValueError("rho_in must be in [0,1]")
    if float(config["J"]) < 0: raise ValueError("J must be nonnegative")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(prog="collective-agents")
    sub = parser.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate-config"); v.add_argument("--config", required=True)
    r = sub.add_parser("run"); r.add_argument("--config", required=True); r.add_argument("--output", required=True)
    a = sub.add_parser("analyze"); a.add_argument("--input", required=True); a.add_argument("--output", required=True)
    g = sub.add_parser("grid"); g.add_argument("--config", required=True); g.add_argument("--grid", required=True); g.add_argument("--output", required=True)
    p = sub.add_parser("report"); p.add_argument("--input", required=True); p.add_argument("--outdir", required=True); p.add_argument("--label", default="results")
    u = sub.add_parser("audit-configs"); u.add_argument("--directory", default="configs")
    z = sub.add_parser("equilibrium-grid"); z.add_argument("--config", required=True); z.add_argument("--grid", required=True); z.add_argument("--output", required=True)
    e = sub.add_parser("theory-checks"); e.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    if args.command == "audit-configs":
        directory = Path(args.directory)
        bases = sorted(directory.glob("*_base.json"))
        if not bases: raise ValueError(f"no *_base.json files in {directory}")
        for base_path in bases:
            config = json.loads(base_path.read_text(encoding="utf-8")); validate_config(config)
            grid_path = base_path.with_name(base_path.name.replace("_base.json", "_grid.json"))
            if grid_path.exists():
                grid = json.loads(grid_path.read_text(encoding="utf-8"))
                if not grid or any(not isinstance(v, list) or not v for v in grid.values()):
                    raise ValueError(f"invalid grid specification: {grid_path}")
        print(f"validated {len(bases)} base configurations and matching grids")
    elif args.command == "equilibrium-grid":
        config = json.loads(Path(args.config).read_text(encoding="utf-8")); validate_config(config)
        grid = json.loads(Path(args.grid).read_text(encoding="utf-8")); run_equilibrium_grid(config, grid, args.output); print(args.output)
    elif args.command in {"validate-config", "run", "grid"}:
        config = json.loads(Path(args.config).read_text(encoding="utf-8")); validate_config(config)
        if args.command == "validate-config": print("valid")
        elif args.command == "run": run_condition(config, output_path=args.output); print(args.output)
        else:
            grid = json.loads(Path(args.grid).read_text(encoding="utf-8"))
            run_grid(config, grid, args.output); print(args.output)
    elif args.command == "analyze":
        frame = pd.read_csv(args.input)
        summary = summarize(frame, reps=1000)
        Path(args.output).parent.mkdir(parents=True, exist_ok=True); summary.to_csv(args.output, index=False); print(args.output)
    elif args.command == "report":
        frame = pd.read_csv(args.input)
        write_results_report(frame, args.outdir, label=args.label)
        print(args.outdir)
    elif args.command == "theory-checks":
        graph = make_graph("complete", 6, seed_parts=("theory",), normalization="symmetric")
        signals = __import__("numpy").ones(6, dtype="int8")
        payload = {"critical_coupling_H0": critical_coupling_zero_bias(0.0),
                   "critical_coupling_H05": critical_coupling_zero_bias(0.5),
                   "fixed_points": fixed_points(1.0, 0.0, 0.5),
                   "detailed_balance_residual": detailed_balance_residual(signals, graph.weights, 0.7, 0.2)}
        Path(args.output).parent.mkdir(parents=True, exist_ok=True); Path(args.output).write_text(json.dumps(payload, indent=2), encoding="utf-8"); print(args.output)


if __name__ == "__main__":
    main()
