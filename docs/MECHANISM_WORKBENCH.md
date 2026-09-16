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

## How it is wired

`catalytic_earth.workbench.adapter` imports the same verified loaders and query
functions the `catalytic-earth` subcommands use, in process:

| Workbench route | Packaged query | Equivalent command |
| --- | --- | --- |
| `/api/mechanism/<id>` | `query_transformations` | `atlas-transformations --mcsa-id <id>` |
| `/api/sites/<id>` | `query_transformation_sites` | `atlas-transformation-sites --mcsa-id <id>` |
| `/api/evidence` | `query_mechanism_evidence` + `query_fragment_sites` | `atlas-mechanism-evidence --variant H297N --include-source-fragments` |
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
python scripts/run_test_tier.py core/unit
```

An end-to-end run against a live server, including a screen recording:

```sh
python -m catalytic_earth.workbench --port 8766 &
python -m catalytic_earth.workbench.demo_check --port 8766   --shots ./workbench-shots --video ./workbench-video
```

It needs a browser and playwright, which is not a project dependency, so it
sits outside the test tiers. Its screenshots and recording are captures of the
running application; no other image or video may be presented as one.

The feature-local handoff is at
[`src/catalytic_earth/workbench/HANDOFF.md`](../src/catalytic_earth/workbench/HANDOFF.md).
