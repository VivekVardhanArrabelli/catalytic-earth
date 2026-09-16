# Mechanism Workbench — submission notes

Attribution and scope notes for the Workbench sprint. This file records what
was built in this sprint, what already existed, and who or what contributed.
It makes no scientific claim.

## What already existed in Catalytic Earth

None of the following was built in this sprint. The Workbench reads it and
changes none of it. Presented separately so the new work is not credited with
the science it merely displays.

- The packaged offline atlas queries and their schemas: transformations,
  transformation sites, mechanism evidence, source fragments, panel
  comparisons, candidate events and candidate patterns.
- The shared graph-edit engine, its replay and its validators.
- The reviewed source records for M0187 and M0173, their source inventories,
  acquisition receipts, attribution files and audits.
- The mechanism evidence records, their source witnesses, project readings,
  discriminants and mandatory abstentions.
- The site mappings across UniProt, PDB author and mmCIF label numbering, and
  their coordinate verification.
- The unreviewed candidate-event catalog and its shared-atom matcher.
- The claims, errata and truth policy that bound what may be asserted.
- The review and hash machinery, the test tiers and the repository contract
  validator.
- The existing PyMOL review pipeline and its artifacts.

## What this sprint added

A local interface over the above, in `src/catalytic_earth/workbench/`, plus its
documentation and tests. Specifically:

- A narrow adapter calling the same verified loaders and query functions the
  command line uses, in process.
- A deterministic two-dimensional layout for graphs that carry no depiction
  coordinates, labeled as computed.
- A loopback HTTP server, standard library only, serving a fixed asset
  allowlist.
- The interface itself: source-graph replay, atom and fragment inspection,
  evidence with its qualifications, and a structured shared-atom query builder.
- A provider-neutral ledger for external research-suite contributions.
- An end-to-end browser demonstration harness.
- Unit tests for the adapter, the server, the ledger and the claim labels.

No packaged data, expected-value file or review hash was regenerated. No new
source was acquired. No new scientific claim, evidence tier or review status
was added.

## Research-suite plugin credit

**No research-suite plugin was used, and none is credited.** The contribution
ledger at `work/workbench_external_sources.json` is empty.

The sprint ran in Claude Code, where the session plugin list was empty
throughout. Searches of the account plugin catalog and the connector registry
returned no entry for the intended suite. Rosalind is an OpenAI product: its
Life Sciences Research plugin runs in Codex and ChatGPT, and Claude Code cannot
reach or operate it. No plugin call was made, and none is simulated, described
or recorded as if it had succeeded.

When a real contribution is made, record it with
`python -m catalytic_earth.workbench.external_sources`, which credits the suite
and the exact tool that produced it. The checklist for that session is in
`src/catalytic_earth/workbench/HANDOFF.md`.

## Outside coding assistance

The Workbench code, its tests and its documentation were written with
Anthropic's Claude Code, working in this repository under the owner's
direction. Commits carry a co-authorship trailer recording this.

Claude Code performed local Python work only: reading the packaged queries,
writing the interface and its tests, and running them. It made no external
research-suite call, and local Python calculations are never recorded or
presented as external tool output.

## Captures

Screenshots and the screen recording are produced from the running application
by `python -m catalytic_earth.workbench.demo_check --shots ... --video ...`.
They are not committed, because the repository carries no image or video
artifacts and declares its binary types explicitly. No other image or video may
be presented as a capture of this application.

## Before posting

The owner confirms the organizer's current deadline and approves the
submission. Nothing here has been posted, published or shared.
