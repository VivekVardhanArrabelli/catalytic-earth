# M0173 covalent-addition transformation: internal message board

Owner authorized continuing from merged PR #45. Starting main/origin-main:
`5d2bbb4002e1fb406df91ddafca3346ea42e4605`; its tree equals the four-job
CI-tested PR head `3727640e29a85e7d2ef529bec07168b2deb9f4cd`.
Branch: `codex/m0173-covalent-addition`.

## Objective

Make the retained trypsin Step-1 input to Step-2 tetrahedral intermediate
executable with the existing graph-edit engine. This extends the positive
chemical capability to enzyme–substrate covalent bond formation. It is a
source-depiction transformation; the generic peptide representation cannot
become a canonical exact peptide or physiological reaction instance.

Initial feasibility candidate: transfer Ser195's depicted proton to the
source-named histidine, form the serine O–substrate carbonyl C bond, change
the substrate C=O to C–O, and update the oxyanion/histidine charges. Inspect
source atoms, arrows, stereochemistry, wildcard groups and complete before/
after graphs before accepting this candidate. Shared panel IDs are locators,
not an upstream physical atom map.

## Ownership and coordination

- `source_ingestion`: retained-source feasibility, payload/source inventory
  and portable source extraction under `data/atlas/transformations/m0173/`.
- `state_contracts`: generalize `atlas_transformations.py` with a separately
  versioned source-only contract using the shared replay primitive. Avoid a
  copied validator or fabricated canonical correspondence.
- `draft_integration_review`: independent source inspection, decisive
  adversarial tests in `tests/core/test_atlas_m0173_transformations.py` and
  final exact-payload review.
- Root: direct source checks, this board, catalog/query/build integration,
  docs, integration tests, package verification and Git/CI publication.

Agents use the same model family. Their informed challenge reviews may have
correlated errors and are not independent human validation.

## Scope and stop rules

Use retained sources first; zero new source requests are authorized in the
initial implementation budget. A new acquisition needs an explicit internal
decision stating the evidence gap it would resolve, within the existing
owner-authorized public-source policy. No paid compute, outreach, experiments,
benchmark rescoring, protected registry writes or human-review status changes.

Preserve the original M0187 source/package bytes and Atlas-10 runtime result.
Package M0173 as a separate reviewed set. An opt-in catalog will expose both
sets with their separate review/source provenance. The M0187 command and
single-set output remain compatible.

If generic groups, atom omissions or unresolved graph correspondence prevent
the proposed replay, stop at the narrower supported scope rather than create
an exact instance. Do not extend to peptide cleavage, acyl-enzyme hydrolysis,
the full catalytic cycle or an unreviewed structure/sequence mapping.

## Feasibility and implementation decision

Root and both source/review agents independently checked the retained MRV.
Step 1 hash `61e6e50dce4e376699ebbf430c3190a0805efc0586d33f683e31b0f3c7263eab`
and Step 2 hash `7cc3b37af574d0bb078bd46059d6559729ee4bb633ec7190b273182af0497f88`
contain the same 50 node tokens and coordinates. The source snapshot remains
`d3db64e9a1db6e22e8baae48a738bff261a2296f375a884c19f2f4abc7d8f22e`.
Four bond changes and two charge changes take 42 bonds to 43 and merge the
substrate/serine components, reducing nine depicted components to eight.
The full-panel formal-charge sum remains -1.

The exact changes are removal of a44–a50; addition of a3–a44 and a21–a50;
a3–a10 double to single; a10 charge 0 to -1 and a21 charge 0 to +1.
The three Step-1 arrows o24/o25/o26 support these endpoints. The source names
the histidine His56A. Its sequence numbering remains a separate source
namespace, and no atom-level protein mapping is made here.

Both inputs contain two literal elementType=R pseudoatoms (a9, a11), eight
carbon tokens with alias R, and other residue-fragment aliases. Ser195 is
represented in disconnected source fragments. These are 50 depiction nodes,
not a resolved 50-atom physical molecule. Both panels have no bondStereo
tokens; a new absolute configuration is not assigned. Raw bond ID b42 and
flow IDs are reused across panels, so they cannot independently establish
continuity. Bind step numbers, graph endpoints and source bytes together.

State implements a separately versioned `source_panel_only` v2 record using
the same edit/replay and source-flow checking functions as v1. It preserves
all source labels, aliases and R-group tokens as unresolved context. It does
not manufacture a Rhea/canonical participant bridge or symmetry result.

Root adds separate package assets for M0173 and an explicit reviewed-set
registry. The original M0187 data/package and single-set query remain
compatible. `--mcsa-id M0173` retrieves the new set; `--all` returns a catalog
of independent results and their own review/source pins. The default command
continues to reproduce M0187.

Initial compatibility check: all 17 pre-existing transformation/query tests
pass after generalizing the shared validator. Root also caught Windows path
separators in the new portable audit before final pins; root corrected
them to repository-relative POSIX strings.


## Integration handoff and source challenge

After the initial agent turns stalled during initialization, root took ownership
of final source/payload assembly and all module fixes. The restarted reviewer
owns only the M0173 challenge test file and final scientific review. State's
follow-up reviews are read-only; the source agent's files are now root-owned.

The review found a concrete coordinated-mutation gap: a compiled Atlas10 arrow
and authored edit could be renamed together while contradicting the retained
MRV. Root corrected v2 repository validation to compare the full before-step
arrow projection directly with the raw MRV using the existing source adapter.
The raw scheme lookup now binds the mechanism as well as the step, and the
embedded UTF-8 content is rehashed. Tests reject the coordinated o25-to-o99
rewrite. Two remaining text reads now explicitly use UTF-8.

The standalone source audit reproduced byte-for-byte from only its script and
the retained M0173 snapshot in another checkout and working directory. Its
result SHA is `bd74f7cc8e12da55b1894e5647119ad19135b4a5477e92e99f63f300f11e561e`.
No new network acquisition or chemical toolkit was involved. The exact
payload awaiting final review is
`c2c836e790e80cd2bc3e101f8317997440b4d6b28eedb9f85161dab4ce742da6`.
The on-disk review pin remains unset until acceptance. All 25 source-contract
and prior transformation/query tests currently pass, including eight M0173
challenges. Catalog and installed-package tests follow package generation.


## Exact-payload acceptance

The reviewer accepted canonical payload
`c2c836e790e80cd2bc3e101f8317997440b4d6b28eedb9f85161dab4ce742da6`
after raw-source inspection and the coordinated-arrow falsification. Root
set that exact reviewed-payload pin manually and generated both packages.
The M0187 package bytes and reviewed payload remain unchanged. All 30
transformation, query and catalog tests pass, including M0173 package drift,
exact replay, offline query routing and separate catalog provenance.
This is an informed same-model review with potentially correlated errors;
it does not change human-review status or confer experimental validation.


## Validation and publication boundary

State's final read-only integration review found no blocker: default M0187
output remains exact, M0173 uses separate package files, and the catalog
preserves each reviewed set's provenance verbatim. Final local validation:

- 356 core/unit tests passed, with one optional dependency skip.
- Repository contracts passed against base
  `5d2bbb4002e1fb406df91ddafca3346ea42e4605` in partial-clone mode.
- Both ordinary and index-only report-archive checks passed.
- Fresh wheel queries and both graph replays passed from an empty directory
  with network connections blocked and RDKit absent.
- Atlas-10 remains 10 cases / 30 objects, runtime result
  `57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.
- Human review remains 0 submissions / 97 packets without submissions; frozen
  benchmark labels and historical release source were not changed.

The previous temporary build environment was absent; root recreated an
isolated build environment from the repository's locked requirements. This
was package tooling only, not scientific source acquisition or inference.
The branch will be pushed and merged only after all four Ubuntu/Windows,
Python 3.10/3.12 PR jobs pass. GitHub records the tested head and merge;
the root task verifies the merged tree equals that head and main is clean.
