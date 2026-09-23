# One sequence and a protein-only folding check

Prepared 2026-09-23; **not executed**. Continue the preserved reference once
through sequence design and a separate structure predictor. The question is
whether a designed sequence is predicted to recover this backbone and its
internal motif arrangement. This is a consumer-compatibility check, not a
catalytic-activity or Atlas-efficacy experiment.

The native motif already contains the supported Atlas atom map and covalent
connection. Repeating it as an Atlas arm would not test added information.
That closes this efficacy comparison, but it need not block qualification of
the existing downstream consumer. Do not build a generic compiler from this
one manually mapped case or expand backbone sampling.

## Fixed scope and inputs

- Reuse upstream revision `d365cbf4db3958814a9f8e4f6f94fa309dfebc2b` and the
  existing [150-residue backbone](results/20260923/reference.pdb), SHA-256
  `a08e12068a43923f0abd18de8f91c8a68f5b165cf63a36074675f6b597b0e84c`.
  Retain the original TRB and bundle alongside it; do not rerun diffusion.
- Generate **one** ligand-aware sequence, with one side-chain packing, seed
  43 and temperature 0.1. Fix A24 Asn, A78 Lys, A112 Tyr and A118 Tyr. These
  are final output positions, not the initial guidepost slots.
- Predict that sequence with **one** protein-only Chai invocation, seed 43,
  three trunk recycles and 200 diffusion steps. Retain all five native samples.
  Supply no ligand, template, motif coordinates or restraints to this step.
- Stop after this continuation. A failed interface, poor predicted fold or
  distorted motif is a result to retain, not permission to tune or resample.

## Why the folding input is protein-only

The pinned [scoring wrapper](https://github.com/RosettaCommons/RFdiffusion2/blob/d365cbf4db3958814a9f8e4f6f94fa309dfebc2b/rf_diffusion/benchmark/score_designs.py#L240)
passes `--allow_ccd_pdb_mismatch`. Its
[Chai input conversion](https://github.com/RosettaCommons/RFdiffusion2/blob/d365cbf4db3958814a9f8e4f6f94fa309dfebc2b/lib/chai/predict.py#L459)
converts a recognized LLK residue into a separate CCD component; it does not
transfer the protein-ligand connection. The retained Atlas evidence also lacks
a complete reacted graph and protonation assignment. This route cannot test
the covalent adduct faithfully. Do not use `stop_step=end` as an unqualified
continuation or interpret a separate-LLK prediction as adduct validation.

Protein-only prediction has a narrower interpretation: recovery of the
protein's fold and internal motif in the absence of the ligand. Failure would
not establish failure of the ligand-bound enzyme. LigandMPNN still receives
the unchanged ligand coordinates as geometric context; this does not resolve
their chemical-state limitations.

## Exact native commands for a prepared GPU host

Use fresh absolute paths without whitespace. `RFD2_ROOT` is the pinned source
checkout and `RA95_CONT` is a new output directory containing the unchanged
`reference.pdb`. Verify its hash and the four residue identities before
execution. The official `mlfold.sif`, `chai.sif` and two LigandMPNN checkpoints
must exist at the paths specified in upstream `setup.py`; hash them and retain
all fetched Chai/embedding asset identities. No RFD checkpoint or new
diffusion invocation is needed.

```bash
export PYTHONPATH="$RFD2_ROOT"
cd "$RFD2_ROOT"
apptainer exec --nv --bind "$RFD2_ROOT:$RFD2_ROOT" --bind "$RA95_CONT:$RA95_CONT" \
  rf_diffusion/exec/mlfold.sif python -s -u fused_mpnn/run.py \
  --pdb_path "$RA95_CONT/reference.pdb" \
  --fixed_residues "A24 A78 A112 A118" \
  --checkpoint_ligand_mpnn "$RFD2_ROOT/rf_diffusion/third_party_model_weights/ligand_mpnn/s25_r010_t300_p.pt" \
  --checkpoint_path_sc "$RFD2_ROOT/rf_diffusion/third_party_model_weights/ligand_mpnn/s_300756.pt" \
  --model_type ligand_mpnn --seed 43 --temperature 0.1 \
  --batch_size 1 --number_of_batches 1 \
  --ligand_mpnn_use_atom_context 1 --ligand_mpnn_use_side_chain_context 1 \
  --pack_side_chains 1 --number_of_packs_per_design 1 --repack_everything 0 \
  --omit_AA XC --force_hetatm 1 --out_folder "$RA95_CONT/ligmpnn"
```

The native FASTA includes the input sequence and the generated sequence.
Extract only the single generated `id=1` record. Require length 150, canonical
amino acids and N/K/Y/Y at positions 24/78/112/118. Save that sequence in
`$RA95_CONT/protein_only/design.fasta`, headed `>protein|ra95_design_1`.
Require that this directory contains exactly this one FASTA, then run:

```bash
apptainer exec --nv --bind "$RFD2_ROOT:$RFD2_ROOT" --bind "$RA95_CONT:$RA95_CONT" \
  rf_diffusion/exec/chai.sif python lib/chai/predict.py \
  --fasta_folder "$RA95_CONT/protein_only" --output_dir "$RA95_CONT/chai" \
  --log_dir "$RA95_CONT/chai_logs" --seed 43 \
  --num_trunk_recycles 3 --num_diffn_timesteps 200 \
  --structure_output pdb cif --export_arrays --export_seed
```

These arguments were checked against the pinned source, not executed in a
GPU runtime. The direct MPNN invocation exposes a fixed seed and bypasses
the pipeline's default eight-sequence expansion. The separate FASTA path
avoids the native PDB-to-CCD conversion. Preserve resolved arguments, stdout,
stderr and exit status; stop on an unexpected sequence/sample count or
unsupported runtime rather than silently changing the experiment.

## Report every output

Verify the input and generated-sequence hashes, sequence length and fixed
identities, one packed design and five Chai samples. For each prediction,
report complete backbone/finite coordinates, confidence as supplied by Chai,
global C-alpha RMSD to the preserved backbone after rigid alignment, and
the nine motif atoms' RMSD after that same alignment. Also report the internal
motif pair-distance differences; these separate local rearrangement from
global alignment. Keep missing atoms explicit. Do not select only the best
sample, turn these measurements into an unvalidated pass threshold, or call
the five correlated predictions five independent experiments.

This outcome can identify a broken handoff or a fold-compatibility problem.
Even favorable predictions cannot establish ligand-bound geometry, catalysis,
sequence novelty, compiler fidelity, or an Atlas benefit. Those require
their own evidence.

## Compute boundary

Proposed fresh rental cap: **$5 total**, including setup and failures; at most
90 minutes on one suitable GPU offered at no more than $2/hour, with no paid
fallback or automatic extension. Verify the live price and GPU compatibility
before provisioning. Preserve outputs and terminate the instance at completion
or the time/cost limit. The previous one-reference rental ended and its
authorization does not start this one.

Read-only HEAD checks on 2026-09-23 returned HTTP 200 for both containers and
both LigandMPNN weights: 14,716,790,810 bytes in total, before Chai's additional
model/embedding/cache downloads. No assets were downloaded in this preparation.
Use remote storage with at least 100 GiB free; the local checkout is below its
10 GiB reserve and must not hold these assets. The exact asset manifests and
GPU compatibility remain runtime checks; the $5 cap is a limit, not a promise
that setup or prediction will finish.
