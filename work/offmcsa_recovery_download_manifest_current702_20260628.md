# Off-M-CSA Recovery Download Manifest (sign-off)

Run: 2026-06-28T18:55:56Z
Status: `download_manifest_ready_awaiting_authorization`

## Plan

- Structures to download: **162** AlphaFold CIFs (~97.2 MB est.).
- Atlas families recoverable: flavin_dehydrogenase_reductase, heme_peroxidase_oxidase, metal_dependent_hydrolase, plp_dependent_enzyme, ser_his_acid_hydrolase.
- Family coverage of the sample:
  - flavin_dehydrogenase_reductase: 102
  - metal_dependent_hydrolase: 34
  - heme_peroxidase_oxidase: 20
  - plp_dependent_enzyme: 6
- Accession-list sha256: `1887478a1d37362e918f2841188347d4688273d0bc3c8b23931784a456ed36ea`.

## Selection Criteria

- High confidence; in-scope (not out_of_scope); fingerprint in an M-CSA atlas family; non-M-CSA accession; not already structured locally.

## Fetch Procedure (authorized step, not done here)

1. Confirm >= 10 GiB free (df -h .).
2. For each downloads[].alphafold_cif_url, fetch to a staging dir as afdb_{accession}_v4.cif (skip-if-exists; stop if disk would fall below the floor).
3. foldseek easy-search the staged positives vs the M-CSA train in-scope atlas (artifacts/v3_current57_fold_tm_recompute_current702_20260628_coordinates/train_in_scope_atlas) with the same flags as the calibration recompute.
4. Build the off-M-CSA positive map {rows:[{entry_id,accession,true_fingerprint_id}]} from downloads, then run build-fold-nn-mechanism-recovery-readout --positives <map> --foldseek-tsv <tsv> --surface-label offmcsa_bronze_high_confidence, and compare to the 28/35 (0.80) M-CSA baseline.

## Decision Needed

- Authorize the bounded AlphaFold download (no other gate); fetching is not performed by this manifest.

## Guardrails

- No download performed; fetch requires explicit authorization and >= 10 GiB free.
- Bronze labels are evaluation targets only (admission used sequence/cofactor, not structure, so fold-NN recovery is non-circular).
- No registry, ontology, or label change.
