# Fixed-bond input for the public design consumer

One source-derived RFD3 input now connects the intended `ALQSSWG/MMGML`
bond to the authors' starting catalytic motif and substrate constraints.
**The coordinates and configuration are prepared; native parsing and design
generation have not run.** This removes manual reconstruction of the starting
input, not the remaining chemical-compatibility or model-execution dependency.

The [input PDB](ALQSSWGMMG78.pdb) and
[public candidate configuration](tdp_G7_M8_public_candidate.json) are derived
from Anqi Chen's [author archive](https://zenodo.org/records/22654831).
The retained notebook is inert source material. Its example outputs use tau
windows; applying its documented routine to this TDP sequence is our
reconstruction, not a recovered exact command that generated TDPn3.

The template combines the source's 4QHP active site with its Zn45-derived
substrate/guide geometry. It is distinct from the final selected TDPn3 ES model.
The first listed contig and origin were selected before generation; no search
or optimization was performed. The [provenance](tdp_G7_M8_input_provenance.json)
maps chemical roles, atoms, source choices and transformations.

| Preserved constraint | Input representation |
| --- | --- |
| Zn ligands | A:H293, A:H297 and A:E316 |
| General base/acid | A:E294 |
| Oxyanion donor | A:Y377 |
| Reactive peptide bond | B:G7 carbonyl C to B:M8 N |
| Peptide identities | All ten residues fixed as `ALQSSWGMMG` |
| Peptide coordinates | Only G7/M8 N, CA, C and O fixed; 64 other atoms initialized at zero for diffusion |
| Zn and represented water | Original C1 `ZnO` component, ZN1 and O1 coordinates |

All 205 source A/C atom records are preserved except serial numbering. No OXT,
Zn–O covalent bond, new charge assignment or assay residues M11/L12 were added.
Zero coordinates are intentionally unfixed placeholders, not a predicted pose.

## Three windows, one absolute bond

The [source-defined mapping](window_bond_correspondence.json) resolves
`ALQSSWGMMG78`, `LQSSWGMMGM67` and `QSSWGMMGML56` to the same assay G7–M8
bond. The final two digits are explicitly local P1/P1-prime positions in the
notebook and separate author helpers. The windows move artificial termini;
they do not supply three independently targeted cleavage sites. The 65 cached
monomer groups are candidate proteins, not measured functional enzymes.

## Public interface boundary

The [pinned public Foundry source](https://github.com/RosettaCommons/foundry/tree/0932f1cb165ae7d413c11b1a7acc04ee31758817)
supports the wrapper and sequence/coordinate selections used here. Its de novo
path preserves fixed coordinates for unlisted A residues. An initial suspicion
that the peptide-only mask released the catalytic motif was rejected after
tracing defaults and the complete build path; no corrective mask was needed.
Partial diffusion follows a different path and was not evaluated.

The only configuration adaptation is ligand selection `ZO` to `C1`: the source
PDB calls the component `ZnO`, and the public selector accepts its chain/residue
identity. The [source-style configuration](tdp_G7_M8_author_dialect.json) remains
unchanged for comparison. This resolves a selector mismatch without renaming
the component or asserting that its chemical graph is valid.

Before generation, the actual native loader must establish metal/water
retention, chemical graph and charge interpretation, peptide connectivity and
conditioning masks. No native import or model ran locally: the necessary
structural packages and cached dependencies are absent. Do not treat a JSON
check as consumer acceptance. The source origin calculation also falls back
from residue 376 to Glu378; the saved point is retained as a placement choice,
not described as the Zn-donor plane.

## Reproduce the translation

Copy this directory to a scratch location and run `python3 materialize_tdp_input.py`
there. The script verifies both immutable source hashes and reproduces the PDB,
two configurations and provenance. It does not execute the author notebook,
install packages or launch a model. [Source identities](source_manifest.json)
retain immutable URLs, archive ranges and hashes. Author software is retained
under its [MIT license](AUTHOR_LICENSE); author data attribution remains in
the source manifest.

The next computational question is the
[fixed-enzyme 10-residue versus 12-residue comparison](../window_check/README.md).
It can challenge transfer of the shortened substrate geometry before fresh
design generation. Neither this input nor that proposed comparison establishes
Atlas advantage, a functioning new enzyme or Problem 8 success.
