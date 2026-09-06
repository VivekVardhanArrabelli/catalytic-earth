# M0187 elementary transformation: internal message board

The owner authorized the next atom-resolved feasibility pilot after PR #44.
Base main and origin/main are clean and identical at
`9312c6252edc972e1f4bff9711b9d9c2db69cd8c`. The PR #44 merge tree equals its
four-job-CI-tested head `c2e67e53a933a11448fab39e1d20e354b0904a5a`.
Current branch: `codex/m0187-elementary-transformation`.

## Objective and success condition

Connect authoritative RHEA:13945 participant structures to the retained M0187
mechanism-1 states and derive a defensible transformation at explicit ligand
atoms. The initial two-step target was narrowed after source inspection (below).
The result must answer which atoms, bonds, charges or stereochemical
states change, and expose the exact evidence for that answer. Mapping is a
project computation, not an upstream-supplied map or an observed trajectory.
No implementation/schema expansion starts before the source/graph feasibility
check identifies a defensible result.

The selected source direction is R to S; the retained Rhea master equation is
undirected. Initial feasibility asked whether Step 3's input panel could
witness Step 2's product state; it cannot, because the ligand is absent. Its
inferred regeneration arrows remain outside the transformation. The
inhibitor/modification structure context is not turnover evidence. Local MRV
atom IDs are locators only and may renumber between panels. Symmetry must be
represented explicitly; no manual selection of chemically ambiguous atoms.

## Ownership

- `source_ingestion`: official participant structures and necessary direction
  evidence, capture receipts, source-form comparison and payload assembly in
  `data/atlas/transformations/m0187/`.
- `state_contracts`: graph correspondence, shared graph-edit primitive and
  validation in `atlas_transformations.py`; portable optional chemistry audit.
- `draft_integration_review`: adversarial chemistry, source drawings,
  proton/charge/stereo checks, and `test_atlas_transformations.py`.
- Root: source-arrow semantics, integration decision, bounded package/query,
  this board, tests and Git/CI publication. All agents share a model family;
  their reviews are correlated and not independent human validation.

## Limits and stop rules

Initial new source budget: eight HTTP requests and 2 MiB. Count redirects,
retries and failed responses. This fits within the development authority's
100-request/30-MiB named-batch ceiling; expanding the initial allowance needs
an explicit decision on what additional evidence could change the conclusion.
No paid compute, GPU work, outreach, experiments or registry writes.

Preserve Atlas3/Atlas10, source snapshots, existing annotations, their runtime
results and all benchmark labels. New work is additive and explicitly scoped.
If participant forms disagree or reactive-center correspondence remains
ambiguous, report the exact failure and pivot; do not create a guessed map.
A successful correspondence must retain its computational status and cannot
promote the source to a complete mechanism, physical trajectory or higher tier.

Use the existing optional RDKit 2025.03.3 analysis environment. Do not add it
to production requirements merely for this feasibility check. Avoid another
large bespoke validator: retain only the machinery needed for the supported
chemical primitive and its decisive adversarial checks.

## Feasibility findings and narrowed positive target

Initial inspection changed the target. M0187 panels 3 and 4 omit mandelate;
there is no drawn product state from which to rederive a full R-to-S sequence.
Step 1's drawn ligand is R while its raw atom labels say CHEBI:17756 (S).
Step 2 depicts an sp2 alpha carbon and retains that label. These labels
cannot be treated as changing chemical-state identities.

The source agent acquired two Rhea-hosted participant MOL files and a current
master reaction TSV in three requests / 2,376 response bytes. Acquisition is
now stopped. The curated R participant is CHEBI:32382; the S participant is
CHEBI:17756. The existing Rhea master remains undirected.

There is a supported narrower positive target: Step 1's depicted input to
Step 2's depicted intermediate. Root and reviewer independently checked the
four arrows and raw graph differences: alpha C-H cleavage/proton transfer to
His297, Glu317 O-H cleavage/proton transfer to the ligand carbonyl oxygen,
C-C single-to-double change and C-O double-to-single change. Ligand net charge
stays -1; the alpha carbon changes from R tetrahedral to sp2. This makes no
claim about absence of alkene geometry elsewhere. The extra
explicit Lys166 hydrogen in panel 2 was implicit in panel 1; it is not atom
creation. Do not simplify away the Glu317 proton shuttle.

Root chooses this one depicted transition as the first chemical primitive.
The second step retains source arrows/prose only, and the absent product,
inferred return step and complete physical trajectory remain unasserted.
The canonical-to-panel bridge compares the ligand covalent subgraph, with
metal coordination explicitly excluded from that comparison and preserved as
context. The reactive-center charge, bond order and stereochemistry remain
exact. Standard aromatic graph perception supports two phenyl orientations;
only one preserves the literal raw Kekule orders. Those two comparison levels
are reported separately, without claiming two exact raw-graph replays.
Graph-derived atom correspondence remains a project computation.

## Implementation and review coordination

The durable input contains a 26-atom covalent projection of the ligand,
His297 and Glu317 before and after the step. The shared primitive applies six
bond edits, two charge edits and the alpha stereochemistry update. It checks
the resulting chemical graph against the after projection. Source component
labels are context and change when a proton transfers; they are not asserted
to be conserved atom properties.

The query is `catalytic-earth atlas-transformations --mcsa-id M0187`.
It includes the canonical participant bridge, both ligand mapping alternatives,
before/after graphs, edit-to-arrow references, and the source limitations.
The old Atlas-10 query and its result hash remain the baseline.

Reviewer caught machine-specific paths in the copied chemistry audit before
acceptance. State changed them to paths relative to the retained repository
inputs; the audit output was reproduced without changing its scientific
contents. Root also reproduced the same audit bytes after copying only its
script, the M-CSA snapshot and two MOL files into a fresh directory tree and
running from an unrelated working directory.
Root inspected both rendered input/intermediate panels and checked the
Glu317 and His297 transfer legs against source bonds and arrows.

Agents encountered an account usage limit during implementation. Work resumed
after the owner reported renewed usage. No source acquisition was repeated.

## Adjudication

Root's initial mutations exposed accepted contradictions in stereochemistry,
canonical atom numbering, raw source labels, directional Rhea cross-reference,
and arrow attribution. State added source-backed rejection for those cases.
Reviewer added coherent false-edit/false-after-graph challenges, distinct
symmetry checks and the H67 representation boundary. These tests intentionally
refresh the project review pin in memory so the checks must detect a source
contradiction rather than only a stale payload hash.

Reviewer accepted the final scientific payload
`65057e00ab8191505294987e7be7338b09a991eb9715b1116d09713c9a0d56ab`.
Source materialized its review pin; final repository/package JSON bytes hash
`02135996931cd366945fad1773b1ca067f13cb609a17a56862ebfc91f5d28fa3`.
The portable chemistry audit result remains
`1a4e72d97b534d5a3f65246c90ad5cb1bad4214a7d41340f845aa52af39e3658`.
Raw scientific source files were not modified. All eleven source bindings
are checked at package-build time; the installed query checks package pins
and replays the compact graph without raw structures or RDKit.

Disposition: accept the depicted input-to-intermediate transition and computed
canonical input correspondence at this scope. Retain the raw-label conflict,
the non-unique remote phenyl mapping, the absent product and inferred return
step. This does not constitute independent human review, an exact physical
reaction instance or experimental validation. Benchmark labels, protected
registries and the frozen human-review packets remain unchanged.

## Verification and next priority

Final module hash:
`a127ac66ddbc4576bfd5ed5970f1e298b0feccee2ed7067a27f0543f6e717c9a`.
The focused suite passes 17 tests, including twelve primitive/source challenges
and five query/package tests. The full core suite passes 343 tests with one
optional dependency skip. The fresh wheel passes the Atlas-10/source-draft
checks in an empty working directory, with query network connections blocked
and RDKit absent. The transformation is also replayed inside that installed
environment. Atlas-10 still returns 10 cases / 30 objects and runtime SHA
`57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.
The preserved release manifest still points to source `f00ba6648b18229a840840e9c7dbac95251594be`.

The source agent's bounded next-target inspection favors M0173 Step 1 to 2:
a depicted enzyme–substrate covalent addition that would exercise a different
chemical change using the shared edit engine. Both retained panels are
present. It remains a candidate, not an implemented or reviewed transformation;
generic peptide identities cannot become an exact physiological reaction or
product map. No acquisition or second implementation was started.
