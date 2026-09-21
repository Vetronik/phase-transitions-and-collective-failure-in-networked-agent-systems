# Execution handoff

The first executable milestone is complete when the following commands pass from the repository root:

```powershell
python -m pytest -q
python -m collective_agents.cli validate-config --config configs/smoke.json
python -m collective_agents.cli theory-checks --output results/diagnostics/theory_checks.json
python -m collective_agents.cli run --config configs/smoke.json --output results/smoke.csv
python -m collective_agents.cli analyze --input results/smoke.csv --output results/smoke_summary.csv
python -m collective_agents.cli grid --config configs/pilot_base.json --grid configs/pilot_grid.json --output results/pilot.csv
python -m collective_agents.cli analyze --input results/pilot.csv --output results/pilot_summary.csv
```

After that milestone, run the literature gate and then create frozen pilot/confirmation configurations from `RESEARCH_EXECUTION_PLAN.md`. Do not claim phase transitions from the smoke run. The smoke run validates plumbing, equations, baselines, provenance, and metric definitions only.
