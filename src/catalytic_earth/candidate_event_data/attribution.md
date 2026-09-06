# Candidate event catalog attribution

The retained mechanism records and MRV panels used to derive this catalog come
from the **Mechanism and Catalytic Site Atlas (M-CSA)**:

- [M0049, histidine decarboxylase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/49/)
- [M0066, D-amino-acid transaminase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/66/)
- [M0106, pyruvate dehydrogenase E1](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/106/)
- [M0212, nitrogenase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/212/)
- [M0219, transketolase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/219/)

M-CSA data are available under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the M-CSA
authors for the curated mechanisms and source depictions, and cite Ribeiro AJM
et al., “Mechanism and Catalytic Site Atlas (M-CSA): a database of enzyme
reaction mechanisms and active sites,” *Nucleic Acids Research* 46(D1),
D618-D623 (2018),
[doi:10.1093/nar/gkx1012](https://doi.org/10.1093/nar/gkx1012).

This project generated the packaged catalog offline from twelve candidates in
the frozen 101-pair context scan. Each row retains its exact M-CSA source
snapshot and panel hashes, source-flow witnesses, complete candidate payload,
and the source-specific scope and abstentions copied from the corresponding
packaged Tier-1 source draft. The catalog packages derived candidate data but
does not redistribute the raw M-CSA snapshot files.

The candidates are unreviewed drawing-level graph comparisons. Search results
do not establish a physical atom map, canonical participant identity,
stereochemical or coordination interpretation, complete mechanism,
experimentally observed intermediate, or experimental validation. A
source-arrow-only event is separately labeled from an event confirmed in the
adjacent source graph. Formal-charge replay does not replay raw lone-pair
annotations. Multiple query clauses must match within one candidate, but that
does not assert shared atoms, a shared source arrow, or mechanism equivalence.
