# Silver Geometry Confirmation Audit

Run: 2026-06-14T17:34:44Z

Checks whether `silver_ready_pending_geometry_run` rows are actually runnable by
the separate geometry confirmation gate. This is non-destructive: it does not
run/fake geometry scoring, write the registry, or flip tiers.

## Result

- Silver-ready input rows: 260.
- Ready for geometry confirmation run: 86.
- Blocked before geometry confirmation: 174.
- Silver flips applied: 0.

## Blockers

| blocker | count |
| --- | ---: |
| insufficient_exact_active_site_residues | 20 |
| missing_explicit_pdb_residue_mapping | 172 |
| missing_local_holo_coordinate_file | 125 |

## Policy

- Recorded holo PDB confirmation, a local holo coordinate file, and explicit
  PDB chain/residue mappings are required before geometry confirmation can
  run. UniProt sequence positions alone are not treated as PDB residue
  mappings.
- Silver tier changes remain a separate authorized apply step after the
  geometry gate passes.

## Next Action

- Run the geometry confirmation gate on ready_rows and apply silver only to rows that pass.
