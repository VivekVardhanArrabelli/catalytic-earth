# Mechanism Workbench

A local interface over the existing packaged Atlas queries. It adds no
scientific claim, no source acquisition, no evidence tier and no new review.
Every value it shows is read from a live query result at request time.

```sh
pip install -e .
python -m catalytic_earth.workbench          # http://127.0.0.1:8765/
python -m catalytic_earth.workbench --port 8790
```

The server uses the standard library only, binds to loopback, serves a fixed
allowlist of assets from inside the package, runs no external command and opens
no network connection. The packaged runtime needs neither RDKit nor raw source
files, matching the existing offline query guarantee.

## What it does

Select a mechanism, replay its reviewed source-graph edits, inspect the
supported protein-residue context of a changed atom or fragment, and read the
endpoint-specific experimental evidence bound to that site. A second tab runs
the shared-atom chemical-pattern query through a structured clause builder.

Both M0187 (mandelate racemase) and M0173 (trypsin) load through the same
renderer and the same adapter. Neither is a hard-coded scientific page.

## Guided walkthrough

An optional ordered path over the same controls and queries, reached from the
`Guided walkthrough` button. Each step changes real state: it loads the
mechanism, moves the replay, selects the supported fragment by its own relation
id, re-runs the evidence query and assembles the inspection request. Nothing in
it is precomputed, and every value shown is read from a live result.

It can be left at any time; filters and selections stay where it left them and
the ordinary controls keep working. The expert view is always available, and
locators, hashes and full source detail remain in the inspector and the
provenance disclosures.

The endpoint comparison clears the variant filter before running, so the
contextual observations are genuinely in the result rather than described from
rows that are not loaded. Focal and contextual variants are tabulated
separately, with the contextual table labelled as not matched controls.

## Matched chemistry

A returned candidate and variable assignment can be opened with `View matched
chemistry`. The query is re-run and the named candidate selected from its
result, so what is drawn is always the matcher's own output.

The before and after panels are drawn from the **retained source depiction
coordinates** the record carries, not from a computed layout. An atom the
record does not place is reported as unplaced rather than drawn at a guessed
position. Atoms bound to the query variables are marked with their variable
name, the edits witnessing each clause are listed with their support state, and
the remaining proposed edits are listed separately.

After-panel marks are placed through the retained correspondence, never by
matching identifier strings across panels; a bound atom the correspondence does
not map is left unmarked and disclosed. A bond is highlighted as a witness only
where a bond edit names that exact pair, so two charge edits on connected atoms
do not imply an edge that never changed. Source-graph confirmation carries its
own label, distinct from the one reserved for a published measurement.

Alternative assignments are selectable and labelled: they are different ways one
query binds to one candidate, often through symmetry, and more assignments are
not more evidence. The candidate is marked unreviewed throughout and explicitly
distinguished from the reviewed source-depiction transformations. Correspondence
carries its own meaning, `project_unreviewed_panel_alignment_not_physical_atom_map`,
and coverage, opaque context and scope remain available.

## How it is wired

`catalytic_earth.workbench.adapter` imports the same verified loaders and query
functions the `catalytic-earth` subcommands use, in process:

| Workbench route | Packaged query | Equivalent command |
| --- | --- | --- |
| `/api/mechanism/<id>` | `query_transformations` | `atlas-transformations --mcsa-id <id>` |
| `/api/sites/<id>` | `query_transformation_sites` | `atlas-transformation-sites --mcsa-id <id>` |
| `/api/evidence` | `query_mechanism_evidence` + `query_fragment_sites` | `atlas-mechanism-evidence --variant H297N --include-source-fragments` |
| `/api/match-chemistry` | `query_candidate_patterns`, projected | (no direct equivalent) |
| `/api/patterns` | `query_candidate_patterns` | `atlas-candidate-patterns --bond ... --charge ...` |

The Atlas-10 kernel hash check the CLI performs is applied here too. The
scientific core is read-only from this package; nothing here regenerates
packaged data or rewrites a review hash.

## What the drawing is and is not

The transformation query returns chemical graphs without depiction
coordinates: an atom carries only its identifier, element, formal charge and
stereochemistry. Atom positions are therefore **computed** from graph topology
by a deterministic layout, and the interface says so on screen. They are not
experimentally measured geometry, not a molecular conformation, and not the
original source-panel depiction coordinates.

The layout uses the union of before-panel and after-panel bonds so a single
frame can show both states. That is a drawing choice and asserts no chemistry.

Retained source depiction coordinates do exist, but only for the source
fragments returned by the mechanism-evidence query. The inspector reports them
separately and labels them as depiction coordinates, never as geometry. They
are never mixed into the computed positions.

Stepping the edits replays a published source-depiction proposal as a symbolic
graph edit sequence. It is not a molecular trajectory, shows no physical
motion, and asserts no physical atom identity.

Packaged enumeration values are phrased for reading at render time only. The
underlying value is never rewritten, the raw token stays beside its reading, and
an unrecognised value is shown exactly as it arrived.

## Claim labels

The footer defines every label the interface uses, in two groups, because a
statement about provenance and a statement about a reported outcome are
different kinds of claim and must not share a style.

**Provenance**: source proposal, site mapping, reference structure, external
tool, unresolved. **Reported outcome**: published measurement, nondetection,
no detectable difference, unreviewed.

A label used with no legend entry, or one style reused for a different kind of
claim, misreports the packaged data as surely as a wrong number would, so the
vocabulary is closed and checked in `tests/core/test_workbench_labels.py`.
"Source proposal" in particular labels only the replay; a site mapping, an
external lookup and a reported outcome each carry their own label.

The nine mandatory abstentions on the H297N case are shown on the evidence
panel itself rather than behind a closed disclosure, as collapsed one-line
entries. Deeper supporting detail stays behind disclosures so the caveats
remain available without obscuring the main interaction.

Boundaries the interface is built to preserve:

- Racemization nondetection, retained S-mandelate exchange and R-mandelate
  exchange nondetection are separate endpoints and are never merged.
- The 3.3-fold value is shown with its reported relation, its stated WT
  comparator and its conditions. It is not an absolute rate or an activity
  score.
- Unknown assay details and detection floors render as unknown, never as zero.
- The whole packaged evidence set is reachable. Both variants are offered and
  every observation names its own variant, so a mixed list cannot be read as
  one variant's results. The contextual variant's observations are not bound to
  the focal site fragment, filtered or unfiltered.
- Contextual K166 observations are shown as reference-site context, not as
  matched H297N controls. Where a source states no comparator, the interface
  says no comparator was stated rather than implying one.
- A rejected filter is reported as bad input with the query's own message, not
  as a server fault with a raw exception.
- Clause values are read exactly as written or refused. A bond order or formal
  charge is never rounded, truncated or coerced, because that would quietly
  search for a different chemical constraint than the one requested.
- A failed request never leaves the controls describing something else. It
  restores them to the state actually displayed and says so, or clears the
  dependent views when nothing was ever loaded.
- A refused query retires any request still in flight, so an older response
  cannot replace the refusal with results.
- A selection follows the active filters. The inspector re-resolves it against
  the current result rather than holding an earlier response's object, and a
  selection the current result cannot support is dropped.
- Source-atom locators, UniProt positions, PDB author numbering and mmCIF label
  numbering are displayed as distinct systems that travel together.
- No deposited H297N mutant-context structure exists in the packaged data; the
  available reference structure is labeled as such with its own limitation.
- Two different resolutions are visible: the reference structure's, and the
  one reported for the structural comparison. They come from different records
  and are not the same structure. A structure-kind observation therefore states
  that it names no deposited structure, so its resolution is not read as
  belonging to a reference structure shown elsewhere.
- A nondetection and an unresolved difference are worded separately. Neither is
  a numeric zero.
- The candidate catalog is unreviewed. A pattern match does not promote any
  candidate's evidence status, and binding counts are variable assignments,
  not mechanism counts.
- An empty result means no match in the declared searched collection, not
  absence of the chemistry in nature.

## External tool contributions

Some workflow steps come from an external research suite rather than from the
packaged queries: a literature lookup, a database lookup, or a structure view.
Those are recorded in a provider-neutral ledger at
`work/workbench_external_sources.json`, so the suite behind them can be
swapped without touching the interface.

```sh
python -m catalytic_earth.workbench.external_sources --show
python -m catalytic_earth.workbench.external_sources   --provider-suite "Rosalind" --provider-tool "<exact tool>"   --action literature_lookup --query "<exact query sent>"   --subject paper:PMID:1909893 --retrieved "<identifier returned>"
```

Rules the module enforces rather than leaving to convention:

- The ledger starts empty and stays empty until a real call is recorded. There
  is no seeding, example row or placeholder contribution, and the interface
  shows an empty ledger as empty.
- Every record names the suite and the exact tool that produced it. An
  unattributed contribution is refused.
- Records are marked as external tool calls. Local Python calculations are not
  recorded here and are never presented as external tool output.
- A contribution is context recorded alongside the packaged evidence. It never
  changes, overrides or extends a packaged claim or review status.
- A call that returned nothing is recorded as having returned nothing.

Swapping providers keeps earlier credit intact: the active provider changes,
but each past contribution keeps the suite that actually performed it. Record a
contribution only from a call you actually made and whose output you hold.
Writing up a call that did not happen would be a fabricated receipt.

The subject index carries each record's action, provider, tool and result
count. The interface badges by the recorded action, never by the subject, so a
database lookup against a structure accession is reported as a database lookup
and never as a structure view, and a call that returned nothing says so.

## Returning a result

Recording a contribution says a tool was asked to do something. Returning a
result says what it produced. `external_results` takes the file a tool actually
saved, ties it to the case it answers, and records it beside the packaged
evidence.

```sh
# What a case reference resolves to. Writes nothing.
python -m catalytic_earth.workbench.external_results --resolve-only   --case atlas10.mandelate-racemase-pputida.enolate   --provider-suite x --provider-tool x --action structure_view --query x --artifact x

# Record a saved output against the case it answers.
python -m catalytic_earth.workbench.external_results   --provider-suite "Rosalind" --provider-tool "<exact tool name>"   --action structure_view --query "<exact query sent>"   --case atlas10.mandelate-racemase-pputida.enolate   --publication paper:PMID:1909893 --site P11444:H297 --structure 1MNS   --artifact ./saved/1mns-view.png   --context "residue=His297 (PDB author numbering)"
```

Rules the module enforces:

- **An artifact must exist.** Every file is hashed and measured from disk. A
  missing or empty file refuses the import, and a result with no saved output
  is a request, not a result.
- **The association is checked, not asserted.** The declared publication, site
  and structure are compared with what the packaged record actually carries.
- **A confirmation means exactly one thing.** The declared identifiers were
  found in the case, and the ones it carries were then found together on one of
  its relations. It is not a reading of the output's science and it does not
  authenticate the tool that produced it.
- **Membership is not support.** A publication drawn from one evidence relation
  and a site drawn from another are both in the case and still do not support
  each other; that pair is a conflict, not a match.
- **A mismatch is preserved.** A declared identifier the record does not carry
  is recorded as a conflict, naming what the record does carry. It is never
  dropped and never counted as a match.
- **Source roles are kept apart.** A case's publications are the sources of its
  functional observations. The primary citation of a deposited structure is a
  different role that these records do not enumerate, so a result scoped to a
  structure the case carries records such a citation as separately sourced
  external context: not confirmed, not contradicted, and never silently
  swapped for a functional source that would match.
- **Context is recorded, not checked.** `--context` values are kept as the tool
  stated them and take no part in any comparison; hashing a file does not
  establish that a string was read out of it. Declare `--publication`, `--site`
  or `--structure` to have an identifier compared.
- **An unresolved case stays unresolved.** The result is still recorded,
  without the association it lacks.
- **Nothing is merged into the packaged record.** Results live in the ledger
  and are read back from there; a test asserts the packaged query output is
  byte-identical before and after an import.

One resolver serves both packaged record families with no enzyme-specific
branch. `atlas10.mandelate-racemase-pputida.enolate` resolves through the
mechanism-evidence query; `tk_2020:H473N:DHB_accumulation` resolves through the
perturbation projection. Only the identifier differs.

The interface shows each returned result in full: the scientific context the
tool reported, the saved artifacts with their type, size and hash, and the
association table with per-field status and reasons. Each saved artifact opens
from its own row. The file is read back by the digest the ledger recorded, never
by a path the page supplies, and is shown as text rather than served as a
document a browser would execute; one that has moved or changed since it was
imported says so instead of being displayed as the result it no longer matches.
Association statuses carry their own styling, because an identifier found in a
case is not a published measurement and one the case lacks is not an
experimental nondetection.

Two subject strings are wired into the interface: a `PDB:<id>` subject badges
that reference structure, and a `paper:<id>` subject badges that evidence id on
its observation. Any other subject records normally and simply does not badge.

`CATALYTIC_EARTH_WORKBENCH_LEDGER` overrides the ledger path, so a demo or test
can exercise a populated ledger without writing into the real record.

## Tests

```sh
python -m unittest tests.core.test_workbench_adapter
python -m unittest tests.core.test_workbench_server
python -m unittest tests.core.test_workbench_external_sources
python -m unittest tests.core.test_workbench_labels
python -m unittest tests.core.test_workbench_frontend_state
python -m unittest tests.core.test_workbench_match_chemistry
python scripts/run_test_tier.py core/unit
```

An end-to-end run against a live server, including a screen recording:

```sh
python -m catalytic_earth.workbench --port 8766 &
python -m catalytic_earth.workbench.demo_check --port 8766   --shots ./workbench-shots --video ./workbench-video
```

An exhaustive presentation defect sweep over every interface state:

```sh
python -m catalytic_earth.workbench.demo_check --port 8766 --sweep
```

It walks both mechanisms, every selectable atom and fragment, every variant and
endpoint combination and every pattern preset, at three viewport widths, and
reports leaked placeholder values and horizontal overflow. It exits non-zero if
it finds any.

Both need a browser and playwright, which is not a project dependency, so they
sit outside the test tiers. Its screenshots and recording are captures of the
running application; no other image or video may be presented as one.

Attribution, and what already existed versus what this sprint added, are in
[submission notes](WORKBENCH_SUBMISSION.md).

The feature-local handoff is at
[`src/catalytic_earth/workbench/HANDOFF.md`](../src/catalytic_earth/workbench/HANDOFF.md).
