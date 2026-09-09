# 6HA3 E160Q/F6P-ThDP study context

This packet preserves a source-reviewed, study-scoped association between the
deposited human transketolase E160Q/F6P-ThDP arrangement in PDB 6HA3 and three
separate measurements reported in the same study: acid-quench intermediate
accumulation, reversible F6P-ThDP formation kinetics, and X5P/R5P steady-state
turnover. It does not make the crystal and solution states identical or assign
any measured rate to the deposited distortion.

## Sources and retention

- RCSB PDB entry 6HA3, current mmCIF revision 1.4: retained byte-for-byte as
  `6HA3.cif`; PDB archive data are used under the CC0 1.0 convention with
  structure-author and primary-citation attribution preserved.
- Dai et al., *Low-barrier hydrogen bonds in enzyme cooperativity*, Nature
  (2019), DOI `10.1038/s41586-019-1581-9`, PMID `31534226`: the PubMed record,
  Nature preview/extended-data legends, Supplementary Information, and Extended
  Data Table 2 were inspected locally. Publisher bodies are not redistributed;
  their URLs, hashes, byte counts, inspection depths, and precise locators are
  retained in the inventory and receipt ledger.

The projection is project-authored factual extraction. The Nature page exposed
data-availability and extended-data content but not the complete main article.
The 13-page supplement was text-extracted in full; the three relevant methods
pages and the kinetic table were rendered and visually checked.

## Scientific boundary

The allowed join is same study, same reported E160Q variant, and source-assigned
F6P-ThDP species. Exact protein-preparation equivalence, solution population,
protonation, symmetry-expanded active-site geometry, causal benefit of the
24.19-degree coordinate-derived distortion, F6P full-cycle turnover, and an
M0219 elementary-step assignment remain unestablished.

The apparent scissile-bond distance (1.604779 angstrom) and out-of-plane
deviation are descriptive facts of the retained current deposit. T6F atom
occupancies are nonuniform and are not treated as a solution intermediate
fraction. The four T6F `struct_conn` rows are metal coordination, not
protein-ligand covalency.

## Reproduce

```bash
python scripts/validate_atlas_study_context.py
```

The command validates retained hashes, exact M0219 record-scope binding,
coordinate-derived atom/geometry facts, connection typing, observation/subject
identity, explicit non-promotion to a proposal step, and the manual review pins.
