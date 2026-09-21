# Manuscript build

`main.tex` is the polished results-aware journal-style manuscript (version 1.1). It includes a cover sheet, Inhaltsangabe / table of contents, extended theory and methods, separated evidence batches, uncertainty reporting, appendices, and explicit limitations. It reports the reduced confirmation, replication, topology, mechanism, exploratory one-pass protocol audit, size/time, and approximate-equilibrium benchmark separately, and it does not claim a thermodynamic phase transition.

The figures referenced by the manuscript are generated from the immutable CSV outputs under `results/figures/`. If a TeX engine is available, run `pdflatex main.tex` twice from `paper/`. In the current workspace, the deterministic fallback converters can rebuild both deliverables from the repository root:

```powershell
python scripts/convert_paper_to_pdf.py
python scripts/convert_paper_to_word.py
```

The reduced allocations and later robustness batches are documented in `protocol/deviations.csv` and `protocol/deviations_v2.csv`. The primary paired uncertainty calculation is stored in `analysis/confirmation/primary_uncertainty.csv`.
