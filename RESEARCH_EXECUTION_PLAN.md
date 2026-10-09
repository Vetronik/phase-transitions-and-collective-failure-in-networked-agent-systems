# Research execution plan: communication, collective intelligence, and collective failure

Prepared: 5 September 2026. Status: research protocol and execution instructions; no research experiments or results have been produced.

Research question: **Do networked populations of interacting agents exhibit phase transitions between independent decision-making, collective intelligence, and correlated collective failure as communication strength and information quality are varied?**

This document specifies a complete computational research project and the construction of its paper. It is written for an execution agent that needs explicit defaults, dependencies, deliverables, checks, and decisions. The companion `experiment_spec.json` records default parameters; `AGENT_HANDOFF.md` gives the execution entry point. Commands and source modules described below are interfaces to implement, not software that already exists.

## 1. Scientific objective and scope

### 1.1 The question the paper will actually answer

Determine when communication improves access to distributed information, when it amplifies correlated mistakes, and whether boundaries between these behaviors have evidence of a phase transition as population size increases. Separate three questions:

1. **Performance:** How do individual accuracy, group accuracy, and severe collective-error probability depend on communication strength and information quality?
2. **Mechanism:** How much failure comes from shared input errors, communication, network structure, and finite decision time?
3. **Critical behavior:** Which observed changes are consistent with an equilibrium transition, a dynamical transition under a specified limit, metastability, or a smooth crossover?

An affirmative answer to all three proposed phases is not an acceptance criterion. Correct consensus and incorrect consensus can be opposite outcomes of the same ordered phase. Independent agents can already yield an intelligent majority vote. Collective benefit and occasional collective catastrophe can coexist. Do not force these concepts into three mutually exclusive phases.

### 1.2 Default research design

Use a controlled stochastic binary-agent model as the primary study. Combine analytic baselines, finite-horizon simulation, equilibrium diagnostics, and carefully limited robustness experiments. Include an alternative continuous-opinion model to test whether conclusions depend on the binary updating rule. An LLM-agent study is a separately gated validation extension, specified in Section 15.

This choice permits large population-size experiments, known ground truth, known information quality, and reproducible randomization. Results establish properties of the specified models. Generalizations to people, organisms, or deployed AI systems require corresponding empirical evidence.

The default project needs no human participants, proprietary dataset, paid API, or cloud purchase. If the research owner selects LLMs or humans as the primary subject, revise the protocol before freezing confirmatory experiments; preserve the baseline, error-correlation, resource-matching, and transition-validation requirements.

### 1.3 Proposed contribution, subject to the novelty gate

A defensible contribution would be a controlled account of **how communication-induced dependence and shared input errors change the boundary between useful aggregation and collective failure, with explicit population-size and time-horizon tests**. The classical dynamics are a reference model, not a newly invented mechanism.

Possible contributions, in priority order:

1. Distinguish operational failure boundaries from structural ordering transitions using the same model and matched information.
2. Quantify excess collective-tail risk caused by communication after holding individual signal quality and shared-input correlation fixed.
3. Determine whether failure persists with population size, disappears with additional time, or depends on initial conditions.
4. Explain a reproducible topology or intervention effect using an analytic approximation and an independent model family.

Select the final contribution only after comparing the nearest literature and completing the prespecified evidence gates. Never claim that using an Ising-like model for agents, showing consensus, or finding that communication sometimes hurts is itself new.

## 2. Literature and novelty gate

### 2.1 What the preliminary search already establishes

Social influence has been observed to reduce diversity without commensurate accuracy improvement in a human estimation experiment; this is a reason to measure accuracy separately from agreement. See [Lorenz et al., 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3107299/).

Other experiments and theory identify circumstances under which networked social influence improves collective estimates. The project must represent this evidence as well as failure results. See [Becker, Brackbill, and Centola, 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5495222/) and [Jayles et al., 2017](https://doi.org/10.1073/pnas.1703695114).

Classical social-learning work already relates collective accuracy to the concentration of influence and distinguishes accurate learning from fast consensus. See [Golub and Jackson, 2010](https://www.aeaweb.org/articles?id=10.1257/mic.2.1.112). Informational cascades are another established route to collective mistakes: [Bikhchandani, Hirshleifer, and Welch, 1992](https://www.journals.uchicago.edu/doi/10.1086/261849).

The 2026 preprint [Physics of Agents: Statistical Mechanics Predicts Collective Behavior of AI Agents](https://arxiv.org/abs/2608.16578) is particularly close. It models interacting LLM communities using statistical mechanics and discusses a finite-size analogue of a transition. The [full text](https://arxiv.org/html/2608.16578v1) explicitly distinguishes this from a transition in the infinite-population limit. The paper proposed here must compare its controls, observables, and asymptotic claims directly with that work.

The recent paper [The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams](https://arxiv.org/abs/2608.23541) also makes communication, diversity loss, and matched resource budgets central. Its existence rules out presenting that general observation as a new contribution.

These are a preliminary source check, not a completed systematic review. Full-text access, publication status, bibliographic metadata, and the exact scope of overlapping claims must be checked again during execution.

### 2.2 Executable review procedure

1. Create `literature/search_log.csv`, `literature/evidence_matrix.csv`, `literature/novelty_memo.md`, and `paper/references.bib`.
2. Search publisher sites, arXiv, and institutional repositories. Use scholarly search services for discovery, then inspect the original paper. Record query, service, date, filters, and included/excluded records.
3. Search these query families, including synonyms and references cited by the nearest papers:
   - `collective intelligence social influence information quality network accuracy`
   - `collective failure correlated errors wisdom of crowds communication`
   - `random field Ising asymmetric bimodal mean field phase diagram`
   - `majority vote network finite size scaling external field`
   - `social learning information cascades influence concentration`
   - `multi agent debate communication error correlation matched budget`
   - `LLM agents statistical mechanics phase transition finite size`
4. Read at least 12 directly relevant papers in full and screen at least 25 candidates. These numbers are a minimum coverage check, not a guarantee of completeness. Include classical foundations, supporting and conflicting findings, criticality methods, and the closest recent agent studies.
5. Perform backward and forward citation searches on the five closest studies. Stop expanding after two consecutive targeted passes add no material new mechanism, measurement, or overlapping contribution; record the stop reason.
6. For each included paper record: citation key; verified title/authors/year; DOI or arXiv version; peer-review status; full-text access status; agent type; task; ground truth; graph; update rule; communication manipulation; information-quality manipulation; correlation treatment; population sizes; observation times; baselines; transition evidence; code/data; relevant pages; limitations; overlap with this project.
7. Verify each bibliography entry against a publisher or original repository. Label preprints as preprints unless publication is independently verified. Do not cite a search snippet as evidence of a detailed theorem.
8. Reproduce the equations or controls of the two closest computational papers when feasible. If code cannot be run, write a methods comparison and explain the limitation. Do not make exact replication a dependency when resources are inaccessible.
9. Write a one-page novelty memo with a table containing: existing result, source, proposed additional test, why that test changes what is known, and evidence required.

**Gate LIT:** At least one precise, falsifiable contribution survives comparison with the nearest papers. If all contributions duplicate existing work, first narrow to an identified unresolved comparison or perform a transparent replication/robustness study. If neither supports the desired original-paper scope, prepare an evidence-backed scope decision for the research owner before expensive computation. Do not silently invent a novelty claim.

### 2.3 Seed sources to verify and expand

| Source | Role in the project |
|---|---|
| [DeGroot, Reaching a Consensus, 1974](https://www.cse.cuhk.edu.hk/~cslui/CMSC5734/DeGroot-Reaching_a_concensus.pdf) | Linear social averaging baseline; agreement alone is not proof of intelligence. |
| [Friedkin and Johnsen, Social influence and opinions, 1990](https://escholarship.org/uc/item/2r82w1vs) | Persistent attachment to initial information; alternative-model foundation. |
| [Bikhchandani, Hirshleifer, and Welch, 1992](https://www.journals.uchicago.edu/doi/10.1086/261849) | Informational-cascade mechanism and comparison. |
| [Golub and Jackson, 2010](https://www.aeaweb.org/articles?id=10.1257/mic.2.1.112) | Network influence and asymptotic social learning. |
| [Lorenz et al., 2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3107299/) | Human evidence for diversity loss and the accuracy/agreement distinction. |
| [Becker, Brackbill, and Centola, 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5495222/) | Evidence for beneficial networked social influence. |
| [Jayles et al., 2017](https://doi.org/10.1073/pnas.1703695114) | Controlled quantity and quality of social information. |
| [Binder, Critical Properties from Monte Carlo Coarse Graining and Renormalization, 1981](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.47.693) | Moment-based finite-size diagnostics. |
| [Hong, Ha, and Park, Finite-size scaling in complex networks, 2007](https://arxiv.org/abs/cond-mat/0701516) | Why network finite-size scaling needs its own justification. |
| [The random-field Ising model with asymmetric bimodal probability distribution, 2010](https://doi.org/10.1016/j.physa.2010.05.033) | Direct comparison for the proposed reference model; retrieve complete metadata. |
| [Du et al., Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325) | LLM debate baseline; verify final publication metadata. |
| [El et al., Physics of Agents, 2026](https://arxiv.org/abs/2608.16578) | Mandatory nearest-neighbor novelty comparison. |
| [Ann, Liu, and Tan, The Interaction Tax, 2026](https://arxiv.org/abs/2608.23541) | Mandatory comparison for communication-induced diversity loss and resource controls. |

Source-specific summaries in this plan are intentionally brief. Execution requires reading the relevant methods rather than treating these descriptions as sufficient evidence.

## 3. Hypotheses, estimands, and claim discipline

Use two primary confirmatory questions; treat the remaining questions as mechanistic or conditional analyses.

| ID | Prespecified hypothesis or question | Evidence | If unsupported |
|---|---|---|---|
| H1 | At some communication strengths, mean agent accuracy improves meaningfully over matched uncoupled agents. | Paired accuracy difference and interval; also compare group accuracy and the information oracle. | Report absence or resolution limit of a beneficial range. |
| H2 | Communication increases severe collective-error probability under at least one prespecified information condition. | Paired change in tail risk, accompanied by excess error covariance. | Report no resolved amplification within tested conditions. |
| H3 | Performance or ordering boundaries change systematically with population size and decision time. | Frozen size/time slices and uncertainty bands. | Report finite-size or finite-time behavior only. |
| H4 | An ordering boundary is consistent with a thermodynamic transition in a symmetry-controlled model. | Valid stationary sampling, multiple sizes, moment/response/scaling diagnostics, analytic benchmark. | Classify as crossover, metastability, or unresolved. |
| H5 | Shared input errors and communication interact rather than merely add. | Difference-in-differences in risk/covariance across communication and input correlation. | Report additive effects or uncertainty. |
| H6 | Topology or a specified intervention changes the benefit/risk tradeoff at matched resources. | Paired graph-family or intervention comparison, relevant network descriptors, held-out confirmation. | Limit claims to tested topologies and ineffective interventions. |

Primary effect sizes are accuracy difference and absolute severe-error risk difference. Set the default smallest effect of practical interest to 0.02 for each. These are research-design choices, not universal scientific constants. Freeze or revise them using domain relevance before confirmatory data are generated.

The project succeeds if it produces a reproducible, sufficiently resolved answer to H1/H2 and an honest classification of H3/H4. It does not succeed merely by making an attractive heatmap.

## 4. Reference model: exact specification

### 4.1 Variables and controls

Each episode has a hidden truth `Y` in `{-1,+1}`, sampled with equal probability. There are `N` agents, an undirected communication graph with adjacency matrix `A`, private signals `S_i`, and public decisions `a_i(t)` in `{-1,+1}`. An episode consists of one graph, one truth, one vector of private signals, one initial decision vector, and one stochastic trajectory.

| Symbol | Meaning | Default |
|---|---|---|
| `N` | Population size | 256 for discovery; 64–2048 for size analysis |
| `q` | Probability that a private signal equals truth | 0.50–0.90 |
| `J` | Strength of social influence in the decision rule | 0–4 |
| `H` | Weight attached to one private signal | 0.5 |
| `rho_in` | Pairwise correlation of private signals conditional on truth | 0 initially; 0.10 and 0.25 for shared-source tests |
| `W` | Symmetric normalized interaction matrix | `A/k` on degree-`k` regular graphs |
| `k` | Degree of reference random-regular graph | 8 |
| `T` | Observation horizon in sweeps | 200 |
| `beta` | Inverse decision-noise scale | 1; fixed by units |

Vary `q` and `J` independently. `H` remains fixed in the primary model: agents do not automatically know or recalibrate to true signal reliability. This is a bounded-decision model. Include calibrated use of reliability as an ablation, not a silent substitution.

### 4.2 Independent private information

For `rho_in = 0`, independently draw `S_i = Y` with probability `q`, otherwise `S_i = -Y`. Keep signals fixed throughout an episode: the agents repeatedly use the same evidence. The evaluator knows `Y`; the agents receive only their own `S_i` and accessible public decisions.

At `q = 0.5`, signals carry no truth information. At `q > 0.5`, their distribution favors the truth. Primary scientific analyses use `q >= 0.5`. Include `q < 0.5` and `q = 1` only as validation or explicitly labeled stress tests.

### 4.3 Correlated private information with unchanged marginal quality

To manipulate dependence without changing `q`, use the following latent-source generator:

1. Let `c = sqrt(rho_in)`.
2. Draw one shared signal `Z`, correct with probability `q`.
3. Independently for each agent, draw a private signal `U_i`, correct with probability `q`, and a copy indicator `B_i ~ Bernoulli(c)`.
4. Set `S_i = Z` if `B_i = 1`; otherwise set `S_i = U_i`.

Then `P(S_i = Y) = q` and, for nondegenerate `q`, `Corr(S_i,S_j | Y) = rho_in` for distinct agents. Derive and test this identity. `rho_in = 1` is the all-shared extreme. Dependence comes from a common input, not from communication.

Store the latent-source state for analysis, but never expose it or the truth to ordinary agents. With positive correlation, an uncoupled population is already dependent; call `J = 0` **uncoupled**, and reserve **independent** for the condition with independent inputs and randomization conditional on truth.

### 4.4 Network normalization

The reference network is a connected random 8-regular simple graph, with `W_ij = A_ij/8` and zero diagonal. The fully connected analytic benchmark uses `W_ij = 1/(N-1)` for distinct agents.

For heterogeneous undirected graphs, use `W = A/<k>` as the primary comparison: it is symmetric and fixes average input strength while permitting high-degree agents to receive more total influence. Also run `W_ij = A_ij/k_i` as a robustness check. This second choice fixes each node's total incoming weight but is generally asymmetric. Do not apply the symmetric-model equilibrium distribution to that variant.

Record degree distribution, realized average degree, component sizes, clustering, path-length summary, modularity where appropriate, spectral radius of `W`, and weight normalization. Keep degree approximately fixed as `N` grows in sparse graph families. The complete graph is a separate dense family.

### 4.5 Initialization and updates

Initialize each public decision independently given its private signal:

`P(a_i(0) = +1 | S_i) = sigmoid(2 H S_i)`.

For each update event, choose one agent uniformly with replacement. Given the current state, set

`f_i = H S_i + J sum_j W_ij a_j`,

`P(a_i(new) = +1) = sigmoid(2 f_i)`.

Here `sigmoid(x) = 1/(1+exp(-x))`; use a numerically stable implementation. One sweep is exactly `N` such update events. Record states/metrics at the end of a sweep. Use the state already updated by earlier events in that sweep.

At `J = 0`, public decisions have marginal accuracy

`p0(q,H) = [1 + (2q-1)tanh(H)]/2`.

This is generally different from `q`. It distinguishes signal quality from imperfect decision use. Include the direct private-signal decision `a_i = S_i` as an additional comparator, whose accuracy is `q`.

Truth never appears in an update field. Ground truth may only enter the data generator, scorer, analytic benchmark, and explicitly labeled diagnostic initializations/interventions.

### 4.6 Finite-time and equilibrium studies are separate

The primary decision study measures the terminal state at the fixed horizon `T`. It has no burn-in: early dynamics are part of the decision process. Also retain prespecified checkpoints to measure time dependence.

For symmetric `W` and fixed signals, the asynchronous rule has stationary distribution

`pi(a | S,G) proportional to exp[H sum_i S_i a_i + (J/2) sum_ij W_ij a_i a_j]`.

Validate this distribution by exact enumeration for small systems. It connects the model to an established random-field Ising system; do not present that connection as novel. At every finite `N` with finite fields the stochastic chain can, in principle, switch configurations. Long-lived wrong consensus is not automatically an absorbing state or a separate equilibrium phase.

Equilibrium samples require independent convergence and mixing checks. A stationary distribution may be studied with accelerated sampling, but accelerated sampling cannot estimate physical decision times or escape times.

### 4.7 Initial-condition diagnostics

In addition to the natural initialization above, use four explicitly labeled diagnostic starts: all `+1`, all `-1`, uniformly random public decisions, and public decisions equal to private signals. Truth-aligned and truth-opposed starts can be derived from the first two, but are diagnostic interventions unavailable to ordinary agents.

Compare starts on identical graph/signal instances to identify basins, path dependence, and slow mixing. Never average adversarially initialized failure rates into the natural-start failure rate.

## 5. Analytical work before large simulation

### 5.1 Mandatory baseline derivations

Produce `analysis/derivations.md`, with algebra, assumptions, numerical checks, and references.

1. Derive `p0(q,H)` and verify that truth flipping changes signed decisions but not accuracy distributions.
2. For independent Bernoulli correctness probability `p`, derive group-majority accuracy:
   `B_N(p) = P[Binomial(N,p) > N/2] + 0.5 P[Binomial(N,p) = N/2]`.
   Use it with `p = p0` for uncoupled public decisions and `p = q` for raw signals. It applies to fixed-time states under the specified independent initialization, not an uninitialized chain.
3. For independent equal-quality private signals and equal truth priors, show that the raw-signal likelihood ratio is `log(q/(1-q)) sum_i S_i`. Thus majority vote on raw signals is Bayes optimal for `q > 0.5` under this information model.
4. State the consequence: a communication protocol accessing only those same fixed signals cannot outperform the centralized Bayes decision in expected zero-one loss. Improvement over noisy individual decisions is still meaningful. A measured oracle violation beyond sampling uncertainty is a bug, information leak, mismatched information budget, or incorrect assumption until resolved.
5. Derive the correlated-input likelihood by marginalizing the shared source:
   `P(S=s | Y=y) = sum_z P(Z=z | Y=y) product_i [(1-c) P(U_i=s_i | Y=y) + c 1(s_i=z)]`.
   Compute both truth likelihoods using log-sum-exp. Do not call ordinary majority vote Bayes optimal under this latent mixture without checking.
6. Derive the marginal quality and pair correlation of the shared-source generator.
7. Derive the equilibrium distribution in Section 4.6 and detailed balance for a single-site heat-bath update.

### 5.2 Mean-field prediction

For independent signals and a fully connected population, truth-align the decisions and use the empirical correct-signal fraction `q_hat` in the finite-instance approximation. In the large-population independent-input limit `q_hat -> q`:

`F(m) = q tanh(Jm + H) + (1-q) tanh(Jm - H)`.

The approximate dynamical equation in sweep units is `dm/dt = -m + F(m)`. Fixed points solve `m = F(m)`; local stability requires `F'(m) < 1`. Here

`F'(m) = J [q sech^2(Jm+H) + (1-q) sech^2(Jm-H)]`.

Compute all roots on `[-1,1]`, not just the root reached by one iterative solve. Use bracketing on a fine mesh plus extrema/tangency checks, continuation from both directions, and root-merger conditions `m=F(m), F'(m)=1`.

At `q = 0.5`, the mean-field symmetry-breaking instability is at `J_c = cosh(H)^2`, approximately 1.27154 for `H = 0.5`. This is an analytic reference for this model and normalization, not a prediction to impose on sparse graphs. At `H = 0`, the fully connected benchmark has `J_c = 1` in the large-size limit.

For `q != 0.5`, the information distribution breaks truth-flip symmetry within a truth-aligned ensemble. A sharp-looking plot need not retain the zero-bias transition. Locate stable and metastable branches; do not assume a line of three thermodynamic phases across the entire `(J,q)` plane.

With shared inputs, the empirical correct-signal fraction can remain random as `N` grows. Conditional on a correct shared source, it tends to `q + c(1-q)`; conditional on a wrong shared source, it tends to `(1-c)q`. Solve the corresponding conditional mean-field branches and mix their predictions. Substituting only marginal `q` would erase the mechanism under study.

### 5.3 Distinguishing stable from metastable branches

For the fully connected independent-signal model, evaluate the mean-field free-energy density, up to an additive constant:

`f(m) = J m^2/2 - q log[2 cosh(Jm+H)] - (1-q) log[2 cosh(Jm-H)]`.

Compare local minima and their depths. A locally stable wrong branch is not necessarily the global equilibrium state. Keep numerical trajectory results, dynamical stability, and thermodynamic stability in separate tables.

Optional after the mandatory derivations: use a cavity or pair approximation for sparse graphs. A spectral linearization of a mean-field approximation is an approximation, not an exact sparse-network theorem. Explicitly assess its error against simulation.

**Gate THEORY:** Baselines are derived; exact small-system and zero-coupling checks are specified; the model's relationship to established theory is documented. No new theorem is claimed from numerical fitting alone.

## 6. Observables and regime definitions

### 6.1 Episode-level observables

For each recorded time define

`m = mean_i a_i`, `r = Y m`, `L = mean_i 1(a_i != Y) = (1-r)/2`.

| Quantity | Definition | Purpose |
|---|---|---|
| Mean agent accuracy | `A_ind = E[1-L]` | How well a typical agent uses accessible information. |
| Group accuracy | `A_grp = E[1(r>0) + 0.5*1(r=0)]` | Accuracy of majority vote; half-credit for ties avoids extra scoring noise. |
| Agreement/order | `M = E[abs(m)]` and full `m` distribution | Alignment without confusing it with correctness. |
| Severe collective failure | `F_0.9 = P(L >= 0.9)` | At least 90% of the population is wrong. |
| Majority failure | `P(L>0.5)` plus separately reported ties | Ordinary group error without requiring consensus. |
| Tail severity | 90th/95th/99th percentiles of `L`, where estimable | How bad high-loss episodes become. |
| Communication benefit | `Delta A_ind = A_ind(J)-A_ind(0)` | Paired improvement over uncoupled decisions. |
| Group benefit | `Delta A_grp = A_grp(J)-A_grp(0)` | Separate group-level benefit. |
| Excess catastrophe risk | `Delta F = F_0.9(J)-F_0.9(0)` | Failure amplification at fixed information. |
| Oracle gap | `A_oracle - A_grp` | Information left unused or distorted. |
| Decision time | First entry into `abs(m)>=0.8` sustained for 10 sweeps | Time to substantial agreement; right-censor if absent. |
| Wrong-consensus escape | First subsequent `r>=0` after a declared wrong-consensus start | Lifetime diagnostic; right-censor if absent. |

For even `N`, implement all thresholds using integer counts, e.g. `n_wrong >= ceil(0.9*N)`. Keep terminal tail risk distinct from ever entering failure during a trajectory. Prespecify the terminal measure as primary.

### 6.2 Error covariance and effective population size

Estimate dependence from repeated episodes at the same condition, not from a single terminal state. Use correctness indicators `e_i = 1(a_i != Y)`. Condition on graph and experimental cell, or use the explicitly specified graph-mixture population consistently.

Let `p_i = E[e_i]`, `v_bar = mean_i p_i(1-p_i)`, and let `C_bar` be mean covariance over distinct agent pairs. Then

`Var(L) = v_bar/N + (N-1) C_bar/N`,

`C_bar = [N Var(L) - v_bar]/(N-1)`.

Use this identity to avoid storing a full `N x N` covariance matrix. Estimate `p_i` and variance across independent signal instances, averaging trajectory replicates at the correct hierarchical level. Use sample covariance/unbiased variance conventions consistently and validate against a direct pairwise calculation on small data.

For interpretation, report `rho_eff = C_bar/v_bar` and `N_eff = v_bar/Var(L) = N/[1+(N-1)rho_eff]` when denominators are well determined. `rho_eff` is a variance-normalized covariance summary; with heterogeneous marginals it need not equal the mean of pairwise Pearson correlations. Report undefined values as missing with a reason, not zero. Do not clip negative dependence or `N_eff>N` out of the raw results.

Report `Delta C_bar` relative to matched `J=0`. Existing input correlation can generate covariance and error floors without any social interaction. Do not attribute all observed dependence to communication.

### 6.3 Operational regimes, without forcing a partition

Show continuous metric maps first. Add interpretive overlays only after uncertainty is available:

- **Uncoupled reference:** `J=0`; independent conditional on truth only if `rho_in=0`.
- **Beneficial interaction:** the lower interval bound for `Delta A_ind` exceeds 0.02. Also state whether group accuracy improves, is equivalent within ±0.02, declines, or is unresolved. Improved individual access to collective information does not require beating the raw-signal oracle.
- **Amplified collective failure:** the lower interval bound for `Delta F` exceeds 0.02 and excess covariance is positive with a resolved interval. State the underlying absolute risk as well as the increase.
- **Ordered accurate/wrong outcomes:** classify individual episodes by `r>=0.8` or `r<=-0.8`; these correspond to at least 90% correct or wrong. They are outcome labels, not automatically distinct phases.
- **Weakly affected behavior:** effects and excess normalized covariance lie inside prespecified equivalence intervals. Failure to reject a null alone does not establish independence or equivalence.
- **Mixed/unresolved:** retain this category whenever criteria overlap or uncertainty prevents classification.

Repeat tail/consensus overlays at 80%, 90%, and 95% agreement/error thresholds. Conclusions depending on one arbitrary cutoff must be described as threshold-sensitive. Keep accuracy and severe risk on separate panels because both can increase.

## 7. Baselines and controls

Implement these before the main experiments:

| ID | Comparator | What it isolates |
|---|---|---|
| B0 | Independent private-signal decisions `a_i=S_i` and their majority | Information quality before decision noise or communication. |
| B1 | `J=0` with identical signals, initialization law, and update schedule | Effect of communication at matched private information. |
| B2 | Majority of the original public decisions, retained as a frozen decision | Whether communication improves on simply aggregating what agents initially said. |
| B3 | Centralized Bayes decision from the same raw signals, using the correct generator | Information ceiling; handles correlated inputs by marginalization. |
| B4 | Linear social averaging with persistent private anchors | Whether nonlinear binary dynamics drive the observed effect. |
| B5 | Communication replaced by fixed initial neighbor decisions | Contribution of feedback and repeated circulation of decisions. |
| B6 | Directed one-pass, source-tagged dissemination of unique private signals | Diagnostic for information transmission without repeated counting of a source. |
| B7 | Same additional update opportunities with communication disabled | Effort-matched control for time or computation changes. |

B6 is a mechanistic comparator with a different message representation; record payload sizes and unique source counts. Compare at matched message volume where possible and disclose any remaining advantage. Never imply that a provenance-aware signal aggregator and one-bit imitation have equal information capacity by default.

For any change that introduces fresh evidence, give the matched control the same number and quality of fresh observations. Keep unchanging private evidence as the primary protocol. Count communication events, directed messages, edge reads, and approximate compute separately; `J` changes influence strength, not message count in the reference model.

## 8. Software and reproducibility architecture

### 8.1 Repository to construct

```text
README.md
RESEARCH_EXECUTION_PLAN.md
experiment_spec.json
AGENT_HANDOFF.md
pyproject.toml
<dependency lockfile>
src/collective_agents/
    cli.py
    config.py
    rng.py
    graphs.py
    signals.py
    dynamics.py
    baselines.py
    observables.py
    exact.py
    mean_field.py
    runner.py
    statistics.py
    scaling.py
    plotting.py
tests/
configs/{smoke,pilot,confirmatory,scaling,robustness}/
literature/{search_log.csv,evidence_matrix.csv,novelty_memo.md}
protocol/{frozen_protocol.md,deviations.csv,claim_registry.csv}
data/{raw,processed}/
results/{figures,tables,diagnostics}/
analysis/{derivations.md,results_summary.md,limitations.md}
paper/{when-communication-amplifies-error.tex,references.bib,sections,supplement,generated}/
execution/{state.json,run_manifest.parquet,resource_log.csv,decision_log.md}
release/
```

Use the available supported Python environment and pin exact installed versions. Appropriate dependencies are NumPy, SciPy, a graph library such as NetworkX, pandas/PyArrow, Matplotlib, pytest, and an acceleration library only if benchmarking justifies it. Verify current official documentation before adopting version-sensitive APIs. Keep the simulation callable without notebooks; notebooks may inspect already-generated results.

Implement both a clear reference update loop and an optimized engine. Use adjacency lists/CSR for sparse graphs. Use the running spin sum for the complete graph, excluding the updated node's own state. Avoid dense `N x N` arrays for ordinary simulations. Parallelize independent episode bundles only after correctness checks; keep random streams deterministic across worker counts.

### 8.2 Configuration and command contract

Every executable experiment configuration must specify: model version, graph family and parameters, weight normalization, `N,J,q,H,rho_in`, initialization, update rule, horizon, recording policy, graph count, signal-instance count, trajectory replicates, random seed namespace, experiment status, and resource cap. Reject unknown keys and invalid combinations.

Implement a module CLI with these interfaces or documented equivalents:

```text
python -m collective_agents.cli validate-config --config <path>
python -m collective_agents.cli estimate --config <path>
python -m collective_agents.cli run --config <path> --resume
python -m collective_agents.cli analyze --manifest <path>
python -m collective_agents.cli figures --analysis <path>
python -m collective_agents.cli audit --manifest <path>
python -m collective_agents.cli reproduce --profile smoke
```

`estimate` must enumerate jobs, anticipated spin updates, memory, storage, and measured runtime before launching a batch. `run --resume` must skip only completed jobs with matching hashes. `audit` must check completeness, uniqueness, provenance, and data/figure dependencies.

### 8.3 Randomization and pairing

Use a stable seed derivation based on a canonical tuple and a cryptographic digest or a documented `SeedSequence` hierarchy; never use Python's process-randomized `hash()`.

Use separate random streams for graph, truth, shared source, private signals, copy indicators, initialization, update indices, and heat-bath draws. Use distinct namespaces for smoke, exploratory, confirmatory, and audit datasets. Within a paired contrast, reuse graph, truth, signals, initialization, update indices, and uniform draws when mathematically valid. Exclude the varied parameter `J` from shared stream keys. Store the pairing identifier.

Across `rho_in` conditions, common uniforms can generate the relevant different copy rates while preserving each arm's law. Across sizes, nested graph construction is optional and must not distort the specified graph ensemble. Do not assume comparisons across unrelated graphs are paired.

Always analyze the covariance introduced by common random numbers through paired episode differences. One random seed per entire grid is not independent replication.

### 8.4 Data schema and storage

Each terminal row must include:

`run_id, config_hash, code_revision, stage, model, graph_family, graph_id, signal_id, trajectory_id, pair_id, seed_namespace, N, J, q, H, rho_in, normalization, initialization, update_rule, horizon, truth, latent_shared_correct, n_correct_signals, n_wrong, m, majority_score, severe_failure, elapsed_seconds, status`.

Maintain graph metadata and time-series tables separately, linked by identifiers. Keep per-agent terminal error indicators in packed binary form or another efficient representation so covariance can be reconstructed. Keep every terminal result and aggregate time series; store full agent trajectories only for a deterministic hash-selected subset and designated diagnostics. Do not select trajectories for retention based on whether they make attractive figures.

Write outputs atomically through a temporary target followed by rename. Record failed runs explicitly. A completed result must never be overwritten by a retry with another seed. Raw data are immutable; transformations write new processed artifacts with input hashes.

### 8.5 Required correctness checks

1. Graphs have the expected node count, no self-loops, expected symmetry, correct degree constraints, and declared component handling.
2. Signal generator empirical marginals and correlation agree with the analytic generator within prespecified Monte Carlo uncertainty.
3. `J=0` accuracy and group-majority results agree with `p0` and binomial formulas, including half-credit ties.
4. Global sign reversal preserves accuracy and maps signed observables correctly, preferably using matched randomness.
5. The oracle agrees with enumerated posterior probabilities for small `N`, including `rho_in=0`, intermediate values, and `rho_in=1`.
6. Exact state enumeration at `N<=12` yields the specified stationary distribution; transition rows sum to one; detailed-balance residuals for symmetric `W` are below numerical tolerance.
7. Stationary sampling agrees with exact moments for selected small graphs within Monte Carlo error, rather than an arbitrary decimal tolerance.
8. Sparse and complete-graph optimized updates match the reference field calculations; feed pre-generated update indices/uniforms to both engines for deterministic comparisons.
9. Metric calculations handle all-correct, all-wrong, tied, mixed, constant, and nearly constant data correctly. Direct pair covariance matches the aggregate identity.
10. Checkpoint/resume and changes in worker count preserve job identities and outputs within documented numerical reproducibility limits.
11. No dynamics call has access to truth, latent-source correctness, or scorer outputs.
12. Reproduce a known zero-field ordering benchmark before analyzing claimed criticality in the research model.

**Gate CODE:** These checks pass and a smoke run regenerates its table and figure. If a failure occurs, stop dependent simulations, fix the implementation, invalidate only affected outputs, and rerun the relevant checks. Never modify a scientific expectation solely to make a failing implementation pass.

## 9. Staged experiment schedule

The schedule deliberately separates exploration from confirmation. All values below are defaults. The pilot may change resolution, sample allocation, and resource estimates before the protocol is frozen; record any change. No confirmatory metric, population, or cutoff may be selected using confirmatory outcomes.

### E00: smoke and throughput

- Use `N=32`, random 8-regular graphs, `J={0,1,3}`, `q={0.5,0.7}`, `rho_in={0,0.25}`, `T=20`.
- Use 2 graph instances, 4 signal instances per graph, and 2 trajectories per signal instance: 192 trajectories over 12 parameter cells.
- Verify all schemas, checkpointing, pairing, metrics, and plot generation.
- Benchmark representative production sizes/graphs separately; smoke performance alone does not predict equilibrium or large-size cost.
- Deliver `results/diagnostics/smoke_report.md` and `execution/resource_estimate.md`.

### E10: exploratory communication-quality map

- Reference graph: connected random 8-regular; `N=256`, `H=0.5`, `rho_in=0`.
- `J = 0,0.25,...,4.0`: 17 values.
- `q = {0.50,0.525,0.55,0.60,0.65,0.75,0.90}`: 7 values.
- Natural initialization; `T=200`; record checkpoints `{0,1,2,5,10,20,50,100,200}`.
- Per cell: 10 graphs x 10 signal instances x 2 trajectories = 200 trajectories. Total: 23,800 interacting trajectories. Reuse the matched `J=0` references without counting identical simulations twice.
- Produce maps of accuracy, group accuracy, agreement, severe risk, and covariance. Mark all outputs exploratory.
- Repeat the same map at `rho_in=0.10` only if the measured cost fits the discovery allocation. If not, use the fixed slices `q={0.55,0.65,0.75}` and all 17 `J` values; choose the reduction based on projected cost before examining correlated-input outcomes.
- Deliver `analysis/pilot_report.md`: effect magnitudes, variance components, likely ceiling/floor problems, time dependence, runtime, selected confirmation cells, and reasons.

### E20: frozen confirmation of benefit and failure

Select anchor communication strengths from E10 using this deterministic rule:

1. Set the weak reference to `J=0`.
2. Choose one common intermediate anchor from interior grid values `0.25<=J<=3.75` by maximizing mean exploratory `Delta A_ind` over `q={0.55,0.65,0.75}` at `rho_in=0`. Ties within 0.005 go to the smaller `J`. Record that this is a selected candidate, not proof of an optimum.
3. Set the strong anchor to `J=4` regardless of its observed performance. If it duplicates another anchor, retain only unique cells.

Use these anchors with `q={0.55,0.65,0.75}` and `rho_in={0,0.10,0.25}`, at `N=256,T=200`. This is at most 27 cells including uncoupled references. Use fresh confirmation seeds. The intermediate-versus-zero and strong-versus-zero contrasts form the primary confirmatory family for H1/H2; every contrast is reported, including adverse or null outcomes.

Default per cell: 20 graphs x 50 signal instances x 2 trajectories = 2,000 trajectories, with 1,000 distinct graph/signal combinations. This is a starting allocation to be revised by the pilot power calculation, not a claim of 2,000 independent experimental units. Freeze the final allocation before running any confirmation episode.

Do not claim a continuous beneficial region from three communication anchors. Confirmation establishes effects at those anchors. To claim a boundary, use E30/E40 and fresh data around a frozen candidate interval.

### E30: population size and decision time

Use `N={64,128,256,512,1024,2048}`. Keep sparse degree 8. Select up to four slices before confirmation: independent-input beneficial candidate; independent-input strong coupling; correlated-input intermediate coupling; correlated-input strong coupling. Use `q=0.65` unless the pilot shows a complete accuracy/risk ceiling, in which case switch all four slices to `q=0.55` and record this before freezing.

For each slice and size, run 20 graphs x 25 signal instances x 2 trajectories. Record `T={50,200,1000}` from the same trajectory; account for this dependence in analysis. Include matched uncoupled controls and the same-information oracle.

Plot risk versus `N` separately at each fixed horizon and versus horizon separately at each fixed `N`. Test for declining risk, a positive floor over the observed range, or uncertainty. Do not infer a positive asymptotic floor from a short, flat finite-size curve. Fit competing decreasing-to-zero and positive-floor models with uncertainty and held-out-size prediction; qualify any extrapolation.

Add `T proportional to N` at one frozen representative slice if computationally feasible. State the constant and units. This addresses order-of-limits sensitivity; it is not interchangeable with either stationary sampling or fixed-time results.

### E40: transition diagnostics

This is mandatory if the paper uses “phase transition” as an empirical finding. It includes:

1. The `H=0` benchmark on the fully connected graph, with known large-size critical coupling 1.
2. The same benchmark on random 8-regular graphs, where the infinite locally tree-like reference condition is `(k-1)tanh(J/k)=1`. Verify its assumptions and source before using it; finite graphs have size corrections.
3. The research model at `H=0.5,q=0.5,rho_in=0`, using complete and random-regular graph families separately.
4. Nearby biased slices at `q={0.525,0.55}` to test rounding, metastability, and the relationship between ordering and performance boundaries.

Use the same six population sizes as E30. Explore a coupling window around the analytic or pilot boundary, initially 21 evenly spaced points over `J_center±0.5`, truncated at zero. For the sparse research model, estimate the center in a separate pilot. Refine to at least 7 points inside the peak/crossing window. Freeze the window and sampling rule for new confirmation seeds.

For stochastic graph families begin with 20 graphs x 10 signal configurations, with four chains per configuration from dispersed starts. For a complete graph, replace redundant graph replicas by 200 signal configurations; at `H=0` there is no signal disorder, so use independent chains rather than fictitious signal replicates. Final counts depend on mixing/precision and the resource gate.

Detailed diagnostics and decision rules are in Section 11. Do not label all E40 output equilibrium if mixing fails.

### E50: topology robustness

At frozen weak/intermediate/strong anchors and `q={0.55,0.65}`, compare:

- Random 8-regular reference.
- Erdos–Renyi graphs with `p=8/(N-1)`.
- Watts–Strogatz graphs starting at degree 8 with rewiring probability 0.10.
- A two-block stochastic block model with equal blocks and expected total degree 8: expected within-block degree 7, cross-block degree 1. Thus `p_in=7/(N/2-1)` and `p_out=1/(N/2)`.
- A preferential-attachment graph with 4 new links per arriving node, recording its actual mean degree.

Use `N={256,1024}`, `rho_in={0,0.10}`, and 20 graph replicas x 25 signal instances x 2 trajectories per cell if the budget permits. Prioritize the reference, modular, and heterogeneous-degree families; the other families are secondary and may be omitted with an explicit resource-based scope note.

Do not silently redraw disconnected graphs until connected for families where disconnectedness is part of the model. Retain all nodes and report components, or explicitly declare a conditioned connected-graph ensemble before generation. A giant-component-only analysis changes `N` and needs its own configuration.

Use symmetric average-degree normalization first, then row normalization on the reference and heterogeneous-degree families. Attribute differences to topology only after examining degree, normalization, components, and information allocation. The complete graph is a theoretical reference with a different communication cost.

### E60: mechanism and robustness experiments

Run the following on a small set of frozen cells, not the full Cartesian product:

1. Shared-input correlation `rho_in={0,0.01,0.10,0.25,0.50,1.0}` at fixed marginal `q`, with the correct latent-source oracle.
2. Private-evidence weights `H={0.25,0.5,1.0}`; treat possible changes in transition order as model changes requiring separate diagnosis.
3. Calibrated evidence `H(q)=0.5 log(q/(1-q))` for `0.5<=q<1`; explain that heat-bath posterior sampling and maximum-posterior action are distinct. At `q=0.5`, calibrated agents have zero informative field.
4. Natural, random, truth-aligned, truth-opposed, and direct-signal initializations, reported separately.
5. Synchronous updates versus the asynchronous reference, with matched per-agent update opportunities. Synchronous behavior need not share the same equilibrium law and may oscillate.
6. Frozen-neighbor decisions (B5) and source-tagged one-pass communication (B6).
7. The continuous-opinion model in Section 12.

If E20 finds no communication-induced severe failures, do not keep changing the model until one appears. Execute the prespecified stress tests, report their status, and explain which additional assumptions are needed for failure if any.

### E70: limited intervention study

Only after the mechanism is established, compare three frozen interventions at one beneficial and one failure-prone cell:

- Use the pilot-selected intermediate `J` in place of strong coupling.
- Reduce the shared-input fraction using distinct evidence sources while holding marginal `q` fixed.
- Transmit unique source-tagged signals without counting repeated copies as independent evidence, with measured message cost.

Freeze choices on exploratory data and evaluate them on fresh graphs/signals. Report accuracy, severe risk, communication volume, and added information/compute. An intervention may trade average accuracy for lower tail risk. Do not claim optimal control from these three candidates.

### Experiment priority under resource limits

Complete E00, E10, E20, and the essential E30 size/time slices first. Reserve E40 resources if a transition claim is intended. Then run B4/E60 alternative-model and input-correlation checks, followed by E50 and E70. The LLM extension is last unless it is the selected primary scope. Reduce secondary breadth before reducing the independence or validity of the primary sample.
