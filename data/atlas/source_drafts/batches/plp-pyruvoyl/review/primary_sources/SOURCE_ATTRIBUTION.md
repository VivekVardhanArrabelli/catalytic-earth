# Primary source attribution for the M0049 audit

This directory preserves two official Protein Data Bank structure records and one official UniProt record for a narrow, record-level observation of the processed pyruvoyl state in M-CSA entry M0049.

- **Current structure:** RCSB PDB [1PYA](https://www.rcsb.org/structure/1PYA), DOI [10.2210/pdb1pya/pdb](https://doi.org/10.2210/pdb1pya/pdb). The retained current mmCIF came from <https://files.rcsb.org/download/1PYA.cif> and identifies revision 2.1 dated 2024-11-20.
- **Historical structure:** wwPDB 1PYA revision 1.3, dated 2017-11-29. The retained decoded mmCIF came from the official versioned gzip at <https://files-versioned.wwpdb.org/pdb_versioned/data/entries/py/pdb_00001pya/pdb_00001pya_xyz_v1-3.cif.gz>.
- **Structure citation:** Gallagher, Rozwarski, Ernst and Hackert, “Refined structure of the pyruvoyl-dependent histidine decarboxylase from Lactobacillus 30a,” *Journal of Molecular Biology* 230 (1993), 516–528, DOI [10.1006/jmbi.1993.1168](https://doi.org/10.1006/jmbi.1993.1168), [PubMed 8464063](https://pubmed.ncbi.nlm.nih.gov/8464063/).
- **Curated protein record:** [UniProtKB P00862](https://www.uniprot.org/uniprotkb/P00862/entry), release 2026_03, entry version 136. This record is used only in the project-authored audit mapping; it is not presented as a primary structure or primary research article.
- **Historical sequence citation:** Huynh, Recsei, Vaaler and Snell, “Histidine decarboxylase of Lactobacillus 30a. Sequences of the overlapping peptides, the complete alpha chain, and prohistidine decarboxylase,” *Journal of Biological Chemistry* 259 (1984), 2833–2839, [PubMed 6698997](https://pubmed.ncbi.nlm.nih.gov/6698997/). Its inspected abstract reports the historical Ser81–Ser82 cleavage bond; M-CSA separately uses Prv-82.

PDB archive data are available under the [CC0 1.0 Universal Public Domain Dedication](https://creativecommons.org/publicdomain/zero/1.0/); see the [RCSB PDB usage policy](https://www.rcsb.org/pages/policies). UniProt data are available under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); see the [UniProt copyright notice](https://www.uniprot.org/help/license).

Official PubMed XML abstract responses and RCSB API JSON responses were inspected but are not redistributed here. `source_inventory.json` and `acquisition_receipts.json` retain their URLs, byte counts, SHA-256 values, times, and `repository_path: null`. The complete response bodies remain local-analysis-only. No publisher full text was acquired.

`evidence_projection.json` is project-authored and binds the exact retained source hashes. It separates chain-F author PYR82, processed label position 1, current canonical P00862 Ser83, the historical Ser81–Ser82 cleavage bond, and M-CSA Prv-82. The typed annotation asserts only the deposited processed structure site and leaves sequence mapping unasserted.
