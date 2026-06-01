# Predicted-Geometry In-Distribution Atlas Retrieval

Run: 2026-06-01T01:08:29Z

Deployment-regime AlphaFoldDB retrieval for the current702 `in_distribution` fingerprint atlas rows. No labels, registries, thresholds, production scoring, or splits were changed.

## Counts

- Atlas rows expected: 184
- Rows selected for predicted-geometry coordinate swap: 171
- Retrieval rows emitted for atlas: 171
- Rows scored ok: 168
- Rows missing/unusable: 16
- Heldout predicted retrieval rows carried for direct gate reruns: 128
- Combined retrieval rows: 299

## Missingness

- insufficient_resolved_residues: 1
- missing_accession_compatible_sequence_positions: 13
- predicted_structure_fetch_failed: 2

## Atlas Top1 Fingerprints

- flavin_dehydrogenase_reductase: 16
- flavin_monooxygenase: 1
- heme_peroxidase_oxidase: 13
- metal_dependent_hydrolase: 98
- plp_dependent_enzyme: 4
- ser_his_acid_hydrolase: 36

## Output

- Artifact: `artifacts/v3_predicted_geometry_in_distribution_atlas_retrieval_current702_20260601.json`
- The top-level `results` array combines the new atlas rows with the previous heldout predicted-geometry retrieval rows so the existing `eval-mechanism-abstention-gate` loader can consume one path.
- The atlas-only rows are also preserved under `atlas_predicted_geometry_retrieval.results`.

## Next Method Unblocked

Run the predicted-geometry atlas-percentile gate:

```bash
PYTHONPATH=src python -m catalytic_earth.cli eval-mechanism-abstention-gate --geometry-retrieval artifacts/v3_predicted_geometry_in_distribution_atlas_retrieval_current702_20260601.json --out artifacts/v3_mechanism_abstention_gate_eval_predicted_atlas_current702_20260601.json --report work/mechanism_abstention_gate_eval_predicted_atlas_current702_20260601.md
```
