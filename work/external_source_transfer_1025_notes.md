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
- `artifacts/v3_external_source_review_only_import_safety_audit_1025.json`
  confirms countable import adds 0 labels from that export.
- `artifacts/v3_external_source_transfer_gate_check_1025.json` passes 11/11
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

Next bounded work should use the active-site evidence queue to source or
prototype residue evidence for concrete PDB/AlphaFold handles, resolve the
broad-only EC rows separately, then compare any candidate evidence against the
heuristic geometry-retrieval control before any external label decision is
allowed.
