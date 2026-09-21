# Frozen protocol status

The reference model and analysis definitions are frozen in `RESEARCH_EXECUTION_PLAN.md` and the JSON configurations. The executed batches are marked as follows:

| Batch | Status | Interpretation |
|---|---|---|
| E00 smoke | complete | Plumbing and exact-check validation only. |
| E10 pilot | complete with recorded reduction | Exploratory map; not confirmatory. |
| E20 reduced confirmation | complete | Fresh paired effects at frozen anchors, 20 graph-signal instances per cell. |
| E60 mechanism | complete | Fresh terminal error vectors and covariance diagnostics. |
| E30 reduced size/time | complete with recorded low replication | Descriptive finite-size/horizon evidence only. |
| E40 complete-graph benchmark | complete with insufficient mixing resolution | Sanity check; no critical exponents or application transition claim. |
| Replication v1 | complete with recorded scale deviation | Higher-replication N=128 check at the strong-coupling anchors; not a literal duplicate of E20. |
| Topology v1 | complete with recorded resource reduction | Four-family N=128 robustness screen; not evidence of topology invariance. |
| Equilibrium benchmark v1 | complete with recorded size reduction | Approximate complete-graph equilibrium check through N=64; no thermodynamic claim. |
| E70 interventions | not run | Required before intervention claims. |
| LLM validation | not run | Optional extension, not part of current evidence. |

No confirmatory result was used to select a new primary endpoint or redefine severe failure. Exploratory selection of the intermediate anchor is recorded in the execution plan. The reduced allocations are recorded in `protocol/deviations.csv` and `protocol/deviations_v2.csv`.
