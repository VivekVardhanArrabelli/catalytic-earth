# Scale-Out Annotation-Anchored Bronze Import — drain batch (non-destructive)

Run: 2026-06-09T22:58:55Z

Drains the already-materialized import-ready pools through the same
conservative annotation-anchored engine. No new sourcing. EC/name/prose
stay in excluded_context (never predictive); structure/geometry
confirmation is a deferred bronze->silver promotion signal. The curated
current702 benchmark registry is NOT written by this run.

## Result

- Pool rows considered: 2426.
- **Importable bronze labels this batch: 1381** -> expansion registry 186 -> **1567** if merged.
- Label types: {'out_of_scope': 1139, 'seed_fingerprint': 242}.
- Positive fingerprints: {'flavin_dehydrogenase_reductase': 2, 'metal_dependent_hydrolase': 130, 'plp_dependent_enzyme': 110}.
- Confidence: {'medium': 1381}.
- Held for review: 1037 ({'primary_lane_without_cofactor_corroboration': 129, 'ambiguous_lane_review_required': 107, 'cofactor_confounded_redox_pool_held_for_disambiguation': 743, 'unmapped_lane': 58}).
- Skipped: 8.

## Per-pool decisions

| Pool | decisions |
| --- | --- |
| metal_phosphoryl_glycoside | {'import': 1006, 'hold': 43, 'skip_duplicate': 3} |
| near_orphan_diversity | {'import': 142, 'skip_duplicate': 5} |
| plp_radical_cobalamin | {'hold': 58, 'import': 110} |
| redox_cofactor_confounded | {'hold': 743} |
| wave2_skipped_duplicate_screen_rerun | {'hold': 193, 'import': 131} |

## Diversity by lane (label_type split)

| Lane | imported scope split |
| --- | --- |
| PLP aminotransferase | {'seed_fingerprint': 13} |
| PLP decarboxylase | {'seed_fingerprint': 21} |
| PLP lyase/eliminase | {'seed_fingerprint': 42} |
| PLP racemase/epimerase | {'seed_fingerprint': 16} |
| PLP sulfur lyase boundary | {'seed_fingerprint': 18} |
| carbon-carbon lyase/decarboxylase | {'out_of_scope': 12} |
| dehydratase/hydratase lyase | {'out_of_scope': 37} |
| flavin redox boundary | {'seed_fingerprint': 2} |
| glycoside/nucleoside | {'out_of_scope': 296} |
| isomerase/racemase/epimerase | {'out_of_scope': 30} |
| kinase/phosphotransferase | {'out_of_scope': 225} |
| metal hydrolase | {'seed_fingerprint': 129} |
| metal hydrolase Mg/Mn controls | {'seed_fingerprint': 1} |
| near-orphan/no-reliable-structure | {'out_of_scope': 1} |
| phosphoryl transfer | {'out_of_scope': 84} |
| phosphoryl transfer/phosphatase | {'out_of_scope': 396} |
| terpene synthase/lyase | {'out_of_scope': 49} |
| transferase tail outside current fingerprints | {'out_of_scope': 9} |

## Guardrails

- Curated registry written: False.
- EC/name/prose used as predictive features: False.
- current702 duplicate screen re-run against BOTH registries: True.
- Cofactor-confounded redox pool held: True.
- All new labels bronze / automation_curated; uniprot namespace; heldout benchmark unchanged.

## Next action

- On explicit authorization, append `applied_labels` to the SEPARATE expansion registry `data/registries/external_bronze_labels.json` via `apply-external-annotation-anchored-import` (the frozen current702 benchmark registry is never written; labels dedup against BOTH registries and validate through the label schema). The held cofactor-confounded redox and secondary-probe radical-SAM/cobalamin lanes await the cofactor/EC disambiguation task.
