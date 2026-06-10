# Scaling Plan to 10k Mechanism Labels

Status: durable plan (2026-06-10). This is an entry point for future agents. Read
this first, then verify every claim below against its source before acting — see the
**"Sources & where to verify"** table near the end, which maps every element of this
plan to the exact `docs/decision_log.md` entry, module, artifact, or test. Two
grounding errors in the session that produced this plan (ESM2, and apo-vs-holo
promotion confirmability) both came from asserting decision-claims without first
reading the log. Treat any performance/promotion/capability claim as requiring a
decision-log citation.

---

## The one reframe everything depends on

**10k is not 10k rows. It is a balanced, non-redundant mechanism atlas where the
frozen 702 benchmark never moves and every label earns its place.** The repo's own
findings force this:

- Broad out-of-scope draining is **saturated** — a page-3/4 continuation over
  high-yield lanes "produced 2,793 continuation candidates but added **0** new
  candidate IDs"; the lesson is to split into new EC/keyword subqueries, not
  increase page depth (`decision_log.md`, handoff 2026-06-09).
- The positive classes are **30.8× imbalanced** (fingerprint Gini 0.51,
  positive:OOS 0.42) — coverage/redundancy governor, 2026-06-10.
- **26.7%** of what we already imported (456 of 1,710) would be re-throttled as
  near-duplicates by the novelty gate, concentrated in out_of_scope (373) and
  `metal_dependent_hydrolase` (71) — novelty gate self-audit, 2026-06-10.

So raw count is not the constraint; **diverse, honest supply is.** Chasing 10k of
the current 8 fingerprints by volume would manufacture redundancy and violate the
values.

---

## What is fixed, by our values (non-negotiable)

- **The frozen 702 benchmark is sacred.** `data/registries/curated_mechanism_labels.json`
  = 702 labels (562 in-distribution + 140 heldout); `coherence_audit_702` baseline;
  eval contract `sha256:731b94ebd3b4f7ae483a3cca75d2b8c3b88242024ecd9c364d70bdfcda6624ee`.
  All three are pinned by regression tests (`tests/test_geometry_artifact_regression.py`).
  The atlas grows in the **separate** expansion registry
  `data/registries/external_bronze_labels.json`; the benchmark is byte-unchanged. A
  v2 benchmark, if ever needed, is a **new** expert-reviewed freeze, never an edit of
  this one. The spent one-shot heldout read must not be re-run or tuned against
  (2026-06-04).
- **The leakage wall is absolute.** EC / protein-name / UniProt prose / curated text
  / `target_family_lane` stay in `excluded_context`, never predictive features; EC
  may decide **scope only**. Enforced in code by
  `labels._validate_external_out_of_scope_evidence_separation` and by
  `tests/test_leakage_closure.py`; the representation loop's featurizer has a unit
  test that mutates EC+name+lane+fingerprint and asserts the features are
  byte-identical.
- **The label gate is the only door in** (`src/catalytic_earth/`):
  `external_annotation_anchored_import.classify_row` (default = **HOLD**; a positive
  requires an annotation lane mapped to a fingerprint **and** the matching annotated
  cofactor class) → `labels.MechanismLabel.from_dict` (schema + leakage-separation
  validation) → `external_annotation_anchored_import.apply_external_annotation_anchored_import_to_registry`
  (dedup vs **both** registries, re-validate every label, **non-destructive
  append**, writes only the expansion registry). Nothing bypasses this. Review
  artifacts are **not** imports.
- **Bronze is honest.** `tier=bronze`, `review_status=automation_curated`,
  `evidence_basis=reviewed_swissprot_ec_rhea_cofactor_annotation`; structure/geometry
  confirmation is a **deferred** bronze→silver signal, not faked (2026-06-09 "the 10k
  unlock").
- **Do not scale model size.** The representation shootout settled it
  (`docs/wave1_representation_shootout.md`, 2026-05-26): ESM-2 150M (primary acc
  0.578), ESM-C, ProtT5, SaProt all **underperform** Foldseek (0.622) and the
  geometry baseline (1.000 on dense/near-orphan bins). "Do not scale models first."
  The Northstar Pivot (2026-05-31) showed the binding constraint is **feature
  overlap**, not the combiner. Use chemistry/geometry features only. The learned
  mechanism-feature embedding (Lever 2) is a recorded clean **negative** — it does
  not deployably beat geometry.
- **Safety scope** (`docs/safety_scope.md`): beneficial enzyme function only;
  outputs are hypotheses/candidates requiring wet-lab validation; never "confirmed"
  / "validated" without experimental backing.

---

## The pipeline (every new label runs this, in order)

```
reviewed UniProt/Swiss-Prot row (EC + cofactor + Rhea + active-site residues)
  → classify_row          scope from annotation; positive needs cofactor corroboration; else HOLD
  → governor              is this fingerprint/lane a hole / under-floor / over-cap?   (build-coverage-redundancy-audit)
  → novelty gate          admit only if it adds a new cluster/reaction/organism; throttle near-dups   (build-novelty-admission-gate-audit)
  → from_dict + writer    schema + leakage gate; dedup vs BOTH registries; non-destructive append
  → (later) promotion     bronze→silver ONLY via cofactor restoration/fusion, never apo geometry   (build-bronze-silver-promotion-preview)
```

The governor and novelty gate make growth diverse **by construction**; everything
else already existed. All four CLI tools above are non-destructive (write only to
`artifacts/` + `work/`, never a registry).

---

## The stages

### Stage 0 — Unblock sourcing (environment)
The cloud sandbox blocks UniProt (HTTP 403) and lacks mmseqs / ML backends, and the
hand-curated candidate pools are **drained**. A local/laptop env restores real
UniProt network and (on Mac) mmseqs. Nothing downstream proceeds without this.
Guardrails travel with the work regardless of env.

### Stage 1 — Close the holes (≈339 positive labels; highest value)
Source the holes and under-floor fingerprints to the **100-floor**, via targeted
EC/keyword **subqueries** (not deeper pages). Cap `metal_dependent_hydrolase` (308,
over the 250 ceiling, most redundant at 2.96 labels/distinct-reaction) — add none.

| fingerprint | combined | status | route |
| --- | --- | --- | --- |
| `ser_his_acid_hydrolase` | 42 (0 expansion) | HOLE | triad locator + acquisition contract: EC 3.4.21/3.4.16/3.1.1, **no cofactor**, coordinate Ser-His-Asp triad corroborated against annotated ACT_SITE (`build-ser-his-triad-locator-scan`). The one fingerprint the cofactor engine structurally can't reach. |
| `radical_sam_enzyme` | 10 | HOLE | disambiguation rule (Fe-S+SAM / CX3CX2C). The representation loop already proposed **14 candidates from our own OOS pile** — start there + fresh sourcing. |
| `cobalamin_radical_rearrangement` | 10 | HOLE | disambiguation rule (adenosylcobalamin + mutase EC 5.4.99/5.4.3/4.2.1.28/30/4.3.1.7). |
| `flavin_monooxygenase` | 43 | under-floor | EC 1.14.13/1.14.14, flavin no-heme. |
| `heme_peroxidase_oxidase` | 69 | under-floor | EC 1.11.1, heme. |
| `flavin_dehydrogenase_reductase` | 87 | under-floor | EC 1.3/1.6/1.8.1, flavin no-heme. |

Everything routes through the governor + novelty gate so orthologs are not
re-imported.

**Runnable now:** the two **cofactor-defined** holes (`radical_sam_enzyme`,
`cobalamin_radical_rearrangement`) have an end-to-end runner —
`scripts/stage1_source_holes.py` (module `stage1_hole_sourcing.py`) — that chains
fetch → cofactor/EC disambiguation → novelty gate → non-destructive preview
(`--apply` appends to the expansion registry only). It needs **live UniProt egress**.
`ser_his_acid_hydrolase` is cofactorless and stays on `build-ser-his-triad-locator-scan`.
See `docs/stage1_hole_sourcing_runbook.md`. Triage the existing held pools (Pending
candidate inventory above) through the same gate alongside fresh sourcing.

### Stage 2 — Grow the ontology (the bulk of the climb)
8 fingerprints × 250 cap ≈ **2,000 positives max** — so 10k honestly **requires more
mechanism families**. The coherence audit already flags this: `metal_dependent_hydrolase`
is a coarse bucket collapsing proteases/nucleases/phosphatases/deaminases, queued as
v2 splits. This is the repo's **Lever 4 — expand the family set**. Each new family /
v2 split is added the same disciplined way:

1. Define the fingerprint spec in `data/registries/mechanism_fingerprints.json`
   (cofactor chemistry + active-site residue-role signature + reaction-center bond
   change) and the family node in `data/registries/mechanism_ontology.json`.
2. Add a cofactor+EC rule to `external_cofactor_ec_disambiguation.DISAMBIGUATION_RULES`
   and lane mappings to `external_annotation_anchored_import.LANE_PRIMARY_FINGERPRINT`
   / `COFACTOR_FOR_FINGERPRINT`.
3. **Declare the family's deploy-missing active-site context type** — what the
   apo predicted structure *lacks* and how (or whether) to reconstruct it: cofactor,
   metal, substrate, PTM, oligomeric interface, ordered water, or **none** (e.g. a
   cofactorless catalytic-triad hydrolase loses nothing on apo). See "Reconstructing
   deploy-missing active-site context" below; this drives whether/how the family can
   ever reach silver.
4. Source annotation-anchored bronze under the governor + novelty gate.

Breadth of chemistry, not depth of one bucket, is where 10k comes from.

### Stage 3 — Diverse OOS, novelty-gated
OOS is the abstention target and must keep growing in **coverage**, not redundancy.
Route every candidate through the novelty gate's cluster key
`(scope, full-EC, organism, sequence-length bin)`; admit only new
clusters/reactions/organisms. On Mac, upgrade the gate's metadata near-dup proxy to
true **mmseqs sequence clustering** — a strictly better dedup dimension than
metadata.

### Stage 4 — Bronze→silver promotion, the honest way
Promotion is gated by **deploy-missing active-site context presence in the
coordinates** — for the current cofactor-dependent families that means the cofactor,
and 103/104 of our coordinate-bearing rows are **apo** (cofactor absent), so the
geometry inverse-gate abstains on 100% of apo (the documented Problem-2 degradation;
experimental-apo and predicted-apo both abstain). So promotion does **not** wait for
more predicted structures — it waits on **reconstruction** of the missing context.
For the cofactor families the working lever is cofactor restoration/fusion
(restoration recovers 22/22 lost primaries; the fused sequence→cofactor channel
lifted heldout 23→37/45, one-shot **spent** — do not re-run). Run it (locally, with
backends) over the promotion preview's chemistry-corroborated queue; resolve the
**51 representation-loop review-outliers** (chemistry disagrees with the label)
first. Silver is earned per-row, never bulk-flipped. **Reconstruction is not
"cofactor" for every family** — see the next section.

### Stage 5 — A v2 benchmark, only when the atlas is broad
A 702-row benchmark over 8 families cannot validate a 10k atlas across many
families. When Stage 2 has matured the ontology, freeze a **new** expert-reviewed v2
benchmark (its own SHA; conjunctive win condition — mechanism prediction **and**
calibrated abstention on tail/hard-negative cases; cluster-bootstrapped, not
entry-bootstrapped). The current 702 stays frozen forever as the v1 anchor.

---

## Pending candidate inventory (as of 2026-06-09) — triage these before re-sourcing

A large multi-family intake already ran (Wave 2 + the seven family shards). **Nothing
was lost and almost nothing was force-imported** — the candidates are preserved as
preview/queue artifacts and sit behind the gate. Before sourcing anything fresh
(Stages 1–3), work these queues through the **governor + novelty gate** first; this
intake predates both, so expect a large fraction to be throttled as near-duplicates
or dropped as already-covered.

**The 12,495-candidate review surface** (`v3_external_import_review_preflight_current702_20260609.json`,
`terminal_state_counts`):

| terminal state | count | disposition |
| --- | --- | --- |
| `controlled_import_review_ready` | **275** | machine-clean; **queued for explicit human batch approval — not imported** (`v3_external_import_review_ready_preview_current702_20260609.json`) |
| `repairable_coordinate_blocker` | 5,179 | needs coordinates (network/local) |
| `hard_blocked_with_next_action` | 2,904 | blocked |
| `reject/OOS_preserve_signal` | 1,562 | rejected |
| `duplicate_external_conflict` | 1,275 | already in the expansion registry |
| `repairable_locator_blocker` | 1,096 | needs an active-site locator |
| `duplicate_current702_conflict` | 203 | already in the frozen 702 benchmark |
| `needs_structural_duplicate_screen` | 1 | — |

(275 ready + 12,220 in the repair/blocked queue, `v3_external_import_review_repair_queue_current702_20260609.json`.)

**What was imported from these pipelines (the 1,710 now in the registry)** — only the
cofactor-corroborated / clear-OOS / clean-screen rows passed the gate:
- 186 — original Wave 2 annotation-anchored import.
- 1,381 — scale-out **drain** of the already-materialized import-ready pools (2,426
  rows → 1,389 import decisions; **1,037 held** = 743 cofactor-confounded redox + 129
  no-cofactor + 107 ambiguous + 58 unmapped; `v3_external_scaleout_bronze_import_preview_current702_20260609.json`).
- 143 — cofactor/EC disambiguation recovering held redox/radical lanes (still **~730
  held** for lacking unique cofactor+EC corroboration;
  `v3_external_cofactor_ec_disambiguation_preview_current702_20260609.json`).

**Implications for the plan:** (1) the ~6,275 coordinate/locator-blocked rows resolve
in a **local env** (network/backends) — they are a Stage-0/1 unblock, not lost work;
(2) the ~1,478 duplicates and the held lanes are exactly what the novelty gate exists
to screen; (3) the 275 clean rows still require explicit human authorization +
label-factory gates (review ≠ import) — and should pass the governor/novelty gate
before any merge, so they grow diversity rather than re-saturate. Do **not** re-run
deeper-page sourcing on the same lanes (it added 0 new candidates last time); split
into new EC/keyword subqueries instead.

---

## Reconstructing deploy-missing active-site context (cofactor is the v1 instance, not the whole story)

This is a **parallel axis, not a stage**. The count/diversity stages above reach 10k
*bronze* labels and **do not need reconstruction at all** — annotation-anchored scope
decouples the label from geometry. Reconstruction is the **quality/deploy axis**: it
is what lets a label earn silver and what lets the atlas predict mechanism for novel,
unannotated sequences (the North Star). Run it where the count climb does not — and
do not confuse the two.

**The general problem (not "cofactor"):** the router was validated on experimental
active-site geometry but deploys on a predicted **apo** structure, which lacks
whatever active-site *context* the experimental one carried. Per the 2026-06-04
"Problem 2 Solution Architecture — Reconstruct Deploy-Missing Context From Sequence"
entry, verbatim: *"For the v1 families that context is the cofactor/metal; for future
classes it will be substrate, metal, PTM, oligomeric interface, or ordered water."*
So the lever is **"reconstruct the deploy-missing active-site context from the only
deploy-available signal (sequence), and abstain when you cannot"** — cofactor is the
first instance because the current eight are mostly cofactor-defined, **not** a
universal rule.

**Per-family, the missing context differs:**

- **7 cofactor-dependent fingerprints** (metal, PLP, flavin-monooxygenase, flavin-DR,
  heme, radical-SAM [Fe-S+SAM], cobalamin) — the missing context is the
  cofactor/metal. This is where the 22/22 `cofactor_apo_loss` came from
  (2026-06-03 "Predicted-Geometry Degradation Is Cofactor-Loss-Dominated").
- **`ser_his_acid_hydrolase` is cofactorless** — its catalysis is the Ser-His-Asp
  protein triad, which is *present in the apo structure*. **Nothing to reconstruct**;
  it degrades far less on apo, and its confirmation is the triad geometry itself
  (which is exactly why `build-ser-his-triad-locator-scan` runs on apo coordinates).
- **Even within cofactor families, not every row needs it.** Control in the
  decomposition: 13/23 correctly-called primaries also had an experimental cofactor —
  apo sufficed for them. The loss hits only rows where the cofactor is load-bearing
  for the geometry signal.
- **Future families (Stage 2)** declare their own missing-context type (Stage-2
  checklist item 3), possibly **none**.

**The two reconstruction paths (2026-06-04 architecture):**

- **Path A — sequence→context feature channel (default).** Predict the missing
  context (for cofactor families: cofactor presence) from sequence, **train/cal
  only**, and fuse it where the experimental `ligand_context` plugged into the router.
  Measured: in-distribution out-of-sample recovery **30/35 (70.6%)**, 0 regressions
  (`cofactor_presence_calibration.py` / `sequence_cofactor_channel.py`); the spent
  heldout one-shot went **23 → 37/45** (+14; OOS FP 12.3% → 25.9%) — **that read is
  spent; never re-run or tune against it.**
- **Path B — structure restoration (in reserve).** Graft a **canonical/template**
  context (not the experimental one) into the predicted apo pocket and recompute
  geometry. Idealized restoration recovers **22/22**; realistic rigid graft **19/22**
  (the 3 failures are distorted-*backbone* rows). numpy is available for the Kabsch
  superposition; `torch/esm/foldseek` are not in the cloud, so Path B runs locally
  (`predicted_geometry_recovery.py`).

**The discipline (so reconstruction does not become a leak):**

- **Leakage-safe supervision is non-negotiable:** train the channel on *structural*
  observations (ligand context), **never** the mechanism fingerprint / EC / Rhea /
  text — otherwise it is circular and leaky. Fit on train/cal only.
- **The experimental-cofactor graft is circular** — that cofactor is unavailable at
  deploy — so it is only an oracle / upper bound, never a deploy input. Deploy uses
  Path A (sequence-predicted) or Path B (canonical/template).
- **The metal head is the known systemic weak point** (cal AUC ~0.77, spurious 0.99
  on true flavin/heme rows) and the main driver of OOS over-opening; the 5 hard
  misses need cofactor **localization** (predict binding residues) or transplant, not
  more presence-channel tuning (2026-06-04 "Channel-Recall-Limited").
- **Precision discipline:** prefer the **recalibrated abstention threshold** (reaches
  the suppression dial's precision for free) over the suppression dial, which
  sacrifices in-scope recall (2026-06-09 step-4 entry;
  `cofactor_fusion_operating_point.py`).
- Reconstruction stays a **silver/deploy** signal, **never** a bronze entry gate.

**One-liner:** reconstruction does not get us to 10k labels — annotation-anchored
bronze does — it turns the 10k atlas into a deploy-grade mechanism predictor and lets
bronze earn silver; and the thing reconstructed is **family-specific** (cofactor
first, sometimes nothing).

---

## The honest caveats (so we don't fool ourselves)

- **The cap math is the real story.** 10k forces ontology breadth (Stage 2). If we
  refuse to expand families, the honest ceiling is ~2k positives + diverse OOS, and
  padding to 10k with redundant OOS would violate the values. Say so rather than hit
  10k dishonestly.
- **Promotion may stay mostly bronze** until cofactor restoration is run at scale —
  and that is fine. Bronze is an honest tier; silver is earned, not assumed.
- **Beware the "receding horizon"** (`docs/MAP.md`): per-row deployment-blocker
  grinds (Lever 3/4 chores) that the framing can manufacture infinitely. This plan
  is sourcing-and-diversity-bound, not blocker-bound; if a lever turns into infinite
  per-row chores, stop feeding it.

---

## Assets already built (this plan's tooling)

All merged to `main`, all non-destructive, leakage-safe, with tests:

- `coverage_redundancy_audit.py` — the governor (balance/redundancy + acquisition
  targets). CLI `build-coverage-redundancy-audit`.
- `ser_his_triad_locator.py` — Ser-His-Asp triad corroborator + acquisition contract
  for the ser_his hole. CLI `build-ser-his-triad-locator-scan`.
- `novelty_admission_gate.py` — online near-dup/saturation filter feeding the apply
  path. CLI `build-novelty-admission-gate-audit`.
- `mechanism_representation_loop.py` — leakage-safe chemistry representation
  (cofactor/ligand + residue roles; LOO self-consistency 0.895); triages promotion,
  proposes hole candidates. CLI `build-mechanism-representation-loop`.
- `bronze_silver_promotion_preview.py` — promotion queue gated on **cofactor presence
  in coordinates** (not provenance). CLI `build-bronze-silver-promotion-preview`.
- `stage1_hole_sourcing.py` + `scripts/stage1_source_holes.py` — Stage-1 runner that
  fetches fresh reviewed Swiss-Prot for the two cofactor-defined holes and chains
  pilot → cofactor/EC disambiguation → novelty gate → non-destructive preview
  (`--apply` appends to the expansion registry). Needs live UniProt egress; wiring
  is offline-tested. Runbook: `docs/stage1_hole_sourcing_runbook.md`.

---

## Sources & where to verify (read before acting)

Do not take any claim in this plan on faith — every one is traceable. `docs/decision_log.md`
is reverse-chronological (newest at top); cite entries by their **dated title**
(line numbers drift). The durable human handoff is `docs/project_state.md` +
`docs/decision_log.md` + `docs/session_decision_record_*.md`; `work/handoff.md` is an
**auto-generated hourly ledger** (skim for tactical state, do not treat as
decisions); `docs/artifact_index.md` maps artifact files.

| Plan element | Verify / more info |
| --- | --- |
| North Star, values, "done correctly", honesty culture | `docs/MAP.md`, `docs/research_program.md`, `docs/project_state.md`, `README.md` |
| Leakage discipline + heldout one-shot rule | `docs/agent_runbook.md`; `tests/test_leakage_closure.py`; enforced in `labels._validate_external_out_of_scope_evidence_separation` |
| Safety scope (beneficial-only, hypothesis language) | `docs/safety_scope.md` |
| Frozen 702 benchmark: count, coherence baseline, eval contract | `artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json`; `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json` (hashes to `sha256:731b94ebd3b4f7ae483a3cca75d2b8c3b88242024ecd9c364d70bdfcda6624ee`); pinned by `tests/test_geometry_artifact_regression.py` (`label_count == 702`); split manifest `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json` + `…holdout_eval_1025_current702_split_assignment_repaired_20260525.json` |
| The 8 fingerprints (5 primary + 3 secondary) | `data/registries/mechanism_fingerprints.json`, `data/registries/mechanism_ontology.json`, `docs/mechanism_fingerprint.md`; primary/secondary split in the coherence-audit artifact |
| The label gate / code path | `src/catalytic_earth/labels.py` (`MechanismLabel.from_dict`, `load_labels`, `COUNTABLE_REVIEW_STATUSES`); `docs/label_factory.md` |
| Annotation-anchored bronze = the 10k unlock | `decision_log.md` 2026-06-09 "Annotation-Anchored Bronze Is An Accepted External Label Basis (the 10k unlock)"; engines `external_annotation_anchored_import.py` (`classify_row`, `_build_label`, the apply writer), `external_scaleout_bronze_import.py`, `external_cofactor_ec_disambiguation.py`; `docs/external_source_transfer.md`, `docs/ingestion_plan.md` |
| Diversity governor (imbalance, holes, caps, redundancy) | `decision_log.md` 2026-06-10 "Coverage/Redundancy Governor"; `coverage_redundancy_audit.py`; `artifacts/v3_coverage_redundancy_audit_current702_20260610.json` + `work/…md` |
| Novelty / saturation admission gate | `decision_log.md` 2026-06-10 "Novelty / Saturation Admission Gate"; `novelty_admission_gate.py`; its artifact/work |
| ser_his hole + triad locator | `decision_log.md` 2026-06-10 "Ser/Cys-His-Asp Triad Locator"; `ser_his_triad_locator.py`, `serine_active_site.py`; its artifact/work |
| Stage-1 hole-sourcing runner (radical_sam + cobalamin) | `decision_log.md` 2026-06-10 "Stage-1 Hole-Sourcing Runner"; `stage1_hole_sourcing.py`, `scripts/stage1_source_holes.py`, `tests/test_stage1_hole_sourcing.py`; `docs/stage1_hole_sourcing_runbook.md` |
| Representation loop (chemistry features) | `decision_log.md` 2026-06-10 "Mechanism Representation Loop"; `mechanism_representation_loop.py`; its artifact/work |
| **Do not scale model size** (ESM2 etc. not decision-grade) | `docs/wave1_representation_shootout.md`; `decision_log.md` 2026-05-31 "…Feature Overlap…(Northstar Pivot)" and "Sobering Operating-Point Reality"; `mechanism_feature_embedding.py` (Lever 2 clean negative) |
| Promotion preview + the cofactor-presence correction | `decision_log.md` 2026-06-10 "Bronze->Silver Promotion Preview" and "CORRECTION — Promotion Confirmability Is Cofactor PRESENCE…"; `bronze_silver_promotion_preview.py`; its artifact/work |
| Problem-2 degradation (45/45→23/45, apo cofactor-loss) | `decision_log.md` 2026-06-03 "Predicted-Geometry Degradation Is Cofactor-Loss-Dominated"; `predicted_geometry_robustness.py`; `artifacts/v3_predicted_geometry_failure_decomposition_current702_20260603.json` |
| Reconstruction architecture + the two paths | `decision_log.md` 2026-06-04 "Problem 2 Solution Architecture — Reconstruct Deploy-Missing Context From Sequence" |
| Cofactor restoration 22/22 · realistic graft 19/22 | `decision_log.md` 2026-06-04 "Cofactor Restoration Recovers 22/22…" and "Cofactor Graft Is Realistic For 19/22"; `predicted_geometry_recovery.py`; `artifacts/v3_cofactor_restoration_recovery_probe_current702_20260604.json` |
| Sequence→cofactor channel ~70% · heldout one-shot (SPENT) | `decision_log.md` 2026-06-04 "Cofactor Channel Recovers ~70%…", "HELDOUT ONE-SHOT SPENT…", "Leakage-Safe Cofactor-Presence Channel"; `cofactor_presence_calibration.py`, `sequence_cofactor_channel.py`; `artifacts/v3_in_distribution_predicted_geometry_recovery_current702_20260604.json`, `…heldout_oneshot_cofactor_fusion_blind_pass…json` |
| Metal head weak point · hard misses not channel-recoverable | `decision_log.md` 2026-06-04 "Cofactor Recovery Is Channel-Recall-Limited…" |
| Precision dial (recalibrated threshold > suppression) | `decision_log.md` 2026-06-09 "Step-4 Precision Side Measured…"; `cofactor_fusion_operating_point.py` |
| Predicted-geometry pipeline runbook | `docs/predicted_geometry_robustness_pipeline_runbook.md` |
| Sourcing status: drained pools, 275-row queue, page-depth lesson | `work/handoff.md` (latest), `work/NEXT_WORKS_northstar_20260531.md`, `docs/external_source_transfer.md` |
| Pending candidate inventory (12,495 review surface; what imported vs held/blocked) | `artifacts/v3_external_import_review_preflight_current702_20260609.json` (`terminal_state_counts`), `…import_review_ready_preview…json` (275 ready), `…import_review_repair_queue…json` (12,220), `…scaleout_bronze_import_preview…json` (1,381 import / 1,037 held), `…cofactor_ec_disambiguation_preview…json` (143 / ~730 held) |
| ePK NO-GO (do not revive without non-heuristic approach) | `docs/epk_heuristic_geometry_no_go_20260521.md`; `decision_log.md` 2026-06-06 |

If a reference here ever disagrees with the code or a newer decision-log entry,
**the newer decision-log entry and the code win** — update this plan, don't quietly
work around it.

---

## One-line summary

**Unblock sourcing → close the holes → broaden the ontology → diverse
novelty-gated OOS → earn silver by reconstructing each family's deploy-missing
context (cofactor first, sometimes nothing) → freeze a v2 benchmark when ready** —
all behind the frozen-702 wall, the leakage wall, and the governor.
