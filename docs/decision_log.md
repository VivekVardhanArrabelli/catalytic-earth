# Decision Log

This log records durable decisions that future agents should apply before
interpreting older artifacts. Dates are UTC artifact dates unless noted.

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
geometry and/or predicted-fold channel evidence.

Consequence: the next review work should keep the six source-checked
non-abstained boundary rows review-only, while working the 10 remaining
primary-channel-missing rows in the source-backed sidecar and coordinate
materialization queue.
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
requiring source-backed sidecars and coordinate materialization.

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

Artifacts:
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
`work/mechanism_feature_cobalamin_locus_sidecar_schema_audit_current702_20260601.md`.

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
is entirely geometry gaps, as expected for the panel definition. The near-orphan
glycoside/nucleoside packet has one current row with ok predicted geometry
(`m_csa:10`) and three gaps.

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

Artifacts: `artifacts/v3_fold_augmented_abstention_gate_current702_20260601.json`,
`work/fold_augmented_abstention_gate_current702_20260601.md`,
`artifacts/v3_predicted_structure_fold_augmented_novelty_variants_current702_20260601.json`,
`work/predicted_structure_fold_augmented_novelty_variants_current702_20260601.md`.

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

Artifacts: `artifacts/v3_predicted_atlas_geometry_novelty_variants_current702_20260601.json`,
`work/predicted_atlas_geometry_novelty_variants_current702_20260601.md`.

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
