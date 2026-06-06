# Fold-Augmented Lever 3 Post-Bandpass P07658 Live Probe - current702

Run: 2026-06-04T21:18:00Z

This note records a no-staging live public-route refresh after accepting the
same-family bandpass counteraxis contract. It was a provenance/surface check
only: no coordinate was downloaded into the repo, no coordinate was staged, no
row was scored, and threshold 0.44155 was not changed.

## Probe Results

| route | P07658 result | control/contrast |
| --- | --- | --- |
| AlphaFold API `api/prediction/P07658` | HTTP 404, empty `{}` response | `P68698` returned one API model row from `ColabFold v1.5.2` with provider `VR3D` |
| AlphaFold direct CIF HEAD v6/v4 | HTTP 404 for both `AF-P07658-F1-model_v6.cif` and `AF-P07658-F1-model_v4.cif` | legacy `AF-P68698-F1-model_v6.cif` direct name is also 404 because current AFDB API exposes a model-specific ID |
| 3D-Beacons summary | HTTP 200 with P07658 sequence length 715 and PDBe experimental structures | no deployment-valid predicted structure row observed for P07658 |
| 3D-Beacons detail | HTTP 200 with 5 P07658 structure rows, all experimental-style PDBe mappings with null confidence values | `P68698` detail includes a predicted-style row with confidence values plus experimental rows |
| RCSB computed-model search | HTTP 204 with no returned rows for the P07658 UniProt accession plus computational-methodology query | no deployment-valid computed-model hit observed for P07658 |

## Decision

- The accepted counteraxis operating point remains usable for train/cal:
  31/34 calibration in-scope rows retained and 105/204 train/cal OOS rows
  abstained.
- P07658 remains the only deployment-closure evidence gap after the bandpass
  contract: an accepted exact full-length predicted coordinate plus provider,
  model, version, path, checksum, and U140 handling provenance is still missing.
- Do not rerun the fixed-threshold surface until the P07658 acceptance preflight
  passes.
