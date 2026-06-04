# Decision Log

This log records durable decisions that future agents should apply before
interpreting older artifacts. Dates are UTC artifact dates unless noted.

## 2026-06-04: Cofactor Channel Recovers ~70% of the Apo Drop (in-distribution, out-of-sample)

Decision: the sequence cofactor-presence channel is the right lever for the
predicted-apo primary drop, validated leakage-safe on in-distribution rows
before any heldout read is spent.

Rationale: the headline 45/45 -> predicted 23/45 drop is a heldout number and
the heldout read is one-shot. The new in-distribution recovery harness
reproduces the same question on in-distribution rows, which are never the
benchmark. The router classifies active-site geometry against the eight
mechanism fingerprint templates (no per-row self-match), so the
experimental-minus-apo and fused-minus-apo deltas are meaningful. The cofactor
channel was fit on the train split, so the headline is reported on the
calibration rows (out-of-sample for the channel); train is an in-sample
reference only.

Result (calibration, out-of-sample, 35 rows, threshold 0.4115): experimental
holo geometry 34/35 correct, predicted-apo 17/35 (a ~50% drop mirroring the
heldout 45->23), and predicted-apo + injected sequence cofactor presence
30/35 -- recovering 12 of the 17 apo-lost primaries (70.6%) with **0**
regressions. Train (in-sample reference) recovers 56/59 (94.9%); the
in-sample/out-of-sample gap is why the calibration number is the one to trust.
The router consumes the injected `ligand_context.cofactor_families` through the
0.18-weight `cofactor_context_score` term, which is enough to un-abstain a
cofactor-dependent primary at 0.4115. Sequence-supported suppression lowers
recall on this all-in-scope surface (it protects the OOS-FP side, which is not
measured here).

Consequence / next gate: this projects to roughly 23 -> ~38/45 on heldout if the
out-of-sample recovery rate holds, but that is a PROJECTION; the heldout read
stays one-shot and authorization-gated. Next levers to push recovery further and
cut the residual FP: cofactor localization (which residues), pLDDT active-site
abstention, and a real Kabsch cofactor transplant (numpy is now available).

References:

- `artifacts/v3_in_distribution_predicted_geometry_recovery_current702_20260604.json`
- `work/in_distribution_predicted_geometry_recovery_current702_20260604.md`
- `src/catalytic_earth/predicted_geometry_recovery.py`
- `tests/test_predicted_geometry_recovery.py`

## 2026-06-04: Leakage-Safe Cofactor-Presence Channel (train/cal only)

Decision: the sequence -> cofactor-presence channel must select its per-class
operating thresholds and per-class embedding backend on a held-in calibration
split, never on heldout. The original `sequence_cofactor_channel` fits the
presence heads on `in_distribution` but reads the heldout cofactor labels both
to report ROC-AUC/AP and to pick the best backend per class; even though the
cofactor-presence label is structural (ligand context, not the mechanism
target), reading heldout to score and to choose sources entangles the one-shot
heldout surface with channel design. Per the active instruction to abstain on
the heldout, the channel is rebuilt train/cal-only.

Result: new `cofactor_presence_calibration` module fits one-vs-rest presence
heads (metal_ion/flavin/plp/heme) on the 410 train rows of the frozen
mechanism-feature embedding split, selects max-F1 thresholds and the per-class
backend on the 103 calibration rows, and emits per-entry predictions for all
702 rows (heldout included) without ever reading heldout labels. Calibration
ROC-AUC: metal_ion 0.7707, flavin 0.9263, plp 0.9924, heme 0.88; plp (4
calibration positives) and heme (3) are flagged `low_calibration_support` and
are report-only operating points. A unit test flips every heldout label and
asserts the fitted heads, selected sources, and predictions are byte-identical,
proving heldout is never read. These calibration-honest numbers are
deliberately more conservative than the prior heldout-evaluated channel.

Consequence / next gate: the per-entry predictions are drop-in compatible with
the router `ligand_context` injection (`_fused_geometry_features`). Applying them
to the heldout mechanism router (the cofactor-restoration recovery ceiling) reads
the one-shot heldout mechanism labels and is NOT run here; it stays explicitly
authorization-gated. Built on isolated worktree branch
`claude/cofactor-presence-channel`.

References:

- `artifacts/v3_cofactor_presence_calibration_current702_20260604.json`
- `work/cofactor_presence_calibration_current702_20260604.md`
- `src/catalytic_earth/cofactor_presence_calibration.py`
- `tests/test_cofactor_presence_calibration.py`

## 2026-06-04: Lever 3 Current Evidence Still Blocks Deployment Closure

Decision: keep Lever 3 fail-closed. Do not rerun or retune threshold `0.44155`
from the current residual surface. The local repository does not contain
approved deployment-valid predicted coordinates for the four AFDB-unavailable
coordinate-source blockers, and Q43088 still lacks two approved source-free
locator positions or an equivalent geometry sidecar.

Result: local deployment-input preflight found 0 approved predicted-coordinate
hits for `m_csa:416`/P07071, `m_csa:562`/P07658, `m_csa:586`/P00806, and
`m_csa:637`/P04531. Experimental CIF shortcuts exist for P07658, P00806, and
P04531, but they are explicitly disallowed as deployment inputs. P07071 has no
local CIF hit. Q43088 has a local predicted structure and one Tyr287 anchor; a
review-only neighbor scout generated 12 candidate positions, all pending
review, with 0 locator approvals and 0 rescore readiness. An additional
repo-wide CIF sanity scan over 1,636 local CIFs found only those same three
experimental shortcuts and no P07071 local CIF hit.

Consequence / next gate: the smallest surface-completeness experiment is an
approval/staging manifest for predicted coordinates for P07071, P07658, P00806,
and P04531 with provider/model/version/path/checksum provenance, plus explicit
approval of two Q43088 locator positions or an equivalent geometry sidecar. The
smallest calibration experiment remains the frozen 16-row high-cofactor
train/cal OOS probe; the 170-row same-family structural acquisition remains the
larger calibration blocker.

Artifacts:
`artifacts/v3_fold_augmented_confounded_proxy_deployment_input_preflight_current702_20260604.json`,
`artifacts/v3_fold_augmented_confounded_proxy_repo_wide_coordinate_sanity_scan_current702_20260604.json`,
`artifacts/v3_fold_augmented_q43088_source_free_locator_candidate_scout_current702_20260604.json`,
`artifacts/v3_fold_augmented_confounded_proxy_current_evidence_blocker_after_input_preflight_current702_20260604.json`.

## 2026-06-04: Lever 2 Partial Surface Read Once, Not Deployable

Decision: accept the deterministic missing-locator abstention operating contract
only as a fail-closed readout contract, spend the frozen heldout read exactly
once, and reject the resulting partial-surface Lever 2 channel as deployable.
Do not rerun, retune, lower the threshold, refit the model, or treat the 87
missing-locator rows as feature values.

Result: the accepted partial source-free surface scored 53 feature-complete
heldout rows and carried 87 missing-locator rows as deterministic abstentions.
At the frozen residual threshold, OOS abstain recall is **1.0** but primary
retain recall is **0.0**. The post-readout recovery queue has 119 rows: 32
feature-complete primaries abstain by residual, 16 additional primaries abstain
because their source-free locators are missing, and 71 OOS rows remain
missing-locator coverage rows.

Consequence / next gate: coverage repair alone is not sufficient. Continue Lever
2 with train/cal-safe feature or materialization repair for feature-complete
primary abstentions, then recover primary source-free locator coverage. Treat the
heldout readout as final evidence for this surface.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_partial_surface_operating_contract_decision_current702_20260604.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_heldout_threshold_readout_current702_20260604.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_heldout_threshold_readout_retention_decision_current702_20260604.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_post_readout_recovery_queue_current702_20260604.json`.

## 2026-06-03: Lever 2 Source-Free Token Re-Selection — No Token Clears The Bar

Decision: defer the Lever 2 source-free row-specific feature. A train/cal-only
re-selection (heldout never read) shows **no source-free-replicable token clears a
useful bar**, so the one-shot heldout read will not be spent on any Lever 2 token.
The 53 approved source-free locators remain a banked, split-protected asset; the
source-free discriminative value lives in the geometry/fold structural channel.

Method: on the 43 OOS-augmented train/cal rows (15 in-scope primary, 28 OOS), the
only source-free-replicable feature family is residue-identity counts
(`event_residue_code` / `event_residue_code_count` — countable from a source-free
locator). All role/bond/event-type families are source-derived and excluded.
Labels were used only as the selection target, never as a predictive feature.

Result: multivariate LOO-CV AUC of all source-free residue counts = **0.538**
(≈ random). Best univariate token is His at dir-adjusted AUC 0.601 but
**OOS-pointing** (His is higher in OOS rows). The calibrated His-count fallback
(0.643) was role-dependent: stripped to a raw source-free His count, `HIS>=3`
fires on 4 train/cal rows, all OOS (in-scope precision 0.000). The Lever 2 signal
is entirely in M-CSA role/event bindings, which do not survive source-free.

Contrast: the predicted-structure fold/TM channel is AUC 0.814 (in vs all OOS) and
0.908 for the no-fit geometry+fold mean — a different structural channel and the
project's real source-free signal.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_source_free_token_reselection_train_cal_current702_20260603.json`,
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_source_free_token_reselection_train_cal_current702_20260603.md`.

## 2026-06-03: Lever 2 Source-Free Event Axis Reviewed, NOT Signed Off (Too Thin)

Decision: the source-free proton-transfer / electrostatic-stabiliser event-axis
linker drafted for Path A is **not signed off**. The one-shot heldout read will
not be spent on it. The reviewer judged the source-free feature too thin to
justify the irreplaceable heldout-read budget. No event-axis linker was
materialized, no application surface built, no frozen residual threshold applied,
no heldout row read.

What was drafted: a deterministic, label-blind structural rubric (residue
identity + contacting atoms + distance + source-free role hints only; no label,
fingerprint, EC/Rhea, source text, curated role, or target name) over the 53
approved source-free locators. Result: **14/53 rows carry the token** (both roles
evidenced; 12 in-scope + 2 boundary-OOS, concentrated in PLP/flavin/heme
phosphate-cofactor enzymes), **39 token-absent**, all confidences modest
(0.21–0.47).

Root-cause diagnosis: the source-free locators anchor on the cofactor/metal, so
the electrostatic-stabiliser role only fires when a cation clamps a cofactor
phosphate (PLP/flavin), and the pair requires a co-located proton-transfer axis.
Metal-hydrolase and many heme sites therefore cannot evidence the pair
source-free — the catalytic proton-transfer / oxyanion machinery is
substrate-proximal, not cofactor-proximal, and is not captured by a
cofactor-proximity locator. The 12/14 in-scope skew emerged from structure, not
the label (no leakage), but the surface is too sparse and low-confidence to read
once.

Consequence / next gate: do not feed this axis to the heldout read. Reconsider
the strengthening strategy before spending the one-shot budget. The 53 approved
locators remain a banked, split-protected asset. The draft and its full per-row
evidence are retained as review-only documentation, not approved inputs.

Artifacts (review-only, not signed off):
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_review_packet_current702_20260603.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_draft_rows_for_signoff_current702_20260603.json`,
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_draft_rows_for_signoff_current702_20260603.md`.

## 2026-06-03: Lever 2 Locator Rewrites — 53 Approved, 2 Rejected (723, 599)

Decision: after a full per-row review of the 55 priority-1 current702 source-free
locator rewrites, record explicit reviewer decisions: **approve 53, reject
`m_csa:723` and `m_csa:599`**. Decisions are recorded in a separate
approval-decisions artifact with candidate and planned-payload hashes preserved
unchanged; the committed review-only approval packet and materialization gate are
left pending and untouched (they remain regression-pinned to the pre-decision
state). No locator sidecars were copied, no heldout rows read, and no frozen
residual threshold applied.

Rationale: the 55 heldout rows split into 32 in-scope primaries
(`seed_fingerprint`, which the model must retain) and 23 out-of-scope negatives
(which it must abstain on). In-scope rows require the locator to land on the
genuine catalytic center; OOS rows only require a faithful source-free pointer to
the real cofactor/metal site. All 55 are integrity-clean (hashes match, zero
forbidden-feature flags, split-protected). 30/32 in-scope rows anchor correctly
(PLP catalytic-Lys Schiff base ~1.3 A, covalent 8a-His-FAD, Cys-ligated heme,
His/Asp/Glu-metal first shells, 4Fe-4S Cys ligation). All 23 OOS rows are
faithful source-free anchors (structural-metal anchors such as KDM4A Cys3His zinc
and MetRS zinc knuckle remain out-of-distribution).

The two rejected rows are both in-scope `ser_his_acid_hydrolase`:
`m_csa:723` (subtilisin) anchored on the structural Ca loop, not the Ser-His-Asp
triad; `m_csa:599` anchored on a crystallographic Cd ion (curated rationale: "no
metal required"), missing the Ser nucleophile. They expose a method gap:
ligand-proximity locators structurally cannot reach cofactorless catalytic
triads.

Materialization (done): the 53 approved source-free locator sidecars were copied
into the audited locator directory
`artifacts/family_panel_source_free_active_site_locators_current702_20260601/`
(now 5 family-panel + 53 Lever 2 = 58 sidecars) via the write-enabled
materialization gate. Each sidecar carries `manual_review_approval.approved_by:
VivekVardhanArrabelli`, `locator_policy:
human_approved_structure_local_ligand_geometry_without_source_text`,
`ready_for_predicted_geometry_scoring: True`, and stays split-protected
(review_only, not for training/threshold/import). The 2 rejected rows
(`m_csa:723`, `m_csa:599`) were not written. The audited-dir regression snapshot
test was updated to the 58-sidecar post-approval state. No heldout rows were read
and no frozen residual threshold was applied.

Consequence / next gate: (1) the approved source-free locator surface now exists;
the frozen residual threshold and any heldout read remain blocked on the
source-free event-axis proton-transfer linker (0 linker rows) or an explicit
His-count fallback acceptance, plus the heldout-safe application surface. (2)
Build a source-free catalytic-triad geometric locator for serine hydrolases
(decision: design): detect a Ser/Cys/Thr-His-Asp/Glu triad from coordinates +
residue identity only, under the same forbidden-feature contract, emitting the
same `residue_locators` schema, then re-decide `m_csa:723`/`m_csa:599`.

Verification: write-enabled materialization gate reports 53
`approved_locator_sidecars_written`, 0 critical violations,
`approved_source_free_locator_surface_ready: True`, with
`heldout_rows_evaluated: False` and `frozen_residual_threshold_applied: False`;
intake preflight reports status ready with 53 locator-materialization-ready
approvals, 2 rejections, 0 invalid, 0 source-edit-contract violations.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_approval_decisions_current702_20260603.json`,
`artifacts/v3_active_lever_source_decision_intake_preflight_lever2_decision_applied_current702_20260603.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_materialization_gate_materialized_current702_20260603.json`,
the 53 materialized sidecars under
`artifacts/family_panel_source_free_active_site_locators_current702_20260601/`,
and
`work/active_lever_lever2_locator_rewrite_reviewer_decision_record_current702_20260603.md`.

## 2026-06-03: Organic-Score Follow-Up Proxy Axis Scored, Still Partial

Decision: keep the `organic_score_0_30_to_below_high_axis_threshold` Lever 3
follow-up proxy axis as a bounded train/cal-only tranche readout. It excludes
the already scored overlap row `m_csa:89`, scores only the four remaining
contracted rows, and does not authorize a global fixed-threshold proxy audit
rerun or deployment closure claim. No labels, registries, ontologies, imports,
production thresholds, splits, model weights, source decisions, or heldout
threshold tuning changed.

Result: the follow-up contract selects `m_csa:60`, `m_csa:75`, `m_csa:214`,
and `m_csa:288`. All four now have AFDB-v6 query coordinates, nearest-train
Foldseek/TM hits, predicted-geometry scores, selected cofactor scores, and
combined geometry/fold channel scores. At fixed threshold `0.44155`, only
`m_csa:288` abstains. The composed train/cal OOS surface expands to 196/202
full-channel rows and remains partial because six prior/base blockers are still
unresolved. The post-follow-up background-axis scout now reports 160 remaining
background-only rows, 0 active-site-count candidates, 0 organic-score
candidates, and 8 unsupported-geometry rows that remain data-quality blockers
rather than countable abstention evidence. A repair-only queue now records all
eight unsupported-geometry rows with accessions and required coordinate/locus
repair gates; 0/8 expected AFDB-v6 coordinate files are local and 0 rows are
ready to score.

Consequence / next gate: do not promote this readout to an operating-point
claim. First clear the remaining prior/base full-channel and policy/calibration
blockers, starting with the P10746 decision if reviewed, or pre-register another
non-overlapping train/cal-only source-free proxy-axis contract before further
scoring.

Artifacts:
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_contract_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_contract_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_scoring_input_manifest_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_scoring_input_manifest_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_scored_extension_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_scored_extension_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_fixed_threshold_readout_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_fixed_threshold_readout_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_extended_train_cal_oos_surface_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_extended_train_cal_oos_surface_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_post_followup_background_axis_blocker_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_post_followup_background_axis_blocker_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_post_followup_background_axis_scout_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_post_followup_background_axis_scout_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_post_followup_unsupported_geometry_repair_queue_current702_20260603.json`,
and
`work/fold_augmented_confounded_proxy_train_cal_post_followup_unsupported_geometry_repair_queue_current702_20260603.md`.

## 2026-06-03: Active-Site-Count Proxy Axis Scored, Not Closure-Sufficient

Decision: keep the new `active_site_residue_count_10_plus` Lever 3 proxy axis
as a bounded train/cal-only readout. It is pre-registered and fully scored, but
it does not authorize a global fixed-threshold proxy audit rerun or deployment
closure claim. No labels, registries, ontologies, imports, production
thresholds, splits, model weights, source decisions, or heldout threshold tuning
changed.

Result: the contract selects six train/cal rows and the scoring extension gives
6/6 full-channel geometry/fold/cofactor rows. The appended surface has 192/198
train/cal OOS full-channel rows and remains partial because six prior/base
blockers are still unresolved. At fixed threshold `0.44155`, the new proxy axis
abstains only `m_csa:466` and retains the other five rows.

Consequence / next gate: do not promote this readout to an operating-point
claim. First clear the remaining prior/base full-channel and policy/calibration
blockers, or pre-register another train/cal-only source-free proxy-axis contract
before further scoring.

Artifacts:
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_contract_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_new_proxy_axis_contract_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_scoring_input_manifest_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_new_proxy_axis_scoring_input_manifest_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_scored_extension_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_new_proxy_axis_scored_extension_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_extended_train_cal_oos_surface_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_new_proxy_axis_extended_train_cal_oos_surface_current702_20260603.md`,
`artifacts/v3_fold_augmented_confounded_proxy_train_cal_new_proxy_axis_fixed_threshold_readout_current702_20260603.json`,
`work/fold_augmented_confounded_proxy_train_cal_new_proxy_axis_fixed_threshold_readout_current702_20260603.md`,
`artifacts/v3_active_lever_mechanical_actionability_audit_current702_20260603.json`,
and
`work/active_lever_mechanical_actionability_audit_current702_20260603.md`.

## 2026-06-03: Source-Free Locator Policy Queue Closed For Automation

Decision: close the remaining family-panel source-free locator policy queue for
automation. This is not an import/countability unlock: all five locator rows
remain blocked, no locator copy/scoring is authorized, and no labels,
registries, ontologies, imports, thresholds, splits, model weights, or
coordinates changed.

Result: the consolidated closure status composes the `mh_065`/`mh_072`,
external glycoside, Q59490, and `mh_064` block decisions with the import-preview
blocker gate. It records 5 blocked locator rows, 0 automation-clearable locator
decisions, 0 rows approved for locator copy or predicted-geometry scoring, 0
import-preview-ready rows, and 0 countable label candidates.

Consequence / next gate: do not continue locator automation on these five rows
until external approval/evidence is supplied. If evidence arrives, rerun the
relevant locator schema/integrity and import-preview blocker gates before
scoring or countability claims.

Artifacts:
`artifacts/v3_family_panel_source_free_locator_policy_closure_status_current702_20260603.json`
and
`work/family_panel_source_free_locator_policy_closure_status_current702_20260603.md`.

## 2026-06-03: mh_064 Locator Left Blocked; No Alternate Fetch Authorized

Decision: leave `mh_064` blocked. Do not fetch alternate coordinates in this
automation run, do not copy locator sidecars, and do not run predicted-geometry
scoring. No import, label, registry, ontology, threshold, split, or model-weight
change is authorized.

Rationale: the local-cache preflight found zero of five bounded alternate
coordinate files cached for `3RKJ`, `3RKK`, `3SBL`, `3SFP`, and `3SPU`. The
selected `3PG4` coordinate and requested AFDB coordinate are cached but do not
clear the no-ligand alternate-coordinate blocker. Fetching new coordinates is a
policy action and is not authorized by this automation run.

Consequence / next gate: unblock only after explicit approval to fetch one or
more bounded alternate coordinates, then rerun candidate extraction and locator
schema/integrity review before predicted-geometry scoring. The remaining
locator-policy queue is now closed for automation: all unresolved rows require
external approval/evidence before copy, fetch, scoring, import, or label action.

Artifacts:
`artifacts/v3_family_panel_source_free_locator_mh064_block_decision_current702_20260603.json`
and
`work/family_panel_source_free_locator_mh064_block_decision_current702_20260603.md`.

## 2026-06-03: Q59490 Locator Left Blocked; No Alternate Source Or Fabricated Locators

Decision: leave `secondary_probe::cobalamin_radical_rearrangement` / Q59490
blocked. Do not authorize alternate-source substitution, do not fabricate
residue locators from panel identity or source prose, and do not run
predicted-geometry scoring. No coordinate fetch, locator copy, import, label,
registry, ontology, threshold, split, or model-weight change is authorized.

Rationale: the nonlabel-locator feasibility audit found no coordinate anchor
that can safely provide at least two source-free sequence-position locators for
Q59490. The alternate-source cache scout found zero eligible alternate cobalamin
source rows and zero excluded rows with local coordinates. The three primary
Q59490 local coordinate paths do not by themselves authorize locator
fabrication.

Consequence / next gate: unblock only with an explicitly authorized alternate
source row/coordinate or a nonlabel locator strategy with at least two
source-free sequence-position locators, then rerun locator schema/integrity
review before predicted-geometry scoring. The remaining open locator-policy
decision is now `mh_064` alternate-coordinate fetch approval.

Artifacts:
`artifacts/v3_family_panel_source_free_locator_q59490_block_decision_current702_20260603.json`
and
`work/family_panel_source_free_locator_q59490_block_decision_current702_20260603.md`.

## 2026-06-03: External Glycoside Locator Left Blocked; No Acetate/NAG Copy

Decision: leave `external_glycoside_panel` blocked. Do not copy the 7QQF
acetate locator, NAG/glycan-derived locator, or any raw glycan/buffer
retargeting into the audited source-free locator directory. No predicted-
geometry scoring, coordinate fetch, import, label, registry, ontology,
threshold, split, or model-weight change is authorized.

Rationale: the NAG validator already rejected glycan-context retargeting. The
local-cache substrate-coordinate scout scanned 60 coordinate files and found
four same-accession coordinate records but zero substrate-like coordinate
candidates. The only same-accession PDB coordinate with non-water HETATMs has
ACT/BMA/FUC/MAN/MLI/NAG glycan or buffer ligands, which cannot clear the
non-glycan substrate-coordinate gate.

Consequence / next gate: unblock only with an explicit substrate-complex
coordinate or expert-approved non-glycan active-site locator, then rerun
locator schema/integrity review before predicted-geometry scoring. The remaining
open locator-policy decisions are now `mh_064` alternate-coordinate fetch
approval and Q59490 nonlabel locator or alternate-source authorization.

Artifacts:
`artifacts/v3_family_panel_source_free_locator_external_glycoside_block_decision_current702_20260603.json`
and
`work/family_panel_source_free_locator_external_glycoside_block_decision_current702_20260603.md`.

## 2026-06-03: Expanded Train/Cal OOS Threshold Regeneration Keeps 0.44155

Decision: materialize the post-rerun expanded train/cal OOS-negative surface
and regenerate the OOS-calibrated fold-augmented threshold contract from that
surface. This is a research calibration artifact only: no production threshold,
label, registry, ontology, import, split, model weight, or heldout-tuned surface
changed.

Result: the expanded surface composes the four fixed-threshold combined readout
rows into the prior train/cal OOS negative surface, increasing full-channel
coverage from 71/76 to 75/76 rows. `m_csa:204`/P10746 remains the sole
fold-only policy caveat and the surface is still partial. The regenerated
OOS-calibrated research contract keeps the primary
`combined_mean_geometry_fold` threshold at `0.44155`; calibration OOS
abstention is 30/75, and the heldout final readout remains 45/47 in-scope rows
retained, 44/79 OOS rows abstained, and 5/6 cofactor-confounded OOS rows
abstained.

Consequence / next gate: do not rerun this threshold-selection step unless the
train/cal surface changes again. Lever 3 deployment closure is still blocked by
the P10746 fold-only caveat: either explicitly accept that caveat for
deployment closure or provide an approved non-residue sidecar.

Artifacts:
`artifacts/v3_fold_augmented_expanded_train_cal_oos_negative_surface_scores_current702_20260603.json`,
`work/fold_augmented_expanded_train_cal_oos_negative_surface_scores_current702_20260603.md`,
`artifacts/v3_fold_augmented_abstention_threshold_contract_expanded_oos_calibrated_current702_20260603.json`,
and
`work/fold_augmented_abstention_threshold_contract_expanded_oos_calibrated_current702_20260603.md`.

## 2026-06-03: mh_065/mh_072 Remapped Locators Rejected; Leave Blocked

Decision: leave `mh_065` and `mh_072` blocked. Do not copy the raw
`1DDK`/`1E9I` locators and do not approve alignment/remapped locators from the
current evidence.

Rationale: the matching-coordinate scout scanned 712 local coordinate files and
found 0 matching non-AFDB replacement coordinates. The selected PDBs map by
`struct_ref` to `Q932P5` and `P08324`, not the requested source rows `Q79MP6`
and `P0A6P9`. The only same-accession AFDB options already failed residue-code
transfer with 0/6 expected residue-code matches. Approving remapped locators
would accept the unverified-transfer failure mode the locator schema is meant
to block.

Consequence / next gate: these rows remain review-only/non-countable and
source-free predicted-geometry scoring stays blocked. Unblock only with a
matching frozen coordinate whose `struct_ref` maps to the requested source
accession, or with a real expert alignment/remapping that resolves the
residue-code mismatch, followed by locator schema/integrity review.

Artifacts:
`artifacts/v3_family_panel_source_free_locator_mh065_mh072_block_decision_current702_20260603.json`
and
`work/family_panel_source_free_locator_mh065_mh072_block_decision_current702_20260603.md`.

## 2026-06-03: Lever 3 Human Decisions Applied; Combined Rerun Readout Lands

Decision: record the five Lever 3 production-blocker human/policy decisions as
a decision-application artifact, materialize the three approved source-feature
sidecars, fetch/hash the authorized P00889 ortholog surrogate coordinate, and
compose a fixed-threshold pre-rerun readiness gate. P10746 is kept fold-only
with the non-residue-sidecar policy caveat. No Foldseek/TM or combined-channel
rerun was performed before the readiness gate. A follow-on fixed-threshold
readout then reran only the P00889 surrogate Foldseek query against the existing
train atlas, scored the four combined rows at threshold `0.44155`, and kept
P10746 fold-only. No labels, registries, ontologies, imports, thresholds,
splits, model weights, or heldout-tuned surfaces changed.

Result: the human/policy decision blockers are now 0, but deployment closure is
still false. The approved source-feature sidecar surface has been materialized
for rerun input with 3 rows and 18 source-feature support records. The P00889
AFDB CIF has been fetched and hashed (`8e41533a...`). The pre-rerun readiness
gate reports ready=true with 0 remaining pre-rerun blockers. The fixed-threshold
combined readout scores four rows: `m_csa:78` and `uniprot:P78549` abstain,
while `m_csa:531` and `uniprot:Q3LXA3` are retained. The calibration-impact
audit expands the train/cal OOS combined-score surface from 71/76 to 75/76
rows, with 30/75 abstained at the fixed threshold and only `m_csa:204` still
blocked from combined scoring. The post-rerun closure-status gate therefore
reduces the prior five production blockers to one unresolved P10746 fold-only
caveat, while preserving the existing 5/6 heldout confounded OOS abstention
readout from the prior readiness artifact. The post-rerun confounded closure
audit now composes the expanded threshold contract directly and records the
current state as research-ready with one P10746 caveat, not five production
blockers.

Consequence / next gate: carry the fixed-threshold impact and P10746 fold-only
caveat into the deployment decision. Either explicitly accept the P10746
fold-only caveat for deployment closure or provide an approved non-residue
sidecar. A 2026-06-03 UniProtKB refresh for P10746 returned HTTP 200 and 63
features, but 0 eligible active-site/binding-site source-feature rows, so it
does not open an automation-clearable sidecar path. A P10746 decision packet now
stages the one remaining accept/reject choice with an unchanged context hash;
the companion application gate validates the current packet as hash-matched
but still pending. The post-decision closure gate therefore remains blocked
only by the unaccepted P10746 caveat. No caveat was accepted and deployment
remains unclosed. A separate OOS-calibrated threshold regeneration may be run
from the expanded train/cal surface only if wanted; do not tune on heldout rows.

Artifacts:
`artifacts/v3_fold_augmented_blocker_human_decision_application_current702_20260603.json`,
`work/fold_augmented_blocker_human_decision_application_current702_20260603.md`,
`artifacts/v3_fold_augmented_approved_source_feature_active_site_sidecar_materialization_current702_20260603.json`,
`work/fold_augmented_approved_source_feature_active_site_sidecar_materialization_current702_20260603.md`,
`artifacts/v3_fold_augmented_p00889_ortholog_coordinate_fetch_manifest_current702_20260603.json`,
`work/fold_augmented_p00889_ortholog_coordinate_fetch_manifest_current702_20260603.md`,
`artifacts/v3_fold_augmented_fixed_threshold_rerun_readiness_current702_20260603.json`,
`work/fold_augmented_fixed_threshold_rerun_readiness_current702_20260603.md`,
`artifacts/v3_fold_augmented_fixed_threshold_combined_rerun_readout_current702_20260603.json`,
`work/fold_augmented_fixed_threshold_combined_rerun_readout_current702_20260603.md`,
`artifacts/v3_fold_augmented_fixed_threshold_combined_rerun_calibration_impact_current702_20260603.json`,
`work/fold_augmented_fixed_threshold_combined_rerun_calibration_impact_current702_20260603.md`,
`artifacts/v3_fold_augmented_p10746_source_feature_refresh_audit_current702_20260603.json`,
`work/fold_augmented_p10746_source_feature_refresh_audit_current702_20260603.md`,
`artifacts/v3_fold_augmented_post_rerun_deployment_closure_status_current702_20260603.json`,
`work/fold_augmented_post_rerun_deployment_closure_status_current702_20260603.md`,
`artifacts/v3_fold_augmented_post_rerun_confounded_deployment_closure_audit_current702_20260603.json`,
`work/fold_augmented_post_rerun_confounded_deployment_closure_audit_current702_20260603.md`,
`artifacts/v3_fold_augmented_p10746_deployment_caveat_decision_packet_current702_20260603.json`,
`work/fold_augmented_p10746_deployment_caveat_decision_packet_current702_20260603.md`,
`artifacts/v3_fold_augmented_p10746_deployment_caveat_decision_application_current702_20260603.json`,
`work/fold_augmented_p10746_deployment_caveat_decision_application_current702_20260603.md`,
`artifacts/v3_fold_augmented_post_decision_deployment_closure_status_current702_20260603.json`,
and
`work/fold_augmented_post_decision_deployment_closure_status_current702_20260603.md`.

## 2026-06-03: Lever 4 Local-Cache Locator Discovery Closes With Five Human/Policy Blockers

Decision: treat the remaining family-panel source-free locator blockers as
human/policy decisions, not automation-discovery tasks. No coordinates were
fetched, no locator sidecars were copied, no predicted-geometry scoring was
run, no import preview was written, and no labels, registries, ontologies,
thresholds, splits, model weights, or heldout-tuned surfaces changed.

Result: local-cache scouts found 0 non-AFDB replacement coordinates for
`mh_065`/`mh_072`, 0 same-accession substrate-like coordinates for
`external_glycoside_panel`, and 0 eligible alternate source rows for Q59490.
The human-decision matrix now tracks 5 remaining blocker rows across 4 decision
classes, with 0 automation-clearable rows. The refreshed family-panel
import-preview blocker gate still reports 0/22 import-preview-ready rows and
0 countable label candidates.

Consequence / next gate: decide the `mh_065`/`mh_072` matching-coordinate or
remapped-locator policy first, then rerun the relevant locator schema/candidate
audit and the import-preview blocker gate before any copy, fetch, scoring,
import preview, or label-factory action.

Artifacts:
`artifacts/v3_family_panel_source_free_locator_matching_coordinate_scout_mh065_mh072_current702_20260602.json`,
`work/family_panel_source_free_locator_matching_coordinate_scout_mh065_mh072_current702_20260602.md`,
`artifacts/v3_family_panel_source_free_locator_glycoside_substrate_coordinate_scout_external_glycoside_panel_current702_20260602.json`,
`work/family_panel_source_free_locator_glycoside_substrate_coordinate_scout_external_glycoside_panel_current702_20260602.md`,
`artifacts/v3_family_panel_source_free_locator_q59490_alternate_source_cache_scout_current702_20260602.json`,
`work/family_panel_source_free_locator_q59490_alternate_source_cache_scout_current702_20260602.md`,
`artifacts/v3_family_panel_source_free_locator_human_decision_matrix_current702_20260601.json`,
`work/family_panel_source_free_locator_human_decision_matrix_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_import_preview_blocker_gate_current702_20260602.json`,
and
`work/fold_augmented_family_panel_import_preview_blocker_gate_current702_20260602.md`.

## 2026-06-02: Lever 3 Blocker-Specific Gates Cover All Five Remaining Fold Deployment Rows

Decision: keep the predicted-structure-vs-atlas fold channel at the fixed
OOS-calibrated operating threshold `0.44155` and treat the five remaining
production blocker rows as explicit review/policy gates, not as fold-only or
automatic sidecar escapes. No sidecar was approved or copied, no alternate
accession was authorized, no coordinate was fetched, no Foldseek/TM scores were
rerun, and no thresholds, labels, registries, ontologies, imports, or model
weights changed.

Result: the source-feature sidecar review gate covers the three
coordinate-available source-feature blocker rows (`m_csa:531`,
`uniprot:P78549`, and `uniprot:Q3LXA3`) with 3 strict-audit-clean draft rows
and 3 manual approval decisions required. The P23007 alternate-accession policy
gate exposes 4 AFDB-backed pattern-compatible citrate-synthase candidates
(`O75390`, `P00889`, `Q8VHF5`, and `Q9CZU6`) but authorizes 0 replacements and
0 coordinate fetches. The P10746 non-residue interaction preflight keeps
`m_csa:204` blocked with 0 source-feature rows, 0 curated residue nodes, and 0
approved non-residue policy rows; mechanism text remains forbidden as a
predictive sidecar source.

Consequence / next gate: decide the three draft source-feature sidecar
approvals, decide exactly one P23007 alternate accession or reject the
substitution path, and approve a concrete P10746 non-residue interaction
sidecar policy or keep it fold-only. Only after those decisions should the
combined predicted-geometry/fold channel be rerun at the fixed threshold.

Artifacts:
`artifacts/v3_fold_augmented_source_feature_active_site_sidecar_review_gate_current702_20260602.json`,
`work/fold_augmented_source_feature_active_site_sidecar_review_gate_current702_20260602.md`,
`artifacts/v3_fold_augmented_p23007_alternate_accession_policy_gate_current702_20260602.json`,
`work/fold_augmented_p23007_alternate_accession_policy_gate_current702_20260602.md`,
`artifacts/v3_fold_augmented_non_residue_interaction_sidecar_policy_preflight_current702_20260602.json`,
`work/fold_augmented_non_residue_interaction_sidecar_policy_preflight_current702_20260602.md`,
`artifacts/v3_predicted_structure_fold_confounded_operating_point_readiness_current702_20260602.json`,
and
`work/predicted_structure_fold_confounded_operating_point_readiness_current702_20260602.md`.

## 2026-06-03: Priority-1 Source-Free Locator Preflight Is Not Copy Approval

Decision: the 55 priority-1 current702 heldout coordinate-anchor locator rows
that passed rewrite preflight remain blocked until an explicit approval-decision
artifact supplies matching candidate and planned-payload hashes. Preflight alone
does not authorize copying locator sidecars into the audited directory, scoring
heldout rows, or applying the frozen row-specific residual threshold.
The approval packet is an intake worksheet, not an approval artifact: it stages
55 pending approve/reject records with immutable candidate and planned-payload
hashes, while recording 0 approvals.

Rationale: the calibrated Lever 2 row-specific feature pair still needs a
source-free heldout locator surface and a source-free proton-transfer event
axis. Copying from preflight without explicit approval would bypass the manual
forbidden-feature review gate that separates source-free locator evidence from
heldout M-CSA mechanism text and curated role labels. The approval packet now
names the exact hash-matched records reviewers must produce; the new gate
consumes approvals mechanically when they exist but fails closed now: 55
preflight rows, 0 explicit approvals, 0 locator writes, and 0 heldout reads.
The composed pre-threshold readiness gate additionally requires materialized
source-free event-axis linkers and a complete heldout-safe pair application
surface before the frozen residual threshold can be applied once.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_approval_packet_current702_20260603.json`,
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_approval_packet_current702_20260603.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_materialization_gate_current702_20260603.json`,
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_materialization_gate_current702_20260603.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_pre_threshold_readiness_current702_20260603.json`,
and
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_pre_threshold_readiness_current702_20260603.md`.

## 2026-06-02: Source-Free Pair Deployment Blocks On Event Linker; His-Only Fallback Is Lower Recall

Decision: keep the calibrated row-specific best-token follow-up pair as
calibration-only until a source-free event/residue-role linker exists. The pair
uses `event_residue_role:proton_transfer|electrostatic_stabiliser` plus
`residue_code_count:his=3`; the first token cannot be computed from the current
source-free heldout surface without a source-free proton-transfer event axis.
Do not substitute the M-CSA curated heldout active-site role graph as a
deployment feature.

Result: the event-linker blocker audit confirms 0 current702 heldout locator
sidecars, 0 source-free event/residue-role feature rows, and 132 M-CSA curated
heldout role-graph rows that remain forbidden as deployment inputs. The
calibrated pair keeps calibration OOS abstention at 0.857143. A separate
His-count-only fallback contract avoids the event axis but drops calibration OOS
abstention to 0.642857 (AUC 0.758929), so it is not accepted as a deployable
replacement without an explicit policy decision. The fallback is also blocked
by the same source-free locator surface: 55 preflight-passed locator rewrites
remain pending explicit approval, including 6 warning rows and 0 approved
rewrites.

Consequence / next gate: choose one of two explicit paths before any heldout
read. Preferred path: build the source-free proton-transfer event-axis linker
for `proton_transfer|electrostatic_stabiliser`, then rerun the source-free
application surface and heldout-safe surface plan. Fallback path: explicitly
accept the lower-recall His-count-only contract, approve/copy audited
current702 heldout locator sidecars, and only then apply the frozen fallback
threshold once. No labels, registries, ontologies, imports, production
thresholds, model weights, or heldout readouts changed.

Schema gate: the source-free event-axis linker schema is now staged. It requires
an approved current702 heldout locator sidecar, accession-compatible
UniProt-validated residue positions, a source-free residue-role assignment, and
source-free proton-transfer event-axis evidence. It explicitly forbids M-CSA
heldout mechanism text, curated heldout active-site roles, labels/outcomes,
source IDs, target names, and EC/Rhea IDs as predictive inputs. It materializes
0 linker rows.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_linker_blocker_audit_current702_20260602.json`,
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_linker_blocker_audit_current702_20260602.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_residue_count_fallback_contract_current702_20260602.json`,
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_residue_count_fallback_contract_current702_20260602.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_schema_current702_20260602.json`,
and
`work/mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_schema_current702_20260602.md`.

## 2026-06-02: P0 Approved Rows Materialized Train/Cal-Only; No-Template Rerun Now Blocks On Calibration Review

Decision: materialize only the three reviewer-approved P0 M-CSA-only source
rows (`m_csa:5`, `m_csa:11`, and `m_csa:169`) into a partial train/cal
row-specific bond/proton/electron feature sidecar. The sidecar copies only
label-stripped event-count/boolean features from approved source evidence; it
does not copy draft rows, heldout rows, source text, source IDs, reviewer IDs,
labels, fingerprints, or accessions as predictive features. No model weights,
thresholds, labels, registries, ontologies, imports, or production scorers
changed.

Result: all three approved rows are assigned to the train split, so the partial
feature surface is materialized but not sufficient for a no-template centroid or
residual rerun. It contains 3 feature rows and 0 calibration rows, with approved
event counts of 3 `bond_broken`, 2 `bond_formed`, 2 `electron_transfer`, and 2
`proton_transfer` events. A strict train/cal feature guardrail audit passes with
0 critical violations and confirms the predictive payload is restricted to
numeric/boolean event features. The remaining 12 P0 source-evidence rows stay
draft and non-consumable.

Consequence / next gate: the coverage-gap audit identifies four
calibration-assigned draft rows as the next manual review gate:
`m_csa:186`, `m_csa:147`, `m_csa:6`, and `m_csa:133`. `m_csa:186` and
`m_csa:147` also add the currently unmaterialized `bond_order_changed` event
type. A manual calibration review packet now carries those four rows and 16
event-review records, but records no approvals. After human approve/rewrite/reject
decisions are copied into the source-evidence sidecar, rerun the strict
sidecar/readiness/materialization artifacts before attempting the no-template
centroid pilot or the out-of-span residual on the richer feature surface.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_train_cal_feature_sidecar_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_train_cal_feature_sidecar_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_train_cal_feature_guardrail_audit_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_train_cal_feature_guardrail_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_train_cal_coverage_gap_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_train_cal_coverage_gap_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_calibration_review_packet_current702_20260601.json`,
and
`work/mechanism_feature_row_specific_bond_change_p0_calibration_review_packet_current702_20260601.md`.

## 2026-06-02: P0 Rhea-Absent Rows Approved As M-CSA-Only Source Evidence With Split-Filtered Use Only

Decision: approve all three P0 row-specific bond-change rows that official
Rhea/UniProt lookup could not Rhea-resolve: `m_csa:5`, `m_csa:11`, and
`m_csa:169`. The reviewer decision is `approve_m_csa_only_source_evidence`,
with reviewer provenance recorded as Vivek Vardhan Arrabelli in the P0 source
evidence sidecar. UniProt confirms matching EC activity for all three rows, but
Rhea returns no EC/accession cross-reference; these are explicitly
reviewer-approved M-CSA-only source-evidence rows, not Rhea-resolved rows.

Consequence: the strict sidecar audit now passes with 3 approved consumable rows
and 12 remaining draft rows. The Rhea lookup manifest has 0 remaining rows, the
Rhea consumption audit reports 3 reviewer-approved M-CSA-only rows, and the
reviewer decision matrix is copy-ready for those three rows. Full 15-row
no-template feature-contract refresh remains blocked until the remaining draft
rows are reviewed, but partial train/cal feature materialization is allowed for
only the three approved rows.

Load-bearing guardrail: these bond-change/proton/electron features are
M-CSA-derived. They are safe only because the feature materialization path must
filter to train/cal rows and keep the 140 heldout M-CSA rows excluded from
training and threshold selection. Do not train, calibrate, or tune deployment
thresholds on heldout M-CSA rows using these features.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_current702_20260601.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_strict_audit_current702_20260601.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_rhea_lookup_manifest_current702_20260601.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_rhea_resolution_consumption_audit_current702_20260601.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_reviewer_decision_matrix_current702_20260601.json`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_feature_readiness_audit_current702_20260601.json`,
and
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_refresh_blocker_audit_current702_20260601.json`.

## 2026-06-02: Lever 2 Integrated — Two Independent Builds Become One Result; The Closed-Form Residual Is The Live Deployable Signal, The Centroid Pilot's Discipline And Feature Track Are Retained

Decision: integrate the two independent Lever 2 implementations rather than
choosing one and discarding the other. The closed-form information-preserving
metric (the "residual line") and the standardized nearest-primary centroid pilot
(the "centroid line") are both agent-built, treated as equals, and kept; the
genuine advancement of each is carried forward into a single Lever 2 result.

Synthesis:
- Consolidated negative (robust precisely because two independent builds agree):
  a learned or standardized embedding over the CURRENT feature surface does not
  deployably beat the geometry baseline. The metric's predeclared primary is a
  clean negative (AUC 0.616 vs top1_score 0.757). The centroid pilot's strong
  numbers (calibration AUC 0.948, heldout 0.881) are reaction-template dependent;
  its deployment-valid no-template ablation is at chance (heldout AUC 0.489).
  Neither full-contract score is deployment evidence.
- Live deployable signal: the residual line's unsupervised out-of-atlas-span
  residual is the surviving win — deployment-valid (sequence-only), confirmed
  (PCA cutoff-robust sweep + a held-out-from-design confirmatory split with a
  label-permutation null, p=0.0005), and integrated into the per-channel rule
  gate for a +0.076 confounded-safe OOS-abstain lift at the >=85% retention floor.
  The residual threshold remains research-grade pending deployable calibration.
- Retained from the centroid line (genuine advancements, not discarded): (1) its
  train/cal/heldout fitting discipline (fit on 418 train rows, threshold on 106
  calibration rows, once-only heldout readout) becomes the standard the residual's
  deployable calibration must meet; (2) the audited mechanism-feature contract
  surface and the P0 source-evidence sidecar / bond-change / proton-transfer /
  electron-flow feature-materialization track (with Rhea provenance) is the kept
  forward path to the genuinely-new mechanism feature.

Consequence / unified next: materialize the row-specific bond-change/proton/
electron features (resolve open Rhea rows `m_csa:11`, `m_csa:169`, `m_csa:5` and
reviewer provenance first), then re-run BOTH the no-template centroid pilot and
the out-of-span residual on that template-free surface under the centroid line's
train/cal/heldout discipline; give the residual a deployable calibration; and
close a deployment-valid confounded-safe channel (Lever 3). No code or artifacts
from either build were removed.

Work/artifacts: `work/mechanism_feature_embedding_current702_20260601.md`,
`work/mechanism_feature_residual_robustness_current702_20260601.md`,
`work/mechanism_residual_gate_integration_current702_20260601.md`,
`artifacts/v3_mechanism_feature_embedding_pilot_current702_20260601.json`,
`artifacts/v3_mechanism_feature_embedding_heldout_readout_current702_20260601.json`.

## 2026-06-02: Confirmed Residual Adds A Confounded-Safe Operating-Point Lift To The Rule Gate (Research-Grade Threshold)

Decision: integrate the now-confirmed out-of-span residual into the per-channel
RULE gate as a third orthogonal lift channel and measure its marginal
operating-point contribution, rather than promoting it on AUC alone. The deployed
rule (geometry leads; cofactor adds abstentions only where its signature is weak)
is extended with a residual term carrying the SAME confounded-safe guard:

    abstain = geom < tg
              OR (cof < signature AND cof < tc)              # cofactor-agnostic-lift
              OR (cof < signature AND residual_novelty >= tr)  # residual-agnostic-lift

The residual is concentrated on the cofactor-agnostic majority and is NOT
confounded-safe (confounded AUC ~0.66 vs geometry 0.84), so gating it on
`cof < signature` keeps confounded rows decided by geometry alone. The
three-channel search space contains the two-channel gate (a high tr disables the
term), so a three-channel optimum can never be worse; the question was the lift
magnitude and confounded-safety preservation. Predeclared PASS = residual adds
OOS-abstain-recall AND preserves confounded-abstain-recall, at the operative
retention floor.

Result (deployment pool 47 in-scope / 79 OOS; 6 confounded / 73 agnostic; residual
channel all-OOS AUC reproduced live at 0.72098, matching the embedding eval). The
operative floor is >=85% in-scope retention: neither gate has a >=90% point because
the agnostic-lift terms unavoidably abstain too many low-cofactor in-scope rows at
the minimum threshold. At >=85% retention the two-channel gate abstains on 0.3038
of OOS (confounded 0.1667, agnostic 0.3151); adding the residual-agnostic-lift
raises OOS-abstain-recall to 0.3797 (+0.0759), ENTIRELY from the agnostic subset
(0.3151 -> 0.3973), with the confounded subset UNCHANGED at 0.1667 -- the
predeclared PASS holds (adds lift, confounded-safe). The confounded subset remains
the binding constraint, exactly motivating the Lever 3 fold channel.

Deployability (honest scope). tg and tc are thresholds on calibrated [0,1]
confidences and are deployable constants; the residual threshold tr is NOT. 100% of
held-out rows sit above the atlas residual maximum, so the residual's
atlas-percentile calibration SATURATES and the signal survives only in raw/relative
form -- tr is an eval-pool-relative RESEARCH operating point (a calibration-free ROC
sweep over observed residual values), not a production threshold. The reported lift
is the residual's marginal operating-point contribution; a deployable residual
calibration, or the Lever 4 expanded family set, is required before production
promotion. An exploratory ungated variant (residual firing on all rows) is recorded
for transparency but is not the predeclared agnostic-lift form.

Consequence: the confirmed residual translates into a real, confounded-safe
operating-point lift on the cofactor-agnostic majority (+0.076 OOS-abstain-recall at
85% retention), banking the Lever 2 win at the gate level -- but it does NOT close
the operational gap, because the safety-critical confounded subset is unmoved and
the residual threshold is not yet deployable. The next gains must come from a
confounded-safe channel (Lever 3, deployment-valid fold/structure novelty) and a
deployable residual calibration or the wider Lever 4 surface. No labels, registries,
ontologies, splits, thresholds, or production scorers changed; the residual is
sequence-only and atlas-only-fit, M-CSA rows are eval-only, the deployable
thresholds are untuned, and the cofactor channel is read-only for stratification.

Reproduce: `PYTHONPATH=src python -m catalytic_earth.cli
eval-mechanism-residual-gate-integration`. Module:
`src/catalytic_earth/mechanism_residual_gate_integration.py`. Tests:
`tests/test_mechanism_residual_gate_integration.py` (3 fast + 1 slow integration
gated behind `CATALYTIC_RUN_SLOW`). Artifacts:
`artifacts/v3_mechanism_residual_gate_integration_current702_20260601.json`,
`work/mechanism_residual_gate_integration_current702_20260601.md`.

## 2026-06-01: Out-Of-Span Residual Survives The Cutoff-Robustness And Predeclared Confirmatory Tests

Decision: before treating the out-of-atlas-span residual (the AUC 0.721 Lever 2
lead) as more than an eval-pool hypothesis, run the two checks that were
predeclared as its gate -- a PCA variance-cutoff robustness sweep (leakage/overfit
test) and a held-out-from-its-own-design confirmatory split -- with the pass/fail
bars, fold salt, and permutation seed all fixed a priori. Both pass, so the
residual graduates from exploratory readout to a confirmed candidate third
orthogonal lift channel.

Robustness sweep (leakage/overfit). The residual is the representation energy
outside the atlas PCA span, and the span size is a fixed variance cutoff. Sweeping
it (95% / 97% / 99%) re-derives the residual off a single shared atlas
eigendecomposition (an anchor assertion confirms the 99%/128-dim point reproduces
the committed 0.72098). Deployment-pool all-OOS AUC is 0.7072 (95%, 81-dim span),
0.7215 (97%, 98-dim), 0.7210 (99%, 128-dim cap, 0.9891 variance) -- range 0.0143,
inside the predeclared <=0.05 band; all three >=0.65; and agnostic-subset AUC
exceeds confounded-subset AUC at every cutoff. Note the 99% target is cap-limited
to 128 dims, so the 95%/97% points genuinely shrink the span (81/98 dims) -- the
sweep tests real span-size sensitivity, not a no-op. S1/S2/S3 all hold: the 0.721
is NOT an artifact of the chosen cutoff.

Confirmatory split (held out from the lead's own design). The lead was surfaced on
the whole deployment pool, so its 47/79 sample could be lucky. The held-out rows
were partitioned into two folds by a salted hash of the entry id
(`sha256('residual_confirm::'+id) % 2`) -- a split independent of the residual
values and of how the lead was found -- with fold 1 reserved as the confirmation
fold and the pass criteria committed before reading it. Significance is a
label-permutation null (2000 shuffles, seed 20260601) over the fixed residual
scores. The confirmation fold (29 in / 30 OOS) scores AUC 0.7885 at permutation
p=0.0005; the design-echo fold (18/49) scores 0.654 at p=0.029; pooled 0.721 at
p=0.0005. H1 (confirmation AUC>=0.65 AND p<0.05), H2 (both folds AUC>=0.60), and
H3 (confirmation agnostic AUC >= confounded AUC) all hold: the separation is real
and significant on data that played no role in the discovery, and the
cofactor-agnostic directional structure replicates.

Consequence: the out-of-span residual is a stable, generalizing novelty signal,
not a cutoff/eval-pool artifact -- it is promoted to a candidate third orthogonal
lift channel (geometry-led gate + cofactor-agnostic-lift + residual-agnostic-lift)
for predeclared threshold work. It remains NOT confounded-safe (confounded AUC
~0.66 vs geometry 0.84), so it must still be paired with a confounded-safe channel
(Lever 3, fold) before any threshold promotion -- the confirmatory test validated
the lift, not standalone gating. Lever 4 (an expanded family set) is the stronger
confirmation surface but is a proposal only today; this test used the design-split
route on the existing eval pool and should be re-run once an expanded set is
materialized. No labels, registries, ontologies, splits, thresholds, or production
scorers changed; the atlas-only fit and M-CSA-eval-only constraints are preserved,
and the fold split is independent of the residual scores.

Reproduce: `PYTHONPATH=src python -m catalytic_earth.cli
eval-mechanism-residual-robustness`. Module:
`src/catalytic_earth/mechanism_feature_residual_robustness.py`. Tests:
`tests/test_mechanism_feature_residual_robustness.py` (8 fast + 1 slow integration
gated behind `CATALYTIC_RUN_SLOW`). Artifacts:
`artifacts/v3_mechanism_feature_residual_robustness_current702_20260601.json`,
`work/mechanism_feature_residual_robustness_current702_20260601.md`.

## 2026-06-01: Lever 2 Learned Mechanism-Feature Embedding Is A Clean Negative With An Out-Of-Span Residual Lead

Decision: implement Lever 2 (a learned mechanism-feature embedding) as a
closed-form, information-preserving supervised metric rather than a trainable
network, and report the result honestly at the operating point. The space is
sequence-only (ESM2-150M), fit ONLY on the in-distribution atlas: robust
standardize (atlas median/IQR) -> PCA over the atlas span (keep >=99% atlas
variance, capped at 128 dims; here 128 dims capturing 0.9891) -> within-class
whitening (a regularized full-rank Mahalanobis metric, fixed 0.10 shrinkage,
condition number 99.4). All hyperparameters are fixed a priori, NOT tuned on
heldout. A trainable GNN/classifier was explicitly rejected for this lever: the
supervised surface is only 184 atlas rows across 7 represented classes (the 8th
fingerprint, `radical_sam_enzyme`, has zero in-distribution rows; classes range
1-66 rows), there is no deployment-valid per-residue graph on disk, the
no-heldout-tuning guardrail forbids validation-based training, and a
high-capacity discriminative model worsens novelty by pulling OOS confidently
onto class manifolds.

Result (deployment pool: 47 in-scope / 79 OOS; 6 confounded / 73 agnostic;
baseline geometry top1_score reproduced live at AUC 0.757). The PREDECLARED
primary signal (equal-weight percentile mean of nearest-prototype, kNN-density,
and out-of-span residual) does NOT beat the baseline: AUC 0.616 and
OOS-abstain-recall 0.165 at >=90% retention vs 0.757 / 0.215. The supervised
whitening DISTANCE signals (prototype 0.606, kNN 0.613) are near the bare-PLM
level, confirming that discriminative reshaping is the wrong lever for novelty
(the linear discriminant-energy signal was already at chance, AUC 0.524). The
one genuinely new, orthogonal signal is the UNSUPERVISED out-of-atlas-span
residual (sequence-representation mass outside the directions known mechanism
chemistry occupies): AUC 0.721, and at the operating point it abstains on 0.241
of OOS at >=90% retention -- ABOVE the geometry baseline's 0.215 -- concentrated
on the cofactor-agnostic OOS majority. It is NOT safe on the safety-critical
cofactor-confounded subset (confounded abstain-recall 0.333 vs baseline 0.500;
confounded AUC 0.663 vs 0.840), so it is a COMPLEMENTARY LIFT channel, not a
replacement gate -- the same role the cofactor channel plays. The predeclared
percentile combiner washes out the residual (every held-out row sits below the
atlas residual distribution, so its atlas-percentile saturates to 0); the
residual carries signal only in RAW form and must be used as its own channel.

Consequence: Lever 2 does not by itself make de novo abstention operational, and
that is a valid, expected outcome cleanly reported. The actionable lead is the
out-of-span residual as a third, orthogonal lift channel (geometry-led gate +
cofactor-agnostic-lift + residual-agnostic-lift), to be validated with a
PREDECLARED confirmatory test (not the exploratory readout here) and paired with
a confounded-safe channel before any threshold promotion. The committed row-keyed
learned embedding (702 rows, 128-d whitened coords + residual) is reusable for
downstream de novo work. No labels, registries, ontologies, splits, thresholds,
or production scorers changed; M-CSA heldout rows were eval-only, never trained.

Reproduce: `PYTHONPATH=src python -m catalytic_earth.cli
eval-mechanism-feature-embedding`. Module:
`src/catalytic_earth/mechanism_feature_embedding.py`. Tests:
`tests/test_mechanism_feature_embedding.py` (10 fast + 1 slow integration gated
behind `CATALYTIC_RUN_SLOW`). Artifacts:
`artifacts/v3_mechanism_feature_embedding_eval_current702_20260601.json`,
`artifacts/v3_mechanism_feature_embedding_current702_20260601.jsonl`,
`work/mechanism_feature_embedding_current702_20260601.md`.
## 2026-06-01: Mechanism-Feature Embedding Pilot Is Implemented, But Template-Dependent

Decision: move the learned mechanism-feature lane from a no-fit scaffold to a
real train/cal-only pilot. The pilot consumes the audited
`v3_mechanism_feature_embedding_feature_contract_current702_20260601.json`
surface, fits standardized nearest-primary centroids on the 418 assigned train
rows, and selects the operating threshold only on the 106 assigned calibration
rows. No heldout rows are used for fitting, threshold selection, or evaluation;
no labels, registries, ontologies, imports, production scorers, or production
thresholds changed.

Result: the full contract variant reaches calibration AUC `0.948491` for
primary-vs-OOS nearest-primary similarity and abstains on 100% of calibration
OOS rows at 91.43% primary retention. The stricter
`no_reaction_template_ablation` drops to calibration AUC `0.549698` and 14.08%
OOS abstention at the same retention target.

Follow-up: materialize the same feature surface for heldout rows and apply the
train-fit/calibration-thresholded pilot once. Existing sidecars cover 132/140
heldout rows; 8 remain blocked by accession-compatible role-graph gaps. The
full-contract heldout readout reaches AUC `0.8812` and abstains on 100% of
ready OOS rows, but retains only 75% of ready primary rows at the
calibration-selected threshold. The no-template ablation is near chance on
heldout with AUC `0.488591` and 9.52% OOS abstention at 85.42% primary
retention.

Consequence: treat the pilot as implemented but not yet scientifically
sufficient. The strong full-contract result is largely reaction-template
dependent; the next useful mechanism-feature work is to materialize
row-specific bond-change, proton-transfer, and electron-flow evidence. Do not
cite the full-contract train/cal or heldout scores as deployment evidence.

Artifact:
`artifacts/v3_mechanism_feature_embedding_pilot_current702_20260601.json`;
`artifacts/v3_mechanism_feature_embedding_heldout_readout_current702_20260601.json`.

## 2026-06-01: Fold-Augmented Threshold Contract Selects Thresholds On Train/Calibration Rows, Not Heldout

Decision: promote the fold-augmented heldout-only diagnostic into a bounded
thresholding contract. The run used deterministic, fingerprint-stratified
partitioning over the in-distribution predicted atlas rows: 134 train targets and
34 calibration queries. AlphaFoldDB v6 CIFs were materialized transiently, and
Foldseek exact TM scoring was run only for the 34 calibration queries against the
133 available train-target CIFs. The resulting small TSV and parsed
JSON/report are committed; persistent coordinate files are not. No label,
registry, ontology, import, split, production scorer, or production threshold
changed.

Result: the primary predeclared channel, `combined_mean_geometry_fold`, selected
threshold `0.44155` at the >=90% calibration in-scope retention target, retaining
31/34 calibration rows (`0.9118`). Applying that threshold once to heldout rows
retains 45/47 in-scope rows (`0.9574`), abstains on 44/79 OOS rows (`0.557`),
and abstains on 5/6 cofactor-confounded OOS rows (`0.8333`). The
cofactor-including mean abstains on more all-OOS heldout rows (`0.6329`) but
still abstains on none of the cofactor-confounded OOS rows, matching the earlier
safety warning.

Consequence: the fold-augmented gate now has a leakage-safe research threshold
contract rather than a post-hoc heldout threshold. It is still not an authorized
production threshold because train/cal provides in-scope retention calibration
only: the current predicted atlas does not include train/cal OOS negatives for
threshold optimization. Next work should either add a frozen train/cal OOS
negative surface for threshold selection or move to the mechanism-feature
embedding gap with this threshold contract as the current fold-aware baseline.

Artifacts:
`artifacts/v3_fold_augmented_abstention_threshold_contract_current702_20260601.json`,
`artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/in_distribution_atlas_self_vs_atlas.tsv`,
`work/fold_augmented_abstention_threshold_contract_current702_20260601.md`.

Follow-up: add a review-only matched-retention delta audit between the frozen
predicted-atlas geometry operating grid and the frozen fold-augmented operating
grid. At the 90% in-scope-retention diagnostic, fold augmentation lifts OOS
abstention from `0.2278` to `0.7722` and cofactor-confounded OOS abstention
from `0.3333` to `0.8333`. This comparison reads existing heldout diagnostic
artifacts only and does not select, tune, or promote a threshold.

## 2026-06-01: Fold-Augmented Research Gate Applied To Review-Only Family Panels

Decision: add a downstream readout that applies the already selected
OOS-calibrated `combined_mean_geometry_fold` research threshold to the seven
review-only family-expansion evidence packets. This consumes the
research-sufficient 71/76 train/cal OOS-negative surface decision and the
family-panel coverage audit. It does not select thresholds on family-panel rows,
fit a model, promote rows, import labels, or mutate registries/ontologies.

Result: after the M-CSA repair follow-up, 12/22 review rows are score-complete
for the primary geometry-plus-predicted-fold channel. Of those, 6 remain
non-abstained at the fixed `0.44155` research threshold: `m_csa:267`,
`m_csa:131`, `m_csa:750`, `m_csa:551`, `m_csa:132`, and `m_csa:116`. Six
score-complete rows abstain, including `m_csa:973` after joining its frozen
train/calibration fold score, and 10 rows remain blocked by missing predicted
active-site geometry evidence. Those 10 rows now have source-backed
AFDB-vs-predicted-atlas fold scores from the P0/P1 materialization follow-up.

Consequence: the next review work should keep the six source-checked
non-abstained boundary rows review-only, while working the 10 remaining
primary-channel-missing rows through source-free predicted-geometry sidecars.
This readout is review-only and must not be interpreted as a family promotion,
production threshold, or training signal.

Follow-up: the rank-1 queue row, `m_csa:267`, was source-checked against frozen
local M-CSA graph and label artifacts. The check keeps it as a review-only OOS
boundary control: local mechanism evidence supports dihydrodipicolinate
synthase lysine Schiff-base aldol/cyclization chemistry, not a current
seed-family promotion.

Second follow-up: the rank-2 row, `m_csa:131`, was source-checked against
frozen local M-CSA graph and label artifacts. The check confirms direct flavin
monooxygenase/oxygen-transfer support for the existing secondary-probe row, but
does not authorize primary FMO promotion while the project-state FMO blockers
remain active.

Third follow-up: the rank-3 row, `m_csa:750`, was source-checked through the
current registry and the existing `m_csa:750` revision artifact. The check
keeps it as OOS/boundary evidence and a future radical flavin/Fe-S dehydratase
candidate, not a current v1 flavin, FMO, cobalamin, or radical-SAM promotion.

Fourth follow-up: the rank-4 row, `m_csa:551`, was source-checked through
frozen M-CSA graph evidence and the existing FMO local-candidate adjudication.
The check confirms mechanism-clean future FMO support, but the prior
adjudication explicitly blocks import and registry edits, so no label or
promotion state changed.

Repair follow-up: apply the existing accession-compatible predicted-geometry
repair policy to the two queued M-CSA rows. `m_csa:132` switches from manifest
accession `P07739` to real-sequence accession `P07740`, resolves 5/5 catalytic
positions, and scores nearest-atlas Foldseek/TM `0.6879`. `m_csa:116` uses the
manifest accession-compatible residue subset on `Q2RSB2`, resolves 5/5 scored
positions, and scores nearest-atlas Foldseek/TM `0.5417`. Both become
score-complete and non-abstained at the fixed research threshold. The refreshed
missing queue now has 10 rows, all secondary-probe or external/placeholder rows
that required source-backed sidecars and coordinate materialization before the
later P0/P1 materialization follow-up.

Fifth/sixth follow-up: the newly non-abstained repaired M-CSA rows were
source-checked from frozen local graph, registry, repair, and readout artifacts.
`m_csa:132` is confirmed only as secondary FMO support after geometry repair,
with no primary FMO promotion. `m_csa:116` stays a review-only OOS
NAD(P)+-transhydrogenase/hydride-transfer control. No label, registry, import,
threshold, split, or production scorer changed.

Queue follow-up: add and refresh a separate review-only materialization queue
for the family-panel rows that lack primary geometry-plus-predicted-fold channel
scores. The first queue/diagnosis showed `m_csa:973` already had frozen
train/calibration fold evidence in the threshold contract. The family-panel
readout now joins that score without rerunning Foldseek/TM, so `m_csa:973`
becomes score-complete and abstained at the fixed research threshold
(`combined_mean_geometry_fold=0.41` versus `0.44155`). After the M-CSA repair,
the remaining queue has 10 rows, all secondary-probe or external/placeholder
rows requiring source-backed row sidecars and coordinate materialization.

FMO subtype follow-up: add and refresh a review-only subtype/hard-negative
packet for the FMO lane. It keeps `m_csa:131` and repaired `m_csa:132` as
secondary-probe support, `m_csa:551` and `m_csa:973` as future support only,
and `m_csa:750` as radical flavin/Fe-S boundary negative. No row is
import-ready or registry-edit-ready, so primary FMO promotion remains blocked.

Materialization-plan follow-up: stage the next review-only carryover for the
10 remaining missing primary-channel rows without fetching coordinates or
scoring them. The plan selects source-backed representatives from frozen
artifacts: Q59490 for `secondary_probe::cobalamin_radical_rearrangement`,
A0A1M6T2I7 for `secondary_probe::radical_sam_enzyme`, Q6NSJ0 for
`external_glycoside_panel`, and the seven prior-resolved `mh_*` rows from the
external identifier scout. It records exact PDB/AFDB candidate commands and
sidecar fields while keeping every row review-only and non-countable.

P0/P1 materialization follow-up: materialize and hash the selected PDB
coordinates plus AFDB-v6 predicted coordinates for all 10 queued source-backed
representatives, then run Foldseek exact TM against the frozen predicted
in-distribution atlas. All 10 rows now have real predicted-fold hits, including
`0.4655` for Q59490, `0.7039` for A0A1M6T2I7, `0.6259` for Q6NSJ0, and
metal-hydrolase/boundary nearest TM scores from `0.5936` to `1.004`. The family
packets, readout, missing-channel queue, and diagnosis were refreshed. The rows
remain primary-channel incomplete because source-free predicted active-site
geometry top1 scores are still missing. No labels, registries, imports,
thresholds, splits, or production scorers changed.

Source-free geometry follow-up: validate that the real fold channel and the
10-row source-backed materialization are not runtime-blocked, then stage the
source-free predicted-geometry sidecar manifest. All 10 rows have AFDB-v6 CIF
hashes and source-backed Foldseek/TM scores, but 0/10 have approved source-free
active-site locator sidecars. The blocker-clearing attempts checked existing
predicted-geometry retrieval rows, current702 label-manifest membership,
source-backed sidecars, and coordinate/Foldseek runtime state. The result is a
semantic blocker, not a Foldseek or coordinate blocker: these rows are
secondary/external review rows outside the current702 graph-backed residue
locator surface. A companion strict locator schema now requires at least two
source-free sequence-position residue locators per row and explicitly forbids
entry names, EC/Rhea identifiers, source prose, mechanism text, labels,
benchmark roles, and panel IDs as predictive geometry features. No labels,
registries, imports, thresholds, splits, or production scorers changed.
The companion schema audit is staged and currently reports 0/10 locator
sidecars present, with `locator_sidecar_missing` as the only critical violation
class. A materialization plan now records the exact locator sidecar paths and
rerun commands for all 10 rows; eight rows start from a
structure-local-ligand-geometry policy candidate, while `mh_067` and `mh_068`
carry same-accession current702 geometry matches and require split-safe
train/cal-template checks before any locator use. A template-only bundle now
stages the 10 planned locator sidecar shells outside the audited locator
directory. The templates are review-only, contain no residue locators, create no
audited sidecars, and are not ready for predicted-geometry scoring.

Candidate-audit follow-up: a coordinate-only candidate extractor now stages
review-only locator candidates outside the audited locator directory. It uses
only selected mmCIF atom coordinates, residue/ligand comp IDs, atom names,
distances, and `_struct_ref_seq` accession mappings; no source prose, labels,
EC/Rhea IDs, or mechanism text are admitted as predictive features. Eight rows
have at least two candidate locators from selected-structure ligand/metal
contacts, and six of those rows have all candidate positions prevalidated
against matching UniProt mapping metadata. Q59490 and C7C422 remain blocked
because their selected PDB coordinates expose no non-water/non-metal ligand
candidate under this extractor; Q79MP6 and P0A6P9 still need UniProt
position-validation review. No candidate is scoring-ready: all still require
manual forbidden-feature review, and `mh_067`/`mh_068` need a split-safe
template check before any sidecar can be copied to the audited locator
directory.

Candidate-integrity follow-up: audit the staged locator candidate sidecar files
against the candidate-audit payload before manual review. All 10 candidate files
are present, payload-matched, outside the audited locator directory, and
guardrail-clean; 0 are scoring-ready. This keeps the next step as manual
scientific/forbidden-feature review rather than predicted-geometry scoring.

Review-queue follow-up: rank the candidate sidecars by the next validation
blocker. Three rows are priority-1 for manual forbidden-feature review
(`mh_066`, `mh_073`, and `secondary_probe::radical_sam_enzyme`). Q6NSJ0 needs
ligand-specificity review because the selected ligand candidate is acetate;
P00918/P15289 need split-safe template checks; Q79MP6/P0A6P9 still need UniProt
position-validation review; Q59490/C7C422 require a new source-free locator path
or alternate coordinate. The queue still creates no audited locator sidecars and
scores no predicted geometry.

Manual-review packet follow-up: combine candidate sidecar SHA-256s, integrity
status, review priority, and per-row checklists into a single handoff artifact.
The packet is ready for human review with 10 integrity-passed rows, three
priority-1 manual review rows, 0 copy-ready rows, and 0 scoring-ready rows.

Priority-1 preflight follow-up: dry-run the three priority-1 manual-review
rows (`mh_066`, `mh_073`, and
`secondary_probe::radical_sam_enzyme`) against the locator schema, candidate
guardrails, and coordinate-contact plausibility checks. All three pass this
automation preflight, with `mh_073` flagged because it sits exactly at the
minimum two-locator floor. This does not approve or copy sidecars: human
approval remains required before rewriting any locator into the audited
directory and rerunning the schema audit.

Blocked-row rescue follow-up: inspect the two source-free locator rows blocked
by no non-water/non-metal ligand candidate. Both selected local coordinates
contain only water HETATMs. `mh_064` has five frozen source alternate PDB IDs
from the existing identifier scout (`3RKJ`, `3RKK`, `3SBL`, `3SFP`, and
`3SPU`), so the manifest stages exact fetch commands pending manual approval.
Q59490 has only `1L1L` in the frozen cobalamin blocker artifact, so it remains
blocked on a new nonlabel locator strategy or an explicitly authorized
alternate source row. No coordinate fetch, locator copy, predicted geometry
scoring, label/import, registry, ontology, split, threshold, or production
scorer change occurred.

Approved-locator scoring follow-up: after human approval moved `mh_066`,
`mh_073`, and `secondary_probe::radical_sam_enzyme` into the audited
source-free locator directory, run a bounded review-only predicted-geometry
retrieval over those three rows. The run uses only approved sequence-position
locators, residue codes, generic locator role hints, local AFDB-v6 CIFs, and
geometry-derived pocket context; it does not use source prose, entry names,
panel IDs, labels, EC/Rhea IDs, benchmark roles, heldout training, or new
downloads. All three rows resolve at least two predicted residues and receive
top1 geometry scores, and all three are retained when joined to their existing
source-backed fold scores under the fixed `combined_mean_geometry_fold`
research threshold. The review-only family-panel readout was refreshed to
consume those scores: 15/22 rows are now primary score-complete, 9 are
non-abstained, 6 abstain, and 7 remain missing primary-channel scores. Seven
rows remain blocked on approved source-free locators. No labels, imports,
registries, ontology entries, splits, thresholds, model weights, production
scorers, source fetches, or coordinate downloads changed.

Source-check preflight follow-up: package those three newly non-abstained
source-free geometry rows for local review before any family-panel action. The
preflight keeps all three rows in `hold_review_only_pending_source_check`,
identifies `mh_066` as the first source-check target because its geometry and
fold fingerprints agree, and flags `mh_073` plus
`secondary_probe::radical_sam_enzyme` for mechanism-locus and duplicate/leakage
review. No source adjudication, family admission, labels, imports, registries,
thresholds, splits, or production scorers changed.

`mh_066` source-check follow-up: complete a frozen-local review-only source
check for the IMP-1 metallo-beta-lactamase row. The source-free geometry and
predicted-fold channels agree on `metal_dependent_hydrolase`, local 1DD6
coordinate metadata supports a zinc metallo-beta-lactamase hydrolase context,
and current702 has no exact P52699 accession duplicate. The nearest predicted
fold atlas row is still an occupied B1 beta-lactamase seed (`m_csa:15`), and
the external row lacks an extracted row-specific bond-change/residue-role
sidecar plus duplicate/split/expert admission. Keep `mh_066` review-only and
non-countable; do not promote or import it without a future explicitly
authorized admission packet.

`mh_073` source-check follow-up: complete a frozen-local review-only source
check for the H-Ras row. Local 121P coordinate metadata supports an Mg/GTPase
nucleotide locus, the external panel predeclares it as a hard negative against
Mg/nucleotide leakage, and the source-free geometry channel disagrees with the
metal-hydrolase fold hit. The nearest predicted-fold atlas row is `m_csa:535`,
a current702 GTPase-like seed currently labeled `metal_dependent_hydrolase`,
which makes `mh_073` a boundary/leakage diagnostic rather than promotion
evidence. Keep it review-only and non-countable unless a future authorized
GTPase-boundary policy reopens current702 scope.

Radical-SAM source-check follow-up: complete a frozen-local review-only source
check for `secondary_probe::radical_sam_enzyme` using the freeze artifact,
local 8VPO coordinate metadata, the approved SF4-contact locator, and current
family-panel readouts. The evidence supports a TigE radical-SAM/Fe-S locus, but
the source-free geometry channel calls `metal_dependent_hydrolase` and the
nearest predicted-fold atlas row is the PLP-dependent seed `m_csa:358`.
Current702 has no exact A0A1M6T2I7 duplicate and only one radical-SAM secondary
probe row, so this is useful radical/Fe-S panel evidence but remains
review-only and non-importable pending row-specific bond-change, duplicate/split
review, and expert admission.

Remaining-locator queue follow-up: classify the seven family-panel rows still
blocked on approved source-free active-site locators after the three source
checks. All seven have AFDB coordinate hashes and source-backed fold scores, but
none is scoring-ready. Two rows need UniProt position validation (`mh_065`,
`mh_072`), two need split-safe same-accession template checks (`mh_067`,
`mh_068`), one needs ligand-specificity review (`external_glycoside_panel`),
one has manually approved alternate-coordinate fetch commands but requires
approval before any fetch (`mh_064`), and Q59490 needs a new nonlabel locator
strategy or explicitly authorized alternate source row. No sidecars were copied,
coordinates fetched, geometry scored, labels/imports changed, or thresholds
touched.

UniProt-position validation follow-up: attempt the `mh_065`/`mh_072`
sequence-position validation using only frozen local candidate sidecars and
selected PDB mmCIF mappings. Both rows remain blocked because the selected PDB
`struct_ref` accessions do not match the source-row accessions: `1DDK` maps to
`Q932P5` rather than `Q79MP6`, and `1E9I` maps to `P08324` rather than
`P0A6P9`. The candidate contacts remain review evidence, but no source-free
locator sidecar can be copied and no predicted-geometry score can be produced
without an explicit representative-accession equivalence policy or a frozen
coordinate whose mapping matches the requested source accession.

Split-safe template follow-up: check `mh_067` and `mh_068` against the current702
manifest before any locator copy. Both candidates have validated
sequence-position locators, no forbidden source/label predictive fields, and
same-accession current702 matches that are in-distribution seed rows
(`m_csa:216` for P00918 and `m_csa:158` for P15289), not heldout rows. This
clears the split-safety question as review-only evidence, but it does not copy
sidecars or authorize predicted-geometry scoring; manual locator-copy approval
is still required before either row can enter the audited locator directory.

Ligand-specificity follow-up: review the `external_glycoside_panel` selected
coordinate ligand before any locator copy. The current candidate selected
acetate (`ACT`) in local unliganded MYORG structure `7QQF`; that ligand is too
nonspecific for a glycoside-hydrolase active-site locator. Frozen NAG contacts
exist in the same candidate extraction, but local annotations include
glycan/N-glycosylation context, so they are not an automatic catalytic-substrate
replacement. Keep the row blocked until a dedicated glycoside-ligand validator
or an explicitly approved substrate-complex coordinate is available.

No-ligand policy-blocker follow-up: isolate the remaining no-ligand/metal
source-free locator blockers. `mh_064` cannot proceed from selected structure
`3PG4`; it has five frozen alternate-coordinate fetch commands but those
require explicit approval before any download. Q59490 has no detected ligand or
metal site in selected `1L1L` and no frozen alternate PDB IDs, so it needs a
reviewed nonlabel locator strategy or approved alternate source row. No
coordinates were fetched, no locator sidecars were copied, and no scoring was
run.

Resolution-status follow-up: consolidate the seven unresolved source-free
locator blockers into one current status artifact. Automation discovery is now
complete for all seven, 0/7 are scoring-ready, and every remaining action is a
policy or human-review decision: accession equivalence or matching coordinates
for `mh_065`/`mh_072`, copy approval for `mh_067`/`mh_068`, ligand validator or
substrate coordinate for `external_glycoside_panel`, alternate-coordinate fetch
approval for `mh_064`, and a nonlabel locator strategy or alternate source row
for Q59490.

Integrity follow-up: index the current run's 10 new JSON artifacts and 10 work
reports in a parse/presence audit. The audit records no label/registry/ontology
mutation, no production-threshold mutation, no coordinate fetches, no model
fit, and no predicted-geometry scoring; validation results are captured for
pytest, unittest discovery, compileall, `validate`, and diff-check.

Artifacts:
`artifacts/v3_fold_augmented_family_panel_research_readout_current702_20260601.json`,
`work/fold_augmented_family_panel_research_readout_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_source_check_queue_current702_20260601.json`,
`work/fold_augmented_family_panel_source_check_queue_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_source_check_m_csa267_current702_20260601.json`,
`work/fold_augmented_family_panel_source_check_m_csa267_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_source_check_m_csa131_current702_20260601.json`,
`work/fold_augmented_family_panel_source_check_m_csa131_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_source_check_m_csa750_current702_20260601.json`,
`work/fold_augmented_family_panel_source_check_m_csa750_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_source_check_m_csa551_current702_20260601.json`,
`work/fold_augmented_family_panel_source_check_m_csa551_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_m_csa_primary_channel_repair_current702_20260601.json`,
`work/fold_augmented_family_panel_m_csa_primary_channel_repair_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_source_check_m_csa132_current702_20260601.json`,
`work/fold_augmented_family_panel_source_check_m_csa132_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_source_check_m_csa116_current702_20260601.json`,
`work/fold_augmented_family_panel_source_check_m_csa116_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_missing_primary_channel_queue_current702_20260601.json`,
`work/fold_augmented_family_panel_missing_primary_channel_queue_current702_20260601.md`,
`artifacts/v3_fold_augmented_family_panel_missing_primary_channel_diagnosis_current702_20260601.json`,
`work/fold_augmented_family_panel_missing_primary_channel_diagnosis_current702_20260601.md`,
`artifacts/v3_family_panel_source_backed_sidecar_materialization_plan_current702_20260601.json`,
`work/family_panel_source_backed_sidecar_materialization_plan_current702_20260601.md`,
`artifacts/v3_family_panel_source_backed_sidecar_materialization_current702_20260601.json`,
`work/family_panel_source_backed_sidecar_materialization_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_predicted_geometry_sidecar_manifest_current702_20260601.json`,
`work/family_panel_source_free_predicted_geometry_sidecar_manifest_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_predicted_geometry_retrieval_current702_20260601.json`,
`work/family_panel_source_free_predicted_geometry_retrieval_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_predicted_geometry_source_check_preflight_current702_20260601.json`,
`work/family_panel_source_free_predicted_geometry_source_check_preflight_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_predicted_geometry_source_check_mh_066_current702_20260601.json`,
`work/family_panel_source_free_predicted_geometry_source_check_mh_066_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_predicted_geometry_source_check_mh_073_current702_20260601.json`,
`work/family_panel_source_free_predicted_geometry_source_check_mh_073_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_predicted_geometry_source_check_secondary_probe_radical_sam_enzyme_current702_20260601.json`,
`work/family_panel_source_free_predicted_geometry_source_check_secondary_probe_radical_sam_enzyme_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_locator_remaining_blocker_action_queue_current702_20260601.json`,
`work/family_panel_source_free_locator_remaining_blocker_action_queue_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_locator_uniprot_position_validation_mh065_mh072_current702_20260601.json`,
`work/family_panel_source_free_locator_uniprot_position_validation_mh065_mh072_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_locator_split_safe_template_check_mh067_mh068_current702_20260601.json`,
`work/family_panel_source_free_locator_split_safe_template_check_mh067_mh068_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_locator_ligand_specificity_review_external_glycoside_panel_current702_20260601.json`,
`work/family_panel_source_free_locator_ligand_specificity_review_external_glycoside_panel_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_locator_policy_blockers_mh064_q59490_current702_20260601.json`,
`work/family_panel_source_free_locator_policy_blockers_mh064_q59490_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_locator_blocker_resolution_status_current702_20260601.json`,
`work/family_panel_source_free_locator_blocker_resolution_status_current702_20260601.md`,
`artifacts/v3_current_run_artifact_integrity_audit_current702_20260601.json`,
`work/current_run_artifact_integrity_audit_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_schema_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_schema_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_schema_audit_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_schema_audit_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_materialization_plan_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_materialization_plan_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_template_bundle_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_template_bundle_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_candidate_audit_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_candidate_audit_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_candidate_integrity_audit_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_candidate_integrity_audit_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_review_queue_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_review_queue_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_manual_review_packet_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_manual_review_packet_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_active_site_locator_priority1_review_preflight_current702_20260601.json`,
`work/family_panel_source_free_active_site_locator_priority1_review_preflight_current702_20260601.md`,
`artifacts/v3_family_panel_source_free_locator_blocked_row_rescue_manifest_current702_20260601.json`,
`work/family_panel_source_free_locator_blocked_row_rescue_manifest_current702_20260601.md`,
`artifacts/v3_fmo_subtype_hard_negative_packet_current702_20260601.json`,
`work/fmo_subtype_hard_negative_packet_current702_20260601.md`.

## 2026-06-01: Predicted-Structure Fold Channel Contract Audit Passes

Decision: add a strict validation layer for the already-scored AlphaFoldDB
predicted-structure Foldseek/TM channel rather than regenerating the scored
artifact. The audit checks frozen current702 row counts, parsed Foldseek TSV
coverage, source artifact hashes, guardrails, score ranges, expected command
tokens, and the allowed computed blockers. No label, registry, ontology, import,
split, threshold, production scorer, or scored fold-channel value changed.

Result: the contract audit passes with zero critical violations. It confirms
126/126 ok heldout rows have nearest-atlas Foldseek/TM hits, all six priority
cofactor-confounded OOS rows have parsed priority hits, and the only fold-channel
blockers are persistent coordinate-file provenance blockers. The all-heldout TSV
has 11,297 mapped pairs; the priority TSV has 402 mapped pairs.

Consequence: downstream fold-augmented gate work can treat the scored predicted
fold channel as validated for current702. Persistent predicted-CIF provenance is
still useful reproducibility infrastructure, but it is not a score-completeness
blocker under this contract.

Artifacts:
`artifacts/v3_predicted_structure_fold_channel_contract_audit_current702_20260601.json`,
`work/predicted_structure_fold_channel_contract_audit_current702_20260601.md`.

Reproduction-manifest follow-up: add a validation-only reproduction manifest
for the same scored channel. It records the 299 expected AFDB-v6 coordinate
paths across 293 deduplicated accessions, exact Foldseek rerun commands, scored
TSV SHA-256 hashes, contract/provenance audit hashes, and the single blocker
class `persistent_afdb_v6_coordinate_bundle_missing`. No coordinate download,
Foldseek/TM rerun, label, registry, ontology, import, split, threshold, or
production scorer change occurred.

Artifacts:
`artifacts/v3_predicted_structure_fold_channel_reproduction_manifest_current702_20260601.json`,
`work/predicted_structure_fold_channel_reproduction_manifest_current702_20260601.md`.

Carryover-resolution follow-up: add a validation-only audit for stale
automation prompts that still ask to build or stage the predicted-structure fold
channel. It consumes the scored channel, contract audit, coordinate provenance
audit, reproduction manifest, predicted-atlas retrieval, and fold-level signal.
The audit confirms the requested fold-channel artifact/report are present,
126/126 ok heldout rows and 6/6 priority cofactor-confounded rows are scored,
the contract has zero critical violations, and no Foldseek/TM rerun is needed.
The remaining `persistent_afdb_v6_coordinate_bundle_missing` blocker is only for
byte-level reproduction.

Artifacts:
`artifacts/v3_predicted_structure_fold_channel_carryover_resolution_current702_20260601.json`,
`work/predicted_structure_fold_channel_carryover_resolution_current702_20260601.md`.

2026-06-02 persistence follow-up: materialized the exact AFDB-v6 coordinate
bundle recorded by the predicted-structure fold channel: 299 expected CIF paths
across 293 deduplicated accessions. No Foldseek/TM score was recomputed, no
threshold changed, and no label/import/registry surface changed. The fold-channel
manifest, contract audit, deployment-input audit, coordinate-provenance audit,
reproduction manifest, carryover-resolution audit, and confounded readiness
artifact were regenerated against the persisted bytes. The coordinate-provenance
gate is now complete, byte-level reproduction is ready, and Lever 3 deployment
closure remains blocked only by the five production blocker rows plus the
rejected fold-only escape hatch.

Artifacts:
`artifacts/v3_predicted_structure_fold_channel_current702_20260601.json`,
`artifacts/v3_predicted_structure_fold_channel_coordinate_provenance_audit_current702_20260601.json`,
`artifacts/v3_predicted_structure_fold_channel_reproduction_manifest_current702_20260601.json`,
`artifacts/v3_predicted_structure_fold_channel_carryover_resolution_current702_20260601.json`,
`artifacts/v3_predicted_structure_fold_confounded_operating_point_readiness_current702_20260602.json`.

## 2026-06-01: Train/Cal OOS Negatives Add A Partial OOS Calibration Surface For The Fold-Augmented Gate

Decision: score the hash-selected in-distribution OOS calibration negatives
staged by the train/cal negative-surface manifest, then build a separate
OOS-calibrated research threshold contract. The run used frozen current702
inputs, transient AlphaFoldDB v6 CIF materialization under `/private/tmp`, exact
Foldseek/TM scoring against the threshold-contract train atlas, and the existing
selected organic cofactor sidecar. Heldout rows stayed final-only. No label,
registry, ontology, import, split, production scorer, or production threshold
changed.

Result: 71/76 selected calibration OOS candidates have full channel scores
(`predicted_geometry`, selected organic cofactor, and nearest-train Foldseek/TM).
Foldseek produced nearest-train hits for 75 candidates. The six
accession-compatible active-site mapping blockers (`m_csa:57`, `m_csa:106`,
`m_csa:178`, `m_csa:284`, `m_csa:314`, and `m_csa:503`) have been cleared with
bounded current702-safe accession/subset repair; `m_csa:284` uses `O66188` for
predicted geometry and the Foldseek query because the manifest accession
`O66186` has only one usable catalytic residue. `m_csa:78`/`P23007` still lacks
an AFDB query coordinate. The OOS-calibrated primary channel,
`combined_mean_geometry_fold`, keeps the same >=90% in-scope threshold,
`0.44155`, as the in-scope-only contract. At that threshold calibration OOS
abstain recall is 28/71 (`0.3944`), while heldout final readout remains
45/47 in-scope retained, 44/79 OOS abstained, and 5/6 cofactor-confounded OOS
abstained.

Consequence: the fold-augmented gate now has a real train/cal OOS-negative
surface, but it is partial and does not justify a production threshold. The next
decision is whether the 71-row surface is sufficient for a research operating
point or whether to clear the remaining five blockers first: AFDB coordinate
replacement for `m_csa:78`, source-geometry repair for `m_csa:204` and
`m_csa:531`, and active-site sidecars for `uniprot:P78549` and
`uniprot:Q3LXA3`. Four of the missing combined-channel rows have fold-only
scores and are preserved in a separate diagnostic salvage surface.

Artifacts:
`artifacts/v3_fold_augmented_train_cal_oos_negative_surface_scores_current702_20260601.json`,
`artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/train_cal_oos_negatives_vs_train_atlas.tsv`,
`artifacts/v3_fold_augmented_abstention_threshold_contract_oos_calibrated_current702_20260601.json`,
`artifacts/v3_fold_augmented_train_cal_oos_negative_surface_blocker_resolution_current702_20260601.json`,
`artifacts/v3_fold_only_train_cal_oos_negative_surface_current702_20260601.json`,
`work/fold_augmented_train_cal_oos_negative_surface_scores_current702_20260601.md`,
`work/fold_augmented_train_cal_oos_negative_surface_blocker_resolution_current702_20260601.md`,
`work/fold_only_train_cal_oos_negative_surface_current702_20260601.md`,
`work/fold_augmented_abstention_threshold_contract_oos_calibrated_current702_20260601.md`.

## 2026-06-01: Partial Train/Cal OOS Surface Is Sufficient For The Research Contract

Decision: resolve the handoff question about whether to block downstream
fold-augmented research diagnostics on the remaining five train/cal OOS-negative
surface gaps. The decision artifact applies a bounded, explicit policy: at least
90% score-complete coverage, no unresolved accession-compatible mapping
blockers, OOS-calibrated contract total matching the score-complete rows, and no
movement in the primary threshold relative to the in-scope-only contract. No
label, registry, ontology, import, split, production scorer, or threshold value
changed.

Result: the 71/76 surface is sufficient for the current research contract with
blocker disclosure. Coverage is `0.934211`; the OOS-calibrated contract consumes
exactly 71 calibration OOS rows; all accession-compatible mapping blockers are
cleared; and the primary `combined_mean_geometry_fold` threshold remains
`0.44155`. The surface is not sufficient for production-like claims while
`m_csa:78`, `m_csa:204`, `m_csa:531`, `uniprot:P78549`, and
`uniprot:Q3LXA3` remain unresolved.

Consequence: future runs should proceed with downstream diagnostics using this
research contract and disclosed blockers, rather than redoing the sufficiency
decision. Clear the five blockers before making any stronger threshold claim.

Artifacts:
`artifacts/v3_fold_augmented_train_cal_oos_negative_surface_sufficiency_decision_current702_20260601.json`,
`work/fold_augmented_train_cal_oos_negative_surface_sufficiency_decision_current702_20260601.md`.

## 2026-06-01: Remaining Train/Cal OOS Blockers Require New Source Evidence Or Coordinate Policy

Decision: inspect the five remaining score-surface blockers after the research
sufficiency decision and record whether any can be cleared from frozen current702
inputs. No label, registry, ontology, import, split, threshold, production
scorer, active-site sidecar, or coordinate policy changed.

Result: no blocker can be safely cleared in-repo from current inputs. `m_csa:78`
still exposes only P23007 locally and the scorer already recorded AFDB v1-v6
404s; experimental PDB 1AL6 does not clear the deployment predicted-coordinate
requirement. `m_csa:204` has no catalytic residue nodes in the current graph.
`m_csa:531` has only one catalytic residue and remains below geometry
eligibility. `uniprot:P78549` and `uniprot:Q3LXA3` are UniProt-only external
hard negatives without current active-site sidecars. Four rows have fold-only
evidence and should remain fold-only until source-backed sidecars exist.

Consequence: proceed with the research-sufficient 71/76 surface for downstream
diagnostics. Clear the five blockers only after new source-backed active-site
evidence, an alternate predicted coordinate, or an explicitly authorized
experimental-coordinate-only policy exists.

Artifacts:
`artifacts/v3_fold_augmented_train_cal_oos_remaining_blocker_clearance_attempts_current702_20260601.json`,
`work/fold_augmented_train_cal_oos_remaining_blocker_clearance_attempts_current702_20260601.md`.

## 2026-06-01: Active-Site Role Graph Sidecar Closes One Mechanism-Feature Embedding Gap

Decision: materialize a normalized row-level active-site residue-role graph
sidecar from the frozen current702 manifest and existing M-CSA graph. This is a
feature-readiness artifact only: it does not fit a model, tune a threshold, edit
labels, import rows, or change registries.

Result: 656/702 current702 rows have an accession-compatible active-site role
graph. The sidecar normalizes 53 residue-role vocabulary terms and 669
same-entry role co-occurrence edges. Remaining gaps are not inferred here:
directed proton/electron-transfer edges and row-specific bond-change mappings
still need a source-backed sidecar before a learned mechanism-feature embedding
pilot. A companion reaction-center template sidecar row-aligns fingerprint-level
chemical operations and bond-change descriptors for 232 rows, but it remains
template evidence rather than row-specific reaction evidence.

Consequence: the learned mechanism-feature embedding plan has one concrete
row-level feature sidecar available for future train/cal-only pilots, but it is
not itself model evidence and must not be used to train on heldout rows.

Artifacts:
`artifacts/v3_mechanism_feature_active_site_role_graph_sidecar_current702_20260601.json`,
`artifacts/v3_mechanism_feature_reaction_center_template_sidecar_current702_20260601.json`,
`work/mechanism_feature_active_site_role_graph_sidecar_current702_20260601.md`,
`work/mechanism_feature_reaction_center_template_sidecar_current702_20260601.md`.

## 2026-06-01: Mechanism-Feature Sidecar Schema Audit Passes

Decision: add a strict schema and row-alignment audit over the two current
mechanism-feature sidecars: active-site residue-role graphs and reaction-center
templates. The audit validates one row per current702 manifest entry, split /
accession / fingerprint alignment, required keys, allowed status values,
internal role/residue counts, template status consistency, and source status.
No model was fit and no label, registry, ontology, import, threshold, split, or
sidecar value changed.

Result: the schema audit passes with zero critical violations. Both sidecars
cover all 702 manifest rows. The active-site sidecar has 656 ok role-graph rows,
42 accession-position blockers, one missing catalytic-residue-node row, and
three non-M-CSA rows. The reaction-center template sidecar has 232 template rows
and 470 OOS/unlabeled rows without mechanism-fingerprint templates. The learned
mechanism-feature embedding plan now records this schema audit and marks the
current sidecars schema-safe for train/cal-only pilots.

Consequence: the current mechanism-feature sidecars are validated for
train/cal-only embedding pilots as schema-safe inputs. The scientific feature
gap remains directed electron/proton-transfer edges and row-specific bond-change
evidence.

Follow-up: tighten the cofactor-catalytic-locus gap into a review-only schema
and materialization queue for `metal_ion_locus`, `cobalamin_locus`,
`radical_sam_locus`, and `iron_sulfur_locus`. The schema uses existing current702
geometry ligand context only: 176 rows have proximal metal context, 4 cobalamin,
8 SAM, and 17 Fe-S cluster context. No sidecar values were emitted yet; the next
safe implementation is a metal-ion locus sidecar with proximal versus
structure-wide-only status.

Second follow-up: materialize the first such sidecar, `metal_ion_locus`, for all
702 current rows from existing geometry ligand context only. It records 175 rows
with proximal metal context, 85 with structure-wide-only metal context, 422 with
no metal context, and 20 unsupported/missing-geometry rows. All records are
review-only and have `predictive_use_allowed=false` and `ready_for_label_import=false`.
A matching strict schema audit passes with zero critical violations.

Third follow-up: materialize and audit `cobalamin_locus` with the same
review-only pattern and explicit structure-wide-only guardrail. It records 4
proximal cobalamin rows, 678 no-context rows, 20 unsupported/missing-geometry
rows, and no structure-wide-only B12 rows in the current geometry source. The
schema audit passes with zero critical violations.

Fourth follow-up: materialize and audit `radical_sam_locus` and
`iron_sulfur_locus` separately, preserving SAM/Fe-S copresence as an explicit
row status. The radical-SAM sidecar records 8 proximal SAM rows, 2
structure-wide-only SAM rows, and 20 unsupported/missing-geometry rows. The
Fe-S sidecar records 17 proximal Fe-S rows, 11 structure-wide-only Fe-S rows,
and 20 unsupported/missing-geometry rows. Both remain review-only, keep all
predictive/import flags false, and pass strict schema audits with zero critical
violations.

Completion audit follow-up: validate that all four schema-named
cofactor-locus sidecar classes are now materialized and schema-passing. The
completion audit records 4/4 materialized classes, 4/4 passing schema audits,
702 rows per class, zero critical violations, and zero predictive/import-ready
rows. The next mechanism-feature step is a train/cal-only embedding pilot; no
labels, registries, imports, thresholds, splits, or production scorers changed.

Train/cal input-manifest follow-up: stage the no-fit input surface for that
future embedding pilot. The manifest enumerates only the 562 in-distribution
candidate rows and keeps all 140 heldout rows excluded from training and
threshold tuning. It finds 524 rows with the minimal active-site role-graph plus
organic cofactor plus inorganic cofactor-locus feature bundle, records 184
train/cal reaction-template rows, and does not fit weights, select thresholds,
or evaluate heldout rows.

Train/cal split-manifest follow-up: deterministically partition only the 524
minimal-bundle-ready rows into 418 train rows and 106 calibration rows across
six strata. The split manifest carries heldout only as an excluded count, records
38 blocked train/cal candidates by role-graph readiness class, and still does
not fit weights, select thresholds, or evaluate heldout rows.

Feature-contract follow-up: add a no-fit, label-stripped feature contract for
the 524 ready train/cal rows. It records four allowed feature groups
(active-site role graph, reaction-center template, organic cofactor scores, and
inorganic cofactor loci), strips `fingerprint_id`, `label_type`, stratum, and
split fields out of the feature-row surface, and keeps heldout absent from
feature rows. It is a materialization contract only; feature-vector code, model
weights, thresholds, directed electron/proton-transfer edges, and row-specific
bond-change mappings remain blocked until explicitly authorized.

Strict-audit follow-up: add a no-fit audit for that feature contract. It
validates 524/524 feature rows against the train/cal split manifest, confirms
forbidden label/outcome fields are absent from feature groups, keeps heldout
absent from feature rows, and reports zero critical violations. This does not
authorize feature-vector materialization or model fitting.

Train/cal guardrail follow-up: add a no-fit audit across the input manifest,
split manifest, and feature contract. It confirms that the 524 feature rows
exactly match the 524 train/cal split rows, split rows are a subset of the 562
input rows, 140 heldout rows remain excluded, and fingerprint/label/stratum
fields remain outside the feature surface. No model fit, threshold selection,
heldout evaluation, import, label change, or production scorer change occurred.

Row-specific bond-change priority follow-up: intersect the staged
row-specific bond-change schema with the current no-fit feature contract and
train/cal split manifest. The priority manifest partitions 232 evidence-required
rows into 171 P0 train/cal feature-contract gap rows, 13 P1 in-distribution rows
that need upstream feature-bundle repair before contract use, and 48 P2 heldout
final-only rows. It also stages a balanced 15-row P0 pilot seed queue across the
five current primary fingerprints. No source evidence was materialized and no
feature contract, label, split, threshold, model weight, import, registry,
ontology, or production scorer changed.

P0 source-graph readiness follow-up: audit that balanced 15-row P0 seed queue
against the frozen local M-CSA graph. All 15 rows have entry-node,
mechanism-text, catalytic-residue, and EC context; 11/15 have EC-to-Rhea
mappings; 0/15 have structured row-specific bond-change event predicates. This
does not materialize source evidence or authorize feature-contract consumption;
it converts the next work into manual/source-backed extraction of reaction
participant mappings and bond-change events.

P0 extraction-work-package follow-up: turn the readiness audit into a bounded
manual extraction package with 15 row templates, nine required source-backed
fields, event/mapping acceptance criteria, and per-row Rhea lookup flags. The
package is templates-only: every row remains `manual_extraction_not_started`,
and no source evidence, feature row, model input, threshold, label, registry,
ontology, import, or production scorer changed.

P0 extraction-package strict-audit follow-up: add a schema/guardrail audit for
that work package. It validates 15/15 template rows, 0 non-null extracted
values, 0 rows allowed for feature-contract or model use, and 0 critical
violations. The next safe step remains filling those templates from
source-backed evidence, then auditing the resulting sidecar before any no-fit
feature-contract refresh.

P0 extraction-worksheet follow-up: export the same 15 P0 template rows as a TSV
manual-fill worksheet. All source-evidence fields are blank by construction and
four rows are flagged for Rhea lookup. The worksheet is not a sidecar and must
not be consumed by a feature contract unless it is later filled from
source-backed evidence and passes a strict evidence audit.

P0 source-evidence sidecar-schema follow-up: stage the schema and audit plan
for the future filled sidecar. It requires 12 row fields, six event fields, and
four participant-mapping fields, names forbidden predictive fields, and defines
evidence/leakage checks. This remains schema-only with 0 materialized source
values.

P0 source-evidence draft-sidecar follow-up: fill the 15-row P0 worksheet into a
draft sidecar from frozen local M-CSA graph evidence. All rows now have M-CSA
source spans and draft bond-change events; 11/15 also have Rhea equations and
4/15 remain Rhea-missing. A strict audit confirms row alignment, required
fields, forbidden-field absence, and 0 critical violations. The sidecar remains
non-consumable: 0 rows are approved, no feature contract was refreshed, and no
model, threshold, label, registry, ontology, import, or production scorer
changed.

P0 source-evidence review-queue follow-up: add a manual-only queue over the
draft sidecar and strict audit. It ranks four Rhea-missing rows first
(`m_csa:124`, `m_csa:11`, `m_csa:169`, and `m_csa:5`), then four
high-complexity multi-event rows, then seven standard draft-review rows. This
does not approve or reject any row, refresh a feature contract, fit a model,
select a threshold, or mutate labels, registries, ontologies, imports, or
production scoring.

P0 Rhea lookup-manifest follow-up: stage exact manual lookup targets for those
four Rhea-missing rows from the frozen source-graph readiness evidence. The
manifest records `ec:1.9.3.1`, `ec:3.1.21.2`, `ec:3.4.14.5`, and
`ec:3.4.16.6` as the lookup targets, with rerun instructions for the strict
sidecar audit after any manual source update. No source fetch, source import,
approval, feature-contract refresh, model fit, threshold selection, label edit,
registry edit, ontology edit, or production-scorer change occurred.

P0 Rhea lookup-resolution follow-up: run a bounded official Rhea lookup for the
four staged rows. Exact EC queries returned zero Rhea records for all four
worksheet ECs; accession query `uniprot:P00396` resolved `m_csa:124` to
`RHEA:11436` with equation
`4 Fe(II)-[cytochrome c] + O2 + 8 H(+)(in) = 4 Fe(III)-[cytochrome c] + 2 H2O + 4 H(+)(out)`
and Rhea EC `7.1.1.9`. The source-evidence sidecar now records that official
Rhea equation as review-only evidence, increasing Rhea-covered rows from 11/15
to 12/15. The refreshed manual review queue leaves three Rhea-missing rows
(`m_csa:11`, `m_csa:169`, and `m_csa:5`) and moves `m_csa:124` into
high-complexity manual review. All rows remain draft/non-consumable: no
approval, feature-contract refresh, model fit, threshold selection, label edit,
registry edit, ontology edit, import, or production-scorer change occurred.

P0 Rhea resolution-consumption follow-up: add a strict audit tying the bounded
Rhea lookup resolution to the refreshed sidecar, review queue, remaining lookup
manifest, and feature-readiness audit. It confirms `m_csa:124` carries
`RHEA:11436` in the sidecar, is absent from the remaining lookup manifest, and
stays draft/non-consumable; `m_csa:11`, `m_csa:169`, and `m_csa:5` remain in
the lookup manifest and readiness blockers. The audit reports 0 critical
violations, 0 approved rows, 0 feature-contract-consumable rows, and 0
model-training-eligible rows.

P0 unresolved-Rhea official-source follow-up: recheck the three remaining rows
(`m_csa:11`, `m_csa:169`, and `m_csa:5`) against bounded Rhea EC queries with
and without the `ec:` prefix, Rhea accession queries, and current UniProtKB
catalytic-activity records. Rhea returns 0 records for all nine bounded queries.
UniProt confirms matching EC catalytic activity for all three accessions but
provides no Rhea cross-references. The rows remain non-consumable and cannot be
automation-resolved from official Rhea/UniProt alone; the next gate is reviewer
provenance for M-CSA-only approval, rejection/hold, or an explicitly authorized
alternate reaction source.

P0 reviewer-decision matrix follow-up: stage the review-only decision matrix
for those three unresolved rows. It records each row's draft event count,
readiness blockers, official-source status, and three allowed reviewer choices:
approve M-CSA-only source evidence with reviewer provenance, reject/rewrite
draft events, or hold for an alternate reaction source. It records no reviewer
decision, approval, feature-contract consumption, model-training eligibility,
label edit, registry edit, ontology edit, import, threshold change, or
production-scorer change.

P0 feature-readiness follow-up: audit the draft source-evidence sidecar against
the strict audit, manual review queue, Rhea lookup manifest, and current
feature contract. All 15 rows are structurally ready as drafts, with draft
coverage for 10 bond-change rows, 6 proton-transfer rows, and 9
electron-transfer rows. Zero rows are approved or consumable, and the current
feature contract contains no row-specific bond/proton/electron fields. The
next blocker remains the three unresolved Rhea rows plus reviewer-provenance approval
before any train/cal-only no-template feature refresh.

P0 refresh-blocker follow-up: add a compact automation decision audit over the
strict sidecar audit, feature-readiness audit, Rhea consumption audit,
unresolved official-source audit, reviewer decision matrix, and feature-contract
gap audit. It confirms automation must not refresh the no-template
mechanism-feature contract: all 15 draft rows are structurally ready, but 0 are
approved/consumable, 0 reviewer IDs are present, 0 copy-ready decisions exist,
and `m_csa:5`, `m_csa:11`, and `m_csa:169` still require reviewer provenance.
No feature contract, model, threshold, label, registry, ontology, import, or
production scorer changed.

Artifacts:
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_refresh_blocker_audit_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_refresh_blocker_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_sidecar_schema_audit_current702_20260601.json`,
`work/mechanism_feature_sidecar_schema_audit_current702_20260601.md`,
`artifacts/v3_learned_mechanism_feature_embedding_plan_current702_20260601.json`,
`work/learned_mechanism_feature_embedding_plan_current702_20260601.md`,
`artifacts/v3_mechanism_feature_inorganic_cofactor_locus_schema_current702_20260601.json`,
`work/mechanism_feature_inorganic_cofactor_locus_schema_current702_20260601.md`,
`artifacts/v3_mechanism_feature_metal_ion_locus_sidecar_current702_20260601.json`,
`work/mechanism_feature_metal_ion_locus_sidecar_current702_20260601.md`,
`artifacts/v3_mechanism_feature_metal_ion_locus_sidecar_schema_audit_current702_20260601.json`,
`work/mechanism_feature_metal_ion_locus_sidecar_schema_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_cobalamin_locus_sidecar_current702_20260601.json`,
`work/mechanism_feature_cobalamin_locus_sidecar_current702_20260601.md`,
`artifacts/v3_mechanism_feature_cobalamin_locus_sidecar_schema_audit_current702_20260601.json`,
`work/mechanism_feature_cobalamin_locus_sidecar_schema_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_radical_sam_locus_sidecar_current702_20260601.json`,
`work/mechanism_feature_radical_sam_locus_sidecar_current702_20260601.md`,
`artifacts/v3_mechanism_feature_radical_sam_locus_sidecar_schema_audit_current702_20260601.json`,
`work/mechanism_feature_radical_sam_locus_sidecar_schema_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_iron_sulfur_locus_sidecar_current702_20260601.json`,
`work/mechanism_feature_iron_sulfur_locus_sidecar_current702_20260601.md`,
`artifacts/v3_mechanism_feature_iron_sulfur_locus_sidecar_schema_audit_current702_20260601.json`,
`work/mechanism_feature_iron_sulfur_locus_sidecar_schema_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_inorganic_cofactor_locus_completion_audit_current702_20260601.json`,
`work/mechanism_feature_inorganic_cofactor_locus_completion_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_embedding_train_cal_input_manifest_current702_20260601.json`,
`work/mechanism_feature_embedding_train_cal_input_manifest_current702_20260601.md`,
`artifacts/v3_mechanism_feature_embedding_train_cal_split_manifest_current702_20260601.json`,
`work/mechanism_feature_embedding_train_cal_split_manifest_current702_20260601.md`,
`artifacts/v3_mechanism_feature_embedding_feature_contract_current702_20260601.json`,
`work/mechanism_feature_embedding_feature_contract_current702_20260601.md`,
`artifacts/v3_mechanism_feature_embedding_feature_contract_strict_audit_current702_20260601.json`,
`work/mechanism_feature_embedding_feature_contract_strict_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_embedding_train_cal_guardrail_audit_current702_20260601.json`,
`work/mechanism_feature_embedding_train_cal_guardrail_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_materialization_priority_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_materialization_priority_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_graph_readiness_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_source_graph_readiness_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_extraction_work_package_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_extraction_work_package_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_extraction_package_strict_audit_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_extraction_package_strict_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_extraction_worksheet_current702_20260601.tsv`,
`work/mechanism_feature_row_specific_bond_change_p0_extraction_worksheet_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_schema_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_schema_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_strict_audit_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_strict_audit_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_review_queue_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_source_evidence_review_queue_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_rhea_lookup_manifest_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_rhea_lookup_manifest_current702_20260601.md`,
`artifacts/v3_mechanism_feature_row_specific_bond_change_p0_feature_readiness_audit_current702_20260601.json`,
`work/mechanism_feature_row_specific_bond_change_p0_feature_readiness_audit_current702_20260601.md`.

## 2026-06-01: Thiol/Disulfide Redox Boundary Panel Packet Added

Decision: build one additional review-only family-set expansion evidence packet
for the `thiol_disulfide_oxidoreductase_isomerase_boundary` panel. This uses
existing frozen current702 predicted geometry, predicted-atlas novelty variants,
selected organic cofactor scores, selected-PDB fold proxy evidence, and the real
predicted-structure fold channel. No label, registry, ontology, import,
promotion, threshold, split, or production scorer changed.

Result: the packet covers `m_csa:191` and is ready for review. The row has ok
predicted geometry, selected cofactor scores, selected-PDB fold proxy evidence,
and a real predicted-structure nearest-atlas TM score of `0.3863` against
`m_csa:631` / `ser_his_acid_hydrolase`.

Consequence: this widens the review-only family expansion evidence set for a
cofactor-confounded redox boundary without promoting any row. The next review
step is source-checking row-level bond-change and redox-partner evidence before
any countable family discussion.

Artifacts:
`artifacts/v3_family_panel_evidence_packet_thiol_disulfide_oxidoreductase_isomerase_boundary_current702_20260601.json`,
`work/family_panel_evidence_packet_thiol_disulfide_oxidoreductase_isomerase_boundary_current702_20260601.md`.

## 2026-06-01: Family Panel Packets Use All-Heldout Predicted-Fold Hits

Decision: update the family-panel evidence packet builder to use
all-heldout predicted-structure Foldseek/TM hits whenever available, while still
preserving priority cofactor-confounded hits. Then build a review-only
`flavin_monooxygenase_and_flavin_oxygen_transfer` evidence packet. No label,
registry, ontology, import, promotion, threshold, split, or production scorer
changed.

Result: the FMO/flavin oxygen-transfer packet covers four review rows:
`m_csa:131`, `m_csa:132`, `m_csa:551`, and `m_csa:973`. Three rows have ok
predicted geometry; `m_csa:132` remains a geometry gap. The all-heldout fold
channel supplies predicted-fold TM hits for `m_csa:131` (`0.751`) and
`m_csa:551` (`0.7309`), which were not available through the priority-only hit
lookup.

Consequence: review-only family expansion packets can now consume the completed
all-heldout fold channel, making non-priority panels better populated without
changing benchmark labels or training data. FMO remains secondary/review-only.

Artifacts:
`artifacts/v3_family_panel_evidence_packet_flavin_monooxygenase_and_flavin_oxygen_transfer_current702_20260601.json`,
`work/family_panel_evidence_packet_flavin_monooxygenase_and_flavin_oxygen_transfer_current702_20260601.md`.

## 2026-06-01: Remaining Family-Expansion Panels Have Review Packets

Decision: complete the review-only evidence packet set for the remaining
family-expansion panels after the panel builder was updated to consume
all-heldout predicted-fold hits. No label, registry, ontology, import,
promotion, threshold, split, or production scorer changed.

Result: new packets now cover `cobalamin_and_radical_rearrangement_panel`,
`no_reliable_structure_metal_hydrolase_controls`, and
`near_orphan_glycoside_or_nucleoside_hydrolase_controls`. The cobalamin/radical
packet has one current row with ok predicted geometry (`m_csa:750`) and two
secondary-probe geometry gaps. The no-reliable-structure metal hydrolase packet
originally had only geometry gaps, as expected for the panel definition. The
near-orphan glycoside/nucleoside packet has one current row with ok predicted
geometry (`m_csa:10`) and three gaps.

Follow-up: after the source-free predicted-geometry retrieval became available,
refresh the affected family-panel evidence packets to consume approved
source-free geometry scores for `secondary_probe::radical_sam_enzyme`, `mh_066`,
and `mh_073`. The packet coverage audit now has 15/22 predicted-geometry-ok rows
and 21 predicted-fold hits; the cobalamin/radical, no-reliable-structure metal
hydrolase, and near-orphan packets each retain one or more explicit geometry gaps
that still need approved source-free locators. No labels, imports, thresholds,
splits, registries, or production scorers changed.

Consequence: all seven family-set expansion target panels now have review-only
evidence packets. Use them for source/materialization triage only; none authorize
countable imports, label promotions, or training use.

Artifacts:
`artifacts/v3_family_panel_evidence_packet_cobalamin_and_radical_rearrangement_panel_current702_20260601.json`,
`work/family_panel_evidence_packet_cobalamin_and_radical_rearrangement_panel_current702_20260601.md`,
`artifacts/v3_family_panel_evidence_packet_no_reliable_structure_metal_hydrolase_controls_current702_20260601.json`,
`work/family_panel_evidence_packet_no_reliable_structure_metal_hydrolase_controls_current702_20260601.md`,
`artifacts/v3_family_panel_evidence_packet_near_orphan_glycoside_or_nucleoside_hydrolase_controls_current702_20260601.json`,
`work/family_panel_evidence_packet_near_orphan_glycoside_or_nucleoside_hydrolase_controls_current702_20260601.md`.

## 2026-06-01: Real Predicted-Structure Foldseek Channel Is Scored For All Ok Heldout Rows

Decision: move beyond the selected-PDB fold proxy by staging the real
AlphaFoldDB-predicted fold channel for heldout rows against the predicted
in-distribution atlas. The run used exact AFDB v6 CIF requests derived from the
current702 predicted-geometry atlas artifact, staged coordinates transiently
under `/private/tmp`, and committed only the small Foldseek TSVs plus parsed
JSON/report. No label, registry, ontology, threshold, production scoring, import,
or split changed.

Result: Foldseek exact TM scoring completed for all 126 heldout rows with ok
predicted geometry against 167 unique predicted atlas CIFs, yielding 11,297
mapped heldout-vs-atlas pairs and 0 unmapped names. The nearest-atlas TM signal
separates in-scope heldout from OOS at AUC `0.814301` overall and `0.829787`
against the six cofactor-confounded OOS rows. At the diagnostic >=90% in-scope
retention point it abstains on `0.4177` of all OOS and `0.3333` of confounded
OOS; at >=85% retention it abstains on `0.5063` of all OOS and `0.5` of
confounded OOS. Priority nearest-atlas TM scores were: `m_csa:30` 0.4988,
`m_csa:31` 0.3809, `m_csa:80` 0.5109, `m_csa:191` 0.3863, `m_csa:267` 0.7389,
and `m_csa:448` 0.5106.

Consequence: the real predicted-structure fold channel is now an all-heldout
rank signal, not only a manifest. It clears the 0.75 rank bar and is partly
aligned with the desired confounded-OOS behavior, but the high-retention operating
point is still not standalone deployment. Next work should combine this fold
channel with geometry/cofactor signals and decide whether persistent predicted-CIF
coordinate provenance should be committed.

Artifacts: `artifacts/v3_predicted_structure_fold_channel_current702_20260601.json`,
`artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/cofactor_confounded_oos_vs_atlas.tsv`,
`artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/all_heldout_vs_atlas.tsv`,
`work/predicted_structure_fold_channel_current702_20260601.md`.

## 2026-06-01: Fold-Augmented Predicted-Geometry Gate Is The Strongest No-Fit Abstention Diagnostic So Far

Decision: combine the real predicted-structure nearest-atlas Foldseek/TM score
with frozen predicted-geometry confidence in a bounded heldout-only diagnostic.
This is explicitly no-fit and post-hoc: it selects no production threshold, does
not train on heldout, and changes no label, registry, ontology, import, split, or
production scorer.

Result: among raw and simple combined channels, `combined_mean_geometry_fold` is
best. It separates in-scope heldout rows from all OOS rows at AUC `0.907622` and
from the six cofactor-confounded OOS rows at AUC `0.911348`, above standalone
predicted geometry (`0.756935`/`0.840426`) and standalone nearest-atlas fold TM
(`0.814301`/`0.829787`). At the diagnostic >=90% in-scope retention point it
retains `0.9149` of in-scope rows while abstaining on `0.7215` of all OOS rows
and `0.8333` of cofactor-confounded OOS rows; at >=85% retention it abstains on
`0.7722` of all OOS rows and `0.8333` of cofactor-confounded OOS rows.

Consequence: the next deployment-gate work should promote this from a
heldout-only diagnostic into a leakage-safe train/cal/heldout thresholding
contract, with any fitted weights or threshold selected on train/cal only. Do
not treat these post-hoc operating points as authorized production thresholds.

Follow-up: add a companion novelty-variant artifact that recomputes the same
geometry-plus-predicted-fold combinations from existing scored artifacts, without
rerunning Foldseek/TM or fetching coordinates. It confirms the best existing
channel is the mean of predicted-geometry top1 score and nearest-atlas predicted
fold TM (`mean_top1_raw_and_tm`, equivalent to the earlier
`combined_mean_geometry_fold`) with AUC `0.907622` overall and `0.911348` on the
six confounded OOS rows.

Operating-grid follow-up: enumerate 0.95/0.90/0.85/0.80 retention diagnostics for
all 11 frozen geometry-plus-predicted-fold variant signals using the existing
variant rows only. The best variant artifact signal (`mean_top1_raw_and_tm`)
abstains on `0.7215` of OOS rows and `0.8333` of cofactor-confounded OOS rows at
>=90% in-scope retention. The best signal at the 0.90 target is
`mean_top1_atlas_percentile_and_tm`, with `0.7722` OOS abstain recall. This
remains post-hoc heldout evidence and does not authorize a deployment threshold.

Artifacts: `artifacts/v3_fold_augmented_abstention_gate_current702_20260601.json`,
`work/fold_augmented_abstention_gate_current702_20260601.md`,
`artifacts/v3_predicted_structure_fold_augmented_novelty_variants_current702_20260601.json`,
`work/predicted_structure_fold_augmented_novelty_variants_current702_20260601.md`,
`artifacts/v3_predicted_structure_fold_augmented_novelty_operating_grid_current702_20260601.json`,
`work/predicted_structure_fold_augmented_novelty_operating_grid_current702_20260601.md`.

## 2026-06-01: Predicted-Atlas Geometry Robust-Distance Variant Adds Modest Rank Lift, But Not An Operating-Point Breakthrough

Decision: after the in-distribution predicted-geometry atlas was materialized,
rerun the blocked atlas-normalized novelty variants rather than combining only raw
heldout scores. The bounded rerun used predicted-geometry retrieval rows only:
168 in-distribution atlas rows, 47 in-scope heldout rows, 79 OOS heldout rows,
and the six cofactor-confounded OOS rows already identified by the current gate.
All normalization was atlas-only; no labels, thresholds, registries, imports, or
splits changed.

Result: the best variant is a robust feature-distance signal to the nearest
in-distribution mechanism class centroid over top1 geometry subfeatures. It
improves novelty rank AUC over raw predicted-geometry top1 score:
`0.776461` vs `0.756935` overall, and `0.847518` vs `0.840426` on the
cofactor-confounded subset. The lift is real but bounded: at the diagnostic
>=90% in-scope retention point it abstains on only `0.2278` of OOS rows and
`0.3333` of confounded rows. Relaxing to >=85% retention reaches `0.5949` OOS
abstain recall and `0.6667` confounded abstain recall, still post-hoc and not a
deployment threshold.

Consequence: predicted-atlas robust-distance geometry is the best in-repo
geometry-only novelty variant so far, but it does not erase the operating-point
feature-overlap problem. Future work should treat it as a diagnostic/possible
feature input, not as a standalone deployable gate. The next distinct lever is
the real predicted-structure Foldseek/TM channel or a mechanism-feature embedding
gap closure, not another raw geometry subfeature recombination.

A follow-up operating-grid readout now enumerates 0.95/0.90/0.85/0.80
retention diagnostics for all 10 frozen predicted-atlas geometry novelty
signals without recomputing retrieval or Foldseek/TM. The best geometry-only
signal remains `negative_nearest_class_centroid_robust_distance`; at >=90%
in-scope retention it abstains on only 22.78% of OOS rows and 2/6
cofactor-confounded OOS rows. At >=85% retention it abstains on 59.49% of OOS
and 4/6 confounded OOS rows, reinforcing that this is evidence for a later
fold/mechanism-feature channel rather than a standalone threshold.

Artifacts: `artifacts/v3_predicted_atlas_geometry_novelty_variants_current702_20260601.json`,
`work/predicted_atlas_geometry_novelty_variants_current702_20260601.md`,
`artifacts/v3_predicted_atlas_geometry_novelty_operating_grid_current702_20260601.json`,
`work/predicted_atlas_geometry_novelty_operating_grid_current702_20260601.md`.

## 2026-05-31: Ruled Out In-Repo Lever — Richer Geometry Sub-Features Do NOT Beat Collapsed top1_score For Novelty

Decision: before reaching for a new external feature, test whether the
novelty signal is already in the repo but hidden -- the predicted-geometry
retrieval collapses a rich per-row fingerprint match (mechanistic_coherence_score,
role_match_fraction, substrate_pocket_score, compactness_score,
cofactor_context_score, counterevidence_penalty, distance stats) into one
top1_score. Measured each sub-field's individual novelty AUC (in-scope > OOS) on
the deployment held-out pool (47 in-scope, 79 OOS).

Result: top1_score (AUC 0.757) is already the best single geometry novelty signal.
No sub-field beats it -- next best are cofactor_context_score 0.688 and
role_match_fraction 0.655; mechanistic_coherence, residue_match, substrate_pocket,
compactness, counterevidence_penalty, plp_anchor are all 0.50-0.55 (near chance). A
naive mean of the positive sub-fields (0.724) DILUTES the score rather than
improving it. The atlas-standardized (Mahalanobis) variant is blocked by the
known no-predicted-geometry-atlas issue.

Consequence: the in-repo geometry decomposition has no headroom over the score
that already integrates it. This rules out "unpack the features we have" and
confirms the northstar redirect from the entry below: the next lever must be a
GENUINELY NEW mechanism-discriminative feature (learned active-site/electron-flow
embeddings, fold-level novelty, or a predicted-geometry retrieval that also scores
the in_distribution atlas), not a recombination of existing channels. Probe-only
(negative result); no module/artifact added. Atlas-free, deployment regime,
M-CSA eval-only.

## 2026-05-31: Operational Gate Architecture Settled — Binding Constraint Is Feature Overlap, Not Combiner Design (Northstar Pivot)

Decision: act on the operating-point gap. Built the per-channel RULE gate that the
prior entry pointed to: `abstain if geometry_score < tg OR (cofactor_max <
signature_threshold AND cofactor_max < tc)` -- geometry leads (safe on the
cofactor-confounded subset), and the cofactor channel may only ADD abstentions
where it is trustworthy (no strong known-cofactor signature), never KEEP a row
geometry flags. Swept a fixed untuned 2D threshold grid (0.02 steps); no tuning on
eval labels.

Result (predicted/apo deployment geometry; 47 in-scope, 79 OOS, 6 confounded, 73
agnostic):
  * At 90% in-scope retention there is STILL no viable operating point -- for any
    combiner. The geometry score distributions overlap hard: in-scope median 0.434
    (min 0.291), agnostic-OOS median 0.370 (max 0.676), confounded-OOS median 0.358.
    Known and novel chemistry are not linearly separable on this feature.
  * Relaxing to 85% retention, the per-channel rule gives a REAL lift: OOS
    abstain-recall 0.139 (geometry only) -> 0.304 (rule), +0.165, entirely on the
    cofactor-agnostic subset (0.315). The confounded subset stays hard (~0.17)
    until retention drops to ~80%.

Northstar consequence: the per-channel rule is the correct OPERATIONAL ARCHITECTURE
(geometry-led, cofactor-as-agnostic-lift, confounded-safe) and is now committed.
But the binding constraint on de novo abstention is no longer combiner design or
thresholding -- it is FEATURE OVERLAP. The current channels (predicted-geometry
fingerprint-retrieval confidence + organic-cofactor head probability) do not place
novel chemistry far enough from known chemistry to abstain at deployable retention.
This redirects the northstar: the next lever is a stronger mechanism-discriminative
FEATURE (e.g. learned active-site/electron-flow embeddings, predicted-geometry role
decomposition for atlas rows, or fold-level novelty signals), evaluated at the
operating point -- not another way to combine the features we already have.

Guardrails: predicted-geometry deployment regime, sequence-only PLM input, no atlas,
no training/refit, fixed untuned threshold grid; geometry fingerprint score is
tuning-adjacent; M-CSA eval-only. `compute_deployment_gate` now emits
`per_channel_rule_gate`. Refines the operating-point entry below; both stand.

## 2026-05-31: Sobering Operating-Point Reality — De Novo AUC 0.852 Does NOT Yield A Usable Abstention Threshold

Decision: the pivotal entry showed the deployment abstention AUC clears 0.75, but
AUC is rank-only. Convert the gate to an actual decision (a threshold) and report
its behavior, so the headline AUC is not mistaken for deployability. Thresholds are
a fixed, untuned grid over the calibrated [0,1] scores — not fit to eval labels.

Result (predicted/apo geometry; 47 in-scope, 79 OOS, 6 confounded; threshold chosen
to retain >=90% of in-scope rows):
  * geometry-led gate (thr 0.35): abstains on only **19% of OOS** at 91% in-scope
    retention. The score distributions overlap heavily; there is a cliff near 0.40
    where OOS-recall jumps to 0.84 but in-scope retention collapses to 0.64. No
    threshold gives both high novelty-catch and high retention.
  * blind mean-combined gate (thr 0.25): catches 59% of OOS but abstains on **NONE
    of the 6 safety-critical cofactor-confounded rows** (confounded_abstain_recall
    0.0) — the exact failure the AUC hid. The mean's aggregate edge comes entirely
    from the cofactor-agnostic majority.

Consequence: the de novo precondition is achievable in ranking (AUC 0.852) but NOT
yet operational — there is no fixed threshold that abstains usefully while retaining
known chemistry, and the blind mean is actively unsafe on the confounded subset. The
gate now commits a full operating curve and the >=90%-retention operating points so
this gap is explicit, not hidden behind the AUC. Future work: per-channel
thresholds (geometry-led with a cofactor-agnostic-only cofactor lift), or a
calibrated score, evaluated at the operating point, not by AUC.

Guardrails: predicted-geometry deployment regime, sequence-only PLM input, no atlas,
no training/refit, no heldout tuning (threshold grid is fixed/untuned); geometry
fingerprint score is tuning-adjacent; M-CSA eval-only. Refines (does not overturn)
the pivotal AUC entry below. Artifacts regenerated in place:
`artifacts/v3_mechanism_deployment_abstention_gate_eval_current702_20260531.json`,
`work/mechanism_deployment_abstention_gate_eval_current702_20260531.md`
(`compute_deployment_gate` now emits `operating_points_at_90pct_retention` and
`geometry_led_operating_curve`).

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
