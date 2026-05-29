# Decision Log

This log records durable decisions that future agents should apply before
interpreting older artifacts. Dates are UTC artifact dates unless noted.

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
