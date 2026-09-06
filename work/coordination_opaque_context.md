# Opaque source-context extraction board

Base: `911b16b60fb52f10bc794065753a9c320ad3c5f2` (PR #48), 2026-09-06.

## Objective

Preserve raw stereochemical and coordinate-bond annotations while extracting
only supported covalent-bond/formal-charge changes. First prove the retained
M0219 mechanism 1 Step 2→3 regression, then evaluate the same 101 adjacent pairs.
Existing v1 extractor, scan and reviewed evidence bytes remain unchanged.

## Owners and messages

| Owner | Bounded responsibility |
| --- | --- |
| Root | Shared contract, CLI/scan integration, documentation, checks and publication |
| state_contracts | New `atlas_context_candidates.py` only |
| draft_integration_review | Independent new context-extraction tests only |
| source_ingestion | Direct raw-XML audit, format documentation and retained-source inventory |

Root and state agreed to reuse the frozen extractor on a private parser view:
capture original ordered annotation rows, exclude only captured convention bonds
and stereo markup from that view, then delegate mapping/edit/replay work.
Public source bindings refer to original bytes. The output must distinguish
covalent-graph replay from the unreplayed electronic/stereochemical state.

Every supported special endpoint must be mapped. Atom parity remains unsupported. Ordered raw context
must be unchanged under that map and disjoint from every proposed edit endpoint.
Changed, reversed, duplicate, unmatched, unsupported or interacting context
returns `needs_review` with no edits. No donor/acceptor, CIP, metal-state,
physical-identity, canonical-participant or experimental inference is made.

The raw-source agent independently checks M0219's expected 75-node map, twelve
edits, four stereo rows and two coordinate bonds. The reviewer challenges
metadata loss, projection provenance, ordering and fail-closed behavior.

## Acceptance

First pass the M0219 baseline and decisive adversarial tests. Then scan all
retained pairs, separately report newly supported candidates, and independently
audit every new success. Preserve the old scan byte-for-byte. Run core tests,
repository contracts and offline installed-wheel checks; merge after green CI.
Reviews are informed same-model agent checks and can share errors.

## Results

The first baseline passed: M0219 mechanism 1 Step 2→3 aligns all 75 nodes,
derives twelve graph-confirmed edits, and retains four W/H stereo rows and two
coordinate bonds. Its Step 4→5 also fully replays a 71-node covalent graph.

Independent challenge corrected orphan/global stereo capture, duplicate or
overlapping bond rows, self-loop convention bonds, and vacuous edit-disjointness
claims after failed base extraction. Special references must also have no
covalent crossing bond into unmatched context: direct source checks found
M0222 Step 9→10 adds an unmatched hydrogen at a stereo-marked endpoint, while
M0753 Step 5→6 redraws an unmatched neighbor at such an endpoint. Both stop.

The all-pair scan returns twelve candidates: five retained baseline candidates
and seven newly supported candidates. Eighty-nine pairs need review. Two prior
M0222 candidates (1→2 and 3→4) are withheld because the broader check detects
molecule-level `absStereo=true`, which this version does not support. The frozen
v1 extractor and scan remain byte-identical; the new mode is not a superset.

New successes: M0106 3→4, 7→8, 8→9; M0212 13→14, 15→16; M0219 2→3, 4→5 (all
mechanism 1). Only the two M0219 additions replay complete covalent graphs.
Every successful result remains unreviewed and retains source identity and
applicability limits. No benchmark, tier, participant or experimental promotion.

The reviewer reports thirteen focused tests passing, including renamed IDs,
original byte bindings, context mismatch/order, unsupported forms, both concrete
projection holes and M0222 withholding. State independently verified scanner
pair completeness, provenance hashes and the retained/new/withheld partitions.
The independent direct-XML audit confirmed all seven new mappings, exact edit
support tuples, ordered context and absence of special-boundary/arrow overlap.
It retains M0106 Step 8's inferred status and M0212 Step 15's unarrowed omitted
H `a83` / bond `a33–a83`. All charge changes also change raw lone-pair annotations;
complete electronic-state replay remains unclaimed. Audit SHA256:
`489c392e7bbfe24406b2ef49f747290481e09ce639c387fa7052a27163784adb`.
Machine trace SHA256:
`6694fcd190faa58e1e07375a6933bd7cd5dbbf0860e04276210ac6e20b700f12`.

Final local checks passed: 403 core tests, 15 focused/integration tests, repository
contracts, exact new and frozen-v1 scan reproduction, and fresh-wheel source
queries plus M0173/M0219 extraction with network blocked and RDKit absent.
Atlas-10 retains runtime hash
`57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.
Historical release manifest and all reviewed assets remain unchanged.
Publication is gated on the four-job CI matrix.
