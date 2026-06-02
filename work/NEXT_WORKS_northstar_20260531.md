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

Status addendum, 2026-06-01: the predicted-atlas geometry novelty variants and
operating grid are rerun, and a review-only matched-retention delta audit now
compares them to the fold-augmented operating grid. Fold augmentation improves
all four matched retention targets, including +0.5444 OOS abstention and +0.5
cofactor-confounded OOS abstention at the 90% retention diagnostic. This does
not select a threshold.

### 2. Learned mechanism-feature embedding (the real northstar feature) — DONE (2026-06-01): clean negative + residual lead, now CONFIRMED + INTEGRATED
Two parallel implementations of this lever were pursued; both are recorded — (A) the
closed-form information-preserving metric (residual line), and (B) the standardized
nearest-primary centroid pilot (template-feature line, addenda below).

**(A) Closed-form information-preserving metric (residual line).** Built as a closed-form
supervised metric (sequence-only ESM2-150M; atlas-fit robust-standardize -> atlas-span PCA
-> within-class whitening), evaluated at the operating point. See decision_log 2026-06-01/02
and `work/mechanism_feature_embedding_current702_20260601.md`.
- The predeclared primary novelty score does NOT beat the top1_score baseline
  (AUC 0.616 vs 0.757; OOS-abstain-recall 0.165 vs 0.215 at >=90% retention).
  Supervised whitening distances (prototype/kNN ~0.61) confirm discriminative
  reshaping is the wrong lever for novelty.
- LEAD: the UNSUPERVISED out-of-atlas-span residual (representation mass outside
  known-mechanism directions) is genuinely new and orthogonal — AUC 0.721, and at
  the operating point abstains on 0.241 of OOS (> baseline 0.215), concentrated on
  the cofactor-agnostic majority. It is NOT confounded-safe (0.333 vs 0.500), so
  it is a complementary LIFT channel, not a gate.
- CONFIRMED (2026-06-01): the residual passed both predeclared gates. The PCA
  variance-cutoff sweep holds (deployment all-OOS AUC 0.707/0.722/0.721 at 95/97/99%,
  spread 0.014 — not a cutoff artifact) and the held-out-from-design confirmatory
  split passes (confirmation fold AUC 0.789, permutation p=0.0005; both folds clear
  the floor; agnostic>confounded replicates). See decision_log 2026-06-01 and
  `work/mechanism_feature_residual_robustness_current702_20260601.md`
  (`eval-mechanism-residual-robustness`).
- INTEGRATED (2026-06-02): the confirmed residual is wired into the per-channel RULE
  gate as a third confounded-safe agnostic-lift channel. At the operative >=85%
  retention floor it lifts OOS-abstain-recall 0.3038 -> 0.3797 (+0.076), entirely
  from the cofactor-agnostic subset, with the confounded subset UNCHANGED at 0.1667
  (confounded-safe). Caveat: the residual threshold is research-grade — 100% of
  held-out rows saturate the atlas residual range, so it is eval-pool-relative, not a
  deployable constant. See decision_log 2026-06-02 and
  `work/mechanism_residual_gate_integration_current702_20260601.md`
  (`eval-mechanism-residual-gate-integration`).
- NEXT (residual line): the operational gap is now precisely the confounded subset
  (still 0.1667). (a) close Lever 3 — a DEPLOYMENT-VALID confounded-safe channel
  (predicted-structure Foldseek/TM vs the atlas; the current fold eval uses
  experimental-PDB metadata and is not deployable); and (b) a deployable residual
  calibration (or the Lever 4 expanded family set) so the residual lift survives
  outside an eval-relative threshold. A trainable GNN over active-site reaction
  graphs remains a future lever once a deployment-valid predicted-geometry graph
  dataset exists.

**(B) Standardized nearest-primary centroid pilot (template-feature line).** A separate
take on the same lever (decision_log 2026-06-01, "Mechanism-Feature Embedding Pilot Is
Implemented, But Template-Dependent"); status below.

Current status addendum, 2026-06-01: the train/cal feature contract has now
been consumed by a real standardized nearest-primary centroid pilot, with a
once-only heldout readout. The full contract scores well only while the
reaction-template field is present; the no-reaction-template ablation is weak
on both calibration and heldout. The next embedding-gap action is no longer
another plan: materialize row-specific bond-change, proton-transfer, and
electron-flow features, rerun the no-template pilot/readout, and use the
template-dependent full-contract score only as a ceiling diagnostic.

Readiness addendum, 2026-06-01: the P0 source-evidence sidecar now has a
feature-readiness audit over draft bond/proton/electron events, but 0/15 rows
are approved or consumable. A bounded official Rhea lookup resolved `m_csa:124`
by accession to `RHEA:11436` / EC `7.1.1.9`, and a strict consumption audit
confirms it entered only the draft sidecar. Resolve the remaining three Rhea
lookup rows (`m_csa:11`, `m_csa:169`, and `m_csa:5`) and reviewer provenance
before any no-template feature-contract refresh.

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
