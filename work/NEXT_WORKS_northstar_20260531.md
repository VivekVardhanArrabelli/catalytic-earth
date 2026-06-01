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

### 2. Learned mechanism-feature embedding (the real northstar feature)
Train a representation that answers to mechanism chemistry (electron flow,
transition-state stabilization, proton transfer, bond making/breaking), not to
the hand-feature list. Inputs sequence-only or sequence+predicted-geometry; label
signal from the 8-fingerprint atlas. Evaluate novelty separation at the operating
point. This is the de novo precondition's real lever; everything else is a probe.

Current status addendum, 2026-06-01: the train/cal no-fit feature contract is
still label-stripped and heldout-excluding. The row-specific bond-change gap is
now bounded into a 15-row P0 extraction worksheet plus a source-evidence sidecar
schema/audit plan. The next safe embedding-gap action is to fill that worksheet
from source-backed M-CSA/Rhea/mechanism evidence and audit the resulting sidecar
before any no-fit feature-contract refresh or model work.

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
