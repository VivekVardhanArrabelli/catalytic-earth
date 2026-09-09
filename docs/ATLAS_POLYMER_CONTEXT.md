# Peptidoglycan polymer roles and structural applicability

The current M0970 annotation corrects a consequential role reversal: the
growing glycan is the **donor** in the SaMGT paper's elongation model, while
incoming lipid II is the **acceptor**. The prior state-probe label called the
polymer an acceptor. A compound name or reactant order cannot determine its
role; lipid II can occupy both sites during initiation.

The [source annotation](../data/atlas/polymer_context/m0970/annotations.json)
binds the correction to three reviewed report generations. Read a current
case with its evidence and limits using:

```bash
python scripts/build_atlas50_state_probe.py --query-case M0970
python scripts/build_atlas50_state_probe.py --batch plp-pyruvoyl --query-case M0970
```

The view changes only the component's role wording. It retains the historical
report hash and original role in the correction, and includes the cited
source context beside the result. A changed report, unexpected original role,
or unreviewed annotation is rejected. Historical report bytes and development
permissions remain unchanged: M0970 still permits source annotation only.

## Symbolic cycle scope decision — 2026-09-09

The primary paper supports a **proposed sequence of reaction roles**, which
the current annotation now preserves. A bounded, paper-scoped qualitative
polymer relation **fits the existing representation without numeric chain
lengths**. The current reviewed M0970 gate still permits annotation only.

| Source-model event | Relation retained | Boundary |
| --- | --- | --- |
| Transfer, Fig. 4B-C | Donor at S2 reacts with lipid II at S1; the extension product is associated with S1 | Proposed beta-1,4 linkage; no resolved M0970 product or atom map |
| Product relocation, Fig. 4D | That product is moved to donor site S2 | Same narrative product referent; no measured motion or continuous enzyme retention |
| Substrate reload, Fig. 4E | Another lipid II enters S1 for a subsequent transfer | Repeated roles do not mean return to the previous chemical state or measured processivity |

The caption distinguishes initiation with two lipid II molecules from
elongation with a growing donor chain. These remain distinct contexts of
the authors' model, not assignments to the exact M0970 reaction instance.
The source does not establish a loading order, vacant-site states, separate
product release from the enzyme, product rebinding, or residence times. Leaving-group departure
belongs to the proposed transfer; it is not an additional timed event.
The anonymous `extension_product_after` handle in the annotation tracks a
referent across the paper's schematic. It is not a chemical identifier,
state-catalog entry, equality to X00676, or a numeric chain-length update.

The [contract check](../data/atlas/polymer_context/m0970/annotations.json)
separates three questions:

1. **Can the information be stored?** Yes. The existing annotation view
   returns the source-model events, and the polymer fields can retain
   qualitative text with a null product. No runtime change is needed.
2. **Can the current state probe type each cycle event?** No. Its transition
   vocabulary covers redox, nucleotide hydrolysis and carrier loading.
   In-memory transfer, site-relocation and substrate-binding probes are
   rejected. Free-text strings in the v4 JSON schema do not provide executable
   event or recurrence semantics. This does not prevent a qualitative
   source-state draft. The diagnostic used synthetic before/after labels only
   to isolate the event-kind check; they are not source states.
3. **Is a M0970 draft authorized?** No. The live gate accepts annotation and
   rejects a mechanism draft or exact instance. The draft is missing
   source-bound product identity and before/after topology. Numeric chain
   lengths, initiation/elongation and processivity occur only in the stricter
   exact-instance requirement list. **Unknown numeric n alone is not the
   draft blocker.** A separate in-memory trial accepted a paper-source
   `source_proposal_label` and qualitative before/after relation while leaving
   X00676 unresolved and numeric chain lengths null. Conditionally satisfying
   only those three missing draft clauses allows a draft in the evaluator;
   all four exact-only clauses remain missing. This is a structural trial,
   not a new reviewed source generation or live permission change.

The decision is positive for bounded qualitative representation, with the
current permission unchanged. A future draft needs an explicit paper-scoped
source challenge and adjudication of the product/topology relation. Richer
event semantics and a concrete consumer are reasons to invest, not formal
source-draft requirements. Before any future exact-instance promotion,
distinguish a source-proposal product handle from exact chemical identity;
the shared product clause alone does not make that distinction. Adding an
enzyme-specific branch or calling the product `n+1` would not resolve it.
The exact-instance gate is unchanged.

The source check reused the retained article and its existing SHA-256; no new
polymer-source acquisition was necessary. The scope check prevents both
rejecting a legitimate symbolic relation solely for unknown n and promoting
a narrative product into exact chemical identity. Further re-encoding of
this same model adds little value without a concrete consumer, so research
should move to a different evidence gap. No new mechanism draft or
design-performance result is claimed.

## What the primary sources establish

The [2012 SaMGT study](https://pmc.ncbi.nlm.nih.gov/articles/PMC3340074/),
Introduction and Figure 4, places the growing glycan in donor site S2 and
monomer lipid II in acceptor site S1. Its proposed model has the incoming
GlcNAc 4-OH attack donor C1 and then moves the new chain to S2. This is a
structure- and mutagenesis-supported model, not an observed atom-transfer
trajectory or a resolution of all M-CSA alternatives.

The same paper's Discussion describes analogue 3 with GalNAc in place of
GlcNAc: the position-4 hydroxyl is inverted. The authors state that it binds
but cannot serve as an E100 substrate. The 3VMT analogue pose therefore does
not establish a productive native lipid-II arrangement or donor-chain pose.
The study uses a stabilized Mu50 Q28–R269 construct containing the membrane
and TG regions, with a cleaved His6 tag. This review inspected the paper and
entry metadata, not current atom coordinates or supplementary assay details.

The [2007 direction experiment](https://pmc.ncbi.nlm.nih.gov/articles/PMC3206585/)
uses longer glycan oligomers capped at their non-reducing end. They extend
when lipid II is supplied, supporting growth at the anomeric diphospholipid
end, conventionally called the reducing end even though it is not a free
lactol. The short capped Lipid II/IV experiments alone were insufficient:
their uncapped counterparts can self-condense. The longer-oligomer test and
no-lipid-II controls provide the discriminating evidence.

That study tests E. coli PBP1A/PBP1B, A. aeolicus PBP1A, and S. aureus PBP2.
It does not directly test Q99T05/SaMGT; the broader family conclusion is an
author proposal. Published experimental evidence is not a project-run
experiment or an independent review of this atlas annotation.

## Conflicts and limits retained

Current [M-CSA M0970](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/970/)
mechanism-1 Step-1 prose assigns the nucleophilic attack to the donor-site
strand, contrary to the primary SaMGT model. Its mechanism-2 Step-2 prose
instead has the acceptor attack the donor. The source text is preserved as a
conflict; it is not silently rewritten or compiled into resolved steps.
The linked [2020 study](https://pubmed.ncbi.nlm.nih.gov/32786224/) is explicitly
computational modeling; its abstract does not resolve this conflict by
experimental observation.

No exact identity is assigned to product placeholder X00676, no numeric chain
length or complete M0970 reaction instance is supplied, and no processivity
claim is made. Direction, initiation/elongation models, reaction roles and
processivity are different questions. The current state variables remain
unresolved under the existing gate.

The [acquisition appendix](../data/atlas/polymer_context/m0970/acquisition_appendix.json)
carries the earlier panel review's 21 measured captures and 1,125,005 bytes.
Seven new requests, including one empty 404 response, add 349,400 bytes:
**28 measured requests / 1,474,405 bytes** cumulatively. Historical unmetered
browser checks remain disclosed. The separate transketolase/POX batch is
unchanged at seven direct captures / 3,004,884 bytes. No raw paper, figure or
new coordinate file is redistributed.

This increment corrects an existing case. It adds no protein, reaction,
mechanism draft, tier promotion, performance result or design validation.
Chemistry stays in reviewed data; the same current-view code applies the
correction to all three report generations without repeating their curation.
No measured curation speedup is claimed.
