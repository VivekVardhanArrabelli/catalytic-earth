# M0173 source-panel transformation attribution

The retained mechanism and MRV panels derive from the **Mechanism and Catalytic
Site Atlas (M-CSA)**, [entry M0173, trypsin](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/173/),
available under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
The source authors retain credit for the mechanism curation and depictions.

This project extracted the complete Step 1 and Step 2 depiction graphs from the
existing snapshot and authored a six-edit replay with source-step/arrow bindings.
No new source acquisition was performed. `source_inventory.json` records the
retained snapshot and embedded scheme hashes; `audit_m0173.py` reproduces the
extraction and checks the reviewed edits using only Python's standard library.

The correspondence is a project-reviewed alignment of source panel locators.
Generic R groups, residue aliases and source numbering remain unresolved. It
establishes neither an exact physical peptide nor canonical participant identity,
stereochemistry, experimental intermediate observation or a complete catalytic
path. Same-model agent review may contain correlated errors and is not human
review or statistical independence.
