# Project State

Last refreshed: 2026-06-01

This file is the durable state summary for agents who do not have chat context.
Treat it as an orientation layer, not as a replacement for the referenced
artifacts.

Read order for a fresh run:

1. `docs/project_state.md`
2. `docs/decision_log.md`
3. `docs/artifact_index.md`
4. `docs/agent_runbook.md`

## North Star

Catalytic Earth is a mechanism-first enzyme atlas scaffold. The objective is a
computable map from sequence, structure, active-site geometry, catalytic roles,
cofactors, substrate-pocket constraints, reaction bond changes, and evolutionary
context to mechanism-level function hypotheses.

The repo is not an EC-number classifier, a wet-lab protocol, or a production
biological design system. Current benchmark claims must be framed as local,
artifact-backed mechanism diagnostics.

## Current Benchmark State

- Current label surface: 702 curated labels in the current sequence-NN manifest,
  with 562 in-distribution rows and 140 heldout rows.
- Current v1 primary mechanism targets: `ser_his_acid_hydrolase`,
  `metal_dependent_hydrolase`, `plp_dependent_enzyme`,
  `flavin_dehydrogenase_reductase`, and `heme_peroxidase_oxidase`.
- Secondary OOD probe fingerprints: `radical_sam_enzyme`,
  `cobalamin_radical_rearrangement`, and `flavin_monooxygenase`.
- The 2026-05-25 sequence manifest predates the later canonical `m_csa:497` and
  `m_csa:750` OOS revisions. Use the Wave 1 readthrough masks when reading
  Wave 1 artifacts that still carry those rows as primary flavin labels.
- Current Wave 1.2 standardized heldout readout:
  - canonical mask: 45 primary rows, 92 pure OOS rows, 3 secondary-probe rows;
  - Wave 1 readthrough mask after excluding `m_csa:497` and `m_csa:750` from
    primary metrics: 43 primary rows and 97 nonprimary/OOS rows.

When a report predates 2026-05-27 row-level revisions, do not copy its primary
flavin counts directly. Check the decision log and the row-level revision
artifacts first.

## Trusted Results

- Geometry re-export removed the prior join confound. The current Wave 1.2 audit
  joins 140/140 standardized heldout rows, recovers the five rows missed by the
  older preview geometry eval (`m_csa:577`, `m_csa:599`, `m_csa:710`,
  `m_csa:892`, and `m_csa:897`), and reports 45/45 canonical primary accuracy
  with 0/92 pure-OOS false positives under the existing 0.4115 geometry
  abstention threshold.
- Hand-scored active-site geometry remains the current first router. The
  geometry-feature logistic probe is useful but weaker on the audit: 66.7%
  canonical primary accuracy and 4.2% OOS/secondary false-positive rate.
- The clean experimental-coordinate geometry result is not deployment-ready by
  itself. The AlphaFoldDB predicted-geometry audit drops the hand router from
  45/45 to 23/45 primary heldout correct, with 17 primary abstentions, 5 wrong
  non-abstained primary calls, and a 12.3% OOS/secondary false-positive rate.
  This makes robustness to predicted active-site geometry degradation a learned
  model job description, not a raw clean-M-CSA accuracy contest.
- A real AlphaFoldDB-predicted structure Foldseek channel is now scored for all
  126 heldout rows with ok predicted geometry against the predicted
  in-distribution atlas. The standalone nearest-atlas TM signal separates
  in-scope from all OOS at AUC 0.814301; a no-fit mean of predicted geometry
  confidence and fold TM reaches AUC 0.907622 overall and 0.911348 on the six
  cofactor-confounded OOS rows. These are diagnostics, not production thresholds.
- The scored predicted-structure fold channel now has a strict contract audit.
  It confirms 126/126 ok heldout rows and 6/6 priority cofactor-confounded OOS
  rows have parsed nearest-atlas Foldseek/TM hits, with zero critical contract
  violations. Persistent predicted-CIF coordinate provenance remains a
  reproducibility task, not a score-completeness blocker.
- The fold-augmented gate now has a leakage-safe thresholding contract. A
  deterministic in-distribution train/cal split selected the
  `combined_mean_geometry_fold` threshold `0.44155` at >=90% calibration
  in-scope retention. Heldout final readout at that fixed threshold retains
  45/47 in-scope rows, abstains on 44/79 OOS rows, and abstains on 5/6
  cofactor-confounded OOS rows. This is a research contract, not a production
  threshold.
- A companion fold-augmented novelty-variant diagnostic now records the existing
  predicted-geometry plus predicted-fold combinations without rerunning
  Foldseek/TM. The best existing-channel variant is still
  `mean_top1_raw_and_tm`, with all-OOS AUC `0.907622` and confounded-OOS AUC
  `0.911348`; this confirms the rank signal but does not select a threshold.
- A companion fold-augmented novelty operating-grid readout now enumerates
  0.95/0.90/0.85/0.80 in-scope-retention diagnostics over those existing
  variant rows. The best frozen variant artifact signal abstains on 72.15% of
  OOS rows and 5/6 cofactor-confounded OOS rows at >=90% in-scope retention; the
  best 0.90 grid row uses `mean_top1_atlas_percentile_and_tm` and abstains on
  77.22% of OOS rows. This remains a heldout review-only diagnostic.
- A geometry-only predicted-atlas operating-grid readout now enumerates the
  post-hoc retention/OOS-abstention tradeoff for all 10 frozen geometry novelty
  signals. The best geometry-only signal remains
  `negative_nearest_class_centroid_robust_distance`; at >=90% in-scope retention
  it abstains on only 22.78% of OOS and 2/6 cofactor-confounded OOS rows, so it
  remains diagnostic input rather than a standalone deployment gate.
- A train/cal OOS-negative calibration surface now exists for the fold-augmented
  gate. The hash-selected 76-row surface has 71 score-complete rows with
  predicted geometry, selected organic cofactor scores, and exact Foldseek/TM
  nearest-train scores. The OOS-calibrated research contract keeps the primary
  `combined_mean_geometry_fold` threshold at `0.44155`; at that threshold it
  abstains on 28/71 calibration OOS negatives while preserving the heldout final
  readout above. The six accession-compatible active-site mapping blockers have
  been cleared; the surface remains partial because `m_csa:78` lacks an AFDB
  coordinate, `m_csa:204` and `m_csa:531` need source-geometry repair, and two
  UniProt-only rows need active-site sidecars.
- The partial train/cal OOS-negative surface is now explicitly sufficient for
  the bounded fold-augmented research contract with blocker disclosure, because
  71/76 rows are score-complete, the OOS-calibrated contract consumes exactly
  those 71 rows, no accession-compatible mapping blockers remain, and the
  primary threshold did not move. It is not sufficient for production-like
  threshold claims until the remaining five blockers are cleared.
- The remaining five train/cal OOS score-surface blockers were inspected from
  frozen inputs. None can be safely cleared without new source-backed
  active-site evidence, an alternate predicted coordinate, or an explicitly
  authorized experimental-coordinate-only policy.
- A downstream fold-augmented research readout now applies the fixed
  OOS-calibrated `combined_mean_geometry_fold` threshold to the seven
  review-only family expansion packets. After the repaired M-CSA primary-channel
  pass and the source-free predicted-geometry retrieval for three approved
  locator rows, it finds 15/22 primary score-complete rows, with 9
  non-abstained review-priority rows (`mh_066`, `m_csa:267`, `m_csa:131`,
  `m_csa:750`, `m_csa:551`, `m_csa:132`, `mh_073`,
  `secondary_probe::radical_sam_enzyme`, and `m_csa:116`), 6 abstained rows,
  and 7 geometry/fold-missing rows. `m_csa:973` is score-complete via its
  frozen train/calibration fold score and abstains at the fixed threshold. This
  is a triage signal only, not a family promotion or threshold change.
- The rank-1 family-panel source check for `m_csa:267` is complete from frozen
  local artifacts and keeps the row as a review-only OOS boundary control:
  local M-CSA graph evidence supports dihydrodipicolinate synthase lysine
  Schiff-base aldol/cyclization chemistry rather than any current seed-family
  promotion.
- The rank-2 family-panel source check for `m_csa:131` confirms source-backed
  flavin monooxygenase/oxygen-transfer support for the existing secondary-probe
  row, but does not authorize primary FMO promotion while subtype,
  coordinate/materialization, hard-negative, and expert-admission blockers
  remain active.
- The rank-3 family-panel source check for `m_csa:750` reads through the current
  registry and existing label-revision artifact, keeping it as OOS/boundary
  evidence and a future radical flavin/Fe-S dehydratase candidate, not a
  current v1 flavin, FMO, cobalamin, or radical-SAM promotion.
- The rank-4 family-panel source check for `m_csa:551` confirms mechanism-clean
  future FMO support, but the prior local adjudication explicitly blocks import
  and registry edits.
- The repaired M-CSA primary-channel pass cleared the remaining M-CSA
  missing-channel rows without label, threshold, split, import, registry, or
  production-scorer changes. `m_csa:132` uses real-sequence accession `P07740`
  and nearest-atlas TM `0.6879`; `m_csa:116` uses the accession-compatible
  `Q2RSB2` residue subset and nearest-atlas TM `0.5417`. Both are
  non-abstained under the fixed research gate and have frozen-local
  source-check packets: `m_csa:132` remains secondary FMO support only, and
  `m_csa:116` remains an OOS transhydrogenase/hydride-transfer control.
- The family-panel primary-channel gaps are queued separately. The original
  10 secondary/external rows all have source-backed predicted-fold scores; after
  approved source-free locator scoring for three rows, 7 still lack
  source-free predicted active-site geometry top1 scores. There are no
  remaining M-CSA rows in the missing primary-channel queue.
- The 10-row missing queue now has a review-only source-backed materialization
  plan and a scored P0/P1 materialization. It selects Q59490 for the cobalamin
  secondary probe, A0A1M6T2I7 for the radical-SAM secondary probe, Q6NSJ0 for
  the glycoside placeholder, and seven prior-resolved metal-hydrolase/boundary
  representatives. All 10 sidecars record PDB and AFDB-v6 coordinate hashes and
  real Foldseek/TM hits against the frozen predicted atlas, with nearest TM
  scores from `0.4655` to `1.004`. These rows remain review-only and are not
  primary-channel score-complete until source-free predicted geometry is
  materialized.
- The source-free predicted-geometry sidecar manifest now narrows that blocker:
  10/10 queued rows have AFDB-v6 CIF hashes and source-backed Foldseek/TM
  scores, 3/10 have approved source-free active-site locator sidecars, and
  7/10 remain blocked on approved locators. The
  companion locator schema requires at least two source-free sequence-position
  residue locators and forbids source prose, entry names, EC/Rhea identifiers,
  labels, benchmark roles, and panel IDs as predictive geometry features. The
  schema audit currently reports 3/10 locator sidecars present and passing,
  with `locator_sidecar_missing` as the remaining critical violation class. A
  materialization plan names the exact locator sidecar paths and rerun commands;
  eight rows start from structure-local ligand geometry candidates, while
  `mh_067` and `mh_068` require split-safe train/cal-template checks due to
  same-accession current702 geometry matches. A template-only bundle stages all
  10 locator sidecar shells outside the audited locator directory; none are
  scoring-ready until validated source-free residue locators are added and the
  schema audit is rerun.
- A review-only source-free locator candidate audit now stages coordinate-only
  contact candidates outside the audited locator directory. Eight of the 10
  rows have at least two selected-structure ligand/metal contact candidates;
  Q59490 and C7C422 remain blocked by no non-water/non-metal ligand candidate
  in the selected PDB coordinate. Six candidate rows have all candidate
  positions prevalidated against matching `_struct_ref_seq` UniProt mapping;
  Q79MP6 and P0A6P9 still need position validation. All 10 candidates remain
  not ready for predicted-geometry scoring until manual review,
  forbidden-feature review, and any split-safe template checks pass.
- A companion candidate-integrity audit checks those 10 staged sidecar files
  against the candidate audit payload and review-only guardrails. All 10 pass
  file/payload/guardrail integrity checks, remain outside the audited locator
  directory, and still have 0 scoring-ready rows.
- A companion source-free locator review queue ranks those candidates: three
  rows (`mh_066`, `mh_073`, and `secondary_probe::radical_sam_enzyme`) are
  priority-1 for manual forbidden-feature review; Q6NSJ0 needs ligand
  specificity review, P00918/P15289 need split-safe template checks,
  Q79MP6/P0A6P9 need position validation, and Q59490/C7C422 need a new
  source-free locator path or alternate coordinate.
- The manual locator review packet now combines candidate sidecar SHA-256s,
  integrity status, priority classes, and per-row review checklists. It is the
  exact next human-review artifact; no row is copy-ready or scoring-ready.
- A priority-1 locator review preflight dry-ran schema compatibility,
  guardrail cleanliness, and coordinate-contact plausibility for `mh_066`,
  `mh_073`, and `secondary_probe::radical_sam_enzyme`. All three passed the
  automation preflight, with `mh_073` carrying a minimum-two-locator warning.
  Human approval has since moved these three sidecars into the audited locator
  directory and made them scoring-ready.
- A blocked-row rescue manifest now inspects the two no-ligand locator rows.
  Both selected coordinates contain only water HETATMs. `mh_064` has five
  frozen source alternate PDB IDs (`3RKJ`, `3RKK`, `3SBL`, `3SFP`, and `3SPU`)
  staged as exact fetch commands pending manual approval; Q59490 has no frozen
  alternate beyond `1L1L` and needs a new nonlabel locator strategy or an
  explicitly authorized alternate source row.
- A review-only FMO subtype/hard-negative packet keeps `m_csa:131` and repaired
  `m_csa:132` as secondary-probe support, `m_csa:551` and `m_csa:973` as future
  support only, and `m_csa:750` as radical flavin/Fe-S boundary negative. No
  FMO row is import-ready or registry-edit-ready.
- A source-free predicted-geometry retrieval now scores the three approved
  locator rows (`secondary_probe::radical_sam_enzyme`, `mh_073`, and `mh_066`)
  against the existing geometry fingerprint surface using only approved residue
  locators and local AFDB-v6 CIFs. All three rows resolve at least two predicted
  residues and are retained by the existing `combined_mean_geometry_fold`
  research threshold when joined to their source-backed fold scores. This is
  review-only evidence; seven family-panel rows remain blocked on approved
  source-free locators and no labels, imports, thresholds, splits, or
  production scorers changed.
- The family-panel evidence packets now consume the approved source-free
  retrieval where applicable: `secondary_probe::radical_sam_enzyme`, `mh_066`,
  and `mh_073` are geometry-ok in their packet rows. The packet coverage audit
  now reports 15/22 family-panel rows with predicted geometry and 21 rows with
  predicted-fold hits while preserving all review-only guardrails.
- A companion source-check preflight now packages the three newly non-abstained
  source-free geometry rows for local review. It holds `mh_066`, `mh_073`, and
  `secondary_probe::radical_sam_enzyme` as review-only pending source checks,
  with `mh_066` showing geometry/fold agreement and the other two requiring
  mechanism-locus and duplicate/leakage review before any family decision.
- Learned-representation results are diagnostic, not decision-grade. ESM-2
  logistic is the strongest local learned comparator in the Wave 1.2 table but
  does not displace geometry. ESM-C logistic versus ESM-C cosine shows decoder
  choice is a real confound.
- Mechanism-feature embedding readiness now includes a normalized row-level
  active-site residue-role graph sidecar for 656 current702 rows. This closes
  the role-vocabulary sidecar gap only; directed electron/proton-transfer edges
  and row-specific bond-change mapping remain future feature work. A separate
  reaction-center template sidecar row-aligns fingerprint-level chemical
  operations and bond-change descriptors for 232 rows, but it is not
  row-specific reaction evidence.
- The mechanism-feature role-graph and reaction-center sidecars now pass a
  strict schema and row-alignment audit over all 702 current rows with zero
  critical violations. This validates the current sidecars as schema-safe
  train/cal-only embedding inputs, not as new mechanistic supervision.
- The mechanism-feature cofactor-locus gap now has a stricter review-only schema
  and materialization queue for `metal_ion_locus`, `cobalamin_locus`,
  `radical_sam_locus`, and `iron_sulfur_locus`. It uses existing geometry
  ligand context only: 176 current702 rows have proximal metal context, 4 have
  cobalamin, 8 have SAM, and 17 have Fe-S cluster context.
- The review-only `metal_ion_locus` sidecar is now materialized for all 702
  current rows from existing geometry ligand context. It marks 175 rows with
  proximal metal context, 85 with structure-wide-only metal context, 422 with no
  metal context, and 20 with unsupported/missing geometry. It is not label or
  predictive evidence until a future train/cal-only embedding pilot consumes it
  under split filtering. Its strict schema audit passes with zero critical
  violations.
- The review-only `cobalamin_locus` sidecar is also materialized and audited. It
  marks 4 rows with proximal cobalamin context, 678 with no cobalamin context,
  and 20 unsupported/missing-geometry rows; there are no structure-wide-only B12
  rows in the current geometry source.
- The review-only `radical_sam_locus` and `iron_sulfur_locus` sidecars are now
  materialized and audited from the same existing ligand context. The
  radical-SAM sidecar marks 8 proximal SAM-context rows and 2
  structure-wide-only rows; the Fe-S sidecar marks 17 proximal Fe-S-context rows
  and 11 structure-wide-only rows. Both carry explicit SAM/Fe-S copresence
  status, keep predictive/import flags false for all 702 rows, and pass schema
  audits with zero critical violations.
- A completion audit now confirms that all four schema-named cofactor-locus
  sidecar classes are materialized for 702 rows and schema-passing with zero
  critical violations. The next mechanism-feature action is a train/cal-only
  embedding pilot that consumes these sidecars without label/import changes or
  heldout leakage.
- A no-fit mechanism-feature embedding train/cal input manifest now enumerates
  the current sidecar surface without fitting weights or evaluating heldout
  rows. It keeps all 140 heldout rows excluded, marks 562 in-distribution
  candidate rows, and finds 524 rows with the minimal role-graph plus organic
  and inorganic cofactor-locus feature bundle.
- A deterministic train/cal split manifest now partitions those 524 ready
  mechanism-feature rows into 418 train rows and 106 calibration rows across six
  strata. Heldout remains excluded, 38 train/cal candidates remain blocked by
  role-graph readiness, and no model weights or thresholds are fit.
- A no-fit mechanism-feature embedding feature contract now strips labels from
  the ready train/cal feature-row surface. It exposes 524 feature rows with 418
  train and 106 calibration assignments, records allowed feature groups
  (role-graph, reaction-template, organic cofactor, and inorganic cofactor
  loci), excludes heldout rows, and keeps model fitting explicitly blocked until
  authorized.
- A strict audit now validates that feature contract against train/cal row
  alignment, forbidden label/outcome field exclusion, no-heldout discipline, and
  no-model-fit guardrails. It passes for 524/524 rows with zero critical
  violations; model fitting remains blocked until explicitly authorized.
- ProtT5 and SaProt have only NN/cosine-style local standardized exports today.
  Matched logistic-head reruns are blocked until raw local sidecars or weights
  exist; do not download large models for this by default.
- FMO remains secondary-only. Local FMO rows and external candidates are useful
  review/acquisition evidence, but no canonical primary promotion, registry
  change, threshold change, production scorer change, or import is authorized.

## Active Blockers

- Fair ProtT5/SaProt logistic-head comparison needs local raw embedding or
  structure-token sidecars and an ESM-2-style train/cal-only head. Existing
  local exports are not equivalent decoders.
- Sequence-to-deployment geometry is blocked by predicted-structure active-site
  degradation: AlphaFoldDB has no proximal ligands and perturbs the hand
  geometry evidence enough to introduce primary wrong calls and OOS false
  positives. ESMFold is not locally available without staging runtime/weights.
- FMO primary promotion is blocked by missing or unsuitable exact coordinate
  materialization for key external subtype rows, subtype/child-stratum
  definition work, PHBH-leaning gate behavior, hard-negative separation, and
  expert review.
- `m_csa:497` and `m_csa:750` must not be used as primary flavin support in old
  Wave 1 cells. They are OOS/boundary negatives under the current registry.
- Review surfaces are not labels. AI-visual review packets, PyMOL queues, FMO
  scouts, and external packets are review-only until a dedicated import preview,
  label-factory gate, and batch acceptance authorize counting.
- Disk must stay above 10 GiB free. Avoid large downloads and broad artifact
  regeneration unless the task explicitly asks for them.

## Next Gates

1. Use the fold-augmented research gate with the disclosed 71/76 train/cal
   OOS-negative surface when running downstream diagnostics; clear the remaining
   five source-geometry/coordinate/sidecar blockers before any stronger
   threshold or production-like claim.
2. For family-panel review, the six non-abstained fold-augmented rows are
   source-checked and remain review-only. `m_csa:973` reuses its frozen
   train/calibration fold score, is score-complete, and abstains under the fixed
   research threshold. The 10-row source-backed coordinate/Foldseek pass is
   done, and three approved locator rows now have source-free predicted-geometry
   scores joined into the readout. Next source-check the three new
   non-abstained review rows (`mh_066`, `mh_073`, and
   `secondary_probe::radical_sam_enzyme`) and continue clearing the seven
   remaining source-free locator blockers before any family-expansion decision.
3. If representation work resumes, produce row-aligned local sidecars first,
   start from
   `artifacts/v3_mechanism_feature_embedding_train_cal_input_manifest_current702_20260601.json`,
   then
   `artifacts/v3_mechanism_feature_embedding_train_cal_split_manifest_current702_20260601.json`,
   then train heads on train/cal rows only and evaluate heldout once, including
   a predicted-geometry robustness cell.
4. For FMO, revise the review/silver evidence gate into subtype panels, finish
   coordinate/materialization blockers, and keep candidate rows review-only.
5. For label growth, require explicit expert decision, no-import safety checks
   where applicable, label-factory gate pass, batch acceptance, and registry
   summary refresh before any countable import.

## Maintenance Notes

- Keep this file short enough to scan. Put detailed historical reasoning in the
  decision log or the specific artifact report.
- Refresh this file only when the current gate, trusted result set, blockers, or
  source-of-truth order changes.
- If a run only validates existing outputs, update automation memory rather than
  inflating this file.

## Primary References

- `artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json`
- `work/wave1_2_decoder_join_confound_audit_702_20260528.md`
- `artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json`
- `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json`
- `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`
- `artifacts/v3_predicted_structure_fold_channel_current702_20260601.json`
- `artifacts/v3_predicted_structure_fold_channel_contract_audit_current702_20260601.json`
- `artifacts/v3_predicted_structure_fold_augmented_novelty_variants_current702_20260601.json`
- `artifacts/v3_predicted_structure_fold_augmented_novelty_operating_grid_current702_20260601.json`
- `artifacts/v3_predicted_atlas_geometry_novelty_variants_current702_20260601.json`
- `artifacts/v3_predicted_atlas_geometry_novelty_operating_grid_current702_20260601.json`
- `artifacts/v3_fold_augmented_abstention_threshold_contract_current702_20260601.json`
- `artifacts/v3_fold_augmented_abstention_threshold_contract_oos_calibrated_current702_20260601.json`
- `artifacts/v3_fold_augmented_train_cal_oos_negative_surface_sufficiency_decision_current702_20260601.json`
- `artifacts/v3_mechanism_feature_sidecar_schema_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_inorganic_cofactor_locus_schema_current702_20260601.json`
- `artifacts/v3_mechanism_feature_metal_ion_locus_sidecar_current702_20260601.json`
- `artifacts/v3_mechanism_feature_metal_ion_locus_sidecar_schema_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_cobalamin_locus_sidecar_current702_20260601.json`
- `artifacts/v3_mechanism_feature_cobalamin_locus_sidecar_schema_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_radical_sam_locus_sidecar_current702_20260601.json`
- `artifacts/v3_mechanism_feature_radical_sam_locus_sidecar_schema_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_iron_sulfur_locus_sidecar_current702_20260601.json`
- `artifacts/v3_mechanism_feature_iron_sulfur_locus_sidecar_schema_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_inorganic_cofactor_locus_completion_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_embedding_train_cal_input_manifest_current702_20260601.json`
- `artifacts/v3_mechanism_feature_embedding_train_cal_split_manifest_current702_20260601.json`
- `artifacts/v3_mechanism_feature_embedding_feature_contract_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_research_readout_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_queue_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_m_csa267_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_m_csa131_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_m_csa750_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_m_csa551_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_m_csa_primary_channel_repair_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_m_csa132_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_m_csa116_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_missing_primary_channel_queue_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_missing_primary_channel_diagnosis_current702_20260601.json`
- `artifacts/v3_family_panel_source_backed_sidecar_materialization_plan_current702_20260601.json`
- `artifacts/v3_family_panel_source_backed_sidecar_materialization_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_predicted_geometry_sidecar_manifest_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_predicted_geometry_retrieval_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_predicted_geometry_source_check_preflight_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_schema_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_schema_audit_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_materialization_plan_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_template_bundle_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_candidate_audit_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_candidate_integrity_audit_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_review_queue_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_manual_review_packet_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_active_site_locator_priority1_review_preflight_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_locator_blocked_row_rescue_manifest_current702_20260601.json`
- `artifacts/v3_fmo_subtype_hard_negative_packet_current702_20260601.json`
- `artifacts/v3_m_csa497_label_revision_702_20260527.json`
- `artifacts/v3_m_csa750_label_revision_702_20260527.json`
- `artifacts/v3_fmo_fingerprint_definition_audit_702_20260528.json`
- `artifacts/v3_fmo_local_candidate_adjudication_551_973_702_20260528.json`
