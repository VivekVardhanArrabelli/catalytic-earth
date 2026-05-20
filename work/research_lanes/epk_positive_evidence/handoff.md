# ePK Positive Evidence Handoff

Last updated: 2026-05-20T15:04:30Z

## Current Outcome

Primary outcome: `evidence_for`.

This run found clean review-only peptide positive evidence, including two
CDK2/Cyclin A transition-state mimic structures (`3QHR`, `3QHW`) with
ADP/MG/MGF and source-mapped CDK2 substrate peptide Thr acceptors. It also
found ATP/MG or ACP/MG peptide evidence for `1QMZ`, `3X2U`, `3X2V`, `3X2W`,
and `4IAC`.

No new non-peptide folded-protein substrate positive was found. The broader
folded/protein search surface returned only known positive repeat `5HVK` as a
heteromeric source-free geometry hit.

## Files

- `artifacts/research_lanes/epk_positive_evidence/rcsb_positive_evidence_source_review_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/rcsb_fulltext_kinase_substrate_peptide_atp_mg_all39_scout_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/rcsb_fulltext_kinase_substrate_peptide_atp_mg_all39_source_validation_builtin_20260520.json`
- `artifacts/research_lanes/epk_positive_evidence/rcsb_fulltext_kinase_substrate_protein_atp_mg_46_scout_20260520.json`

## Search Surfaces

- RCSB full text `"protein kinase" "substrate peptide" ATP magnesium`: 39 rows reviewed, 12 heteromeric geometry hits. Manual review accepts CDK2 and PKA peptide rows as review-only positives and rejects proteasome ATPase substrate-processing false positives.
- RCSB full text `"protein kinase" "protein substrate" ATP magnesium`: 16 rows reviewed, no fresh folded-protein ePK positive; the hits were the same PKA peptide rows.
- RCSB full text `protein kinase transition state mimic substrate MGF`: 2 rows reviewed, `3QHR` and `3QHW`; both are accepted review-only peptide transition-state evidence.
- RCSB full text `protein kinase substrate peptide MGF`: 10 rows reviewed; only `3QHR` and `3QHW` are ePK transition-state evidence, while the other eight rows are GDP/MgF3 GTPase contexts.
- RCSB full text `"kinase-substrate" protein ATP Mg`: 46 rows reviewed; only known positive repeat `5HVK` hit the heteromeric geometry rule.
- RCSB full text `phosphoacceptor protein kinase substrate`: 21 rows reviewed; no heteromeric gamma geometry hits. PAK4/Paktide rows are source-relevant but not gamma-transfer measurement-ready under the atom-level check.
- RCSB full text `"protein kinase" "substrate" "AMP-PNP" "protein"`: 67 rows reviewed; recovered known positives `1O6K`, `1O6L`, and `4EKK`, plus known counterexamples `4HPU` and `7ZE5`. No fresh folded-protein positive was added.

## Decision Notes

The strongest new positive evidence is peptide evidence, not production-ready
general protein-substrate evidence. The CDK2 transition-state structures are
especially useful for review because the source maps the peptide sequence
`PKTPKKAKKL` and the Thr acceptor, while MGF provides an equivalent
gamma-transfer analog state.

Keep all outputs review-only. Do not score ePK, calibrate thresholds, import
labels, edit registries, or claim production readiness.

Run record: `artifacts/research_lanes/epk_positive_evidence/epk_positive_evidence_runs.jsonl`

## Next Query

Target a non-peptide folded-protein substrate co-complex query with explicit
acceptor wording, for example:

`"protein kinase" "substrate protein" phosphoacceptor "AMP-PNP"`

Use the same bounded pattern: RCSB query IDs first, scout heteromeric
gamma/analog geometry, then source-review only the hits.
