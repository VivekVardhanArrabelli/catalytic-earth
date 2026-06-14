# PDB ID Backfill Scout — post registry sharding

Bounded live UniProt xref scout for external seed rows missing `structure_provenance.pdb_ids`. No registry was written.

## Counts

- Seed labels: 5638.
- Rows with registry PDB IDs: 1234.
- Rows missing registry PDB IDs: 4404.
- Sampled missing-PDB rows: 120.
- Sample rows with UniProt PDB xrefs: 0 (0.0).

## Sample hit rate by fingerprint

| fingerprint | sampled | UniProt PDB hits | sample hit fraction | total missing PDB rows | current registry PDB rows |
| --- | ---: | ---: | ---: | ---: | ---: |
| metal_dependent_hydrolase | 15 | 0 | 0.0 | 179 | 46 |
| metallopeptidase | 15 | 0 | 0.0 | 106 | 44 |
| metallophosphoesterase_nuclease | 15 | 0 | 0.0 | 90 | 60 |
| metallophosphomonoesterase | 15 | 0 | 0.0 | 88 | 62 |
| metal_racemase_epimerase_non_plp | 15 | 0 | 0.0 | 79 | 71 |
| glycoside_hydrolase | 15 | 0 | 0.0 | 128 | 22 |
| nad_p_dehydrogenase | 15 | 0 | 0.0 | 111 | 39 |
| cytochrome_p450_monooxygenase | 15 | 0 | 0.0 | 208 | 42 |

## Top missing-PDB families

| fingerprint | missing PDB seed rows | current registry PDB rows |
| --- | ---: | ---: |
| molybdopterin_oxidoreductase | 231 | 19 |
| cytochrome_p450_monooxygenase | 208 | 42 |
| coa_acyltransferase | 188 | 62 |
| non_heme_iron_2og_dioxygenase | 186 | 64 |
| glycosyltransferase | 182 | 68 |
| radical_sam_enzyme | 180 | 4 |
| metal_dependent_hydrolase | 179 | 46 |
| sam_methyltransferase | 164 | 86 |
| terpene_cyclase_synthase | 164 | 9 |
| flavin_dehydrogenase_reductase | 139 | 63 |
| glycoside_hydrolase | 128 | 22 |
| class_ii_metal_aldolase | 125 | 25 |
| thiamine_diphosphate_enzyme | 123 | 27 |
| copper_oxidoreductase | 122 | 18 |
| pfkb_ribokinase_family | 119 | 9 |
| cobalamin_radical_rearrangement | 116 | 4 |
| nad_p_dehydrogenase | 111 | 39 |
| plp_dependent_enzyme | 110 | 6 |
| metallopeptidase | 106 | 44 |
| atp_amide_ligase | 98 | 52 |

## Guardrails

- PDB IDs were fetched as UniProt cross-reference provenance only; they are not predictive features.
- No labels, tiers, review statuses, or frozen current702 rows were mutated.
- Next action is a gated external-registry-only writer plus holo confirmation rerun.
