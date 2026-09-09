# Structural-context source attribution

This is a computational source review of two existing Atlas-10 cases. It is
not independent expert review, new biological coverage or a new experiment.

- `1PQ5` and `1SUP` are reused from the retained CC0 wwPDB/RCSB mmCIF archives
  already acquired for Atlas-10. The specification binds each compressed file
  by its exact SHA-256. Deposited coordinates, identifiers, per-atom occupancy,
  B factors, connections, modification features and selected metadata are
  derived from those bytes. Raw coordinate archives are not added to the wheel.
- Protein/site identities, source roles and distinct author/mmCIF/UniProt
  numbering are reused from the exact frozen Atlas-10 kernel. That source
  bundle remains unchanged and retains its original M-CSA/UniProt attribution.
- Schmidt et al., JBC (2003), DOI `10.1074/jbc.M306944200`, PMID `12937176`:
  a six-page primary-paper copy hosted on coauthor Wojciech Rypniewski's
  institutional page was inspected for the product-fragment context and
  Table II's mapping of the pH-5 dataset to 1PQ5. One local capture used
  318,096 bytes. Its URL, response hash and date are in
  `acquisition_receipts.json`. The PDF stays outside the repository and wheel.
  The specification contains a short witness and factual projection with
  precise article locators. Article-level summaries are not substituted for
  atom-specific deposited occupancy or deposition resolution.
- Gallagher et al., Acta Crystallographica D (1996), DOI
  `10.1107/S0907444996007500`, PMID `15299573`: the official RCSB entry and
  primary abstract were inspected. The complete article was not inspected.
  The covalent-modification assertion comes directly from deposited
  `_struct_conn` and `_pdbx_modification_feature` records, not inferred prose.

Official entry pages: [1PQ5](https://www.rcsb.org/structure/1PQ5) and
[1SUP](https://www.rcsb.org/structure/1SUP). Web discovery is distinct from the
one-file capture ledger. No source drawing is mapped to a deposited atom.
No current coordinate archive is asserted identical to the original paper's
coordinate bytes. No hydrogen-bond, active fraction, co-occupancy, protonation,
energetic competence or productive design restraint is inferred from distance.
