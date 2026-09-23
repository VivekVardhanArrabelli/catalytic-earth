# RA95 sequence and protein-only fold continuation — 2026-09-23

The prepared handoff executed successfully: one LigandMPNN sequence and one
side-chain packing, followed by one Chai invocation with five native samples.
The sequence-based predictions approximately recover the scaffold backbone,
but all five substantially rearrange the specified catalytic atoms. This
demonstrates execution of this sequence/folding handoff; it does not establish
preservation of catalytic constraints, a functional catalyst or an Atlas
contribution to design.

## Every prediction

All five PDB/CIF/score sets are present. Each PDB contains the same 150-residue
sequence, complete N/CA/C/O coverage, finite coordinates and all nine motif
atoms. The fixed positions remain A24 Asn, A78 Lys, A112 Tyr and A118 Tyr.
No prediction was discarded, ranked as a winner or assigned a post hoc pass
threshold. These are five correlated samples from one invocation.

| Native index | C-alpha RMSD (Å) | Motif RMSD (Å) | Mean absolute pair change (Å) | Max absolute pair change (Å) | Tyr112 OH–Tyr118 OH (Å) | Chai `ptm` | Chai `complex_plddt` |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.406 | 4.963 | 4.116 | 13.708 | 16.083 | 0.7486 | 0.8443 |
| 1 | 2.318 | 4.466 | 3.295 | 11.939 | 14.314 | 0.7369 | 0.8365 |
| 2 | 1.320 | 5.384 | 4.881 | 13.888 | 16.263 | 0.7453 | 0.8429 |
| 3 | 2.092 | 5.611 | 4.686 | 13.110 | 15.486 | 0.7444 | 0.8394 |
| 4 | 1.681 | 5.518 | 5.300 | 14.861 | 17.236 | 0.7503 | 0.8426 |

RMSDs compare with the unchanged generated reference: a least-squares rigid
alignment of all 150 C-alpha atoms, followed by the same transform for the
nine motif atoms. The motif is A112 OH/CZ, A78 NZ/CE, A24 OD1/CG/ND2 and A118
OH/CZ. All 36 internal atom-pair differences are also retained in
[checks.json](checks.json); these distances do not depend on alignment.

The Tyr112 OH–Tyr118 OH distance is 2.375 Å in the supplied reference and
14.314–17.236 Å in the predictions. This is the largest pair-distance change
in every sample. Consequently, global backbone similarity and model confidence
do not establish retention of the intended local catalytic arrangement.
The confidence columns retain upstream field names and native values; they
are model scores, not measured accuracy or probabilities of catalysis.

A post-run inspection also found geometry loss at the packing stage: its
C-alpha coordinates are unchanged, but the nine motif atoms have 2.425 Å RMSD
and a maximum internal pair-distance change of 4.097 Å. Residue identities
were fixed successfully; their original atom coordinates were not preserved
exactly despite `--repack_everything 0`. These intermediate-output measurements
are reported separately in `checks.json`. Chai consumed only FASTA, so this
packing displacement was not passed to the predictor as coordinates.

Chai received only [the designed sequence](design.fasta), with no ligand,
template, motif coordinates or restraints. These results therefore do not
establish failure of a ligand-bound enzyme. They also do not establish
activity, sequence novelty, compiler fidelity or incremental Atlas efficacy.
The existing chemistry record does not supply a complete reacted adduct graph
and protonation assignment, so a guessed ligand-bound rerun is not justified.
Stop this one-continuation attempt here; do not expand sampling to seek a hit.

## Execution and reproducibility

- Preserved reference SHA-256:
  `a08e12068a43923f0abd18de8f91c8a68f5b165cf63a36074675f6b597b0e84c`.
- Designed sequence SHA-256 (150 letters, no newline):
  `cca888eda0ad18a829b9eedb138d9182b76567db759d0c731f369cbb18d6a2b6`.
- Unmodified upstream revision:
  `d365cbf4db3958814a9f8e4f6f94fa309dfebc2b`.
- LigandMPNN: seed 43, temperature 0.1, one sequence/packing; completed
  11:05:25–11:05:42 UTC. The packed structure in the bundle
  (`output/ligmpnn/packed/reference_packed_1_1.pdb`) has the same sequence
  and fixed identities.
- Chai: seed 43, three trunk recycles, 200 diffusion timesteps; the one
  invocation ran 11:05:42–11:13:30 UTC, including its asset downloads, and
  exited zero. All five native output indices are retained.
- Hardware: one A100-SXM4 40 GB, driver 570.148.08, Apptainer 1.5.4.
  The official containers reported PyTorch 1.9.0 for LigandMPNN and
  2.3.1+cu121 for Chai; both detected the GPU.

The [complete bundle](continuation-bundle.tgz) is 6,225,291 bytes, SHA-256
`3ccf8b5f7ea3673fffc8058bf49f119c0f059588682fe5e49499e4138482f097`.
All 40 payload files and the 41-member archive were verified after transfer.
It includes every prediction, raw score/confidence array, input FASTA/PDB,
MPNN outputs, logs, executed scripts, source/GPU identity, downloaded-asset
hashes and the unchanged original backbone/TRB bundle. Model/container bytes
remain upstream; their identities and the resolved ESM revision are retained.

[inspect_continuation.py](inspect_continuation.py) recomputes the descriptive
audit from an expanded bundle using Python and NumPy. Pass `--reference`,
`--mpnn-fasta`, `--packed-pdb`, `--chai-dir` and `--output`. The committed
`checks.json` omits the large score arrays and uses archive-relative paths;
the original arrays remain unchanged inside the bundle.

## Rental-limit failure

The approved cap was $5 and 90 minutes. **The actual charge was $6.17**, and
Prime's history records creation at 10:47 UTC and termination at 14:00 UTC.
Both limits were exceeded. The model process finished at 11:13:30 UTC, but
the next observed clock after an 11:12 UTC check was 13:57:57 UTC. The cause
of this observation gap is not established. The remote timeout bounded the
model process, not the paid VM lifetime; it was an inadequate cost safeguard.

All outputs were copied and verified before termination. Prime then showed
successful termination, no running instances, and the $6.17 final bill.
[execution.json](execution.json) records the overrun. Before another paid
rental, verify provider-side termination independent of the interactive
session. Neither a process timeout nor host shutdown proves billing has ended.
