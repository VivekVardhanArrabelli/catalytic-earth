# 700 Label-Factory Notes

## Accepted Countable Labels

The 700-entry gated pass accepted five additional automation-curated bronze
labels for counting:

- `m_csa:686` (`diisopropyl-fluorophosphatase`) as
  `metal_dependent_hydrolase`; retrieval top1 score `0.5817`, local calcium
  evidence, no counterevidence, no review-gap reasons.
- `m_csa:688` (`classical-complement-pathway C3/C5 convertase`) as
  `ser_his_acid_hydrolase`; retrieval top1 score `0.8300`, Ser-His-Asp/Glu
  mechanism text support, no cofactor requirement, no review-gap reasons.
- `m_csa:694` (`6-deoxyerythronolide B hydroxylase`) as
  `heme_peroxidase_oxidase`; retrieval top1 score `0.7112`, local heme
  evidence, no counterevidence, no review-gap reasons.
- `m_csa:697` (`12-oxophytodienoate reductase`) as
  `flavin_dehydrogenase_reductase`; retrieval top1 score `0.6850`, local FMN
  evidence, no counterevidence, no review-gap reasons.
- `m_csa:699` (`cytochrome P450 (BM-3)`) as `heme_peroxidase_oxidase`;
  retrieval top1 score `0.5208`, local heme evidence, no counterevidence, no
  review-gap reasons.

`artifacts/v3_label_batch_acceptance_check_700.json` records these five labels
as accepted for counting and confirms 0 hard negatives, 0 near misses, 0
out-of-scope false non-abstentions, 0 actionable in-scope failures, and 0
accepted review-gap labels. The countable registry now has 624 labels.

## Review Debt

The 700 review-state pass leaves 81 `needs_more_evidence` rows outside the
countable benchmark: 61 carried from the 675 state plus 20 new rows. The top
priority rows remain dominated by selected-structure cofactor gaps and
counterevidence:

- `m_csa:494` remains the highest-priority cobalamin/local-cofactor gap.
- New high-priority rows include `m_csa:687`, `m_csa:684`, `m_csa:680`,
  `m_csa:678`, `m_csa:690`, `m_csa:691`, and `m_csa:692`.
- New-debt next actions are 16 `inspect_alternate_structure_or_cofactor_source`,
  2 `expert_review_decision_needed`, 1 `expert_family_boundary_review`, and
  1 `verify_local_cofactor_or_active_site_mapping`.

The 700 scaling-quality audit classifies the new review-debt rows before
promotion: ontology scope pressure, family-propagation boundary, cofactor
family ambiguity, mixed evidence, reaction/substrate mismatch, and active-site
mapping gaps are observed in the deferred rows. Accepted clean labels have 0
review debt and the sequence-cluster proxy has 0 missing assignments and 0
near-duplicate hits among audited rows.

## Next Review Focus

Do not count the 81 review-state rows unless a later evidence pass removes
their gap reasons. The highest-value next repair is an alternate-structure or
cofactor-source inspection for the new 700 debt rows, especially the heme/flavin
absence patterns that are producing below-threshold, counterevidence-heavy
deferrals.

## 700 Remediation Pass

`artifacts/v3_review_debt_remediation_700.json` now expands the 20 new
review-debt rows into a structure-aware repair plan. The buckets are:

- 12 `alternate_pdb_ligand_scan`
- 3 `external_cofactor_source_review`
- 1 `active_site_mapping_repair`
- 1 `local_mapping_or_structure_selection_review`
- 1 `expert_family_boundary_review`
- 2 `expert_label_decision`

`artifacts/v3_review_debt_remediation_700_all.json` applies the same
structure-aware plan to all 81 review-debt rows. Across the full debt surface,
the repair buckets are 37 `alternate_pdb_ligand_scan`, 9
`local_mapping_or_structure_selection_review`, 9 `external_cofactor_source_review`,
7 `expert_family_boundary_review`, 16 `expert_label_decision`, and 3
`active_site_mapping_repair`. The full plan also records 69 rows where
alternate PDBs exist but none of those alternates have M-CSA residue-position
support, making them structure-wide review leads rather than local active-site
evidence.

`artifacts/v3_expert_label_decision_review_export_700.json` now routes the
active-queue expert-decision lane separately from generic review debt. It
exports all 76 `expert_label_decision_needed` rows as `no_decision`, records 0
countable candidates, links 56 carried and 20 new review-debt rows, and keeps
the 7 overlapping reaction/substrate mismatch rows covered by the dedicated
mismatch export. See `work/expert_label_decision_review_700_notes.md` for the
review-only risk profile. The paired
`artifacts/v3_expert_label_decision_repair_candidates_700.json` artifact covers
all 76 rows with 0 countable candidates and links remediation context for all
76 plus alternate-structure scan context for 42; the `_700_all` companion
artifact emits the full 76-row table.

`artifacts/v3_review_debt_alternate_structure_scan_700.json` scanned all 13
rows that needed alternate-PDB or local-structure selection review, covering
152 candidate PDB structures with 0 fetch failures. The scan now
conservatively remaps selected active-site residue positions onto 63
alternate-PDB structures; `m_csa:680` remains the only focused-scan row without
usable alternate-PDB active-site positions. Ten rows had no expected cofactor
family in any scanned candidate structure: `m_csa:687`, `m_csa:680`,
`m_csa:678`, `m_csa:690`, `m_csa:691`, `m_csa:700`, `m_csa:682`,
`m_csa:693`, `m_csa:695`, and `m_csa:702`.

Three rows had structure-wide expected-family hits: `m_csa:679`, `m_csa:696`,
and `m_csa:698`. The scan also computed local ligand context wherever M-CSA
residue positions were available, and no row had a local expected-family hit.
These rows remain review debt, not countable labels. In particular, the
alternate PDB hits for `m_csa:679` and `m_csa:696` have 0 M-CSA
residue-position support, and `m_csa:698` resolves the selected catalytic
residues but only sees local `MTE`, not local metal support.

`artifacts/v3_review_debt_alternate_structure_scan_700_all_bounded.json`
extends the scan to all 46 scan-candidate review-debt rows and all 739
candidate PDB structures. It remaps 362 alternate-PDB structures and finds
review-only local expected-family hits for `m_csa:577`, `m_csa:592`, and
`m_csa:641`. The companion
`artifacts/v3_review_debt_remap_leads_700_all_bounded.json` summarizes 44
review-only leads and keeps every row non-countable until review import,
evidence-gap clearance, and label-factory gates pass.

`artifacts/v3_review_debt_remap_local_lead_audit_700.json` audits the three
remap-local leads before any review import. `m_csa:577` and `m_csa:641` route
to expert family-boundary review because counterevidence remains after the
alternate-PDB local remap hits. `m_csa:592` routes to expert
reaction/substrate review because glucokinase and ATP phosphoryl-transfer text
conflict with the hydrolase top hit; local `MG` in alternate structures does
not resolve the reaction-class mismatch. All three rows keep a strict remap
guardrail: remap-local evidence is non-countable unless explicit
alternate-PDB residue positions or expert review/import evidence clear the gap
and the label-factory gate passes. The structure-selection candidate summary
therefore has 0 current candidates after reaction mismatch triage. The 700
scaling-quality audit now attaches this remap-local audit and records
`conservative_remap_local_evidence_without_explicit_alt_positions` as an
observed review-only failure mode.

`artifacts/v3_reaction_substrate_mismatch_audit_700.json` broadens the audit to
the active-learning queue. It flags 18 hydrolase-top1 rows with kinase names or
ATP phosphoryl-transfer text, keeps all 18 non-countable, and feeds a
`reaction_substrate_mismatch_value` ranking term in the 700 active-learning
queue. The accepted 700 batch still has 0 accepted reaction/substrate mismatch
rows.

`artifacts/v3_reaction_substrate_mismatch_review_export_700.json` now carries
the full family-guardrail mismatch surface: all 24 hydrolase-top1
reaction/substrate mismatch lanes, split into 17 current out-of-scope labels
and 7 unlabeled pending-review rows. The export records 0 labeled seed
mismatches, defers any kinase/phosphoryl-transfer ontology-family split until
expert reaction/substrate review, and feeds the 12th 700 factory gate.
`artifacts/v3_reaction_substrate_mismatch_decision_batch_700.json` keeps all
24 review items as `no_decision`, so automation cannot count or reject them.

## Remaining-Time Plan 2026-05-10T19:01Z

The assigned remap-local audit is complete early, with countable labels still
held at 624. Use the rest of the productive window to harden the factory around
that finding: keep the remap-local audit attached to scaling-quality checks,
add reaction/substrate mismatch triage and active-queue ranking, and verify the
new artifacts with regression tests before wrap-up.

Completed during the run: family-propagation guardrails now retain all 24
hydrolase-top1 reaction/substrate mismatch blockers, including 14 rows beyond
`max_rows`, with 17 labeled propagation blocks and 7 unlabeled pending-review
blocks.
