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
