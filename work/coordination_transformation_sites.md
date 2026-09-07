# Transformation atoms and protein sites

## Objective — 2026-09-07

Connect an existing executable source transformation to its exact catalytic
residue, protein and structure evidence. Choose the first case by the evidence
available, then expose the supported correspondence through the offline atlas.
This closes a missing scientific link; it does not add a new performance claim.

Baseline: `f674297c7d488ba5ce9fba455d40f4feb7964986` on clean `main`.
Work branch: `codex/transformation-site-evidence`.

## Assignments

- Root: integration, case selection, source-budget authority, release checks,
  documentation and this coordination board.
- source_ingestion: M0173 source-atom/residue/protein/structure evidence audit.
- progress_evidence_audit: independent M0187 evidence audit and applicability
  challenge.
- state_contracts: smallest reusable additive contract and existing-code reuse.

Initial audits are read-only and reuse retained sources. No external messages,
paid services, model inference jobs or laboratory work are authorized by this
development step. Any necessary public-primary-source acquisition will be
bounded and recorded before execution.

## Required distinctions

- A source drawing node is a depiction locator, not a PDB atom identifier.
- An alias, source residue assertion, sequence mapping and deposited coordinate
  witness each establish only their stated relationship.
- Protein and structure evidence must belong to the exact mechanism proposal;
  an entry-level link alone cannot establish proposal applicability.
- Deposition of a catalytic atom does not establish that the illustrated
  intermediate was observed or that a catalytic trajectory is validated.
- Original transformation objects, review pins, Atlas-3/10 objects and protected
  benchmark registries remain unchanged. New scientific review is additive and
  does not become independent human review.

## Progress

The retained Atlas-10 records already supply sequence and coordinate-checked
sites. The missing edge is the relationship from an edited depiction node to
one of those sites. Implement an additive pure query over the existing frozen
records; a new manually maintained evidence catalog is unnecessary.

M0173 Step 1 explicitly labels a44 as `res:Ser195A` and a21 as `res:His56A`
in the bound electron-flow endpoints. The same step declares P35049:S204 and
P35049:H65 as catalysts. Their existing direct 1PQ5 chain A mappings are author
195 / label 180 and author 56 / label 41, respectively. Preserve the pH-5,
static-structure and protonation limitations.

M0187 is an informative negative: a58 and a63 have no residue label on their
compiled flow endpoints, and only H297 occurs in the Step-1 catalyst list.
Do not infer an atom/site correspondence from nearby aliases, chemical roles
or component connectivity in this change. Unlabeled changed nodes remain
explicitly unresolved.

Implementation ownership: state_contracts owns only
`src/catalytic_earth/atlas_transformation_sites.py`; root owns CLI, documentation,
integration and release checks. Source agents remain read-only.

## Source challenge and decisions

The M0173 audit checked the raw MRV labels, source residue rows, UniProt natural
sequence and retained 1PQ5 mmCIF. The coordinate file's protein-reference and
polymer-residue records corroborate chain A / P35049 and the distinct author
and label positions. This establishes residue/site context only; the presence
of OG, ND1 and NE2 in the deposit does not explicitly map a drawing node to a
named physical atom.

The source has two Ser195 role rows with identical residue mappings: one
main-chain nitrogen spectator row and one catalytic-role row. Existing combined
site roles remain residue-level context. They must not all become roles of the
edited oxygen a44. The separate Ser alias fragments a42 and a49 are not merged.
His56 is the correct retained author numbering and must not become His57.

The M0187 challenge independently confirmed that aliases a52=His297A and
a59=Glu317A are elsewhere in the corresponding connected fragments. Neither
the accepted free-text replay scope nor those aliases is an explicit per-atom
site edge. Keep a58/a63 unresolved. The existing 1MNS structure remains a
chemically modified, inhibitor-bound context, not a turnover observation.

No source acquisition was needed. All review roles use related computational
models and may share errors; this is source challenge and software review, not
independent domain-expert validation.

draft_integration_review owns the new adversarial API test module. Root owns
CLI tests, including an altered-package residue-number rejection. The CLI checks
the full Atlas-10 kernel against its original packaged hash before resolving
sites. The generic API checks relationships in its supplied inputs and reports
their provenance; no original source or transformation review pin is refreshed.

## Integration review

The reviewer reproduced a false join after altering only the copied Tier-2
before-step witness. The query now requires the exact transformation-bound
record and Tier-2 context to agree on the proposal, step, source evidence, sites,
structures, biological scope and provenance. A matching step ID or declared
source hash alone is insufficient.

Raw flow references retain their molecule-qualified source IDs. The molecule
prefix comes from the MRV molecule, not the M-CSA mechanism number; no such
namespace is guessed. Missing qualification is invalid, and different molecule
references sharing a local atom token remain ambiguous. Conflicting labels and
repeated direct PDB author locators cannot produce a resolved link.

The returned Atlas-10 provenance hash uses the existing kernel convention:
`27c2f16477911db206f1ff67cfc4c54aa150877e59dc31a7c1ff32dcca4a049e`.
The derived query has two transformation matches, twelve changed source nodes,
two resolved residue links and ten unresolved nodes. These are correspondence
coverage counts, not experimental or predictive performance measurements.

Reviewer disposition: no remaining material blocker. The nine adversarial API
tests and four CLI integration tests pass. The implementation is frozen at
SHA-256 `b2335061459f4455443b181a396015333fbcf3e035097eea493a992978f2e9b5`.
The fresh wheel reproduces the site query and existing Atlas-10, draft,
transformation and candidate queries from an empty directory with network
connections blocked. All 439 core tests and repository contracts pass.
The original transformation and candidate-event builders also pass
their unchanged-data checks.

## Continuation

The next scientific milestone is one useful mechanistic question with an
inspectable chain from source edits to residues, protein/structure evidence,
alternative explanations and a discriminating observation. Select the question
by its scientific consequence and the evidence needed to resolve it. Additional
catalog volume or presentation work is not a substitute for closing that chain.

A new conversation should read `docs/CURRENT_STATE.md`,
`docs/ATLAS_TRANSFORMATIONS.md` and this board, verify local/remote Git state,
then continue from the highest-impact unresolved scientific edge. Reuse
subagents for independent source challenges and focused implementation review;
preserve their shared-model limitations. Publication of this feature follows
the passing local checks and the pull request's Linux/Windows CI matrix.
