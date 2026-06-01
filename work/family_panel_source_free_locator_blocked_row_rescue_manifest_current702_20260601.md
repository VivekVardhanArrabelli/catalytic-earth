# Family Panel Source-Free Locator Blocked-Row Rescue Manifest - current702

Run: 2026-06-01T14:01:09Z

Review-only rescue manifest for source-free locator rows blocked because their selected local coordinates expose no non-water ligand or metal site. It records frozen source alternate-coordinate options and exact commands without fetching or scoring them.

## Status

- source_free_locator_blocked_row_rescue_manifest_ready_review_only
- Blocked rows: 2
- Rows with selected-coordinate only-water HETATMs: 2
- Rows with alternate source PDB IDs: 1
- Alternate PDB IDs total: 5
- Alternate fetch commands: 5
- Ready for predicted-geometry scoring: 0

## Row Plans

| row | accession | selected PDB | selected HETATM comps | alternate PDB IDs | status |
| --- | --- | --- | --- | --- | --- |
| mh_064 | uniprot:C7C422 | 3PG4 | {'HOH': 132} | 3RKJ, 3RKK, 3SBL, 3SFP, 3SPU | alternate_coordinate_fetch_manifested_review_only |
| secondary_probe::cobalamin_radical_rearrangement | uniprot:Q59490 | 1L1L | {'HOH': 2875} |  | no_frozen_source_alternate_pdb_ids_found |

## Commands

```bash
curl -L --fail https://files.rcsb.org/download/3RKJ.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_3RKJ.cif
```

```bash
curl -L --fail https://files.rcsb.org/download/3RKK.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_3RKK.cif
```

```bash
curl -L --fail https://files.rcsb.org/download/3SBL.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_3SBL.cif
```

```bash
curl -L --fail https://files.rcsb.org/download/3SFP.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_3SFP.cif
```

```bash
curl -L --fail https://files.rcsb.org/download/3SPU.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_3SPU.cif
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-family-panel-source-free-locator-blocked-row-rescue-manifest
```

## Interpretation

- 1/2 blocked locator rows have frozen source alternate PDB IDs; no coordinates were fetched.
- If manual approval allows bounded coordinate fetches, start with `mh_064` alternates and rerun candidate extraction; Q59490 needs a new source-free nonlabel locator strategy or an explicitly authorized alternate source row.
