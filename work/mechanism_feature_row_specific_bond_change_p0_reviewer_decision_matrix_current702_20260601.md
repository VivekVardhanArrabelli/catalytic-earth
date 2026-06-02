# Mechanism Feature Row-Specific Bond-Change P0 Reviewer Decision Matrix - current702

Run: 2026-06-02T08:15:33Z

Review-only decision matrix for P0 source-evidence rows where official Rhea/UniProt checks did not provide a Rhea cross-reference. It defines the reviewer provenance gate without approving rows or changing feature contracts.

## Status

- p0_reviewer_decision_matrix_copy_ready_reviewed
- Decision rows: 3
- Rows with UniProt matching EC activity: 3
- Rows with existing reviewer ID: 3
- Copy-ready approved decisions: 3
- Feature-contract consumable rows: 3

## Decision Rows

| row | accession | events | readiness blockers | available decisions |
| --- | --- | ---: | --- | ---: |
| m_csa:5 | P08819 | 1 |  | 3 |
| m_csa:11 | P0A6C1 | 4 |  | 3 |
| m_csa:169 | P27487 | 4 |  | 3 |

## Interpretation

- 3 unresolved P0 Rhea rows now have an explicit reviewer decision matrix; copy-ready rows reflect reviewer provenance recorded in the sidecar.
- Use copy-ready decisions only through split-filtered train/cal feature materialization; heldout M-CSA rows remain excluded.
