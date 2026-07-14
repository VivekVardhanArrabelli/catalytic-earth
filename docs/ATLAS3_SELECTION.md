# Atlas-3 — frozen first-kernel selection

**Decision date:** 2026-07-13

**Machine contract:**
[`data/atlas/atlas3_selection.json`](../data/atlas/atlas3_selection.json)

**Status:** cases and boundaries frozen before evidence compilation

## Outcome

Atlas-3 is the first real biological kernel of Catalytic Earth. The P0 core
proved that a small typed package, provenance path, negative record, and
repository contract could reproduce deterministically, but its golden records
were deliberately synthetic fixtures. Atlas-3 replaces no P0 control. It adds
the first three non-fixture biological mechanism compilations outside the
protected historical registries.

The selected cases are:

| Case | Representation pressure | Frozen authoritative anchors | Target |
| --- | --- | --- | --- |
| Methylmalonyl-CoA mutase from *P. freudenreichii* | AdoCbl radical formation and rearrangement; two protein chains; incompletely observed intermediates | UniProtKB P11653/P11652, RHEA:22888, PDB 1REQ, M-CSA M0062 | Tier-2 protein/site-grounded hypothesis |
| Mn superoxide dismutase from *E. coli* K-12 | Mn redox cycling, proton-coupled electron transfer, inhibited-state ambiguity, same-EC mechanism trap | UniProtKB P00448, RHEA:20696, PDB 1D5N, two primary studies; M-CSA M0138 only as counterevidence | Tier-2 protein/site-grounded hypothesis |
| TEM-1 class A beta-lactamase from *E. coli* | Covalent acyl-enzyme, alternative general-base proposals, residue-numbering crosswalk, generic reaction versus specific assay | UniProtKB P62593, RHEA:20401, PDB 1BTL, M-CSA M0002, primary mechanism and assay precedents | Tier-2 protein/site-grounded hypothesis and provisional assay lane |

The target is Tier 2, not Tier 3. Upstream expert curation is evidence for the
compiled object; it is not independent review of Catalytic Earth's
interpretation. Tier 3 requires a later reviewer outside the producing loop.

## Why these three

The cases were chosen to break a weak representation quickly, not to estimate
coverage or accuracy.

1. Methylmalonyl-CoA mutase requires explicit cofactor bond homolysis,
   radical-state changes, ordered intermediates, and a two-accession protein
   assembly. A record that only says “B12 enzyme” fails.
2. MnSOD shares EC 1.15.1.1 and RHEA:20696 with Cu/Zn SOD, but it does not share
   the M-CSA M0138 copper/histidine-bridge mechanism. A compiler that transfers
   that mechanism by EC or reaction has failed even if its output sounds
   chemically fluent.
3. TEM-1 requires a covalent enzyme-substrate intermediate and preserves
   competing mechanistic proposals. Its established chromogenic activity
   readout offers a practical first experimental lane while testing the rule
   that activity is not detailed-mechanism validation.

Together the trio tests three distinct reaction-mechanism relationships:

```text
well-anchored reaction + detailed direct source mechanism
same reaction/EC + non-applicable source mechanism that must be rejected
direct source mechanism + meaningful alternative proposal + assay boundary
```

That diversity is more informative for the first schema iteration than three
easy records of the same catalytic strategy.

## What the selection freezes

The machine contract freezes before compilation:

- case identity, organism, protein, reaction, structure, mechanism, and primary
  literature handles;
- representation pressures and the historical fingerprint used only as a
  crosswalk;
- canonical Rhea/ChEBI participant identifiers;
- target evidence tier and required output classes;
- known ambiguities, success conditions, stop conditions, and compute ceilings;
- exactly one provisional assay candidate;
- the prohibition on modifying `data/registries`.

Changing a selected accession, treating the MnSOD M-CSA counterexample as a
direct source, selecting a second assay candidate, enabling GPU use, or
authorizing registry mutation causes validation to fail. A scientifically
necessary change therefore requires an explicit reviewed amendment, not a
quiet edit during evidence compilation.

## Source-applicability boundary

M-CSA M0138 is deliberately present in the MnSOD case with applicability
`counterexample_same_ec`. The current M-CSA reference is yeast Cu/Zn SOD
P00445/PDB 2JCW. It uses copper redox chemistry, zinc, and a histidine bridge.
The selected target is *E. coli* MnSOD P00448/PDB 1D5N in the unrelated Fe/Mn
SOD family. Rhea's M-CSA cross-reference is valid at the broad net-reaction/EC
level but cannot license step or residue transfer.

This is the first explicit Atlas-3 anti-cheating test: a polished mechanism
assembled from the wrong same-EC family is a failure, not a partial success.

## Compute contract

The ceilings are budgets, not targets or timelines:

| Resource | Per case | Atlas-3 selection ceiling |
| --- | ---: | ---: |
| CPU | 6 hours | 18 hours |
| GPU | 0 hours | 0 hours |
| External requests | 150 | 450 |
| Downloads | 100 MiB | 300 MiB |

Every downloaded or derived source artifact must be reused by content hash.
If a case reaches a ceiling, the correct output is a partial, explicitly
abstaining record and a named missing-evidence item—not an unlogged expansion
of compute. These ceilings can later be amended with a scientific reason and
expected information gain; they are not claims that the work should consume
the maximum.

## Provisional assay lane

TEM-1 nitrocefin hydrolysis is the sole candidate. It has a published
continuous absorbance precedent and can support enzyme, no-enzyme/background,
and inactive-enzyme controls. Nothing has been ordered, commissioned,
preregistered, or run by this selection.

Before physical execution, a separate contract must freeze:

- exact enzyme/material identity and provenance;
- executor and cost;
- buffer, substrate, concentrations, temperature, readout, and time window;
- positive, negative, background, and handling controls;
- exclusion rules, acceptance thresholds, and analysis;
- the computational decision hash before outcomes are exposed.

A nitrocefin signal can become a Tier-4 activity observation. It cannot alone
resolve which detailed proton-transfer proposal is correct.

## Immediate build sequence

1. Snapshot the selected authoritative records and store retrieval metadata and
   content hashes in the lean atlas namespace.
2. Extend the mechanism IR only for fields demanded by these cases; unsupported
   states must fail or remain null explicitly.
3. Encode separate Tier-0 reaction, Tier-1 source-mechanism, and Tier-2
   protein/site-grounded hypothesis objects rather than inflating one object.
4. Compile evidence and counterevidence, including source conflicts and
   applicability.
5. Materialize a tiny SQLite surface and one query returning all three records,
   tiers, uncertainty, and source handles.
6. Reproduce the release and query on fresh Windows and Linux environments.
7. Only after the computational decision is frozen, prepare the separate assay
   preregistration and external execution decision.

Atlas-3 is complete only when all six machine exit gates in the selection
contract pass. The frozen selection itself is the start checkpoint, not the
finished biological kernel.

## Validation

```bash
python scripts/validate_atlas3_selection.py
python scripts/validate_repository_contracts.py
python scripts/run_test_tier.py "core/unit"
```

The selection schema is
[`src/catalytic_earth/schemas/atlas3-selection-v1.schema.json`](../src/catalytic_earth/schemas/atlas3-selection-v1.schema.json),
and semantic enforcement lives in
[`src/catalytic_earth/atlas_selection.py`](../src/catalytic_earth/atlas_selection.py).
