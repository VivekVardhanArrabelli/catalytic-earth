# Fixed-sidechain context on one retained protease scaffold

This prospective comparison asks whether supplying fixed enzyme and substrate
sidechain geometry during LigandMPNN sequence design improves independent
recovery of the whole imposed catalytic arrangement. It uses the retained
`water_fixed_seed3` scaffold from the completed water-conditioning comparison.
That scaffold was selected after viewing the earlier results; this is a local
follow-up, not an independent generalization test or Atlas-efficacy comparison.

Four new sequence seeds (200–203) are paired across `atomize_side_chains=False`
and `True`, one sequence per condition. All 17 fixed residues, the full12mer
`ALQSSWGMMGML`, intended G7–M8 bond, scaffold, checkpoints, temperature and noise
are held fixed. No new backbone is generated. Each of eight sequences receives
five monomer and five complex RF3 predictions, with no coordinates, templates
or MSA. The native RNG seed is reset before each input and each single-input
prediction call; this does not guarantee atom-matched noise or bitwise GPU
identity across different sequences.

The [frozen decision](prospective_context_comparison.json) measures eight
chemical groups in one common frame after fitting all187 enzyme C-alpha atoms.
The per-output score is the largest group RMSD; the primary contrasts compare
candidate medians over all five complex outputs, using four paired sequence
seeds. Consistent benefit requires improvement in all four primary contrasts
and no worse per-group medians within any pair. All40 complex assignments are
required; all40 monomer assignments retain separate missingness and fold
context. No geometry cutoff is called an activity threshold. The source-derived
scaffold itself is not a validated productive structure.

## Native feature check

The actual installed native parser, pipeline, collator, mask and geometric
context methods passed both conditions without loading checkpoints or calling
a learned forward pass. Input features differ only in the specified switch;
coordinates, native chemistry, bonds and sequence masks match. False exposes
zero protein sidechain atoms; True exposes55 (25 catalytic-enzyme atoms and30
substrate atoms, excluding CB). Zinc and water remain present in the selected
context for all199 polymer residues in both conditions. Context has2–25 valid
atoms when revealed, compared with2 ligand atoms when hidden. Native fixed
residue sidechains are a combined intervention, not a Tyr-only perturbation.
The [local receipt](native_context_local.json) records exact source and scaffold
hashes; the portable checker repeats on the remote runtime before checkpoints.

Four arithmetic/accounting checks cover rigid transforms/reflections, equivalent
Glu oxygen permutations, all-assignment missingness and the no-regression guard.
The runner reuses the previous frozen native identity consumer and fixed RF3
settings; it permits no retries, replacements or additional samples. Cached
MACE descriptor absence remains a known possible runtime limitation and must
be reported from actual logs, not treated as equivalent prediction quality.

## Execution

The runtime package contains this folder and the unchanged sibling
`water_conditioning` consumer files. Bootstrap uses the official pinned
Foundry source and only the LigandMPNN and RF3 weights. The lead owns the
separate one-GPU, two-hour/$5 ceiling, retrieval and provider termination.

```sh
python run_context_comparison.py \
  --foundry-root "$CE_P8_RUNTIME/foundry" \
  --out-dir "$CE_P8_RUNTIME/experiment" \
  --checkpoint-dir "$CE_P8_RUNTIME/checkpoints" \
  --checkpoint-receipt "$CE_P8_RUNTIME/checkpoint_receipts.json" \
  --native-context-receipt "$CE_P8_RUNTIME/native_context_verified.json" \
  --max-seconds 5400 --execute
```

Without `--execute`, only all frozen assignments and source checks are written.
Output directories must be new. Measure using `measure_context_recovery.py`
with `--manifest`, `--decision`, `--reference-scaffold` and a new `--output`.
Keep every assigned output and the full per-group vectors. A mixed or incomplete
result does not authorize rescue sampling or establish equivalence.

Before sampling, single-A100 offers became unavailable. The operational plan
was amended to one48GB RTX6000Ada at the observed$0.75/hour within the same
bounds. No instance or model execution preceded that amendment. Both arms
share the actual recorded hardware; scientific assignments/readout are unchanged.
