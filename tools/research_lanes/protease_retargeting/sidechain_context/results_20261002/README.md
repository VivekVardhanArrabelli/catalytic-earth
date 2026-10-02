# Fixed-sidechain context did not consistently improve recovery

All eight assigned sequence designs and all 80 RF3 predictions completed.
Revealing fixed catalytic and substrate sidechains during LigandMPNN sequence
design improved the primary joint-geometry score in one paired seed and
worsened it in three. The frozen result is
**no consistent joint reference-recovery advantage**. Do not adopt this switch
as an established repair or continue this comparison with rescue sampling.

| Sequence seed | Hidden median worst-group RMSD (Å) | Revealed median (Å) | Revealed minus hidden (Å) |
| --- | ---: | ---: | ---: |
| 200 | 18.351 | 13.696 | −4.655 |
| 201 | 12.734 | 21.043 | +8.309 |
| 202 | 3.676 | 13.160 | +9.484 |
| 203 | 4.724 | 19.660 | +14.937 |

The [prospective endpoint](../prospective_context_comparison.json) uses one
proper fit of all 187 enzyme C-alpha atoms, then scores eight chemical groups
in that common frame. Each output's score is the largest group RMSD; each
candidate's primary value is the median across all five complex predictions.
The four paired sequence seeds are the comparison units, not 40 independent
experiments. Consistent benefit requires all four improvements and no worsening
of any group median within a pair. Even seed 200's scalar improvement fails
the second condition: base and reactive-backbone errors increase by 0.227 and
0.236 Å. The numerical tolerance is not a biochemical activity threshold.

## Scientific consequence

The suspected omission was real, but exposing the missing context did not
repair recovery on this selected scaffold. Actual native feature checks show
that the option exposes 55 fixed sidechain atoms (25 enzyme, 30 substrate),
while both arms retain zinc and water in context for all 199 polymer residues.
The eight sequences are distinct. Fixed residue identities, chemistry and
coordinates were preserved through sequence design. This tests the combined
fixed-sidechain intervention, not an isolated Tyr115 interaction.

Revealed-context complex predictions have median enzyme C-alpha RMSDs of
9.166–14.617 Å to the retained scaffold. In seed 201, the tyrosine group improves
by 7.385 Å while the metal-binding glutamate group worsens by 19.687 Å. A better
individual interaction cannot stand in for recovery of the full arrangement.
Hidden seeds 202 and 203 recover the overall scaffold more closely (1.457 and
1.778 Å complex C-alpha RMSD), but their worst-group errors remain 3.676 and
4.724 Å. These are computational diagnostics, not proof of physical misfolding
or inactivity, nor a nomination for synthesis.

The reference is the imposed hybrid `water_fixed_seed3` scaffold, selected
post hoc from the previous experiment. Its source motif adapted cropped
V6–N7–F8 backbone coordinates to target G7/M8. It is not a measured productive
structure of this sequence and substrate. The result is local to this scaffold,
four sequence seeds, public LigandMPNN and the pinned prediction runtime.
It neither establishes equivalence nor refutes fixed-sidechain conditioning
in general. Both arms have the same source-derived mechanistic knowledge;
this is not an Atlas-versus-direct design comparison.

## Reassessing the prediction readout

We reused the already completed TDPn3 substrate-window outputs as retrospective
positive-only context; no additional predictions were generated. TDPn3's
published cleavage evidence is tied to exact constructs and intended G7–M8
product identities in the [source record](../../fixed_target_evidence.json).
It is not an isolated-peptide kinetic measurement by this project.

Using the same eight-role calculation with TDPn3's own residue numbering and
its own author-selected AF3 complex reference, the two seed medians are
0.646/0.797 Å for the 10mer and 2.864/2.672 Å for the 12mer. The 12mer discrepancy
is mainly water displacement; global enzyme C-alpha medians remain
0.368/0.380 Å and general-base group errors 0.519/0.461 Å. Thus imperfect
predicted water geometry also occurs for a construct with published activity.
This does not establish that the predictor can distinguish active from inactive
enzymes. The selected AF3 reference differs from our imposed RFD3 scaffold;
these scores must not rank activity across the two scaffolds or define a
post hoc activity threshold. The full calculation and source identities are
in [positive-control context](tdpn3_positive_reference_calibration.json).

The next consequential dependency is an exact sequence- and assay-matched
inactive control that retains the catalytic atoms scored by this endpoint.
The retained source calls TDPn3's control a general-base knockout but does not
identify its substitution. Do not invent E147A; even a confirmed E147A would
remove scored Glu atoms. Treating those missing atoms as a bad geometric score
would be tautological, not predictor discrimination. Such a knockout would
require a separately justified, prospectively frozen endpoint applicable to
both constructs. The reported 113-design screen was not enzyme-normalized,
so its weak signals cannot supply matched inactive labels automatically.

Resolve this control dependency from primary construct and assay records under
the remaining source budget; stop if comparable identities and measurements
cannot be established. No suitable matched negative is currently established.
Until then, stop optimizing designs against an unvalidated activity proxy.
Additional water or sidechain seeds would not resolve this dependency, and
the completed positive-only reanalysis must not be relabeled validation.

## Execution and evidence

Scientific assignments, endpoint and source pins were committed before sampling
at `dddd4e8c77bdc186ad1d56c97d8477eb9ccc861c`. A100 offers vanished before creation;
the operational substitution to one RTX6000Ada was committed at
`14119cfdb1a54168d5bd5c1a341ea9a9fc0749cd`, also before sampling. Both arms used
that hardware, the same checkpoints and one retained scaffold; no new backbone,
retry, replacement, exclusion, template, MSA or coordinate-conditioned RF3
prediction was introduced. The native RNG was reset before each input and
single-input prediction call. This does not guarantee atom-matched noise or
bitwise GPU determinism across differing sequences.

Inference ran from 19:59:55 to 20:06:50 UTC on 2026-10-02. All 40 complex and
40 monomer outputs were measured. After verified retrieval, the provider
confirmed **TERMINATED** at 20:07:41 UTC. Estimated cost is $0.20 at $0.75/hour;
the final provider charge is unavailable. The one-instance, two-hour/$5 bound
was respected, and no paid resource remains from this experiment.

Cached MACE descriptors were absent in the pinned RF3 runtime. Both arms
share that missing-feature path; this does not establish descriptor-present
prediction quality. Public LigandMPNN differs from the authors' EnhancedMPNN.
The isolated 12mer termini differ from reporter/full-protein context. Saved
MPNN coordinates are not relaxed structures. No rate, reaction barrier,
cleavage specificity, measured physical fold or biological function is claimed.

- [All 80 assignments and measurements](all_80_measurements.csv), including all eight group errors, fold agreement, confidence, contact geometry and peptide-register context. Blank monomer geometry fields are inapplicable.
- [Result summary](result_summary.json), with paired outcomes, sequence identities, runtime, rental and verification receipts.
- [Raw bundle](result_bundle.tar.gz), with 431 hashed files: every assigned structure, additional native ranked copies, confidence files, input manifests, context/RNG receipts, frozen package and complete logs. Ranked copies are not extra assigned samples. No checkpoints or credentials are included.
- [Independent checks and retrospective analysis](posthoc_analysis.tar.gz). These checks do not change the frozen primary and are not independent expert or experimental validation.

Bundle SHA256: `5f0b505a18ac95b9a2e50800cf09286f44c2eee1f05eda65146f59b62e66172b`.
All 431 archived file hashes and 80 assigned structure hashes were verified.
Local recomputation reproduced all 1,548 floating-point readouts within
2.85e-14 and the exact decision. A separate implementation independently
recomputed all 320 group RMSDs, 40 per-output maxima, eight candidate medians
and four paired differences, agreeing within 2.49e-14 Å. Native identity checks
also verified all 80 outputs, 16 RNG receipts and 398 matched context rows.

To reproduce, extract the bundle and verify `result_bundle_manifest.json`.
Preserve the original remote manifest. In a separate manifest copy, replace
`/home/ubuntu/ce-sc-20261002/` with the absolute extraction-directory prefix
in path values only. Run bundled `package/sidechain_context/measure_context_recovery.py`
with that manifest, bundled decision and scaffold, and a new output path.
The unchanged sibling `water_conditioning` files supply the shared parser.
