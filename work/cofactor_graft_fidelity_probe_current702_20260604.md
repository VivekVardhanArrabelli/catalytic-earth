# Cofactor Graft Fidelity Probe

Backend: `alphafold_db` | source probe: `v3_cofactor_restoration_recovery_probe_current702_20260604`

## Question

Would a real rigid cofactor graft keep the cofactor proximal, or does the predicted pocket distort it? (Refines the perfect-placement upper bound.)

## Result

- targets: 22
- idealized recovered (upper bound): 22
- graft-realistic recovery: 19
- active-site faithful (internal RMSD <= 1.5 A): 20
- distorted active-site rows: ['m_csa:213', 'm_csa:854']

## Interpretation

A real rigid cofactor graft realistically recovers 19/22 rows (vs the 22/22 perfect-placement upper bound). 20/22 predicted active sites are faithful (internal distance RMSD <= 1.5 A), so most pockets hold the grafted cofactor in a near-native pose. The 2 distorted rows (m_csa:213, m_csa:854) are where the predicted backbone itself is off — exactly the rows where a better structure predictor (the ESMFold2 secondary lever) could help, since cofactor restoration alone is insufficient there.

this is a coordinate-free fidelity proxy on CA/centroid internal distances, not a full atom-level superposition; numpy is unavailable in this environment, and proximal-ligand atom coordinates are not stored in the geometry features. The true atom-level graft (superpose on catalytic residue atoms, transplant cofactor atoms, recompute proximity) is the next escalation; predicted heldout CIFs are already staged locally under artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/queries_all_heldout/

Coordinate-free fidelity proxy: no superposition, no model fit, no threshold selection, no new heldout read.
