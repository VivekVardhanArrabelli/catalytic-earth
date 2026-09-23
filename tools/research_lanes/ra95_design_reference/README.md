# RA95 native design reference

One bounded connection from Atlas evidence to an existing enzyme-design
consumer: run RFdiffusion2's author-provided RA95.5-8F / 5AN7 input with its
current public model configuration. This prepares an infrastructure control.
No protein has been generated or experimentally tested in this task.

The full computable Atlas and its de novo design purpose remain the mission.
This case checks a real consumer before building another adapter or expanding
sampling. It does not yet test an Atlas contribution: the native input already
contains all four residues and nine atoms supported by the current Atlas map.

## Pinned native input

Use RFdiffusion2 revision
`d365cbf4db3958814a9f8e4f6f94fa309dfebc2b`:

- [Public runtime configuration](https://github.com/RosettaCommons/RFdiffusion2/blob/d365cbf4db3958814a9f8e4f6f94fa309dfebc2b/rf_diffusion/benchmark/configs/open_source_demo.yaml):
  `aa`, `RFD_173.pt`, deterministic seed offset 43, one design, stop at `sweep`.
- [Author RA95 benchmark entry](https://github.com/RosettaCommons/RFdiffusion2/blob/d365cbf4db3958814a9f8e4f6f94fa309dfebc2b/rf_diffusion/benchmark/demo_enzymes.json):
  `retroaldolase`, ligand `LLK`, unindexed guideposts, 150-residue scaffold.
- [Exact author PDB](https://github.com/RosettaCommons/RFdiffusion2/blob/d365cbf4db3958814a9f8e4f6f94fa309dfebc2b/rf_diffusion/benchmark/input/ra_5an7_no_cov_ORI_cm1.pdb):
  SHA-256 `6dc747dbb1840892ed1f2f05e44d544a888db09336f4bb9df8b7732ace663682`.

| RA95 residue | Author identifier | Guidepost atoms |
| --- | --- | --- |
| Tyr51 | A1051 | OH, CZ |
| Lys83 | A1083 | NZ, CE |
| Asn110 | A1110 | OD1, CG, ND2 |
| Tyr180 | A1180 | OH, CZ |

This combination is a **new development reference**, not a reproduction of
the published RA95 experiment. The older `retroaldolase_demo.yaml` points to
a private `RFD_30.pt` checkpoint. No equivalence with that run is asserted.
The source checkout provides the original fixtures; this directory does not
duplicate them or download model weights.

The launcher replaces the configuration's `REPO_ROOT` checkpoint placeholder
with the absolute selected checkout path, preserving the model and settings.

## Chemical interpretation

[input_state.json](input_state.json) maps the author input onto the retained
Atlas evidence. The nine selected coordinates match the retained 5AN7 CIF.
The file selects Tyr51 alternative A (occupancy 0.75) and Lys83 alternative A
(0.57), with LLK occupancy 0.75; their joint physical state is unknown.

Despite `no_cov` in its name, the author PDB contains `CONECT 1462 4448`,
joining Lys83 NZ to LLK C13. Preserve it as an author input choice. The
deposited CIF lacks a corresponding typed LLK/Lys connection, while the
primary source describes attachment. Neither that omission nor PDB
connectivity settles bond order, protonation or the complete adduct graph.
The input is inhibitor-derived geometry, not an established transition state
or productive catalytic complex. See the existing
[chemical-state evidence](../../../docs/ATLAS_RA95_CHEMICAL_STATE.md) and
[perturbation controls](../../../docs/ATLAS_RA95_TETRAD_CONTROLS.md).

## Run on an existing GPU environment

Follow the pinned upstream [setup documentation](https://github.com/RosettaCommons/RFdiffusion2/blob/d365cbf4db3958814a9f8e4f6f94fa309dfebc2b/README.md)
on a suitable NVIDIA GPU host. The launcher requires the existing Apptainer
image and `RFD_173.pt`; it does not provision a host or download assets.
Use paths without whitespace, an existing output parent and a fresh output
directory name. The launcher binds the checkout and output parent into Apptainer.

```bash
export RFD2_ROOT=/absolute/path/to/RFdiffusion2
export RFD2_OUTDIR=/absolute/path/to/new-ra95-output
bash tools/research_lanes/ra95_design_reference/launch_ra95_reference.sh --print
bash tools/research_lanes/ra95_design_reference/launch_ra95_reference.sh --check
bash tools/research_lanes/ra95_design_reference/launch_ra95_reference.sh --execute
```

`--print` is the default and performs no execution. `--check` verifies source
and input identity, runtime assets and the native resolved pipeline settings.
It does not load the model or establish inference compatibility. `--execute`
repeats those checks and launches one design. Keep the output PDB, TRB,
configuration, logs and runtime asset identities together; model and container
file presence alone does not establish their integrity.

The initial result is whether this exact input can generate a 150-residue
backbone while retaining the requested motif and ligand mapping. It is not
catalytic activity or an unseen-mechanism prediction. Do not increase sample
count merely because the control runs.

## What would justify an Atlas comparison

Before another arm, identify one independently supported Atlas constraint that
changes a field or atom set actually consumed by the generator, and state what
output decision it could change. Hold runtime, seeds, length, sample count
and downstream filters fixed. Copying the same nine atoms into a new file, or
measuring their conditioned RMSD, cannot demonstrate added Atlas value.

No current RA95 field supports that extra constraint. Stop this proposed
efficacy comparison at the input audit; retain the native control for runtime
compatibility. Advancing the design mission next needs an evidence-supported
change to a design input, with a consequential test of that change.
