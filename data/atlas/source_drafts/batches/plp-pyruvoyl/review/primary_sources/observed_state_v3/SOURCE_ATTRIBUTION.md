# Observed-state v3 source attribution

This directory contains additive, record-level evidence for deposited chemical states. It does not validate an exact reaction instance, source-step trajectory, catalytic role, protonation state, physiological direction, or canonical mechanism.

The retained `1L6G.cif` and `1PWH.cif` files are Protein Data Bank archive data obtained from the official RCSB download service. PDB archive data are provided under the [CC0 1.0 Universal dedication](https://creativecommons.org/publicdomain/zero/1.0/); see the [RCSB PDB usage policies](https://www.rcsb.org/pages/policies). Cite the corresponding entries and primary papers:

- [PDB 1L6G](https://www.rcsb.org/structure/1L6G), DOI `10.2210/pdb1L6G/pdb`; Watanabe et al., *J. Biol. Chem.* (2002), PMID `11886871`, DOI `10.1074/jbc.M201615200`.
- [PDB 1PWH](https://www.rcsb.org/structure/1PWH), DOI `10.2210/pdb1PWH/pdb`; Yamada et al., *Biochemistry* (2003), PMID `14596599`, DOI `10.1021/bi035324p`.

`UniProt_P10724.json` is redistributed under the [Creative Commons Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/). Cite [UniProtKB P10724](https://www.uniprot.org/uniprotkb/P10724/entry) and the [UniProt license terms](https://www.uniprot.org/help/license). It supplies curated protein identity only; it is not primary structure or mechanistic evidence.

The two `PMID_*_projection.json` files are project-authored factual projections of inspected official PubMed abstracts. The raw PubMed XML and publisher article bodies are not redistributed or bound as repository evidence. Each projection records the official citation, raw-response hash, retrieval scope, and claim limits.

The M0049 v3 projection reuses, without modifying, the source files and attribution already retained in the parent `primary_sources` directory and the official M-CSA M0049 snapshot. M-CSA data are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); see the batch source attribution for its citation and entry URL.

All `evidence_projection.json` and source-inventory files in this directory are project-authored factual projections released with this repository. Their review pins validate the exact retained bytes and declared scope; they do not make the source representations statistically independent.
