# RA95 known-active parent control — 2026-09-23

One protein-only Chai invocation on the exact 258-residue RA95.5-8F parent
completed and retained all five native outputs. The predictions recover the
apo reference's overall fold reasonably closely, but appreciably rearrange
its catalytic motif: global C-alpha RMSD is **0.827–1.170 Å**, whereas the
nine-atom motif RMSD is **2.413–2.877 Å** under the same alignment.

This changes the interpretation of the earlier design result. The known-active
parent also has substantial predicted local deviations, so motif distortion
alone cannot establish catalytic inactivity. The design's larger deviations
remain a structural warning within this setup. This single exposed control
provides neither an activity classifier nor a calibrated rejection threshold.
Close this RA95 sampling attempt; more seeds or a rescued input would answer
a different question.

## Every prediction

All five PDB/CIF/score sets are present. Each PDB contains the exact parent
sequence, residues A1–A258, complete finite backbone coordinates and all nine
selected motif atoms. No sample is selected as a winner. These are five
correlated outputs from one
invocation, not five independent experiments.

| Native index | Global CA RMSD (Å) | Core CA RMSD (Å) | Motif RMSD (Å) | Mean pair change (Å) | Max pair change (Å) | Tyr51 OH–Tyr180 OH (Å) | Chai `ptm` | Chai `complex_plddt` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.170 | 1.161 | 2.413 | 1.388 | 4.968 | 5.740 | 0.9213 | 0.8847 |
| 1 | 0.836 | 0.827 | 2.877 | 1.783 | 6.080 | 7.325 | 0.9235 | 0.8866 |
| 2 | 0.900 | 0.895 | 2.500 | 1.463 | 5.225 | 6.339 | 0.9222 | 0.8857 |
| 3 | 0.972 | 0.966 | 2.746 | 1.736 | 5.764 | 7.033 | 0.9231 | 0.8855 |
| 4 | 0.827 | 0.819 | 2.754 | 1.686 | 5.658 | 6.899 | 0.9230 | 0.8868 |

Pair-change columns are absolute differences across all 36 internal pairs.
[checks.json](checks.json) retains every pair, native confidence fields, array
shapes, exact residue mapping, input hashes and complete output inventory.
The raw confidence arrays remain unchanged inside the bundle. Confidence
scores are supplied by the model and are not probabilities of catalysis.
The largest internal change in every sample is Asn110 ND2–Tyr180 OH:
3.364 Å in the reference versus 8.333–9.444 Å in the predictions.

The frozen comparison aligns the 241 actual C-alpha positions in apo 5AOU
(labels 2–57 and 64–248). The motif is Tyr51 OH/CZ, Lys83 NZ/CE, Asn110
OD1/CG/ND2 and Tyr180 OH/CZ. Its RMSD uses that global transform; it is not
separately fitted. The secondary core alignment uses 238 positions through
245. Internal pair distances do not depend on alignment. Reference selection
and sequence/structure caveats are fixed in the
[parent preparation](../../parent_control/README.md).

The Tyr51 OH–Tyr180 OH distance is **3.827 Å** in apo 5AOU and
**5.740–7.325 Å** in these predictions. For context, the precomputed comparison
of apo and inhibitor-associated crystals has 0.693 Å motif RMSD and mean/max internal
pair changes of 0.407/1.183 Å. That observed-state comparison is not a
solution ensemble or a pass threshold.

The earlier [150-residue design](../20260923-sequence-fold/README.md) has
4.466–5.611 Å motif RMSD against its generated reference and Tyr OH distances
of 14.314–17.236 Å versus 2.375 Å in that reference. These are descriptive
within-arm deviations, not a matched activity experiment. Length, scaffold,
reference state and compiled export size differ. Parent training familiarity
is unknown. The parent reference is a 100 K, pH 4.6 crystal with incomplete
coverage and MHO237, while the input uses canonical Met. Source-reported
activity does not prove identity of the assayed and crystallized preparations.
Neither this control nor the design predictions measure enzyme activity,
validate ligand-bound chemistry or demonstrate incremental Atlas benefit.

## Execution and reproduction

- Exact parent FASTA SHA-256:
  `cbba0f396a63b32b7d12189a203f2ec39be62ea99c83afad7ec4a6133c0fe1d5`.
- Unmodified RFdiffusion2 revision:
  `d365cbf4db3958814a9f8e4f6f94fa309dfebc2b`.
- One Chai invocation, seed 43, three trunk recycles, `num_diffn_timesteps=200`
  (the native progress log reports 199 transitions);
  **18:00:14–18:02:35 UTC**, exit zero. No ligand, template, motif coordinates
  or restraints were supplied.
- A100-SXM4 40 GB, driver 570.148.08, Apptainer 1.5.4,
  PyTorch 2.3.1+cu121. The full parent selected the **384-token exports**;
  the earlier design selected 256. All five new export hashes were recorded
  and rechecked before inference. Container, conformer and seven-file ESM
  payload hashes match the earlier run.
- The first launcher stopped during preflight because its expected sequence
  hash literal omitted two characters. The actual FASTA file hash passed;
  no model ran. Correcting that literal changed no input or prediction
  setting. Original script, failed logs, launch receipt and correction are
  preserved under `logs/preflight-1-*` and `logs/preflight-correction.json`.

The [bundle](parent-control-bundle.tgz) is **3,284,473 bytes**, SHA-256
`a569a805a365b0a423cbf10b59cee222fe701de3c0393aaa5dac58d6cc55c26a`.
All 39 payload hashes and the 40-member archive were verified after transfer.
It contains the input, all predictions and scores, logs, executed scripts,
source/GPU identity and asset inventories. Large model/container bytes remain
upstream and are identified by their hashes.

Expand the bundle into a fresh directory, then run the supplied inspector
with Python and NumPy:

```bash
python3 tools/research_lanes/ra95_design_reference/results/20260923-parent-control/inspect_parent.py \
  --repo "$PWD" --prediction-dir /absolute/path/to/bundle/output/chai \
  --output /absolute/path/to/checks.json
```

The published `checks.json` uses `bundle/` paths for extracted predictions.
`--self-test` instead checks the reference against itself and rejects an
intentional residue-number shift. The native score reader was also checked
against an actual score file from the preceding design run.

After verified retrieval, Prime confirmed GPU termination at **18:04:54 UTC**
and no active GPU instances. A separate cloud CPU watchdog had been armed
before provisioning, with a 19:06 UTC API termination deadline independent
of this interactive session. It observed the GPU disappear and exited zero;
the CPU sandbox was then deleted at 18:06 UTC. The deadline was a hosted
watchdog, not a native expiry setting on the GPU. Provider history displayed
**$0.75** for the GPU and approximately **$0.03** for the watchdog. Full timing,
limits and the billing observation are in [execution.json](execution.json).
