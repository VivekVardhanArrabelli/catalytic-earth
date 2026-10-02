# Eight designs: no consistent water-conditioning advantage

All eight assigned scaffolds, eight sequences and 80 RF3 predictions completed.
The frozen primary result is **no consistent advantage**: fixing the source
water position reduced median recovery error in three paired design seeds and
increased it in one. All 40 complex and 40 monomer assignments are retained;
no replacements, rescues, score selection or exclusions were used.

| Paired design seed | Fixed-water median error (Å) | Free-water median error (Å) | Fixed minus free (Å) |
| --- | ---: | ---: | ---: |
| 0 | 1.348 | 0.552 | +0.796 |
| 1 | 1.755 | 1.868 | −0.114 |
| 2 | 2.954 | 4.707 | −1.753 |
| 3 | 0.393 | 2.079 | −1.686 |

The readout aligns Zn and two histidine atoms to the source frame, excluding
water from the fit. The four paired medians are the comparison units. The
all-four-sign decision rule tests directional consistency, not statistical
significance or a prespecified practical effect size. Five outputs share a
prediction trunk; they are not independent biological replicates. Fixed/free
scaffolds and their designed sequences can differ, so any downstream effect
would not isolate a direct catalytic-water mechanism.

## What changed scientifically

The new designs expose a broader recovery problem. Median enzyme C-alpha RMSD
to each designed scaffold is:

| Candidate | Complex prediction (Å) | Monomer prediction (Å) |
| --- | ---: | ---: |
| Fixed 0 | 12.916 | 15.211 |
| Free 0 | 9.991 | 10.603 |
| Fixed 1 | 12.440 | 14.596 |
| Free 1 | 2.617 | 6.307 |
| Fixed 2 | 15.591 | 16.902 |
| Free 2 | 18.235 | 18.970 |
| Fixed 3 | 1.425 | 1.789 |
| Free 3 | 3.413 | 3.482 |

Even the closest fold recovery, fixed seed 3, does not recover the full
catalytic arrangement. Its median water error is 0.393 Å and base–water
separation 2.849 Å, but Tyr115 OH–G7 O is 8.305 Å, compared with 2.574 Å in
the source-derived design motif; Zn–G7 O is 3.740 versus 2.101 Å. Across all
40 complex outputs, those distances span 3.850–23.741 Å and 3.308–22.273 Å,
respectively. G7 is the nearest peptide amide carbonyl to Zn in 10/40 outputs;
this is predicted register context, not observed cleavage specificity.

The [post hoc stage comparison](all_stages_geometry.csv) shows that all eight
scaffolds retain imposed non-water motif geometry, and LigandMPNN preserves
all 60 audited motif/reactive/ligand atom coordinates exactly. In fixed seed 3,
independent RF3 prediction moves both the tyrosine backbone and sidechain
relative to Zn. The stage difference cannot distinguish sequence incompatibility
from prediction error.
Low global fold RMSD and low water-position error therefore do not establish
recovery of the catalytic motif. These predictions do not prove the physical
proteins would misfold or be inactive.

The source motif contains cropped V6–N7–F8 coordinates; exactly eight backbone
coordinates from N7/F8 are inherited at the prospective target G7/M8. The
[source comparison](source_geometry.json) preserves those identities. It is
not an experimentally measured structure of this target. Free seed 2 also has
a median three-anchor fit residual of 5.116 Å; all its outputs remain in the
primary comparison. A small water error in a fitted local frame cannot stand
in for the full enzyme/substrate geometry.

## Decision

Close this finite water-only comparison without additional sampling. The next
consequential experiment is a [fixed-sidechain-context ablation](fixed_sidechain_context_proposal.json) during sequence
design on the retained fixed-seed-3 scaffold. The current native setting
`atomize_side_chains=False` hides protein sidechains from LigandMPNN's geometric
context even though their identities and saved coordinates are retained.
The pinned consumer supports revealing fixed-residue sidechains. Compare that
option with the unchanged baseline using matched prospective sequence seeds,
then evaluate the complete Tyr/base/metal/substrate arrangement and fold
recovery without coordinate conditioning in RF3.

This tests a specific possible translation gap and reuses a scaffold, rather
than generating more backbones. It is a hypothesis, not an established cause
or guaranteed repair. Enabling the option exposes both the five fixed enzyme
sidechains and fixed substrate sidechains; it would not isolate tyrosine alone.
The finite nearest-context selection also changes, potentially changing how
Zn/water atoms enter the sequence designer's context.
The scaffold was selected after seeing this run, so a future result would be
local to that selection, not an independent generalization test. Freeze the
new endpoint and assignments before execution; keep this experiment closed.

The author source already includes water. This result does not demonstrate an
Atlas design advantage, working protease, kinetic rate or Problem 8 solution.
Product-resolved, enzyme-normalized biochemical measurements remain necessary.
No new design run, wet work, outreach or order follows automatically.

## Runtime and retained evidence

The complete package was frozen at `71cdba8671edba384e90e730d41710581b70fae2`
before sampling and integrated in execution base `e881e3057fe3aaaddc11b7ba5a81d6b3857727f6`.
One RFD3 backbone and one public LigandMPNN sequence were produced per arm/seed.
Public LigandMPNN substitutes for the authors' EnhancedMPNN in both arms.
All eight designed sequences are distinct. Native gates preserved A187/B12,
H36/E37/H40/Y115/E152, Zn2+, neutral represented water and the exact substrate.
RF3 received sequence-only monomer or sequence/12mer/`[Zn+2].O` inputs, without
MSA, templates, coordinates or pose restraints.

Foundry was pinned at `0932f1cb165ae7d413c11b1a7acc04ee31758817`.
Checkpoint hashes, exact commands, native masks, installed versions and logs
are retained. Cached MACE descriptors were absent, using the same pinned
source/checkpoint and missing-feature path as the
[prior runtime audit](../../window_check/results_20261002/mace_warning_audit.json).
The common fallback does not establish equivalence to descriptor-present
predictions. Isolated peptide termini also differ from reporter/full-protein
context. MPNN structures contain unresolved terminal OXT placeholders and are
sequence-design outputs, not relaxed all-atom enzymes.

Inference ran from 18:31:01 to 18:43:17 UTC on 2026-10-02. The A100 was
provider-confirmed **TERMINATED** at 18:44:44 UTC, about 20 minutes after creation.
Estimated cost at $1.20/hour is $0.40; the final provider charge is unavailable.
The two-hour/$5 authorization was respected.

- [All 80 measurements](all_80_measurements.csv): every assignment, hash, fold agreement and native confidence; complex rows also carry all frozen geometry metrics and amide-register distances. Blank monomer geometry cells are inapplicable, not imputed zero.
- [Result summary](result_summary.json): all candidate medians, sequences, paired outcome, runtime, rental and verification receipts.
- [Post hoc analysis](posthoc_analysis.tar.gz): stage-localization calculations, source geometry, independent numerical audit and the next hypothesis. These do not alter the frozen primary. Source hashes and original scripts/paths are retained.
- [Raw bundle](result_bundle.tar.gz): 457 hashed files including all structures, additional native ranked copies, confidence files, complete manifests, native gates, frozen package, measurement output and logs. Ranked copies are not extra assignments. No weights or credentials are included.

Bundle SHA256: `1ed41a47f25e90a31291a22ea23230760c50daf5a037ea63366cf22ec64205ee`.
All 457 file hashes and all 80 assigned CIF hashes were verified after retrieval.
Local recomputation reproduced the decision and all 1,052 floating-point
readouts within 2.85e-14. A separate agent recomputed all 40 water errors from
raw coordinates with an independent SVD implementation; this is computational
cross-checking, not independent expert or experimental validation.

To reproduce, extract the bundle into a fresh directory and verify
`result_bundle_manifest.json`. Preserve the original manifest under
`runtime/experiment/`. In a separate manifest copy, replace the path prefix
`/home/ubuntu/ce-p8-20261002/` with the absolute extraction directory in path
values only. Run the bundled `package/measure_water_recovery.py` with that
manifest, bundled `prospective_water_constraint.json` and `source_motif.pdb`,
and a fresh output filename. The original remote measurement remains immutable.
