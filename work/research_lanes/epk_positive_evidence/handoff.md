# ePK Positive Evidence Handoff

Last updated: 2026-05-20T16:05:14Z

## Current Outcome

Primary outcome: `evidence_against`.

This run exhausted a bounded explicit-acceptor/full-length substrate RCSB
surface and found 0 fresh clean folded-protein ePK positives. The scout
reviewed 177 unique PDB IDs across 14 full-text surfaces. It recovered only
repeat positive-like review rows (`1IR3`, `5HVK`, `6Z3R`, `9UUR`, and `9UUX`)
plus known or newly reinforced counterexample/mapping-risk rows (`2JJ2`,
`7B56`, `7ZE5`, and `9UW4`).

The strict `AMP-PNP` plus phosphoacceptor folded-substrate query returned 0
rows. The added full-length ATP/Mg wording returned 24 rows but no new
heteromeric source-review lead beyond known `5HVK`.

## Files

- `artifacts/research_lanes/epk_positive_evidence/rcsb_explicit_acceptor_folded_substrate_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/rcsb_explicit_acceptor_folded_substrate_source_review_20260520.json`
- `tools/research_lanes/epk_positive_evidence/epk_evidence_search.py`
- `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`

## Search Surfaces

- RCSB full text `protein kinase substrate protein phosphoacceptor AMP-PNP`: 0 rows.
- RCSB full text `protein kinase substrate protein phosphoacceptor ANP`: 2 rows.
- RCSB full text `protein kinase substrate protein phosphoacceptor ATP`: 20 rows.
- RCSB full text `serine threonine protein kinase substrate protein ANP magnesium`: 133 rows, exhausted through offsets.
- RCSB full text `kinase substrate residue AMP-PNP magnesium protein`: 6 rows.
- RCSB full text `protein kinase full-length substrate ANP magnesium`: 1 row.
- RCSB full text `protein kinase full-length substrate ATP magnesium`: 24 rows.
- RCSB full text `protein kinase full-length substrate AMP-PNP magnesium`: 0 rows.
- RCSB full text `full-length protein substrate kinase ANP`: 2 rows.
- RCSB tyrosine phosphoacceptor/residue control surfaces: 12 total rows.

## Decision Notes

The recovered positives are useful review-only regression anchors, not fresh
evidence. `5HVK`, `6Z3R`, `9UUR`, and `9UUX` remain the clean folded-protein
positive-like repeats; `1IR3` remains peptide evidence. `2JJ2` is non-ePK
ATP synthase context, `7ZE5` is CydDC transporter context, `7B56` remains
source-insufficient CaMKII-actinin proximity, and `9UW4` remains a MEK/ERK
mapping-disagreement/product-context risk rather than a clean positive.

Keep all outputs review-only. Do not score ePK, calibrate thresholds, import
labels, edit registries, or claim production readiness.

## Next Query

The explicit phosphoacceptor/full-length route is exhausted for this lane.
Next useful search should avoid broad text surfaces and instead target a
specific under-reviewed kinase-substrate family or paper set with direct
source mapping, for example a bounded RCSB/PubMed route for:

`"kinase-substrate complex" "full-length" "ATP" "phosphorylation site"`

Use the same pattern: query IDs first, scout gamma/analog geometry, then
source-review only heteromeric hits.
