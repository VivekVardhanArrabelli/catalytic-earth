# SAM methyltransferase bronze expansion apply

Run: 2026-06-12T23:19:45Z preview; 2026-06-12T23:27:14Z apply.

## Result

- Preview command: `PYTHONPATH=src python scripts/source_sam_methyltransferase_family.py --max-records-per-lane 120`.
- Apply command: `PYTHONPATH=src python scripts/source_sam_methyltransferase_family.py --max-records-per-lane 120 --apply`.
- Frozen current702 sha before apply: `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Frozen current702 sha after apply: `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- External bronze registry: 3340 -> 3590 (+250).
- Combined label surface: 4042 -> 4292.
- Added family: `sam_methyltransferase` 0 -> 250 (cap 250; floor reached).
- Held/throttled: 14 held at cap; 28 throttled as redundant; 12 rejected over-cap/no new chemistry; 2 multi-fingerprint-signal rows held; 9 skipped as duplicates/current conflicts.
- Fetch failures: 0.

## Guardrails

- Registry growth went only to `data/registries/external_bronze_labels.json`; `data/registries/curated_mechanism_labels.json` was not written.
- EC 2.1.1 is scope-only (`ec_scope_hint`) and never a counted corroborator.
- Counted mechanism corroboration came from SAM/SAH participant/cofactor/cosubstrate, Methyltransferase keyword/domain, active/binding-site evidence, and Rhea participant axes.
- SAM/SAH/keyword handles are scope/admission evidence in excluded context, never predictive features; `predictive_evidence` remains `[]`.
- Fe-S/radical-SAM rows are blocked from `sam_methyltransferase`; off-target fingerprint matches are held by the runner.
- Every appended label is `tier=bronze`, `review_status=automation_curated`, and `uniprot:*`.
- Dedup ran against both frozen current702 and external bronze; novelty and per-fingerprint cap gates ran before apply.

## Honest counters after apply

- positive_bronze: 2579
- oos_bronze: 1696
- silver_ready: 0
- silver_confirmed: 17
- projected: 0

## Artifacts

- Preview: `artifacts/v3_sam_methyltransferase_sourcing_preview_current702.json`
- Preview report: `work/sam_methyltransferase_sourcing_current702.md`
- Post-apply coverage audit: `artifacts/v3_coverage_redundancy_audit_current702_20260612_sam_methyl_applied.json`
- Post-apply coverage report: `work/coverage_redundancy_audit_current702_20260612_sam_methyl_applied.md`
- OOS preregistration re-freeze: `artifacts/v3_external_hard_negative_next_tranche_preregistration_15fp_1025.json`
- Source-trust policy ledger: `artifacts/v3_source_trust_tier_policy_current702.json`
