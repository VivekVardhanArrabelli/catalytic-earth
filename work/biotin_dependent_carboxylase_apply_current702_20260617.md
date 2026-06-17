# Biotin-Dependent Carboxylase Expansion Apply (2026-06-17)

## Outcome

Applied the row-guardrail-clean run0310 biotin-dependent carboxylase
broadened-handle preview into the expansion bronze registry. This grows the
combined mechanism-label count while keeping the frozen current702 benchmark
byte-unchanged.

- Combined labels: **8728 -> 8769** (+41)
- Expansion bronze registry: **8026 -> 8067** (+41 appended, 0 duplicate-skipped)
- Frozen current702 benchmark: **702 rows, byte-unchanged**
  (`5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`,
  `frozen_benchmark_registry_written: false`)
- Appended fingerprint: all 41 `biotin_dependent_carboxylase`, all `bronze`
- Family floor projection: cap 250, family combined 100 -> 141, not over cap,
  floor reached

## Why this was applied now

The run0310 automation built this preview and explicitly held it back only
because the family floor was already reached and 41 rows are below the
*autonomous* high-yield (>=150) apply criterion — not because the rows are
low quality. The rows are reviewed Swiss-Prot, EC/Rhea/cofactor-annotation
anchored, duplicate-screen clear, novelty-admitted, cap-safe, and
row-guardrail clean (0 problem rows; every row carries cofactor, domain, Rhea,
and active-site mechanism axes). An explicit user instruction to make progress
in the label count authorizes this human-directed apply of the already-verified
preview.

## Source and gate evidence

- Preview:
  `artifacts/v3_biotin_dependent_carboxylase_reviewed_broad_handle_preview_current702_20260616_run0310.json`
- Row-guardrail audit (passed, 0 problem rows):
  `artifacts/v3_biotin_dependent_carboxylase_reviewed_broad_handle_preview_row_guardrail_audit_current702_20260616_run0310.json`
- Apply path: `apply_external_annotation_anchored_import_to_registry`
  (dedupes against frozen + expansion, validates each row through
  `MechanismLabel.from_dict`, appends to the expansion registry only, re-shards,
  never writes the frozen benchmark)

## Post-apply audits (clean)

- Coverage/redundancy:
  `artifacts/v3_coverage_redundancy_audit_current702_20260617_biotin_apply.json`
  — 8769 combined = 702 frozen + 8067 expansion; holes none; floor deficit 0;
  over-cap only the pre-existing `metal_dependent_hydrolase`.
- Novelty admission gate:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260617_biotin_apply.json`
  — replayed 8067 expansion rows; admit 7565 -> 7606 (+41, all new biotin rows
  admitted), reject 47 and throttle 414 unchanged.
- `validate`: 702 curated labels, 46 fingerprints, 43 ontology families,
  12 sources. `git diff --check` clean. Shard counts consistent (sum 8067 =
  manifest 8067).

## Leakage posture

Each appended bronze label is reviewed-Swiss-Prot
`reviewed_swissprot_ec_rhea_cofactor_annotation` anchored. Protein name, EC
label, UniProt prose, source annotation, curated mechanism text, and the target
family lane are recorded as `excluded_context` and are not used as predictive
features. The frozen current702 benchmark, its coherence-audit baseline, and the
eval-contract hash are untouched.

## Apply summary artifact

`artifacts/v3_biotin_dependent_carboxylase_apply_summary_current702_20260617.json`
