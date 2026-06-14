# Silver Geometry Confirmation Audit

Run: 2026-06-14T17:09:54Z

Checks whether `silver_ready_pending_geometry_run` rows are actually runnable by
the separate geometry confirmation gate. This is non-destructive: it does not
run/fake geometry scoring, write the registry, or flip tiers.

## Result

- Silver-ready input rows: 260.
- Ready for geometry confirmation run: 0.
- Blocked before geometry confirmation: 260.
- Silver flips applied: 0.

## Blockers

| blocker | count |
| --- | ---: |
| insufficient_exact_active_site_residues | 20 |
| local_coordinate_sha_mismatch_holo_confirmation | 1 |
| missing_explicit_pdb_residue_mapping | 260 |
| missing_local_holo_coordinate_file | 256 |

## Policy

- Recorded holo PDB confirmation, a local holo coordinate file, and explicit
  PDB chain/residue mappings are required before geometry confirmation can
  run. UniProt sequence positions alone are not treated as PDB residue
  mappings.
- Silver tier changes remain a separate authorized apply step after the
  geometry gate passes.

## Next Action

- Backfill/materialize local holo PDB coordinates and explicit PDB residue mappings for the silver-ready rows, then run this audit again before any silver tier apply.
