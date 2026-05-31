# Decision Log

This log records durable decisions that future agents should apply before
interpreting older artifacts. Dates are UTC artifact dates unless noted.

## 2026-05-31: PIVOTAL — De Novo Abstention Precondition IS MET On Deployment (Predicted) Geometry

Decision: the prior "deployment-valid gate is blocked — no predicted-geometry
atlas rows" entry below was solving the wrong problem. The two-channel gate does
not need a predicted-geometry atlas at all. Both channels are already calibrated
[0,1] confidences:
  * predicted-geometry fingerprint-retrieval `top1_score` (from
    `predicted_geometry_retrieval.results` in the robustness audit), and
  * the strongest organic-cofactor head probability (`cofactor max_score`).
They can be combined directly over the held-out pool with NO atlas normalization
and NO eval-pool leakage. This makes the deployment-valid de novo gate computable
from artifacts already in the repo.

Result (predicted/apo deployment geometry; 47 in-scope, 79 OOS, 6 confounded, 73
agnostic; held-out only, no atlas, no tuning):
  * combined_mean: AUC **0.852 overall — CLEARS the 0.75 de novo precondition bar**.
  * geometry_top1_score: 0.757 overall and the single SAFEST channel — no stratum
    below chance, and strongest exactly on the dangerous cofactor-confounded OOS
    (0.840), where the cofactor channel is fooled (0.280, worse than chance).
  * cofactor_max_score: 0.628 overall (good 0.657 on agnostic, fooled on confounded).
  * combined_min: 0.609 (the strict-concordance combiner is the worst here).

This is the decisive de novo result: on the real deployment regime, mechanism
novelty IS detectable with leakage-free, already-available signals. The recommended
deployment gate LEADS WITH GEOMETRY CONFIDENCE (uniformly safe, best on the
confounded cases) and adds the cofactor channel as a complementary lift on the
cofactor-agnostic OOS majority — NOT a blind mean, which scores higher in aggregate
(0.852) only by sacrificing safety on the confounded subset (0.330). Pick the
combiner by the safety profile, not the aggregate AUC.

Caveat: the geometry fingerprint score is hand-authored / tuning-adjacent (D4); the
result is a relationship/abstention AUC, not a calibrated probability, and is bounded
to the current 8-fingerprint family set. Guardrails: sequence-only PLM input,
predicted-geometry deployment regime, no atlas, no training/refit, no heldout tuning,
M-CSA eval-only.

Artifacts: `artifacts/v3_mechanism_deployment_abstention_gate_eval_current702_20260531.json`,
`work/mechanism_deployment_abstention_gate_eval_current702_20260531.md`. Module:
`src/catalytic_earth/mechanism_abstention_gate_eval.py`
(`compute_deployment_gate`, tests in `tests/test_mechanism_abstention_gate_eval.py`;
CLI: `eval-mechanism-deployment-abstention-gate`). Supersedes the "blocked" entry below.

## 2026-05-31: Deployment-Valid Two-Channel Gate Is Blocked — No Predicted-Geometry Atlas Rows

Decision: attempted the deployment-valid rerun of the two-channel abstention gate
flagged as the next step by the teacher-side entry below, pointing
`--geometry-retrieval` at the `predicted_geometry_retrieval` block of
`v3_predicted_geometry_robustness_audit_current702_20260529.json`.

Finding (verified, no scoring claim): that block contains ONLY held-out rows — 47
in-scope (heldout, has fingerprint) + 79 OOS (heldout, no fingerprint), and ZERO
in_distribution rows. The gate needs in-distribution atlas rows to (a) build the
cofactor-augmented PLM class centroids and (b) compute the geometry channel's
atlas-percentile normalization. With atlas=0 the gate returns
`status=insufficient_rows` and no AUC. The broken run artifact was deleted, not
committed; no numbers were produced.

Consequence: the deployment-valid two-channel gate is blocked on a
predicted-geometry retrieval that also covers the ~124 in_distribution atlas rows
(the current audit only re-scored the held-out evaluation set on predicted
structure). Concrete next gate: regenerate geometry retrieval on predicted
(AlphaFold) structures for the in_distribution atlas rows too, persisting per-row
`role_match_fraction`, then rerun `eval-mechanism-abstention-gate
--geometry-retrieval <that artifact>`. The separate predicted-geometry-confidence
finding (raw `top1_score` AUC 0.757) stands because it is a single-channel
rank-based AUC over the held-out pool only and needs no atlas.

## 2026-05-31: Two-Channel Abstention Gate (cofactor + geometry role) — Source-Agnostic, Clears Bar On Teacher Geometry

Decision: productionize the two-channel abstention gate implied by the confounded-
OOS diagnosis. Channel 1 is the cofactor-augmented PLM nearest-centroid; channel 2
is geometry `top1_score x role_match_fraction` (novel chemistry shows the right
active-site residues with the wrong catalytic roles). Each channel is mapped to its
in-distribution ATLAS percentile (atlas-only, deployable, no eval-pool leakage) and
combined by mean.

Result on experimental/teacher geometry (47 in-scope, 88 OOS, 8 confounded): the
combined-mean gate reaches overall AUC 0.830 and clears the 0.75 de novo bar, with
geometry rescuing the cofactor-confounded set (cofactor 0.339 -> combined 0.503;
geometry alone 0.652 there). Per channel: cofactor 0.684, geometry 0.801,
combined-mean 0.830, combined-min 0.733.

Relation to the predicted-geometry finding below: that entry correctly establishes
the deployment-valid signal lives in predicted (apo) geometry, not this
experimental retrieval, and that predicted top1 score alone hits AUC 0.757. This
gate module is SOURCE-AGNOSTIC on `--geometry-retrieval`, so once a predicted-
geometry retrieval persisting per-row `role_match_fraction` exists, the
deployment-valid two-channel number is a one-line rerun. Until then this is a
teacher-side proof the precondition is achievable with the right two channels, not
a deployment claim — the report carries that caveat explicitly.

Guardrails: sequence-only PLM input, atlas-only statistics/percentiles, no
training/refit/heldout tuning; geometry fingerprint score is tuning-adjacent
(role_match_fraction is structural); M-CSA eval-only. Module:
`src/catalytic_earth/mechanism_abstention_gate_eval.py` (tests:
`tests/test_mechanism_abstention_gate_eval.py`; CLI: `eval-mechanism-abstention-gate`;
artifacts: `artifacts/v3_mechanism_abstention_gate_eval_current702_20260531.json`,
`work/mechanism_abstention_gate_eval_current702_20260531.md`).

## 2026-05-31: Predicted-Geometry Confidence Is The Strongest Abstention Signal

Decision: test whether geometry-channel confidence flags the cofactor-confounded
OOS rows where the cofactor channel is confidently wrong — on deployment-valid
PREDICTED (AlphaFold) geometry, not experimental teacher geometry.

First rejected a trap: `v3_geometry_retrieval_1025.json` is experimental/teacher-
side (retains ligand/cofactor context, scores a non-deployment-valid AUC 1.0). The
honest signal is `top1_score` from `hand_router_on_predicted_geometry.rows` in
`v3_predicted_geometry_robustness_audit_current702_20260529.json` (predicted, apo).

Result (heldout split, predicted regime): predicted-geometry top1 score separates
in-scope from OOS at AUC 0.757 (in vs all-OOS, 47 vs 79) — the first single signal
to reach the 0.75 usability bar, beating cofactor-augmented 0.694 and bare-PLM
0.596. It is strongest exactly where the cofactor channel fails: AUC 0.840 on the
cofactor-confounded OOS (n=6 with usable predicted geometry; m_csa:549 fetch-failed,
m_csa:563 excluded) vs the cofactor channel's worse-than-chance 0.443 there. The
channels are complementary.

Consequence: the de novo abstention gate should be geometry-confidence-led with
the cofactor channel complementary. Next: a combined weakest-channel gate
(predicted-geometry confidence AND cofactor agreement) and fold the
predicted-geometry signal into the novelty eval as first-class. Existing per-row
scores only; nothing fit on heldout; no labels/registries/thresholds changed;
M-CSA eval-only. Artifact: `work/predicted_geometry_abstention_finding_current702_20260531.md`;
reproduce with `scripts/predicted_geometry_abstention_probe.py`.

## 2026-05-31: Abstention Leak Is 8 Named Cofactor-Confounded OOS Rows, Not A Uniform Ceiling

Decision: diagnose *why* novel-chemistry abstention plateaus at AUC ~0.69 instead
of treating it as a generic ceiling. Tested two things and stratified the result.

(1) A supervised, atlas-only mechanism-feature readout does NOT beat the
unsupervised cofactor-augmented signal: per-class diagonal-Gaussian log-likelihood
in the between-class subspace gives AUC 0.521 (chance) and a one-vs-rest
mean-difference margin gives 0.637 — both below the cofactor-augmented 0.694. So
the ceiling is not a method-sophistication problem solvable by learning directions
on the current 8-class atlas (probe-only, not committed).

(2) Stratifying the 92 OOS rows by whether they carry a known cofactor signature
(max organic-cofactor score >= 0.5, untuned) splits the aggregate sharply:
   - 84 cofactor-agnostic OOS rows abstain well: AUC 0.718 (near the 0.75 bar).
   - 8 cofactor-signature OOS rows are confidently misplaced: AUC 0.443 (worse
     than chance) — the channel pulls them into occupied clusters.
The residual abstention leak is therefore concentrated in 8 named false-confident
novelty cases (m_csa:30, 31, 80, 191, 267, 448, 549, 563), not spread uniformly.
These are novel-mechanism enzymes that happen to use a known cofactor family, the
single most dangerous failure mode for an abstention gate, and now enumerated.

Consequence: an abstention gate built on the cofactor-augmented signal is viable
for the cofactor-agnostic majority; the named cofactor-confounded OOS rows are the
explicit target for the next mechanism-feature signal (fold/active-site geometry
beyond cofactor identity). This stratified diagnostic is now part of the committed
novelty eval (`stratified_by_cofactor_signature`).

## 2026-05-31: Novelty-Abstention Rerun On Strict t6/t12 Scores (Fallback Removed)

Update to the de novo precondition result below: after the ESM2-150M fallback
cofactor sidecar was replaced with the strict original t6/t12 selected scores
(`trained:esm2_t6_8m` + `trained:esm2_t12_35m`), the source-agnostic
novelty-abstention eval was re-run with no code change. The real cofactor heads
improve separation over the fallback — cofactor-augmented best AUC rises from
0.654 to **0.694**, and the raw cofactor-confidence signal reaches AUC 0.636 with
novel chemistry carrying markedly lower in-class cofactor confidence (in-scope
0.380 vs OOS 0.165). Bare-PLM distance is unchanged at 0.596. The signal is still
below the 0.75 usability bar, so the conclusion stands: distance/cofactor
abstention is not yet sufficient for de novo, but the stronger channel
measurably helps. Artifact and report regenerated in place.

## 2026-05-31: D11 De Novo Precondition — Distance Cannot Abstain On Novelty; Cofactor Helps But Falls Short

Decision: measure the D11 de novo validity check directly — can a cheap,
unsupervised signal separate in-scope held-out queries (known mechanism
fingerprint) from out-of-scope held-out rows (novel chemistry, no fingerprint)?
Abstention-on-novelty is the de novo precondition, so this is a gate, not a
nicety.

Result (48 in-scope, 92 OOS, 184 atlas; all atlas-only statistics, no tuning):
bare ESM2-150M distance signals are near chance — nearest-atlas cosine AUC 0.547,
nearest-centroid 0.596, top1/top2 margin 0.567, between-class subspace projnorm
0.524 (best 0.596). A general-purpose PLM encodes overall protein similarity, so
novel enzymes still look like ordinary proteins and sit inside occupied regions.
Adding the row-level organic-cofactor channel (the now-unblocked, source-agnostic
sidecar) moves the signal in the right direction — augmented nearest-centroid AUC
0.654, with OOS carrying lower in-class cofactor confidence (in 0.716 vs OOS
0.601) — but still below the 0.75 usability bar.

Consequence: distance-thresholded abstention is insufficient for de novo today.
The cofactor channel is a genuine but partial mechanism-discriminative signal;
the precondition needs a stronger one (recovered t6/t12 cofactor heads instead of
the ESM2-150M fallback, and/or explicit mechanism-feature supervision). The
novelty eval is source-agnostic, so re-running it once the fallback is removed is
a one-line change.

Guardrails held: sequence-only PLM input, no training/refit, no held-out tuning,
atlas-only statistics/centroids/subspace, M-CSA eval-only.

Artifacts: `artifacts/v3_mechanism_novelty_abstention_eval_current702_20260530.json`,
`work/mechanism_novelty_abstention_eval_current702_20260530.md`. Module:
`src/catalytic_earth/mechanism_novelty_abstention_eval.py`
(tests: `tests/test_mechanism_novelty_abstention_eval.py`; CLI:
`eval-mechanism-novelty-abstention`).

## 2026-05-30: D11 Hygiene Surface — Real PLM Beats k-mer Control

Decision: add a real protein-language-model sequence surface (persisted
ESM2-150M whole-sequence embeddings) to the D11 relationship faithfulness
measurement, evaluated under one identical, committed, rank-based pipeline
against the deterministic k-mer control.

Result: on the held-out query / in-distribution atlas split (48 queries, 184
candidates), the ESM2-150M surface beats the k-mer control on all 24 reported
metrics with zero losses — exact-top1 rises from ~0.31 to ~0.52 (cosine),
family-top3-any from 0.67 to 0.90, family-MRR from 0.60 to 0.80. The k-mer
control reproduces the prior D11 hygiene eval's ballpark (family-top3-any cosine
0.667 vs 0.652), which cross-validates the new pipeline.

Scope and guardrails: this is a hygiene-tier sequence-surface comparison, not the
real D11 pass. The real pass remains `blocked_missing_row_level_cofactor_channel_scores`
because row-level selected organic-cofactor scores (flavin/heme/PLP) and a
cofactor-augmented predicted-geometry query representation are still missing.
Inputs are amino-acid-sequence-only; no geometry-derived cofactor evidence, no
training/refit, no held-out tuning (robust scaling uses atlas-only statistics).
M-CSA remains eval-only.

Artifacts: `artifacts/v3_mechanism_relationship_plm_surface_current702_20260530.json`,
`work/mechanism_relationship_plm_surface_current702_20260530.md`. Module:
`src/catalytic_earth/mechanism_relationship_surface_eval.py`; reproduce via its
`write_mechanism_relationship_surface_eval(...)` entrypoint, exercised by
`tests/test_mechanism_relationship_surface_eval.py::test_build_from_real_artifacts_if_present`.
A convenience CLI subcommand `eval-mechanism-relationship-surface` is also wired
into `src/catalytic_earth/cli.py`.

## 2026-05-30: Session D1-D11 Decision Record

Decision: preserve the D1-D11 session reasoning as a durable project-memory
record before running D11 relationship-eval automation.

Rationale: the session established the current line of reasoning from Wave 1
decoder/join confounds, through predicted-geometry information loss, sequence
cofactor-channel reconstruction, concordance gating, and the D11 mechanism
relationship-space framing. Future agents should read this record before
interpreting route-policy, LOMO, targeted expansion, or D11 relationship-eval
outputs.

Reference:

- `docs/session_decision_record_20260530.md`

## 2026-05-25: Current702 Benchmark Contract

Decision: freeze the current702 sequence benchmark and mechanism-prediction
contract before interpreting sequence-NN, PLM, or hybrid results.

Rationale: current702 has complete sequence coverage and repaired split
assignments, but representation claims need a fixed target universe, OOS policy,
diversity bins, and active-site evidence-budget rules.

References:

- `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`
- `artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json`
- `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json`
- `artifacts/v3_sequence_nn_metrics_current702_20260525.json`

## 2026-05-27: `m_csa:497` Is Out Of Scope

Decision: relabel `m_csa:497` from
`flavin_dehydrogenase_reductase` to `out_of_scope` for v1 benchmark use.

Rationale: the row is flavodiiron nitric oxide reduction. Catalysis occurs at a
non-heme Fe(II)Fe(II) center, with FMNH2 acting as an electron donor to the
di-iron nitrosyl complex rather than as the v1 flavin hydride-transfer catalytic
locus. It should be retained as a hard OOS/boundary negative for flavin-cofactor
leakage, not as primary flavin support.

References:

- `artifacts/v3_m_csa497_label_revision_702_20260527.json`
- `artifacts/v3_m_csa497_wave1_metric_impact_702_20260527.json`
- `artifacts/v3_packet1_wave1_decision_closure_702_20260527.json`
- `data/registries/curated_mechanism_labels.json`

## 2026-05-27: `m_csa:750` Is Not A Primary Flavin Canary

Decision: remove `m_csa:750` from primary flavin metrics and from Wave 1
Foldseek-success/learned-failure canary use. The current registry label is
`out_of_scope`.

Rationale: 4-hydroxybutanoyl-CoA dehydratase uses radical FAD semiquinone plus
Fe-S dehydration chemistry. That is a future radical-flavin/Fe-S dehydratase
family candidate, not ordinary v1 flavin hydride-transfer
dehydrogenase/reductase chemistry. Older wins against the previous flavin label
are stale.

References:

- `artifacts/v3_m_csa750_label_revision_702_20260527.json`
- `artifacts/v3_m_csa750_wave1_metric_canary_impact_702_20260527.json`
- `artifacts/v3_packet1_wave1_decision_closure_702_20260527.json`
- `data/registries/curated_mechanism_labels.json`

## 2026-05-27/28: FMO Stays Secondary-Only

Decision: keep flavin monooxygenase as secondary OOD/acquisition context only.
Do not promote it to a primary supervised metric, do not add a canonical child
registry entry, and do not import FMO candidates.

Rationale: the source evidence supports real FMO-like chemistry for rows such
as `m_csa:131`, `m_csa:132`, and review-ready future rows `m_csa:551` and
`m_csa:973`, but the current support is underpowered and gate-limited. The
active geometry/counterevidence gate is PHBH-leaning, exact ligand-bearing
coordinates are missing or unsuitable for important external subtype rows, and
subtype panels plus hard-negative controls are still needed.

References:

- `artifacts/v3_fmo_source_evidence_scout_702_20260527.json`
- `artifacts/v3_fmo_v2_fingerprint_design_proposal_702_20260527.json`
- `artifacts/v3_fmo_admission_gate_and_benchmark_impact_702_20260527.json`
- `artifacts/v3_fmo_local_candidate_adjudication_551_973_702_20260528.json`
- `artifacts/v3_fmo_fingerprint_definition_audit_702_20260528.json`
- `artifacts/v3_fmo_external_hard_negative_duplicate_gate_702_20260528.json`

## 2026-05-28/29: Wave 1 Decoder And Geometry-Join Confounds

Decision: use the Wave 1.2 decoder/join confound audit as the current
representation comparison gate.

Rationale: the older geometry preview joined only 135/140 heldout rows, while
the current re-export joins 140/140. Decoder choice is also a real confound:
the same ESM-C representation behaves very differently under a logistic head
versus cosine NN. ProtT5 and SaProt matched logistic reruns are blocked by
missing local raw sidecars/weights, not by a negative result.

References:

- `artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json`
- `work/wave1_2_decoder_join_confound_audit_702_20260528.md`
- `artifacts/v3_wave1_1_model_by_cell_report_702_20260528.json`
- `artifacts/v3_wave1_representation_shootout_result_card_20260526.json`

## 2026-05-29: Geometry-First Router Interpretation

Decision: prefer a geometry-first router for the next gate. Do not scale
learned models first and do not treat Wave 1 learned-representation diagnostics
as proof of mechanism prediction superiority.

Rationale: current hand-scored geometry resolves the audited join gap, reaches
45/45 canonical primary heldout accuracy, and has 0/92 pure-OOS false positives
under the frozen 0.4115 threshold. The local geometry-feature logistic probe and
PLM heads are useful diagnostics, but they do not displace the hand geometry
router.

References:

- `artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json`
- `work/wave1_2_decoder_join_confound_audit_702_20260528.md`
- `work/northstar_wave1_to_engine_handoff_20260526.md`

## 2026-05-29: Predicted Geometry Is Not Deployment-Ready

Decision: do not interpret the clean experimental-coordinate 45/45 hand-router
result as bare-sequence deployment readiness.

Rationale: when current702 heldout M-CSA rows with experimental geometry and
sequence-position mappings are re-scored on AlphaFoldDB predicted coordinates,
the hand router drops to 23/45 canonical primary correct, with 17 primary
abstentions, 5 wrong non-abstained primary calls, and a 12.3% OOS/secondary
false-positive rate. The OOS-aware geometry MLP trained on experimental
geometry stays disciplined on OOS but reaches only 16/45 primary correct via
abstention. The learned-model job is now explicitly robustness to predicted
active-site geometry degradation, not beating clean M-CSA geometry in isolation.

References:

- `artifacts/v3_predicted_geometry_robustness_audit_current702_20260529.json`
- `work/predicted_geometry_robustness_audit_current702_20260529.md`
- `artifacts/v3_predicted_geometry_robustness_audit_current702_esmfold_20260529.json`

## 2026-05-29: Review And Import Posture

Decision: review artifacts are not imports. Countable label changes require a
dedicated review decision, import preview, label-factory gates, batch
acceptance, and registry summary refresh. This cleanup pass does not edit
labels, registries, ontologies, imports, production scoring, or global
thresholds.

Rationale: the repo intentionally separates review evidence from benchmark
labels to avoid leakage, stale claims, and accidental count growth. External
seed-fingerprint imports remain 0, and the three imported external rows are
out-of-scope hard negatives only.

References:

- `docs/label_factory.md`
- `artifacts/v3_mcsa_ai_visual_review_support_index_20260524.json`
- `artifacts/v3_mcsa_ai_visual_remaining_manual_expert_holds_index_20260525.json`
- `artifacts/v3_mcsa_positive_clean9_import_preview_20260523.json`
- `artifacts/v3_mcsa_ai_visual_clean10_accept7_vivek_20260524_import_summary.json`
- `artifacts/v3_artifact_migration_execution_1025.json`

## 2026-05-29: README Becomes The Front Door

Decision: keep `README.md` concise and move active project memory into
dedicated docs.

Rationale: the previous README mixed front-door onboarding with a long
chronological research dump. Future agents need a stable source-of-truth order:
project state, decisions, artifact index, then runbook.

References:

- `docs/project_state.md`
- `docs/decision_log.md`
- `docs/artifact_index.md`
- `docs/agent_runbook.md`
- `README.md`
