# RA95 coordinate translation from Atlas

The nine guidepost atoms and seventeen LLK heavy atoms can now be rebuilt
from the source-checked Atlas 5AN7 deposit record into a real RFdiffusion2 PDB
input. The output is **byte-for-byte identical** to the author reference already
executed: SHA-256 `6dc747dbb1840892ed1f2f05e44d544a888db09336f4bb9df8b7732ace663682`.
There is no reason to repeat model inference on this identical input.

This is a small, case-specific translation check. Its dependencies are explicit:

| Input content | Origin |
| --- | --- |
| XYZ and occupancy of nine guidepost and seventeen LLK heavy atoms | Rebuilt Atlas 5AN7 projection, verified against its retained CIF and source-review pins |
| Which guidepost atoms and alternate conformers to select | Author reference choices; Tyr51 A and Lys83 A are selected explicitly |
| All remaining PDB content, including connectivity and hydrogens | Unchanged author template from the preserved reference bundle |
| Contigs, length, ligand and guidepost settings | Native interface, checked against the executed run configuration |

The builder does not read the sidecar's copied atom coordinates. It rebuilds
coordinates from the Atlas deposit packet. The checks also destroy the selected
template coordinates/occupancies and require Atlas to restore all 26 atoms; a
synthetic source-coordinate change must change exactly one output atom. Missing
or ambiguous atoms, wrong elements, nonfinite coordinates and a missing selected
alternate are rejected. See [checks.json](checks.json).

The Atlas does **not** yet independently choose the motif or provide a complete
protein–inhibitor graph. The author Lys NZ–LLK C13 `CONECT` remains unchanged;
this neither derives that edge from the CIF nor resolves its chemical bond
order. The selected alternates are not an established joint population. This
is inhibitor-associated coordinate transfer, not a productive catalytic-state
assignment, general compiler validation or an Atlas-efficacy result.

Reproduce locally, without model assets or a GPU:

```bash
python3 tools/research_lanes/ra95_design_reference/atlas_input/build_input.py \
  --output-dir /absolute/path/to/new-output-directory
python3 tools/research_lanes/ra95_design_reference/atlas_input/verify_derivation.py
```

The fresh output directory contains the rebuilt PDB, descriptive `interface.json`
and full atom-level provenance receipt. `interface.json` is an audit view, not a
new upstream launcher format. The scientific next step is the known-active
parent folding control, not another equivalent RFdiffusion2 input. Generalizing
this translation should wait for a second source-supported case that exposes a
real new requirement.
