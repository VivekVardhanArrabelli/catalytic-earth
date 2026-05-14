# Foldseek readiness note

Recorded: 2026-05-14T03:05:45Z

Status:

- `foldseek` was absent from the default `PATH`.
- Homebrew 5.1.11 is present, but `brew info foldseek` reported no available
  formula and `brew search foldseek` only returned `folderify`.
- Conda 25.1.1 is present. The default Conda cache path under
  `~/Library/Caches/conda-anaconda-tos` is not writable from this sandbox, so
  the direct Bioconda lookup failed with `CondaToSPermissionError`.
- Redirecting Conda home and package cache to `/private/tmp` allowed Bioconda
  lookup and an isolated install:
  `/private/tmp/catalytic-foldseek-env/bin/foldseek version` reports
  `10.941cd33`.

Current TM-score readiness:

- The 1,025 geometry artifact has 1,002 entries, 998 entries with selected PDB
  identifiers, and 963 `ok` geometry rows, but no `structure_path`,
  `mmcif_path`, `cif_path`, or similar coordinate-file fields.
- The 1,025 graph artifact has 22,440 structure nodes, including 21,399
  `pdb:` nodes and 1,041 `alphafold:` nodes, but no local coordinate paths.
- No `.pdb`, `.cif`, `.mmcif`, `.ent`, or `.bcif` files are currently checked
  into the repo.

TM-score split remains blocked on materializing selected PDB/AlphaFold
coordinate files and adding a Foldseek-backed split builder. The sequence
identity holdout is already the first real distance signal; the structural
signal should come next after coordinates are staged.
