# External Source Transfer 1025 Notes

The 1,025 preview is not promotable and should stay a source-limit audit point:
it adds 0 countable labels and leaves the canonical registry at 679 labels.
External-source transfer is now the active path for post-M-CSA scaling work, but
all current artifacts are review-only.

Current review-only external artifacts:

- `artifacts/v3_external_source_candidate_manifest_1025.json` carries 30
  UniProtKB/Swiss-Prot candidates across six lanes with 0 countable candidates.
- `artifacts/v3_external_source_lane_balance_audit_1025.json` is clean: each
  lane contributes five candidates and the dominant-lane fraction is `0.1667`.
- `artifacts/v3_external_source_candidate_manifest_audit_1025.json` is clean and
  confirms 0 rows are marked ready for label import.
- `artifacts/v3_external_source_evidence_plan_1025.json` requests active-site
  residue positions, curated reaction or mechanism evidence, structure mapping,
  heuristic geometry controls, OOD assignment, sequence holdouts, review
  decisions, and full label-factory gates before import. It flags seven broad
  or incomplete EC-context candidates and routes three broad-only candidates to
  reaction disambiguation before active-site mapping.
- `artifacts/v3_external_source_evidence_request_export_1025.json` exports 30
  no-decision review items and is marked `external_source_review_only`.
- `artifacts/v3_external_source_active_site_evidence_queue_1025.json` prioritizes
  25 review-only candidates for active-site evidence collection and defers five
  rows: two exact-reference holdouts and three broad-EC disambiguation cases.
- `artifacts/v3_external_source_active_site_evidence_sample_1025.json` samples
  all 25 ready rows from UniProtKB features: 15 have active-site features, 10
  are active-site-feature gaps, all 25 have catalytic-activity comments, and 0
  rows are countable or import-ready. The current active-site feature-gap
  accessions are `O60568`, `P29372`, `P27144`, `A2RUC4`, `P51580`, `O95050`,
  `Q9HBK9`, `A5PLL7`, `P32189`, and `Q32P41`.
- `artifacts/v3_external_source_heuristic_control_queue_1025.json` marks 12
  candidates ready for heuristic-control prototyping and defers 13 rows: 10
  active-site-feature gaps and 3 broad-EC disambiguation cases.
- `artifacts/v3_external_source_structure_mapping_plan_1025.json` carries 12
  candidates into structure mapping and keeps 13 deferred. The bounded
  `artifacts/v3_external_source_structure_mapping_sample_1025.json` maps 4/4
  sampled candidates onto current AlphaFold CIFs with 0 fetch failures and 0
  countable labels.
- `artifacts/v3_external_source_heuristic_control_scores_1025.json` runs the
  current geometry-retrieval heuristic on those 4 mapped controls. All 4 rank
  `metal_dependent_hydrolase` top1, so
  `artifacts/v3_external_source_failure_mode_audit_1025.json` records top1
  fingerprint collapse, metal-hydrolase collapse, and scope/top1 mismatch as
  review-only failure modes before any external decision artifact can count.
  The scope/top1 mismatches are the isomerase-lane controls `P60174` and
  `Q13907`; the glycan-chemistry controls `P33025` and `Q6NSJ0` also collapse
  to metal hydrolase top1 but are not marked scope/top1 mismatches by the
  current audit rule.
- `artifacts/v3_external_source_review_only_import_safety_audit_1025.json`
  confirms countable import adds 0 labels from that export.
- `artifacts/v3_external_source_transfer_gate_check_1025.json` passes 22/22
  checks for review-only evidence collection and is still not ready for label
  import.

Sequence-similarity guardrail details:

- `O15527` overlaps `m_csa:185` and must stay a sequence-holdout control.
- `P42126` overlaps `m_csa:341` and must stay a sequence-holdout control.
- No external candidate is countable from exact-reference or lane membership
  alone.

Reaction-context details:

- `artifacts/v3_external_source_reaction_evidence_sample_1025.json` queries Rhea
  for the first six external candidates and records 22 reaction-context rows
  with 0 fetch failures.
- `artifacts/v3_external_source_reaction_evidence_sample_audit_1025.json` is
  guardrail-clean, with 0 countable candidates and 0 import-ready rows.
- The audit flags `1.1.1.-`, `1.11.1.-`, and `1.8.-.-` as broad or incomplete
  EC context. Treat those rows as weak reaction context only, not specific
  mechanism evidence.

Next bounded work should repair the external-control weaknesses before any
external label decision: resolve the 10 active-site-feature gaps, disambiguate
the 3 broad-EC rows, and either improve ontology/representation controls or
explain why the current heuristic collapses mapped external controls into
`metal_dependent_hydrolase`.
