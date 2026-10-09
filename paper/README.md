# Research paper

Read [When Communication Amplifies Error](when-communication-amplifies-error.pdf), by Veronika Loran. Its source is [when-communication-amplifies-error.tex](when-communication-amplifies-error.tex). PDF is the document format maintained by this project. Native LaTeX typesetting renders equations, citations, tables, and a linked table of contents with page numbers.

Install [Tectonic](https://tectonic-typesetting.github.io/en-US/install.html) or a TeX distribution with `latexmk` (or `pdflatex` and `bibtex`). Rebuild from the repository root:

```powershell
python scripts/convert_paper_to_pdf.py
```

Tectonic automatically reruns typesetting and bibliography processing to resolve page numbers and references. Its first run requires internet access to download TeX packages. The script also detects a local Windows executable at `output/tools/tectonic/tectonic.exe`.

Figures are generated from the recorded CSV outputs under `results/figures/`. The paper reports the confirmation, replication, topology, mechanism, exploratory protocol audit, size/time, and approximate-equilibrium batches separately. It does not claim a thermodynamic phase transition.

The reduced allocations and later robustness batches are documented in `protocol/deviations.csv` and `protocol/deviations_v2.csv`. The primary paired uncertainty calculation is stored in `analysis/confirmation/primary_uncertainty.csv`.
