# Predicted Geometry Robustness Audit

Status: `blocked`

Blocker: `local_esmfold_runtime_or_weights_unavailable`

Detail: ESMFold inference is not run by this audit unless a local runtime and weights are already staged. No model-weight download was attempted. Stage ESMFold PDB/mmCIF files keyed by current702 sequence_id/accession, or install a local esmfold runtime, then add that backend as a coordinate supplier.
