# NAD(P)-dehydrogenase + Glycosyltransferase Bronze Expansion Apply

Run: 2026-06-12T21:53:53Z to wrap-up.

## Result

- Frozen current702: 702 labels, sha256 `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505` before and after both applies.
- External bronze registry: 2940 -> 3340 (+400).
- Combined label surface: 3642 -> 4042.
- Honest counters after apply: positive_bronze 2329, oos_bronze 1696, silver_ready 0, silver_confirmed 17, projected 0.
- Refreshed counter artifact: `artifacts/v3_source_trust_tier_policy_current702.json`.
- Refreshed governor artifact: `artifacts/v3_coverage_redundancy_audit_current702_20260612_nad_glyco_applied.json`
  with report `work/coverage_redundancy_audit_current702_20260612_nad_glyco_applied.md`; result:
  fingerprint Gini 0.1578, holes [], over-cap [`metal_dependent_hydrolase`], next-batch floor deficit 0.

## Applied Previews

1. `artifacts/v3_nad_glycosyltransferase_subfamily_sourcing_preview_current702.json`
   - Rerun at `--max-records-per-lane 100`.
   - Fetched 794 rows; mechanism-corroborated 709; gate-admitted before cap 486.
   - Applied 373 rows: `nad_p_dehydrogenase` 150 and `glycosyltransferase` 223.
   - NAD(P) held at cap: 113; novelty throttled/rejected: 223; fetch failures: 0.
   - Registry apply: 2940 -> 3313; combined 3642 -> 4015; duplicate skipped 0.

2. `artifacts/v3_glycosyltransferase_cap_fill_preview_current702.json`
   - Follow-on glycosyltransferase-only cap fill at `--max-records-per-lane 150`.
   - Fetched 445 rows; mechanism-corroborated 157; gate-admitted before cap 37.
   - Applied 27 rows: `glycosyltransferase` 223 -> 250.
   - Glycosyltransferase held at cap: 10; novelty throttled/rejected: 120; fetch failures: 0.
   - Registry apply: 3313 -> 3340; combined 4015 -> 4042; duplicate skipped 0.

## Guardrails

- EC remained scope-only and is recorded as a non-counted `ec_scope_hint`.
- Every applied row is `tier=bronze`, `review_status=automation_curated`, and `entry_id` namespace `uniprot`.
- `predictive_evidence` is `[]` on applied preview rows; broadened keyword/cosubstrate/Rhea/binding handles are admission evidence only.
- Dedup ran against both frozen current702 and external bronze registries through the canonical apply writer.
- Per-fingerprint caps held: NAD(P) dehydrogenase capped at 150 because chemistry-confusable; glycosyltransferase capped at 250.

## Validation

- `PYTHONPATH=src python -m pytest -q tests/test_nad_glycosyltransferase_subfamily_sourcing.py tests/test_source_trust_tiers.py tests/test_leakage_closure.py tests/test_external_annotation_anchored_import.py tests/test_coverage_redundancy_audit.py tests/test_novelty_admission_gate.py tests/test_fingerprints.py` -> 231 passed, 14 subtests passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` -> 12 source records, 14 mechanism fingerprints, 17 ontology families, 702 curated labels.
- `git diff --check` -> clean.

## Next Scaling Action

Wire `sam_methyltransferase` next, but do it as a deliberate 15-fingerprint universe change: add the fingerprint spec and ontology node, add the EC 2.1.1 + methyltransferase/SAM/SAH Rhea participant rule with a no-Fe-S guard to separate radical-SAM, add tests, regenerate the OOS pre-registration to the 15fp universe, then run a non-destructive preview before any apply.
