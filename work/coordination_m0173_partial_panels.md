# M0173 partial-panel comparison: internal message board

Base main/origin-main: `34425197141f3a58549c49ad65f08652dc638a7e` (merged PR #46).
Branch: `codex/m0173-partial-panels`. Owner authorized proceeding with the
next partial-panel capability. No scientific source acquisition, inference,
paid compute, outreach, benchmark rescoring or human-review promotion.

## Objective and ownership

Make a useful comparison of M0173 mechanism 1 Step 2 input and Step 3 input
without manufacturing the omitted released peptide. Keep the existing two
full transformation sets and their exact package bytes unchanged.

- Source agent: independently derive raw mapping, inventories and deltas;
  then own new `data/atlas/panel_comparisons/m0173/` artifacts once assigned.
- State agent: only new `src/catalytic_earth/atlas_partial_panels.py`, a
  generic partial-coverage validator using existing graph/edit primitives.
- Review agent: independent source challenge, only
  `tests/core/test_atlas_partial_panels.py`, and final exact-payload review.
- Root: raw counter-checks, shared schema, query/CLI/build/release integration,
  integration tests, this board, documentation and Git/CI publication.

Reviews are informed same-model agent reviews; errors may be correlated.

## Source findings

Step 2 has 50 nodes and 43 covalent bonds; Step 3 has 42 nodes and 35 bonds.
Exact source coordinates plus identity annotations uniquely align 40 nodes.
Local IDs are renumbered after a3; identity mapping is not valid. Before-node
unmatched set: a4..a9, a12..a14, a50. After-node unmatched set: a6,a7.
The released fragment and transferred proton are omitted; water is redrawn
from explicit H-O-H to H-O. No unique water-H correspondence is established.
The full formal-charge sum changes -1 to 0 because the omitted fragment
contains a carboxylate. The retained 40-node core is net 0 in both panels.

The six source-arrow-supported proposed edits are peptide C3-N4 cleavage,
N4-H50 formation, His N21-H50 removal, His N21 +1 to 0, C3-O10 single to
double, and O10 -1 to 0. Only the last three changes have both endpoints in
the matched core and can be checked against the after graph. The two before
bonds crossing between mapped and unmatched nodes must remain explicit.
No unmatched node is interpreted as a chemically deleted or created atom.

## Contract agreed before implementation

A separate `catalytic-earth.partial-panel-comparisons.v1` artifact contains
comparison_set_id, status, source_bindings, comparisons and manual review.
Each comparison binds the existing record, proposal and state-pair shapes;
complete before/after graphs; complete source node metadata; an exact unique
position-and-identity correspondence; all proposed edits and bound source
flows; derived coverage; explicit scope effects and mandatory abstentions.

Metadata preserves each node's atom_id, x2, y2, isotope, mrv_extra_label,
mrv_alias and rgroup_ref. Matching uses element and all these identity/position
fields, excludes changing formal charge, and requires uniqueness in both
directions. The declared map must equal all such unique source matches;
cherry-picked subsets and arbitrary water-H matches are rejected.

All proposed edit preconditions are checked on the complete before graph.
Only edits whose endpoints are all mapped execute on the projected graph.
The existing replay primitive checks that projection against the matched
after graph. Coverage derives full/matched/unmatched inventories, both
crossing-edge sets, replayed versus unverified edit IDs and per-arrow coverage.
The full graphs remain intact; no synthesized full after graph is published.
Repository validation rederives full graphs, metadata, hashes and ordered
arrows from the bound raw MRV mechanism and step.

Scope permits retained-projection replay only. Complete-panel replay, canonical
participant identity, physical atom mapping, atom creation/deletion from panel
omissions, after-graph confirmation of unverified edits, stereochemical
assignment, full mechanisms and experimental observations remain unasserted.

The new offline `atlas-panel-comparisons --mcsa-id M0173` command exposes these
partial comparisons with comparison counts. Existing `atlas-transformations`
outputs and counts remain unchanged. No cross-step composition is asserted.

## Implementation and challenge findings

The standard-library source audit imports the pinned earlier XML extractor
rather than copying it. The three required inputs (new audit, old extractor,
retained M0173 snapshot) reproduced the retained audit byte-for-byte in a
fresh tree from an unrelated working directory. Audit result SHA:
`999ae8f92de3a1ccc4195ce54f81167677d59ba8ccce1d4739a2bfec7c03e6f6`.
No source requests were needed. The previous transformation files are unchanged.

Root caught two contract issues before acceptance. First, raw MRV bond order
in the file and endpoint ordering must not reject the canonical undirected
edge representation; validation now compares exact edge-to-order maps while
preserving complete source node order. Second, dropping an unverified edit
could make declared arrow coverage look more complete. Validation now requires
every before-panel arrow in source order and exact coverage of its endpoint
nodes by the associated edits. Coordinated removal of the protonation edit
or the whole cleavage arrow fails. Claimed coverage also uses canonical JSON
comparison so boolean and numeric values cannot substitute for each other.

The new module is generic and calls the existing graph-edit/replay primitives.
The source fixture preserves all 50/42 nodes and all metadata. Only e4/e5/e6
replay; e1/e2/e3 remain after-graph-unverified. Per-arrow status is coverage of
the declared proposed edits, not proof of exhaustive chemical interpretation.
State's integration review found no blocker. The 30 existing transformation
and catalog tests and 11 new adversarial tests pass before package generation.

Precision correction before review: ten before nodes lack correspondence;
seven peptide/proton nodes are omitted and three water nodes are redrawn.
They must not collectively be called ten physically omitted atoms.
Pending candidate canonical payload:
`3ecc68c8c15627171c2b1276f33c7e6d9cf15042b2098755ae661da7637f2e6b`.

## Exact-payload acceptance

The reviewer accepted canonical payload
`3ecc68c8c15627171c2b1276f33c7e6d9cf15042b2098755ae661da7637f2e6b`
after raw-source review, all 11 adversarial tests, and the coordinated arrow
omission challenges. The accepted review block is now pinned; source/package
file SHA is `b3c85b645acd1cbcdbd211be55de0f25c9a54d5b3ca778fad678063db504d0d0`.
Module reviewed SHA:
`aa5d8374a63152f36b369c8c58113a2c75510be114be8ee66f2b70df2dd54c1d`.
The package builds with repository-source validation. All 17 new comparison
and query tests pass, including exact existing-package preservation and
package/attribution tampering. Root separately confirmed boolean/integer
coverage substitutions are rejected. Scientific scope is unchanged by review.


## Final local verification and publication boundary

- 373 core/unit tests passed, with one optional dependency skip.
- Repository contracts passed against base
  `34425197141f3a58549c49ad65f08652dc638a7e` in partial-clone mode.
- The current wheel installed and queried from an empty directory with
  network connections blocked and RDKit absent. Derived partial coverage
  matched the reviewed payload and both prior full transformations replayed.
- Atlas-10 remains 10 cases / 30 objects, runtime result
  `57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.
- Human review remains 0 submissions / 97 packets without submissions;
  benchmark labels and historical release source are unchanged.
- Reviewer and root reconciled final source/package file hashes: both are
  `b3c85b645acd1cbcdbd211be55de0f25c9a54d5b3ca778fad678063db504d0d0`,
  and expected.json binds those exact bytes. An earlier agent-reported file
  hash was stale; the approved canonical payload did not change.

The branch is ready for PR publication. Merge is conditional on all four
Ubuntu/Windows, Python 3.10/3.12 jobs passing. The root task will verify that
merged main has the exact tested tree and a clean working directory. GitHub
records the tested head and merge identity; this board does not predeclare
remote CI or merge completion.
