# Fold-Augmented P10746 Source-Feature Refresh Audit - current702

Run: 2026-06-03T07:11:19Z

Lever 3 source-record refresh for the remaining `m_csa:204`/P10746 fold-only caveat. This checks whether the current UniProtKB source record exposes source-backed active-site or binding-site features that could support a non-residue interaction sidecar review path; it does not create a sidecar or change deployment state.

## Status

- p10746_source_feature_refresh_no_eligible_features
- Source: https://rest.uniprot.org/uniprotkb/P10746.json
- HTTP status: 200
- Response SHA-256: `bdf9509aff48ad7c9276be3c373100bbb4d7dbf368b97ac46ab8650d51f689aa`
- Total UniProt features: 63
- Eligible source-feature rows: 0

## Audited Feature Types

- Active site
- Binding site
- Site
- Modified residue
- Metal binding

## Decision

- No P10746 non-residue sidecar review path opened from this refreshed source record.
- No sidecar was created or copied.
- No threshold, label, registry, ontology, import, model-weight, or heldout-training surface changed.

## Next Gate

- Keep `m_csa:204`/P10746 fold-only unless a separate approved non-residue interaction source or an explicit deployment caveat decision is supplied.
