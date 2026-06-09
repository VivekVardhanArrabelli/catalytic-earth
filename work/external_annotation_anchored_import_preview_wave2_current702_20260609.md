# Annotation-Anchored Bronze External Import — Wave 2 (non-destructive preview)

Run: 2026-06-09T22:22:43Z

Reviewed Swiss-Prot/EC/Rhea/cofactor annotation as a bronze label source.
EC, protein names, and prose are excluded from predictive features (the
benchmark scorer never sees them); structure/geometry confirmation is a
deferred bronze->silver promotion signal. The curated registry is NOT
written by this run.

## Result

- Preview rows considered: 600.
- **Importable bronze labels this batch: 186** -> registry 702 -> **888** if merged.
- Label types: {'seed_fingerprint': 101, 'out_of_scope': 85}.
- Positive fingerprints: {'metal_dependent_hydrolase': 95, 'plp_dependent_enzyme': 6}.
- Confidence: {'high': 62, 'medium': 124}.
- Held for review: 90 ({'primary_lane_without_cofactor_corroboration': 15, 'ambiguous_lane_review_required': 75}).
- Skipped: 324 (mostly current702 duplicate screen not yet confirmed — the next batch).

## Diversity by lane (label_type split)

| Lane | imported scope split |
| --- | --- |
| PLP children | {'seed_fingerprint': 6} |
| adjacent high-yield lyase/isomerase | {'out_of_scope': 10} |
| glycoside hydrolase | {'out_of_scope': 1} |
| glycoside/nucleoside | {'out_of_scope': 39} |
| metal hydrolase | {'seed_fingerprint': 94} |
| metal hydrolase Mg/Mn controls | {'seed_fingerprint': 1} |
| near-orphan/no-reliable-structure | {'out_of_scope': 27} |
| nucleotide phosphoryl-transfer boundary | {'out_of_scope': 1} |
| phosphoryl transfer | {'out_of_scope': 6} |
| phosphoryl transfer/phosphatase | {'out_of_scope': 1} |

## Guardrails

- Curated registry written: False.
- EC/name/prose used as predictive features: False.
- All new labels bronze / automation_curated; uniprot namespace; heldout benchmark unchanged.

## Next action

- Review per-lane diversity and the scope assignment. On explicit authorization, append `applied_labels` to the SEPARATE expansion registry `data/registries/external_bronze_labels.json` (the frozen current702 benchmark registry is never written). The combined total is frozen-benchmark + expansion. Held/skipped rows are the next batch: rerun the current702 duplicate screen for skipped rows and disambiguate the cofactor-confounded redox and secondary-probe radical-SAM/cobalamin lanes.
