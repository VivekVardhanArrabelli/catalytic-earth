# Family Panel Source-Backed Sidecar Materialization - current702

Run: 2026-06-01T11:03:56Z

Review-only materialization and Foldseek/TM scoring of targeted source-backed family-panel rows against the frozen current702 in-distribution predicted atlas.

## Status

- source_backed_sidecars_fold_scored_review_only
- Targeted rows: 10
- Sidecars with coordinate hashes: 10
- Foldseek rows with hits: 10
- Remaining predicted-geometry blockers: 10
- Remaining predicted-fold blockers: 0
- Foldseek TSV parse status: parsed

## Row Scores

| rank | row | accession | selected structure | nearest atlas | atlas fingerprint | TM | remaining blockers |
| ---: | --- | --- | --- | --- | --- | ---: | --- |
| 1 | secondary_probe::cobalamin_radical_rearrangement | uniprot:Q59490 | 1L1L | m_csa:697 | flavin_dehydrogenase_reductase | 0.4655 | predicted_geometry_top1_score_missing |
| 2 | secondary_probe::radical_sam_enzyme | uniprot:A0A1M6T2I7 | 8VPO | m_csa:358 | plp_dependent_enzyme | 0.7039 | predicted_geometry_top1_score_missing |
| 3 | external_glycoside_panel | uniprot:Q6NSJ0 | 7QQF | m_csa:697 | flavin_dehydrogenase_reductase | 0.6259 | predicted_geometry_top1_score_missing |
| 4 | mh_073 | uniprot:P01112 | 121P | m_csa:535 | metal_dependent_hydrolase | 0.8022 | predicted_geometry_top1_score_missing |
| 5 | mh_064 | uniprot:C7C422 | 3PG4 | m_csa:16 | metal_dependent_hydrolase | 0.9222 | predicted_geometry_top1_score_missing |
| 6 | mh_065 | uniprot:Q79MP6 | 1DDK | m_csa:15 | metal_dependent_hydrolase | 0.9411 | predicted_geometry_top1_score_missing |
| 7 | mh_066 | uniprot:P52699 | 1DD6 | m_csa:15 | metal_dependent_hydrolase | 0.9445 | predicted_geometry_top1_score_missing |
| 8 | mh_067 | uniprot:P00918 | 12CA | m_csa:216 | metal_dependent_hydrolase | 1.004 | predicted_geometry_top1_score_missing |
| 9 | mh_068 | uniprot:P15289 | 1AUK | m_csa:158 | metal_dependent_hydrolase | 1.002 | predicted_geometry_top1_score_missing |
| 10 | mh_072 | uniprot:P0A6P9 | 1E9I | m_csa:300 | metal_dependent_hydrolase | 0.5936 | predicted_geometry_top1_score_missing |

## Blockers

- None for targeted coordinate hashing or Foldseek/TM parsing.

## Command

```bash
/private/tmp/catalytic-foldseek-env/bin/foldseek easy-search /private/tmp/catalytic-earth-family-panel-source-backed-afdb-queries /private/tmp/catalytic-earth-predicted-structure-fold-channel-current702/atlas_in_distribution artifacts/v3_family_panel_source_backed_sidecar_materialization_current702_20260601_foldseek.tsv /private/tmp/catalytic-earth-family-panel-source-backed-foldseek --format-output query,target,qtmscore,ttmscore,alntmscore,prob,bits --exhaustive-search 1 --alignment-type 1 --tmalign-fast 0 --exact-tmscore 1 --threads 4 -v 1
```

## Interpretation

- 10/10 source-backed rows now have real AFDB-vs-predicted-atlas Foldseek/TM scores.
- Rows without source-free predicted active-site geometry top1 scores remain outside the primary combined gate.
- Materialize source-free predicted-geometry sidecars for the remaining rows, then refresh the family-panel readout again without changing labels, thresholds, imports, or splits.
