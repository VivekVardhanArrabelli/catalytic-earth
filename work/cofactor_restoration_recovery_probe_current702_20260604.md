# Cofactor Restoration Recovery Probe

Backend: `alphafold_db` | source audit: `v3_predicted_geometry_robustness_audit_current702_20260529` | threshold: `0.4115`

## Question

Of the cofactor_apo_loss lost primary rows, how many recover if we restore the cofactor onto the predicted apo backbone (upper bound)?

## Result

- cofactor_apo_loss targets: 22
- recovered under perfect restoration: 22 (fraction 1.0)
- Wave 1 readthrough (excl. m_csa:497/750): 20/20
- apo control rescore matches audit: True

## Interpretation

Restoring the cofactor onto the predicted backbone recovers 22/22 cofactor_apo_loss lost primary rows (upper bound). A high fraction confirms the predicted backbone is faithful and the missing cofactor is the load-bearing loss, so a cofactor-restoration step (dock/graft the cofactor, or a cofactor-presence channel) is the right Problem-2 lever. ESMFold2's better apo side-chains would help this residual backbone term, but cannot supply the cofactor.

this assumes perfect cofactor placement relative to the predicted active site, so the recovery count is an upper bound; real docking is imperfect

This is a counterfactual diagnostic: it reuses the frozen threshold and fingerprints, selects nothing, and trains nothing.
