# Catalytic Earth — Rapid Full-Atlas Plan

**Decision date:** 2026-07-13
**Status:** current execution contract
**Supersedes:** benchmark-as-destination framing and serial 12–24-month execution assumptions

## North Star

Build the world's computable catalytic-mechanism atlas: a continuously
expanding, provenance-grounded map connecting:

```text
canonical biochemical reaction
→ alternative elementary mechanism hypotheses
→ catalytic residues, atoms, cofactors, and geometry
→ protein, structure, evolutionary, and literature evidence
→ counterevidence, conflicts, uncertainty, and abstention
→ design constraints where justified
→ assay, controls, falsification criteria, and outcomes
```

The full atlas is the mission. The mechanism intermediate representation and
evidence compiler are its engine. Benchmarks and exposure controls keep it
honest. Search/API surfaces deliver it. Prospective loops correct it.

## Why the kernel does not narrow the atlas

The kernel is the smallest complete version of the full atlas, not a side
project:

| Kernel output | What it becomes at atlas scale |
| --- | --- |
| Typed mechanism schema | The atlas data model |
| Ten hard mechanisms | The first trusted atlas entries |
| Source crosswalks | Import adapters for existing knowledge |
| Benchmark cases | Permanent regression and calibration surfaces |
| Evidence/counterevidence | Claim-level provenance across the atlas |
| Searchable local release | The public atlas interface |
| One prospective loop | The template for continuous biological correction |

Nothing in the kernel is discarded when the atlas expands.

## Atlas evidence tiers

Breadth is allowed before gold-level evidence, but the tier must always remain
visible and queryable.

### Tier 0 — canonical reaction record

- stable Rhea/ChEBI or equivalent reaction identity;
- balanced participants and source release;
- no mechanism implied.

### Tier 1 — mechanism hypothesis

- explicit ordered steps or rule composition;
- computational/source provenance;
- no protein or experimental validation implied.

### Tier 2 — protein/site-grounded hypothesis

- sequence, structure, residue, cofactor, evolutionary, and counterevidence;
- calibrated applicability domain and abstention;
- computational support, not experimental verification.

### Tier 3 — independently reviewed mechanism

- source-level evidence adjudicated by someone outside the producing
  author/agent loop;
- disagreements and alternatives preserved;
- reviewer identity and review date recorded.

### Tier 4 — experimentally tested outcome

- assay conditions, controls, materials, and measured result;
- positive and negative outcomes treated equally;
- the mechanism may remain unresolved even when activity is measured.

## Non-negotiable truth reset

Further label/family scaling and new performance headlines remain frozen until:

1. a claim ledger marks claims Supported, Diagnostic, Superseded, or Retracted;
2. an append-only exposure ledger records every row/surface exposure;
3. the June 28 M-CSA result is labeled retrospective analysis of an exhausted
   surface;
4. the 76% result is labeled cofactor-bucket consistency and the 31% exact
   result is reported beside it;
5. the 10,001 records are described as 8,305 positive fingerprint assignments
   plus 1,696 OOS protein-label records;
6. `current702` is described by its actual bronze/silver/review composition;
7. the undefined "~2% of mechanism space" claim is removed;
8. one locked environment and command reproduce one bounded result;
9. the live artifact inventory replaces the stale passing inventory;
10. the 74 full-suite failures and 20 errors are triaged rather than hidden by
    bulk snapshot refresh.

This reset is a 48-hour decision sprint, not a long cleanup phase.

## Two clocks

### Clock A — 35-day computational atlas loop

The target is a complete computational loop in five weeks, approximately the
20× cadence requested relative to a two-year serial plan.

### Clock B — 60–90-day experimental target

Physical testing begins in parallel on day one. A 60–90-day readout is a target
only when the first loop uses an existing inexpensive assay and a ready lab,
core, or vendor. If those conditions are absent, the computational loop still
finishes by day 35 but must not be described as biological validation.

## The 35-day execution plan

### Hours 0–48 — correct, freeze, and define

Deliverables:

- claim ledger and errata;
- exposure ledger seed with all known spent surfaces;
- five atlas evidence tiers frozen;
- canonical definitions for reaction, source mechanism, mechanism hypothesis,
  fingerprint/family, protein-label record, and experimental observation;
- one current README/MAP/roadmap path;
- no new performance claim.

Exit gate: no active document calls an exposed surface untouched, a cofactor
bucket a mechanism endpoint, or a protein-label count a mechanism count.

### Days 3–7 — build the atlas kernel

Deliverables:

- versioned mechanism IR/schema;
- lean source release or blob-filtered entry path;
- locked core environment and minimal CI;
- live release/artifact manifest;
- three deliberately different mechanisms encoded end to end;
- M-CSA, Rhea/ChEBI, and project-record adapters sketched;
- one query against a local DuckDB/SQLite/Parquet surface.

Exit gate: a fresh Windows and Linux environment can reproduce the three
records and their provenance without loading the multi-gigabyte artifact tree.

### Days 8–14 — Atlas-10

Select ten cases that pressure the representation rather than flatter it:

- radical chemistry;
- metal/redox chemistry;
- covalent intermediate;
- proton relay/protonation ambiguity;
- same net reaction with alternative mechanisms;
- similar catalytic strategy across unrelated folds;
- same fold with different chemistry;
- conflicting literature interpretation;
- one unsupported case that must abstain;
- one design-relevant geometry case.

Deliverables:

- ten typed mechanism records;
- crosswalks to M-CSA, Rhea/ChEBI, EC-BLAST/EnzymeMap, MechFind/EzMechanism,
  and EnzyMM where applicable;
- two useful queries;
- one strong external baseline pipeline;
- one-command reproduction;
- bounded outside review of five to ten cases.

Exit gate: the schema is converging, unsupported fields fail explicitly, and at
least one query is useful beyond opening the incumbent resources separately.

### Days 15–30 — Atlas-50 alpha

Deliverables:

- 50 diverse mechanisms, expanding only when the ten-case schema is stable;
- automated draft crosswalk for all 57 current fingerprints, each marked as
  duplicate, aggregation, specialization, interoperability bridge, genuinely
  missing concept, or unsupported;
- first 50-row bronze audit to identify error modes;
- public searchable release/API/browser alpha;
- weekly immutable release manifests;
- external task feedback recorded as data, including failures.

Stretch deliverables, never hidden prerequisites:

- expand the bronze audit toward 200 rows;
- recruit a second reviewer;
- run multiple matched sequence, profile, structure, reaction, and learned
  baselines;
- begin machine-import drafts for the broader M-CSA detailed-mechanism core.

Exit gate: the alpha answers at least one real mechanism question faster or
more completely than the unintegrated incumbent stack. Otherwise contribute
the adapters/crosswalk upstream or narrow to the useful component.

### Days 31–35 — first complete computational loop

Choose one reaction/protein question and produce:

1. canonical atom-mapped reaction;
2. ranked alternative mechanisms and exact source analogues;
3. protein/site evidence and counterevidence;
4. calibrated decision or explicit abstention;
5. atomic constraints only when chemically justified;
6. assay, positive/negative controls, and falsification contract;
7. a compact release another person can inspect without the full repository.

This is the first complete atlas loop. It is not a claim of experimental
discovery.

## Parallel 90-day experimental track

Start on day one:

1. choose a mechanism with an existing cheap, fast, discriminating assay;
2. identify one lab, core, CRO, or vendor able to execute it;
3. define a tiny candidate and control panel;
4. order or stage materials while the atlas kernel is built;
5. freeze the computational decision before outcomes are seen;
6. record the assay result, including failure, as a Tier-4 atlas observation;
7. update the mechanism hypotheses without rewriting the original prediction.

Do not make novel assay development the first loop. Do not wait for Atlas-50 to
begin external coordination.

## Full-atlas scaling path

The full atlas proceeds after the kernel; it is not postponed until the kernel
is "finished."

```text
Atlas-3
→ Atlas-10
→ Atlas-50
→ detailed M-CSA mechanism core
→ Rhea/MechFind-scale hypothesis layer
→ protein/site grounding through UniProt/CATH/EnzyMM/structures
→ continuous independent review
→ continuous experimental outcomes
```

At every scale, report separately:

- canonical reactions;
- source mechanisms;
- mechanism hypotheses;
- positive protein assignments;
- OOS/control records;
- independent reviews;
- experimental observations.

No single total is called "mechanisms" unless it counts a formally defined
mechanism object at a declared evidence tier.

## Compute discipline

The project is compute-disciplined, not compute-poor. Every material job should
have a ledger entry:

```text
scientific question
→ cheapest credible baseline
→ expected information gain
→ maximum compute budget
→ stop condition
→ content-hashed reusable output
```

Spend compute on frozen uncertainties, targeted structure/profile searches,
mechanism enumeration, representation comparisons, uncertainty, and a small
prospective candidate panel. Do not train a broad foundation model, bulk-score
proteomes without a user question, rerun spent surfaces, or generate hypotheses
that nobody will adjudicate.

## Weekly operating system

Each seven-day sprint must produce at least one of:

- a corrected claim;
- a new typed mechanism object;
- a source crosswalk;
- a reproduced baseline;
- an external review;
- a useful query;
- a prospective decision;
- an experimental observation.

Narrative artifacts and row volume alone do not count as progress.

## Permanent red lines

- A spent row is never untouched again.
- A post-hoc endpoint is never presented as preregistered.
- Upstream expert curation is never called independent review of a downstream
  automated label.
- Reaction, mechanism, fingerprint, protein record, and experiment counts are
  never conflated.
- Automated geometry/residue consistency is never called experimental
  verification.
- Negative results are never deleted.
- Strong claims are never based only on a weak comparator.
- Speed never comes from weakening evidence labels.

## Success definition

Catalytic Earth succeeds when the atlas gives another scientist useful,
inspectable mechanism knowledge they could not obtain as reliably or quickly
from the unintegrated source stack — and when the atlas can correct itself when
external evidence says it is wrong.
