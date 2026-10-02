# Actual native RFD3 acceptance

The pinned public RFD3 loader and complete de novo input build now run against
the source-derived protease motif. This removed a real dependency between the
mechanistic input and a design consumer. No RFD3 checkpoint or inference ran in
this native acceptance check.

The original ten-residue candidate failed two checks:

- Native Zn formal charge was zero. The source notebook's later AF3 input uses
  `[Zn+2].O`; the original PDB did not encode that charge.
- Public range parsing consumed `A28-A30` as `A28`, leaving A29/A30 sequence-fixed.
  This is measured behavior of the pinned public parser, not evidence that the
  authors' internal wrapper had the same behavior.

The original input and failed read are preserved. A prospective, versioned input
uses standard PDB charge columns `2+` for Zn and range syntax `A28-30`. It extends
the substrate to the assay sequence `ALQSSWGMMGML` with M11/L12 initialized as
unfixed placeholders, and selects fixed gap lengths within the source ranges.
It is an adaptation for a new experiment, not a reconstruction of the authors'
exact generation command.

Both corrected inputs passed the actual native load/build checks:

| Property | Measured result |
| --- | --- |
| Polymer lengths | A187 enzyme, B12 substrate |
| Fixed catalytic identities | H36, E37, H40, Y115, E152 |
| Preserved source motif | 119 selected A atoms, all coordinates fixed |
| Reactive substrate coordinates | Exactly G7/M8 N, CA, C and O fixed |
| Substrate sequence | All 12 identities fixed |
| Metal and water | Zn +2, oxygen 0, disconnected, original `ZnO` name |
| Difference between arms | Only water O1 coordinate-fixed flag changes; the native free-mask operation clears only its coordinate |

The native loaded array contains the ordinary G7 C–M8 N single bond. The final
built array omits ordinary inter-residue polymer edges, while preserving chain
order and reactive backbone geometry. The downstream token-bond representation
also excludes polymer–polymer edges. This representation boundary is recorded;
it is not treated as evidence of a broken peptide or model defect.

The input source is the [retained author-derived motif](../design_input/README.md).
The consumer is official Foundry commit
`0932f1cb165ae7d413c11b1a7acc04ee31758817`, with the intact native
`DesignInputSpecification.safe_init` and `to_pipeline_input` methods. Source
identity, native versions, exact inputs and snapshots accompany this result.
The portable driver repeats the same checks without model weights; the pair
verifier requires the exact input hashes and chemistry/mask invariants.

Acceptance demonstrates faithful input transfer. It does not establish a new
functional enzyme, a benefit from Atlas, or a valid catalytic-activity filter.

The [complete immutable evidence bundle](native_evidence.tar.gz) includes the failed
and corrected reads, raw native snapshots, exact corrected inputs, runtime
receipts, executable verifier and reproduction commands. Its original manifest
and all 34 file hashes remain unchanged. Extract it into a scratch directory to
use the [reproduction instructions](reproduction.md). The
[next eight-candidate experiment](../water_conditioning/README.md) consumes the
accepted pair.
