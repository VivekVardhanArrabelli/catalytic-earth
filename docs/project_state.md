# Project State

Last refreshed: 2026-06-03

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
  violations. The AFDB-v6 coordinate bundle is now persisted locally, so the
  coordinate-provenance gate is no longer a reproducibility blocker.
- The fold-channel coordinate-provenance audit now reports all 299 expected
  AFDB-v6 coordinate paths observed across 293 deduplicated accessions. The
  all-heldout and priority TSVs remain present and parseable, and the contract
  audit still has zero critical violations.
- A reproduction manifest now ties that fold channel together for future reruns:
  it records exact AFDB-v6 coordinate requests, scored TSV hashes, Foldseek
  commands, contract/provenance audit hashes, and no remaining byte-level
  reproduction blockers. No Foldseek/TM score was recomputed.
- A carryover-resolution audit now makes stale fold-channel prompts explicit:
  the requested fold-channel artifact/report are present and score-complete,
  126/126 heldout rows and 6/6 priority cofactor-confounded rows remain scored,
  and no Foldseek/TM rerun is needed unless the contract audit fails.
- The fold-augmented gate now has a leakage-safe thresholding contract. A
  deterministic in-distribution train/cal split selected the
  `combined_mean_geometry_fold` threshold `0.44155` at >=90% calibration
  in-scope retention. Heldout final readout at that fixed threshold retains
  45/47 in-scope rows, abstains on 44/79 OOS rows, and abstains on 5/6
  cofactor-confounded OOS rows. This is a research contract, not a production
  threshold.
- A CLI-generated confounded deployment-closure audit now ties that contract to
  the predicted-structure-vs-atlas fold channel. It confirms 6/6 priority
  cofactor-confounded rows have nearest-atlas Foldseek/TM hits and the fixed
  operating point abstains on 5/6, but production closure remains blocked by
  five train/cal OOS surface gaps.
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
- A matched-retention delta audit now compares that frozen geometry-only grid
  to the fold-augmented grid. Fold augmentation improves OOS and
  cofactor-confounded abstention at all four shared retention targets; at 90%
  in-scope retention, OOS abstention rises by `0.5444` and confounded-OOS
  abstention rises by `0.5`. This is still review-only and selects no threshold.
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
- Those same five Lever 3 fold-channel deployment blockers now have
  blocker-specific review gates plus a decision-application record. Three
  coordinate-available rows (`m_csa:531`, `uniprot:P78549`, and
  `uniprot:Q3LXA3`) now have an approved source-feature sidecar surface
  materialized for rerun input, with 3 rows and 18 source-feature support
  records. `m_csa:78`/P23007 has P00889 authorized as an ortholog surrogate and
  the AFDB coordinate has been fetched and hashed. The fixed-threshold combined
  readout has now been run over the four newly combined-score rows:
  `m_csa:78` and `uniprot:P78549` abstain at threshold `0.44155`, while
  `m_csa:531` and `uniprot:Q3LXA3` are retained. The calibration-impact audit
  expands the train/cal OOS combined-score surface from 71/76 to 75/76 rows and
  raises fixed-threshold OOS abstentions from 28 to 30.
  The expanded train/cal OOS surface is now materialized as a first-class
  threshold-selection input, and the regenerated OOS-calibrated research
  contract keeps the primary threshold unchanged at `0.44155`, with 30/75
  calibration OOS rows abstained and the same heldout final readout
  (45/47 in-scope retained; 5/6 cofactor-confounded OOS abstained).
  `m_csa:204`/P10746 is explicitly kept fold-only with the
  no-non-residue-sidecar policy caveat. The post-rerun closure-status gate
  reduces the prior five production blockers to this single caveat. The
  regenerated confounded readiness gate still keeps threshold `0.44155`,
  remains research-ready for the 5/6 confounded abstention result, and stays
  deployment-blocked until P10746 is resolved by policy acceptance or an
  approved non-residue sidecar.
- Two confounded-proxy train/cal scoring tranches have now been materialized
  and joined back to the deployable predicted-structure-vs-train-atlas surface.
  The first 50-row tranche fetched 48/50 AFDB-v6 query CIFs and produced
  47/50 full-channel rows. The second 66-row structural tranche fetched 64/66
  query CIFs, ran Foldseek against the train atlas, and produced 64/66
  full-channel rows; `P00806` and `P04531` have no AFDB-v6 prediction. The
  composed
  `v3_fold_augmented_confounded_proxy_extended_train_cal_oos_surface_current702_20260603`
  gives 186/192 train/cal OOS full-channel rows. At the fixed threshold
  `0.44155`, the proxy audit abstains on 63/186 calibration OOS rows overall,
  but 0/4 high-cofactor proxy rows and only 10/55 strict same-family structural
  proxy rows. The current candidate pool still has 170 unscored ready
  train/cal OOS rows, but 0 high-cofactor-axis and 0 structural-axis rows under
  the current proxy gate, so the next scoring-tranche plan selects 0 rows and
  the input manifest fails closed on `scoring_tranche_plan_empty`. The
  background-axis blocker confirms all 170 remaining rows are background-only
  under the current proxy axes, and the scout finds 0 mechanically ready
  replacement axes without a pre-registered train/cal-only proxy-axis contract.
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
- The high-value glycyl-radical/thiamine panel now has a no-template
  feature-refresh guardrail. Its two rows (`m_csa:30` and `m_csa:31`) are
  score-complete and abstained at the fixed research threshold, but both are
  heldout OOS/final-only controls, absent from the P0 train/cal readiness
  audit, and absent from the train/cal feature contract. They may be
  source-checked as review-only heldout evidence, but must not feed the
  no-template train/cal feature refresh.
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
- The highest-value glycyl-radical/thiamine-radical boundary panel now has a
  readiness packet. Both rows (`m_csa:30` and `m_csa:31`) are score-complete
  and abstain under the fixed fold-augmented research threshold, so they are
  ready only as review-only OOS boundary controls. Both still lack
  source-backed row-specific bond-change evidence and expert mechanism-locus
  validation before any family-expansion discussion.
- A companion source-check preflight now packages the three newly non-abstained
  source-free geometry rows for local review. It holds `mh_066`, `mh_073`, and
  `secondary_probe::radical_sam_enzyme` as review-only pending source checks,
  with `mh_066` showing geometry/fold agreement and the other two requiring
  mechanism-locus and duplicate/leakage review before any family decision.
- The first source-free geometry source check is complete for `mh_066`. Frozen
  local evidence supports an IMP-1 zinc metallo-beta-lactamase hydrolase
  context and both source-free geometry plus predicted-fold channels agree on
  `metal_dependent_hydrolase`, but the row remains an external non-countable
  review-only expansion candidate. It is not import-ready because row-specific
  bond-change/residue-role evidence, duplicate/split review, and expert
  admission are still unresolved.
- The second source-free geometry source check is complete for `mh_073`. Frozen
  local evidence supports an H-Ras Mg/GTPase nucleotide locus, while source-free
  geometry and predicted-fold channels disagree. The nearest fold hit is a
  current702 GTPase-like `metal_dependent_hydrolase` seed, so the row is kept
  as a review-only Mg/nucleotide boundary hard negative rather than promotion
  support.
- The third source-free geometry source check is complete for
  `secondary_probe::radical_sam_enzyme`. Frozen local evidence supports a TigE
  radical-SAM/Fe-S locus, but source-free geometry calls
  `metal_dependent_hydrolase` and the nearest predicted-fold hit is a
  `plp_dependent_enzyme` seed. The row remains secondary review-only evidence,
  not import-ready family promotion support.
- A remaining source-free locator blocker action queue initially classified
  seven family-panel rows after the three source checks. Two rows,
  `mh_067`/`mh_068`, have since passed copy approval, source-free geometry
  scoring, and source checks as review-only/no-promotion rows. The remaining
  five blocker rows are `mh_065`, `mh_072`, `external_glycoside_panel`,
  `mh_064`, and `secondary_probe::cobalamin_radical_rearrangement` (Q59490).
- The `mh_065`/`mh_072` UniProt position-validation attempt is complete and
  keeps both rows blocked. Their candidate contacts are coordinate-local, but
  frozen selected PDB mappings point to `Q932P5` for `1DDK` and `P08324` for
  `1E9I`, not the source accessions `Q79MP6` and `P0A6P9`. Do not copy these
  locator sidecars or score source-free predicted geometry. A local-cache
  matching-coordinate scout found 0 non-AFDB replacement coordinates;
  same-accession AFDB files exist but already failed residue-transfer with 0/6
  expected residue-code matches. The human decision is to leave both rows
  blocked; unblock only with matching frozen coordinates or a real expert
  alignment/remap that resolves the residue-code mismatch.
- The `external_glycoside_panel` ligand-specificity path remains blocked.
  The selected acetate (`ACT`) locator from unliganded MYORG `7QQF` was
  rejected, NAG contacts remain glycan/glycosylation-context evidence, and a
  local-cache substrate-coordinate scout found 0 same-accession substrate-like
  candidates. The block decision now explicitly rejects copying acetate,
  NAG/glycan, or raw glycan/buffer retargeting. Do not copy or score this row
  until a dedicated substrate-complex coordinate or expert-approved non-glycan
  locator exists.
- The final no-ligand locator blocker packet isolates two policy decisions:
  `mh_064` needs explicit approval before fetching five frozen alternate PDBs
  (`3RKJ`, `3RKK`, `3SBL`, `3SFP`, `3SPU`), and Q59490 needs a nonlabel
  locator strategy or approved alternate source row. A local-cache Q59490
  alternate-source scout found 0 eligible alternate rows. The Q59490 block
  decision now leaves the row blocked rather than fabricating residue locators
  from panel identity or source prose. The `mh_064` block decision now leaves
  the row blocked rather than fetching unapproved alternate coordinates.
  Automation did not fetch coordinates, copy sidecars, or score predicted
  geometry for either blocker.
- A refreshed source-free locator blocker status plus human-decision matrix now
  consolidates the five remaining blocker rows into four decision classes.
  Automation discovery is complete, 0/5 are automation-clearable, 0 are
  import-preview-ready, and `mh_065`/`mh_072` have now been explicitly left
  blocked rather than remapped; `external_glycoside_panel` is now explicitly
  left blocked rather than acetate/NAG-retargeted; Q59490 is now explicitly
  left blocked rather than nonlabel-fabricated or alternate-source-substituted.
  `mh_064` is now explicitly left blocked rather than fetch-authorized. No
  locator-policy decision remains automation-clearable; all remaining unblock
  paths require external approval/evidence before any copy, fetch, scoring,
  import, or label action. The consolidated locator-policy closure status
  records 5/5 blocked locator rows, 0 automation-clearable locator decisions,
  0 rows approved for copy/scoring, 0 import-preview-ready rows, and 0 countable
  label candidates.
- The family-panel import-preview blocker gate has been refreshed against that
  enriched matrix. It still reports 0/22 import-preview-ready rows, 0 countable
  label candidates, 11 completed source checks that remain review-only/no
  promotion, 6 expert family-admission blockers, and 5 source-free
  locator/primary-channel blockers.
- A refreshed current-run artifact integrity audit indexes 28 JSON artifacts
  and 28 matching work reports from this run, including the P0 train/cal
  feature sidecar, coverage-gap audit, and calibration review packet. All
  parse/presence checks passed, and the validation summary records full pytest,
  unittest discovery, compileall, `validate`, repo-wide JSON/JSONL parse,
  current-docs reference check, and diff-check success.
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
- A no-fit row-specific bond-change schema now makes that remaining feature gap
  explicit: 232 rows require source-backed row-specific bond-change evidence,
  with allowed event types, required sidecar fields, forbidden predictive keys,
  and a materialization queue staged before any embedding pilot can consume the
  feature. No source evidence was materialized and no model was fit.
- A companion feature-contract gap audit confirms that the staged
  row-specific bond-change schema has not entered the current no-fit
  mechanism-feature contract: 524 train/cal feature rows contain 0 bond-change
  feature rows, 0 heldout rows, and the strict feature-contract audit still has
  0 critical violations.
- The row-specific bond-change gap now has a no-fit materialization priority
  manifest. It partitions the 232 evidence-required rows into 171 P0 train/cal
  feature-contract gap rows, 13 P1 in-distribution rows needing upstream
  feature-bundle repair, and 48 P2 heldout final-only rows, plus a balanced
  15-row P0 pilot seed queue. It materializes no source evidence and mutates no
  feature contract.
- A no-fit P0 source-graph readiness audit now checks that balanced 15-row
  pilot seed against the frozen M-CSA graph. All 15 rows have entry nodes,
  mechanism-text edges, catalytic-residue edges, and EC mappings; 11/15 have
  local EC-to-Rhea mappings; 0/15 expose structured row-specific bond-change
  event edges. Manual/source-backed extraction remains required before any
  feature-contract refresh.
- A companion P0 extraction work package turns that readiness result into 15
  manual extraction templates with nine required source-backed fields, exact
  event/mapping acceptance criteria, and per-row Rhea lookup flags. It still
  materializes no source evidence and authorizes no feature-contract or model
  use.
- A strict audit now validates that P0 extraction work package as
  template-only: all 15 rows have the expected nine fields, 0 rows contain
  non-null extracted values, 0 rows are contract/model consumable, and the audit
  reports 0 critical violations.
- A companion TSV worksheet now gives the next run a manual filling surface for
  those same 15 P0 rows. All source-evidence cells are blank by construction;
  four rows are flagged for Rhea lookup, and the worksheet must be audited after
  any source-backed values are filled.
- A source-evidence sidecar schema now stages the future filled sidecar contract
  for that worksheet: 12 required row fields, six event fields, four mapping
  fields, forbidden predictive fields, and strict evidence/leakage checks. It
  is schema-only and still materializes 0 source values.
- The P0 worksheet now has a draft source-evidence sidecar derived from frozen
  local M-CSA graph evidence. All 15 rows have source spans and draft
  bond-change events. After the bounded official Rhea lookup resolution, 12/15
  have Rhea equations and 3/15 remain Rhea-missing. `m_csa:5`, `m_csa:11`,
  and `m_csa:169` now carry reviewer-approved M-CSA-only provenance from
  Vivek Vardhan Arrabelli, so 3/15 rows are feature-contract-consumable only
  through train/cal split filtering. The remaining 12 rows stay draft.
- A companion manual-review queue ranks those 15 draft rows without changing
  review state. It now separates the three approved M-CSA-only rows from the
  12 remaining draft rows: five high-complexity multi-event rows including
  Rhea-resolved `m_csa:124`, then seven standard draft reviews. It authorizes
  no full feature-contract refresh, model use, label change, or threshold
  change.
- A bounded official Rhea lookup resolution queried the four staged EC/accession
  rows. Exact EC queries returned no Rhea records, but accession `P00396`
  resolves `m_csa:124` to `RHEA:11436` with Rhea EC `7.1.1.9`, reflecting an
  EC reclassification away from the worksheet `ec:1.9.3.1`. The remaining Rhea
  lookup manifest is now empty because the three unresolved official Rhea rows
  are reviewer-resolved as M-CSA-only source evidence, not Rhea-resolved.
- A bounded official-source audit rechecked those three remaining rows against
  Rhea EC queries with and without the `ec:` prefix, Rhea accession queries, and
  current UniProtKB catalytic-activity records. Rhea still returns 0 records;
  UniProt confirms matching EC activity for all three accessions but provides
  no Rhea cross-references. These rows are not automation-resolvable from
  official Rhea/UniProt alone; the sidecar now records the human decision to
  approve M-CSA-only source evidence for all three with reviewer provenance.
- A companion reviewer decision matrix now makes that human gate explicit for
  `m_csa:11`, `m_csa:169`, and `m_csa:5`. Each row has three allowed decision
  options: approve M-CSA-only source evidence with reviewer provenance,
  reject/rewrite draft events, or hold for an authorized alternate reaction
  source. The matrix now records 3 reviewer IDs, 3 copy-ready approved
  decisions, and 3 feature-contract-consumable rows.
- A strict consumption audit confirms that the Rhea lookup resolution is used
  only as review evidence: `m_csa:124` carries `RHEA:11436` in the sidecar,
  the three Rhea-absent rows are reviewer-approved M-CSA-only evidence, and
  there are 0 unresolved lookup rows, 3 feature-contract-consumable rows, and
  0 model-training-eligible rows.
- A P0 feature-readiness audit now makes the no-template embedding blocker
  exact. All 15 rows are structurally ready as source-evidence rows,
  with 10 rows carrying bond-change events, 6 carrying proton-transfer events,
  and 9 carrying electron-transfer events. Three rows are approved and
  consumable for split-filtered train/cal materialization, but the feature
  contract contains no row-specific bond/proton/electron fields and the full
  15-row refresh remains blocked until the remaining 12 draft rows are reviewed.
- A companion P0 refresh-blocker audit now packages that into the automation
  decision: full no-template feature-contract refresh is not allowed from the
  P0 sidecar, but partial train/cal feature materialization is allowed for only
  the 3 approved rows. The load-bearing guardrail is that M-CSA-derived
  row-specific bond-change features must remain train/cal-only; heldout M-CSA
  rows must not be used for training or threshold tuning.
- The partial train/cal feature sidecar for those approved P0 rows is now
  materialized. It copies only label-stripped row-specific event features for
  `m_csa:5`, `m_csa:11`, and `m_csa:169`; all three are assigned to the train
  split, 12 draft rows are excluded, 0 heldout rows are present, and no model or
  threshold is fit. The materialized approved event surface carries three
  `bond_broken`, two `bond_formed`, two `electron_transfer`, and two
  `proton_transfer` events, but it is not enough to rerun the no-template
  centroid or residual methods because it has no calibration rows. A strict
  guardrail audit passes with 0 critical violations and confirms the predictive
  payload is numeric/boolean event features only.
- A companion P0 train/cal coverage-gap audit makes the next review gate
  exact: the remaining draft P0 queue has 8 train rows and 4 calibration rows.
  The no-template rerun is blocked by absent approved calibration coverage. The
  next manual review rows are `m_csa:186`, `m_csa:147`, `m_csa:6`, and
  `m_csa:133`; `m_csa:186` and `m_csa:147` also add the currently
  unmaterialized `bond_order_changed` event type. A manual calibration review
  packet now carries those four rows and 16 event-review records without
  recording approvals or changing the feature contract.
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
  critical violations.
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
- A train/cal-only mechanism-feature embedding pilot now consumes the audited
  feature contract directly. It fits standardized nearest-primary centroids on
  the 418 assigned train rows and selects a >=90% primary-retention threshold
  on the 106 calibration rows. The full contract reaches calibration AUC
  `0.948491` and 100% OOS abstention at 91.43% primary retention, but the
  no-reaction-template ablation drops to AUC `0.549698` and 14.08% OOS
  abstention at the same retention target. Treat this as a real implementation
  result and a clear signal that the next mechanism-feature work must close
  row-specific bond-change/proton/electron-flow features and then materialize
  the same allowed feature surface for heldout once-only readout; do not trust
  the full-contract score as production evidence.
- That heldout readout is now materialized once. Existing sidecars provide the
  same allowed feature surface for 132/140 heldout rows; 8 remain blocked by
  accession-compatible role-graph gaps. The full-contract variant reaches
  heldout AUC `0.8812` and abstains on 100% of ready OOS rows at the
  calibration-selected threshold, but retains only 75% of ready primary rows.
  The no-reaction-template ablation is near chance on heldout (AUC `0.488591`,
  9.52% OOS abstention at 85.42% primary retention). This confirms the real
  next lever is row-specific mechanism-feature materialization, not another
  template-level classifier.
- The out-of-span residual is the surviving deployable signal from this lever and
  is now confirmed. Built on a separate closed-form information-preserving metric
  line (an independent Lever 2 build), the unsupervised out-of-atlas-span residual
  survives a PCA cutoff-robustness sweep and a held-out-from-design confirmatory
  split with a label-permutation null (p=0.0005). Unlike the template-dependent
  centroid scores it is sequence-only and deployment-valid.
- That confirmed residual is integrated into the per-channel rule gate as a third
  lift channel, adding a +0.076 confounded-safe OOS-abstain lift at the >=85%
  in-scope retention floor. The residual threshold remains research-grade pending a
  deployable calibration.
- 2026-06-02: the two independent Lever 2 builds are integrated into one result
  (see `docs/decision_log.md` 2026-06-02). The consolidated negative — a learned or
  standardized embedding over the CURRENT feature surface does not deployably beat
  geometry — is robust precisely because both builds reach it independently. The
  confirmed gate-integrated residual is the live deployable signal; the centroid
  line's train/cal/heldout discipline (418 train / 106 calibration / once-only
  heldout) becomes the calibration standard the residual must meet; and its
  bond-change/proton/electron feature-materialization track (Rhea provenance) is the
  kept forward path to the genuinely-new mechanism feature. No code or artifacts from
  either build were removed.
- Later 2026-06-02 Lever 2 artifacts materialize the approved row-specific
  bond/proton/electron surface into a 43-row train/cal OOS-augmented feature
  surface and freeze a calibration-only no-template pair contract. The stronger
  pair (`event_residue_role:proton_transfer|electrostatic_stabiliser` plus
  `residue_code_count:his=3`) reaches calibration OOS abstention 0.857143 at
  the residual threshold 3.21469422, with heldout still unread. Deployment is
  blocked by the missing source-free proton-transfer event-axis linker and
  current702 heldout locator surface. A His-count-only fallback avoids the
  event axis but drops calibration OOS abstention to 0.642857 and requires
  explicit acceptance before any heldout read.
- A no-fit mechanism-feature train/cal guardrail audit now pins the same
  surface across the input manifest, split manifest, and feature contract: 524
  feature rows exactly match 524 split rows, 140 heldout rows remain excluded,
  and label identity fields are not features. This still does not authorize
  model fitting or heldout evaluation.
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
   done, and five approved locator rows now have source-free predicted-geometry
   inputs visible to the source-free surface. `mh_067`/`mh_068` passed the
   split-safe check, were approved/copied into the audited locator directory,
   and are source-checked as review-only/no-promotion. The import-preview gate
   still reports 0/22 import-ready rows: `mh_065`/`mh_072` are explicitly left
   blocked until matching coordinates or a residue-code-resolving expert remap
   exist; the remaining open priority locator decisions are
   `external_glycoside_panel` (ligand-specificity validator or substrate
   coordinate), `mh_064` (alternate-coordinate fetch policy), and Q59490 /
   `secondary_probe::cobalamin_radical_rearrangement` (nonlabel locator
   strategy or alternate source). No label/import/family promotion is
   authorized.
3. If representation work resumes, produce row-aligned local sidecars first,
   start from
   `artifacts/v3_mechanism_feature_embedding_train_cal_input_manifest_current702_20260601.json`,
   then
   `artifacts/v3_mechanism_feature_embedding_train_cal_split_manifest_current702_20260601.json`.
   The row-specific train/cal feature rerun is now complete through the
   calibration-only pair contract. Next choose the deployable application path:
   preferred path is filling
   `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_event_axis_linker_schema_current702_20260602.json`
   after approved current702 heldout locator sidecars exist; fallback path is
   explicitly accepting the lower-recall His-count-only contract in
   `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_residue_count_fallback_contract_current702_20260602.json`.
   The current approval packet
   `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_approval_packet_current702_20260603.json`
   normalizes the 55 priority-1 locator rewrites into pending approve/reject
   records with candidate and planned-payload hashes; it records 49 clean rows,
   6 warning rows, and 0 approvals.
   The current locator rewrite materialization gate
   `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_materialization_gate_current702_20260603.json`
   is fail-closed: 55 preflight-passed rows have 0 explicit approvals and 0
   copied locator sidecars, so preflight alone is not enough to build the
   heldout application surface.
   The composed pre-threshold readiness gate
   `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_oos_augmented_best_token_followup_pair_source_free_pre_threshold_readiness_current702_20260603.json`
   keeps the frozen residual threshold unapplied until approved locators,
   event-axis linkers, and the heldout-safe source-free application surface all
   exist.
   In both cases, do not apply any frozen residual threshold or read heldout
   until the chosen source-free application surface is complete and guardrail
   audited.
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
- `artifacts/v3_predicted_structure_fold_channel_coordinate_provenance_audit_current702_20260601.json`
- `artifacts/v3_predicted_structure_fold_channel_reproduction_manifest_current702_20260601.json`
- `artifacts/v3_predicted_structure_fold_augmented_novelty_variants_current702_20260601.json`
- `artifacts/v3_predicted_structure_fold_augmented_novelty_operating_grid_current702_20260601.json`
- `artifacts/v3_predicted_atlas_geometry_novelty_variants_current702_20260601.json`
- `artifacts/v3_predicted_atlas_geometry_novelty_operating_grid_current702_20260601.json`
- `artifacts/v3_fold_augmented_abstention_threshold_contract_current702_20260601.json`
- `artifacts/v3_fold_augmented_abstention_threshold_contract_oos_calibrated_current702_20260601.json`
- `artifacts/v3_fold_augmented_train_cal_oos_negative_surface_sufficiency_decision_current702_20260601.json`
- `artifacts/v3_fold_augmented_confounded_deployment_closure_audit_current702_20260601.json`
- `artifacts/v3_fold_augmented_source_feature_active_site_sidecar_review_gate_current702_20260602.json`
- `artifacts/v3_fold_augmented_p23007_alternate_accession_policy_gate_current702_20260602.json`
- `artifacts/v3_fold_augmented_non_residue_interaction_sidecar_policy_preflight_current702_20260602.json`
- `artifacts/v3_fold_augmented_p10746_source_feature_refresh_audit_current702_20260603.json`
- `artifacts/v3_fold_augmented_blocker_human_decision_application_current702_20260603.json`
- `artifacts/v3_fold_augmented_approved_source_feature_active_site_sidecar_materialization_current702_20260603.json`
- `artifacts/v3_fold_augmented_p00889_ortholog_coordinate_fetch_manifest_current702_20260603.json`
- `artifacts/v3_fold_augmented_fixed_threshold_rerun_readiness_current702_20260603.json`
- `artifacts/v3_fold_augmented_fixed_threshold_combined_rerun_readout_current702_20260603.json`
- `artifacts/v3_fold_augmented_fixed_threshold_combined_rerun_calibration_impact_current702_20260603.json`
- `artifacts/v3_fold_augmented_expanded_train_cal_oos_negative_surface_scores_current702_20260603.json`
- `artifacts/v3_fold_augmented_abstention_threshold_contract_expanded_oos_calibrated_current702_20260603.json`
- `artifacts/v3_fold_augmented_post_rerun_deployment_closure_status_current702_20260603.json`
- `artifacts/v3_fold_augmented_post_rerun_confounded_deployment_closure_audit_current702_20260603.json`
- `artifacts/v3_fold_augmented_p10746_deployment_caveat_decision_packet_current702_20260603.json`
- `artifacts/v3_fold_augmented_p10746_deployment_caveat_decision_application_current702_20260603.json`
- `artifacts/v3_fold_augmented_post_decision_deployment_closure_status_current702_20260603.json`
- `artifacts/v3_predicted_structure_fold_confounded_operating_point_readiness_current702_20260602.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_schema_current702_20260601.json`
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
- `artifacts/v3_mechanism_feature_embedding_pilot_current702_20260601.json`
- `artifacts/v3_mechanism_feature_embedding_heldout_readout_current702_20260601.json`
- `artifacts/v3_mechanism_feature_residual_robustness_current702_20260601.json`
- `artifacts/v3_mechanism_residual_gate_integration_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_feature_contract_gap_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_materialization_priority_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_graph_readiness_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_extraction_work_package_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_extraction_package_strict_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_extraction_worksheet_current702_20260601.tsv`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_source_evidence_sidecar_schema_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_train_cal_feature_sidecar_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_train_cal_feature_guardrail_audit_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_train_cal_coverage_gap_current702_20260601.json`
- `artifacts/v3_mechanism_feature_row_specific_bond_change_p0_calibration_review_packet_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_research_readout_current702_20260601.json`
- `artifacts/v3_family_panel_high_value_glycyl_radical_readiness_packet_current702_20260601.json`
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
- `artifacts/v3_family_panel_source_free_predicted_geometry_source_check_mh_066_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_predicted_geometry_source_check_mh_073_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_predicted_geometry_source_check_secondary_probe_radical_sam_enzyme_current702_20260601.json`
- `artifacts/v3_fold_augmented_family_panel_source_check_completion_reconciliation_current702_20260602.json`
- `artifacts/v3_fold_augmented_family_panel_countability_gate_preflight_current702_20260602.json`
- `artifacts/v3_fold_augmented_family_panel_import_preview_blocker_gate_current702_20260602.json`
- `artifacts/v3_family_panel_source_free_locator_remaining_blocker_action_queue_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_locator_blocker_resolution_status_current702_20260601.json`
- `artifacts/v3_family_panel_source_free_locator_matching_coordinate_scout_mh065_mh072_current702_20260602.json`
- `artifacts/v3_family_panel_source_free_locator_mh065_mh072_block_decision_current702_20260603.json`
- `artifacts/v3_family_panel_source_free_locator_glycoside_substrate_coordinate_scout_external_glycoside_panel_current702_20260602.json`
- `artifacts/v3_family_panel_source_free_locator_external_glycoside_block_decision_current702_20260603.json`
- `artifacts/v3_family_panel_source_free_locator_q59490_alternate_source_cache_scout_current702_20260602.json`
- `artifacts/v3_family_panel_source_free_locator_q59490_block_decision_current702_20260603.json`
- `artifacts/v3_family_panel_source_free_locator_mh064_block_decision_current702_20260603.json`
- `artifacts/v3_family_panel_source_free_locator_policy_closure_status_current702_20260603.json`
- `artifacts/v3_family_panel_source_free_locator_human_decision_matrix_current702_20260601.json`
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
