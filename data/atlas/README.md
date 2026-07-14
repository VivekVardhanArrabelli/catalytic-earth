# Atlas proposal data

This directory is the proposal and release namespace for real atlas objects.
It is deliberately separate from `data/registries`, whose expansion latch
remains active after the P0 truth reset.

`atlas3_selection.json` is the frozen, machine-validated precompilation
contract for the first three biological kernel cases. The case identities,
authoritative handles, representation pressures, compute ceilings, stop
conditions, and provisional assay lane must be frozen before evidence is
compiled. Compiled Atlas-3 objects will live under `data/atlas/atlas3/` and
will not mutate the historical label registries.

Validate the selection with:

```bash
python scripts/validate_atlas3_selection.py
```
