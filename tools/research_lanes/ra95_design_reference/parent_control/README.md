# Known-active RA95 parent control

**Prepared; Chai has not run on this control.** The [FASTA](ra95_5_8f_parent.fasta)
contains the exact 258-residue RA95.5-8F sequence printed in Obexer 2017 SI
Figure S6a, including initial Met and terminal `LEHHHHHH`. Its sequence SHA-256
is `b842c993f9e9e3e80cffb546e6c8b5142541953e89b0bf4ddcfdfcb6aae0297b`.
The source reports activity for this parent; canonical sequence equality does
not prove identity of the assayed and crystallized physical preparations.

The control asks whether the same protein-only predictor can recover the known
parent's apo fold and internal motif geometry. Run one Chai invocation using the
same upstream revision, container/model assets, seed 43, three trunk recycles
and 200 diffusion steps as the [design continuation](../CONTINUATION.md).
Retain all five native outputs. Supply only the parent sequence.

On an already prepared GPU host, place only this FASTA in a fresh
`$RA95_PARENT/protein_only/` directory. The following is a prepared command,
not an execution record or rental authorization:

```bash
cd "$RFD2_ROOT"
apptainer exec --nv --bind "$RFD2_ROOT:$RFD2_ROOT" --bind "$RA95_PARENT:$RA95_PARENT" \
  rf_diffusion/exec/chai.sif python lib/chai/predict.py \
  --fasta_folder "$RA95_PARENT/protein_only" --output_dir "$RA95_PARENT/chai" \
  --log_dir "$RA95_PARENT/chai_logs" --seed 43 \
  --num_trunk_recycles 3 --num_diffn_timesteps 200 \
  --structure_output pdb cif --export_arrays --export_seed
```

Verify the pinned source and retained runtime asset hashes before executing;
retain the run's inputs, logs and every output. A new paid host also needs
provider-side termination that does not depend on the interactive session.
This command neither provisions nor terminates a host.

## Fixed comparison

The [manifest](manifest.json) records the source identity, residue mapping and
comparison plan. Predict all 258 residues, then align each prediction to the
**241 actual C-alpha positions in apo 5AOU**, labels `2–57,64–248`. Gly249 has
only nitrogen; it is not a 242nd C-alpha. Calculate the nine-atom motif RMSD
using that same global transform, plus all 36 internal pair-distance changes.
Report a separate 238-position core alignment excluding tag positions. Do not
use one global offset to convert 5AOU author residue numbers.

Compare deviations within each arm's own reference: parent to apo 5AOU, design
to its generated reference. The parent has 258 residues and the design 150;
this is a descriptive sanity control, not a matched activity experiment. There
is no selected winner or validated cutoff. Recovery of the known parent may
reflect predictor familiarity with its fold; training-set independence is not
established. Parent failure would weaken use of this protein-only setup as a
catalytic-geometry discriminator. Either outcome leaves activity untested.

The reference is a 100 K crystal at pH 4.6, with missing coordinates, ligands
other than the inhibitor and MHO237. Canonical Met in FASTA does not reproduce
that modification. The N-terminus/tag annotations and source/deposit conflicts
remain explicit in the linked source records.

## Observed-state comparison already executed

The [5AOU–5AN7 calculation](apo_complex_comparison.json) uses those 241 shared
C-alpha positions and explicit alternate selections. It gives 0.33793 Å global
C-alpha RMSD and **0.69334 Å motif RMSD** after the same alignment. Mean/max
absolute internal pair changes are 0.40741/1.18253 Å. Tyr51 OH–Tyr180 OH is
3.82710 Å in apo 5AOU and 2.72986 Å in the selected inhibitor-associated 5AN7
model. These are observed differences between selected crystal models, not a
solution ensemble, productive-state assignment, Chai calibration or a pass bar.

Rebuild the exact FASTA, manifest and structural comparison locally with NumPy:

```bash
python3 tools/research_lanes/ra95_design_reference/parent_control/materialize_parent.py \
  --repo "$PWD" --out-dir /absolute/path/to/control-preparation
```

This rebuild verifies both retained deposit packets and pinned source hashes.
It invokes no predictor and downloads no model assets.
