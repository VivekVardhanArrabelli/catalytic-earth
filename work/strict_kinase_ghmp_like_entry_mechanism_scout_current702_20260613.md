# Strict kinase GHMP-like entry/Rhea mechanism scout

Run: 2026-06-13T22:10:34Z

Status: non-destructive scout only; generated 0 labels and wrote no registry.

This bounded scout followed the latest handoff request to check `galactokinase_mevalonate_homoserine` before any further strict-kinase fingerprint work. EC/name/Rhea/reaction/feature handles are scout/admission context only; EC is scope-only and never a counted corroborator; `predictive_evidence` remains empty.

## Result

- Reviewed total: 613.
- Search rows sampled: 120.
- Registry-new sample rows: 5 (0.042).
- Entry fetch attempts: 5; successes 5; failures 0.
- Existing `ghmp_small_molecule_kinase` combined count: 150/150.
- Likely wireable by non-EC handles in fetched registry-new sample: 0.

## Recommendation

- Wire full pipeline next: False.
- Reason: GHMP-like lane is already represented by ghmp_small_molecule_kinase at the chemistry-confusable cap 150/150; registry-new supply in this sample is sparse, so do not split/apply without a new chemistry boundary and OOS preregistration.

Next safe action: prefer a genuinely new non-capped family/source lane or a new non-EC corroborator path for PfkB/biotin/glycoside; do not use this GHMP-like scout for an apply under the current cap.

Artifact: `artifacts/v3_strict_kinase_ghmp_like_entry_mechanism_scout_current702_20260613.json`
