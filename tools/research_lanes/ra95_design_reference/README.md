# RA95 native design reference

One bounded connection from Atlas evidence to an existing enzyme-design
consumer: run RFdiffusion2's author-provided RA95.5-8F / 5AN7 input with its
current public model configuration. One reference backbone was generated on
2026-09-23 and checked for input/output consistency. No experimental activity,
finished enzyme sequence or Atlas efficacy result is claimed.

The full computable Atlas and its de novo design purpose remain the mission.
This case checks a real consumer before expanding sampling. The initial run
used the author input, which already contains all four residues and nine atoms
supported by the current Atlas map; it did not derive that input from Atlas.

The subsequent [coordinate translation](atlas_input/README.md) now rebuilds
the nine guidepost and seventeen LLK heavy-atom coordinates/occupancies from
the verified Atlas deposit record into the author PDB template. It produces
exactly the same input bytes. Atom selection, connectivity and the remaining
PDB content still come from the author; this is a partial translation check,
not an independently generated chemical specification or an efficacy result.

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

The pinned consumer reads this `CONECT`: it becomes a symmetric single-bond
feature between Lys NZ and LLK C13 during atomization. The preserved run's
`indep_true.bond_feats[164,187]` and reverse entry are both 1; its deatomized
representation uses the corresponding residue-level edge. Thus an explicit
attachment would duplicate information already present in this control.
The single-bond feature is an implementation choice, not evidence resolving
the adduct bond order. No additional catalytic-protonation input was found.
See the pinned [consumer](https://github.com/RosettaCommons/RFdiffusion2/blob/d365cbf4db3958814a9f8e4f6f94fa309dfebc2b/rf_diffusion/aa_model.py)
and the original TRB in the unchanged run bundle.

## Observed reference run — 2026-09-23

The unchanged launcher passed `--check` and `--execute` on one NVIDIA A10
with Apptainer 1.5.4 and the official container (Python 3.11, PyTorch 2.4.0,
CUDA 12.4). One seed-43 design completed 100 flow-matching steps in 3.45
minutes; the complete execution, including output writing, ran from
04:19:55 to 04:24:13 UTC and exited zero. During this backbone stage, no
downstream sequence fitting, folding or activity evaluation ran. The temporary VM was terminated after
the complete output bundle was copied and verified.

- [Generated backbone](results/20260923/reference.pdb): 150 residues,
  comprising 146 alanine placeholders and the four supplied motif identities.
  Tyr51/Lys83/Asn110/Tyr180 map to generated A112/A78/A24/A118, respectively.
- [Output checks](results/20260923/checks.json): all nine requested motif
  atoms, 17 LLK heavy atoms, complete N/CA/C/O coverage and finite coordinates.
  After aligning the ligand, the nine motif atoms have 0.256 Å RMSD and
  0.738 Å maximum displacement from the input. These are conditioned-geometry
  and postprocessing measurements, not independent predictive evidence.
- [Complete run bundle](results/20260923/run-bundle.tgz): original PDB/TRB,
  trajectories, exact input, resolved inference configuration, execution logs,
  source/container/checkpoint identities and the one-off output inspection.
  All 32 manifest members were verified after transfer. Bundle SHA-256:
  `1bab79f7a2122ae6a1d44b164b60f65b5833920951b80006a2a3aaf0d68cfaf8`.

The native reference is executable. This completes the compatibility control;
the Atlas comparison below remains unsupported by a distinct input constraint.

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

This exact input generated a 150-residue backbone with the requested motif
and ligand mapping, at the scope reported above. It does not establish
catalytic activity or an unseen-mechanism prediction. Do not increase sample
count merely because the control runs.

## What would justify an Atlas comparison

To test whether extra Atlas information improves designs, identify one
independently supported constraint that changes a field or atom set actually
consumed by the generator, and state what output decision it could change.
Hold runtime, seeds, length, sample count
and downstream filters fixed. Copying the same nine atoms into a new file, or
measuring their conditioned RMSD, cannot demonstrate improved design performance.

Translation of established chemistry is a separate, legitimate Atlas purpose;
it does not require inventing a constraint absent from an author's input. The
case-specific rebuild above tests that narrower translation boundary. It does
not yet establish useful translation across cases or independent motif choice.

The [packing diagnosis](results/20260923-diagnostics/README.md) explains the
fixed-atom displacement: fixed torsions are reconstructed into idealized
Cartesian geometry. The [known-active parent control](parent_control/README.md)
is prepared for the next protein-only prediction. Its existing apo and
inhibitor-associated crystal models differ by 0.693 Å motif RMSD after a shared
241-atom C-alpha alignment; this observed-state comparison is not predictor
calibration or a design pass threshold.

No current RA95 field supports that extra constraint. Stop this proposed
efficacy comparison at the input audit. Atom-set ablations would test generator
sensitivity, and an invented ligand graph would introduce unsupported chemistry.

The [bounded continuation](CONTINUATION.md) has now executed: one ligand-aware
sequence/packing and one protein-only Chai invocation. [All five outputs](results/20260923-sequence-fold/README.md)
have complete 150-residue backbones, C-alpha RMSD 1.32–2.32 Å and motif RMSD
4.47–5.61 Å to the preserved reference. The Tyr112/Tyr118 OH distance changes
from 2.375 Å to 14.314–17.236 Å. The handoff works, but the intended internal
motif is not retained in these protein-only predictions. The packed MPNN output
also moves motif atoms (2.425 Å RMSD) despite unchanged C-alpha coordinates
and fixed residue identities. This does not establish ligand-bound failure,
activity or Atlas efficacy. Stop this attempt without
resampling. The VM is terminated; its $6.17 charge exceeded the $5/90-minute
limits because the process timeout did not terminate the paid instance.
