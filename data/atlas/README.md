# Atlas proposal data

This directory is the proposal and release namespace for real atlas objects.
It is deliberately separate from `data/registries`, whose expansion latch
remains active after the P0 truth reset.

`atlas3_selection.json` is the frozen, machine-validated precompilation
contract for the first three biological kernel cases. The compiled Atlas-3
objects live under `data/atlas/atlas3/` and do not mutate the historical label
registries.

`atlas10_selection.json` freezes the seven-case follow-on that extends the
immutable Atlas-3 selection to ten cases. It adds source-gap, source-granularity,
structure-applicability, relationship-query, baseline, review, compute, and
assay-lane constraints before evidence compilation. Future Atlas-10 objects
will live under `data/atlas/atlas10/`; the selection does not claim those
objects are compiled yet.

Validate the selection with:

```bash
python scripts/validate_atlas3_selection.py
python scripts/validate_atlas10_selection.py
```
