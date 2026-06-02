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

### 2. Learned mechanism-feature embedding (the real northstar feature) — DONE (2026-06): two builds integrated into one result
Two independent agent builds attacked this lever and are now integrated as a single
result, not two competing silos: a **closed-form information-preserving metric** (the
"residual line", sequence-only ESM2-150M; atlas-fit robust-standardize -> atlas-span PCA
-> within-class whitening) and a **standardized nearest-primary centroid pilot** (the
"centroid line", train/cal-fit with a once-only heldout readout). Both are kept; each
contributed a genuine advancement. See decision_log 2026-06-02 ("Lever 2 Integrated") for
the synthesis.

CONSOLIDATED NEGATIVE (robust because two independent builds agree): a learned or
standardized embedding over the CURRENT feature surface does NOT deployably beat the
geometry baseline.
- Residual line: the predeclared primary novelty score AUC 0.616 vs top1_score 0.757
  (OOS-abstain-recall 0.165 vs 0.215 at >=90% retention); supervised whitening distances
  (prototype/kNN ~0.61) confirm discriminative reshaping is the wrong lever. See
  `work/mechanism_feature_embedding_current702_20260601.md`.
- Centroid line: the full contract looks strong (calibration AUC 0.948, heldout 0.881)
  ONLY because of the reaction-template field; the deployment-valid no-template ablation
  is at chance (heldout AUC 0.489, 9.5% OOS abstention). Its own log says not to cite the
  full-contract scores as deployment evidence. Two independent negatives make this robust.
  See `artifacts/v3_mechanism_feature_embedding_pilot_current702_20260601.json` and
  `artifacts/v3_mechanism_feature_embedding_heldout_readout_current702_20260601.json`.

LIVE DEPLOYABLE SIGNAL (the surviving win, from the residual line): the UNSUPERVISED
out-of-atlas-span residual (representation mass outside known-mechanism directions) is
genuinely new, orthogonal, and deployment-valid (sequence-only) — AUC 0.721, abstains on
0.241 of OOS at the operating point (> baseline 0.215), concentrated on the cofactor-agnostic
majority. It is NOT confounded-safe (0.333 vs 0.500), so it is a LIFT channel, not a gate.
- CONFIRMED (2026-06-01): passes both predeclared gates — the PCA variance-cutoff sweep
  holds (deployment all-OOS AUC 0.707/0.722/0.721 at 95/97/99%, spread 0.014, not a cutoff
  artifact) and the held-out-from-design confirmatory split passes (confirmation fold
  AUC 0.789, permutation p=0.0005; both folds clear the floor; agnostic>confounded
  replicates). See `work/mechanism_feature_residual_robustness_current702_20260601.md`
  (`eval-mechanism-residual-robustness`).
- INTEGRATED (2026-06-02): wired into the per-channel RULE gate as a third confounded-safe
  agnostic-lift channel. At the operative >=85% retention floor it lifts OOS-abstain-recall
  0.3038 -> 0.3797 (+0.076), entirely from the cofactor-agnostic subset, the confounded
  subset UNCHANGED at 0.1667 (confounded-safe). Caveat: the residual THRESHOLD is
  research-grade — 100% of held-out rows saturate the atlas residual range, so it is
  eval-pool-relative, not yet a deployable constant. See
  `work/mechanism_residual_gate_integration_current702_20260601.md`
  (`eval-mechanism-residual-gate-integration`).

KEPT FROM THE CENTROID LINE (genuine advancements, retained and reused — not discarded):
- Stronger fitting hygiene: centroids fit on 418 train rows, threshold selected on 106
  calibration rows, with a once-only heldout readout — no heldout used for fitting or
  selection. This train/cal/heldout protocol is the standard the residual's deployable
  calibration should adopt.
- The forward feature path: the audited mechanism-feature contract surface plus the P0
  source-evidence sidecar with a feature-readiness audit over draft bond/proton/electron
  events (currently 0/15 rows approved/consumable). A bounded official Rhea lookup resolved
  `m_csa:124` to `RHEA:11436` / EC `7.1.1.9` (strict consumption audit confirms draft-only);
  `m_csa:11`, `m_csa:169`, `m_csa:5` and reviewer provenance remain open. This is the route
  to the genuinely-new mechanism feature the northstar actually wants.

UNIFIED NEXT (one path; both lines feed it):
(a) Materialize the centroid line's row-specific bond-change / proton-transfer /
    electron-flow features (resolve the three open Rhea rows + provenance first) — the
    genuinely-new, template-free mechanism feature.
(b) On that richer surface, re-run BOTH methods under the centroid line's train/cal/heldout
    discipline: the no-template centroid pilot AND the out-of-span residual. Use the
    template-dependent full contract only as a ceiling diagnostic.
(c) Give the confirmed residual a deployable calibration (or the Lever 4 expanded family
    set) so its +0.076 agnostic lift survives outside an eval-relative threshold.
(d) Close Lever 3 — a DEPLOYMENT-VALID confounded-safe channel (predicted-structure
    Foldseek/TM vs the atlas; the current fold eval uses experimental-PDB metadata and is
    not deployable) — since the residual is agnostic-only and the confounded subset is
    still 0.1667.
A trainable GNN over active-site reaction graphs remains a future lever once a
deployment-valid predicted-geometry graph dataset exists.

Reviewer-decision addendum, 2026-06-02: the remaining three P0 Rhea rows
(`m_csa:5`, `m_csa:11`, and `m_csa:169`) were checked against bounded Rhea
EC/accession queries and current UniProtKB catalytic-activity records. Rhea
returns 0 records; UniProt confirms matching EC activities but provides no Rhea
cross-references. Vivek Vardhan Arrabelli approved all three as
M-CSA-only source evidence with reviewer provenance. The strict sidecar audit
passes with 3 approved consumable rows, the Rhea lookup manifest is empty, and
the refresh-blocker audit allows only partial train/cal feature materialization
for those 3 rows. Do not run a full P0 refresh until the remaining 12 draft
rows are reviewed, and never train or tune thresholds on heldout M-CSA rows.

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
