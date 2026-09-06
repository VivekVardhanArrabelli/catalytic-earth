# M0173 partial-panel comparison attribution

The retained mechanism and MRV panels derive from the **Mechanism and Catalytic
Site Atlas (M-CSA)**, [entry M0173, trypsin](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/173/),
available under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
The source authors retain credit for the mechanism curation and depictions.
Please also cite Ribeiro AJM et al., “Mechanism and Catalytic Site Atlas
(M-CSA): a database of enzyme reaction mechanisms and active sites,” *Nucleic
Acids Research* 46(D1), D618-D623 (2018),
[doi:10.1093/nar/gkx1012](https://doi.org/10.1093/nar/gkx1012).

This project compared the complete retained Step 2 and Step 3 source panels.
`audit_m0173_partial.py` uses Python's standard library and the separately
pinned M0173 source-panel extractor to reproduce the 40 unique source-locator
pairs, the six Step 2 arrow-bound proposed edits, and the three-edit retained
projection replay. No network acquisition was performed for this comparison.

The alignment is a project-reviewed correlation of source position and identity
fields. Unmatched nodes are missing or redrawn evidence, not deleted or created
physical atoms. The result does not establish a physical atom map, a unique
water or hydrogen lineage, an exact peptide, a canonical participant map,
stereochemistry, an experimentally observed intermediate, or a complete
mechanism. Same-model review may contain correlated errors and is neither human
review nor statistical independence.
