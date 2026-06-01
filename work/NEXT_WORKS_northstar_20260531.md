# Next Works — Northstar from D11 (as of 2026-05-31)

State of the northstar (a physically faithful continuous mechanism space that
supports de novo). The gate for de novo is **abstention on novelty working at a
deployable operating point**, not just in AUC.

## Where we are (committed)

- **De novo abstention is achievable in RANKING**: deployment-valid (predicted/apo
  geometry) two-channel gate reaches AUC 0.852, clears the 0.75 bar.
  (`5af7848`, `compute_deployment_gate`).
- **But NOT operational**: at 90% in-scope retention, no combiner gives a usable
  threshold — geometry-led catches only 19% OOS; the blind mean catches 59% but
  abstains on NONE of the safety-critical cofactor-confounded rows. (`6a2451f`).
- **Operational architecture settled**: per-channel RULE gate (geometry-led,
  cofactor-as-agnostic-lift, confounded-safe). Real but bounded lift only at 85%
  retention (OOS 0.139 -> 0.304). (`383fc69`).
- **Binding constraint identified = FEATURE OVERLAP**, not combiner/threshold.
  Geometry score distributions of known vs novel chemistry overlap hard (in-scope
  median 0.434, agnostic-OOS 0.370, confounded-OOS 0.358).
- **In-repo lever ruled out**: richer geometry sub-features (coherence, role/pocket/
  compactness, cofactor context) do NOT beat the collapsed top1_score (0.757);
  no headroom in what we already have. (`605e763`).

## The fork

The next gain must come from a **genuinely new mechanism-discriminative feature**,
evaluated AT THE OPERATING POINT (retention vs OOS-abstain-recall), not by AUC.
Ranked by leverage / cost:

### 1. Predicted-geometry retrieval over the in_distribution atlas (highest leverage, in-repo)
The deployment retrieval currently scores only the 126 held-out rows; there are
**zero predicted-geometry atlas rows**. This blocks every atlas-based method
(Mahalanobis novelty, atlas-percentile gates, learned class boundaries on the
deployment regime). Action: regenerate `predicted_geometry_retrieval` for the
~124 in_distribution rows too (same AlphaFold pipeline, same fields incl.
`role_match_fraction`), then rerun `eval-mechanism-deployment-abstention-gate`
and the atlas-Mahalanobis novelty path. This may itself lift the operating point
and unblocks #2.

### 2. Learned mechanism-feature embedding (the real northstar feature) — DONE (2026-06-01): clean negative + residual lead
Built as a closed-form, information-preserving supervised metric (sequence-only
ESM2-150M; atlas-fit robust-standardize -> atlas-span PCA -> within-class
whitening), evaluated at the operating point. See decision_log 2026-06-01 and
`work/mechanism_feature_embedding_current702_20260601.md`.
- The predeclared primary novelty score does NOT beat the top1_score baseline
  (AUC 0.616 vs 0.757; OOS-abstain-recall 0.165 vs 0.215 at >=90% retention).
  Supervised whitening distances (prototype/kNN ~0.61) confirm discriminative
  reshaping is the wrong lever for novelty.
- LEAD: the UNSUPERVISED out-of-atlas-span residual (representation mass outside
  known-mechanism directions) is genuinely new and orthogonal — AUC 0.721, and at
  the operating point abstains on 0.241 of OOS (> baseline 0.215), concentrated on
  the cofactor-agnostic majority. It is NOT confounded-safe (0.333 vs 0.500), so
  it is a complementary LIFT channel, not a gate.
- NEXT: a PREDECLARED confirmatory test of the residual as a third orthogonal lift
  channel (geometry-led + cofactor-agnostic-lift + residual-agnostic-lift), paired
  with a confounded-safe channel (Lever 3, fold) before any threshold promotion.
  A trainable GNN over active-site reaction graphs remains a future lever once a
  deployment-valid predicted-geometry graph dataset and a larger family set exist.

### 3. Fold-level novelty signal (complementary, catches the confounded subset)
The 6 cofactor-confounded OOS (novel chemistry reusing a known cofactor family)
are the hardest cases. A fold/structure-distance novelty signal (Foldseek/TM
against the atlas) is orthogonal to both current channels and should fire exactly
where geometry-confidence and cofactor are both fooled. Cheap to try if predicted
structures are available.

### 4. Expand the family set (de-risks the bound)
All claims are bounded to 8 fingerprints. The relationship/abstention numbers
organize THIS family set; they do not prove general physical fidelity. Targeted
dark-bin / near-orphan expansion (already scoped in earlier work) widens the
evaluable space and makes the novelty test meaningful.

## Guardrails (do not regress)
- M-CSA is eval/benchmark only, never training.
- Cofactor head input is sequence-only, never geometry-derived.
- Deployment test is predicted geometry; experimental numbers are teacher-side.
- Evaluate abstention at the OPERATING POINT, not AUC. Atlas-only statistics; no
  heldout tuning. OOS false positives are a hard gate.

## Reproduce the current gate
```
PYTHONPATH=src python -m catalytic_earth.cli eval-mechanism-deployment-abstention-gate
```
Module: `src/catalytic_earth/mechanism_abstention_gate_eval.py`
(`compute_deployment_gate` -> channels, operating curve, per_channel_rule_gate).
Tests: `tests/test_mechanism_abstention_gate_eval.py` (9). Full mechanism suite 23/23.
