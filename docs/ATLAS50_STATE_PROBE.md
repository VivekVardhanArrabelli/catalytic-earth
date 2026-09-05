# Atlas-50 source-bound state probe

**Status:** bounded computational development review; same-model informed challenge; no human or domain-expert review; no mechanism compilation, tier upgrade, or selection freeze.

This probe addresses the six representation questions left open by the computational panel review: M0064, M0106, M0107, M0212, M0753, and M0970. It supplies one small source-neutral sidecar contract for typed components and states, tethered carrier instances, and polymer/topology instances. It does not add those fields to mechanism-record v3 or alter any Phase A, Phase B, Atlas-3, Atlas-10, or registry artifact.

The implementing agent and informed source-challenge agent use the same model family. Their errors may be correlated. Agreement between them is not statistical independence, human review, or domain-expert review.

## Result

`PASS` and `SCOPED_PASS` apply only to the operation named in the report. They do not mean that a v3 record, balanced Rhea reaction, mechanism, tier, or structure applicability has been compiled. `ABSTAIN` keeps usable source metadata while blocking the requested operation.

| Case | Probe result | Allowed operations | Computational review recommendation | Required boundary |
|---|---|---|---|---|
| M0064 DNA topoisomerase III | `SCOPED_PASS` | `source_annotation` | `accept_proposed_include` | Same CHEBI:9160 identity on both sides does not establish before/after topology. Block topology-dependent mechanism and reaction-instance claims. |
| M0106 pyruvate dehydrogenase E1 | `SCOPED_PASS` | `source_annotation`, `source_scoped_mechanism_draft` | `accept_proposed_include` | Preserve CHEBI:83099 to CHEBI:83111 as the source-reported tethered state transition. The carrier accession, numbered lysine, and structural localization remain unknown. |
| M0107 aerobic CODH | `PASS` | `source_annotation`, `source_scoped_mechanism_draft` | `accept_proposed_include` | Preserve both M-CSA alternatives and mark Mo/Cu states as source proposals. `PASS` does not authorize an exact reaction instance or v3 compilation. |
| M0212 nitrogenase | `SCOPED_PASS` | `source_annotation`, `source_scoped_mechanism_draft` | `revise_with_evidence` | The generic contract represents component association and ATP-to-ADP state. Abstain from a complete FeMo/P-cluster state sequence and exact reactive atoms. |
| M0753 imidazole glycerol phosphate synthase | `SCOPED_PASS` | `source_annotation`, `source_scoped_mechanism_draft` | `revise_with_evidence` | Scope the exact handle to Q9X0C6 HisF with free ammonium. Do not claim a HisH-to-HisF channel state or full-complex mechanism. |
| M0970 peptidoglycan glycosyltransferase | `ABSTAIN` | `source_annotation` | `accept_fail_closed_exclusion` | Preserve the X00676 placeholder and mechanism alternatives. Block an exact polymer instance, n-to-n+1 state, initiation/elongation, and processivity. |

These are computational development recommendations using the Phase B decision vocabulary. They are not attributable Phase B submissions and do not change the frozen dispositions.

## Minimal contract

Every representation has the same five top-level fields:

- `components`: typed entities with source identifiers, roles, applicability scope, and evidence IDs;
- `assembly`: one of `single_source_component`, `fixed_multisubunit`, `cycle_coupled_association`, or `external_carrier_encounter`;
- `state_transitions`: before/after state IDs, typed transition, subject components, assertion scope, and evidence IDs;
- `tethered_carrier`: carrier owner, attachment residue/site, reactant/product state, structure localization, and status;
- `polymer_topology`: polymer reactant/product identity, qualitative event, before/after topology, chain lengths, initiation or elongation, processivity, and status.

The contract is source-neutral because its fields name relationships shared across cases rather than CODH-, nitrogenase-, topoisomerase-, or glycosyltransferase-specific concepts. Each contract kind defines clauses for three possible operations:

- `source_annotation` preserves source identity and bounded metadata;
- `source_scoped_mechanism_draft` permits a draft only when the state needed for that source projection is present and evidence-bound;
- `exact_reaction_instance` requires every participant/state field needed to identify the instance.

The evaluator derives `allowed_operations` from satisfied clauses. It returns `ABSTAIN` when the requested operation is not allowed, `SCOPED_PASS` when the requested operation is allowed but the scope is narrowed or other clauses remain missing, and `PASS` when the named target is fully satisfied. Every missing clause becomes a `mandatory_abstention` in the report.

Positive state transitions can reference only a state in the case's source extract. Source protein identities must exactly match the frozen Atlas-50 candidate identity. Context-only identities, such as P11961 in 1W85, cannot silently become M-CSA catalyst or carrier identities. Tests demonstrate that an invented state or substituted UniProt identity fails validation.

## Decision-relevant source distinctions

### Fixed CODH assembly versus ATP-coupled nitrogenase association

M-CSA M0107 identifies P19919, P19920, and P19921 and describes CODH itself as a dimer of heterotrimers with small iron-sulfur, medium FAD-containing, and large molybdopterin-containing subunits. The probe encodes this as `fixed_multisubunit`. Here, “fixed” means the source describes that complex as the enzyme assembly; it is not a kinetic lifetime claim. Its Mo(VI)-Cu(I) to Mo(IV)-Cu(I) and reoxidation transitions remain M-CSA mechanism proposals.

M-CSA M0212 and the primary 1N2C study instead describe Fe-protein/MoFe-protein association coupled to ATP hydrolysis and electron transfer. M-CSA further states that the complex dissociates. The probe encodes this as `cycle_coupled_association` and binds ATP-to-ADP to P00459. It withholds the complete FeMo/P-cluster state sequence because M-CSA itself says the electron pathway is poorly understood and the exact reactive atoms are unknown.

This is a source-supported generic distinction between assembly modes. It resolves the earlier false choice between flattening both records into prose and inventing nitrogenase-only fields.

### Tethered carrier without a carrier-structure invention

M-CSA M0106 and PMID 12795594 identify the E1-catalyzed transition from an E2 lysine-bound lipoyl group to an acetyldihydrolipoyl-lysine state. Those states are represented by CHEBI:83099 and CHEBI:83111.

The selected 1W85 structure contains P21873/P21874 E1 and P11961, an E2 peripheral subunit-binding domain. P11961 is recorded as `context_only`. It is not assigned as the mobile lipoyl carrier domain, carrier accession, numbered attachment site, or observed carrier state. This supports a source-scoped mechanism draft while blocking an exact carrier reaction instance and Tier-2 localization.

### HisF half-reaction without a channel claim

The exact M-CSA M0753 protein identity is Q9X0C6 HisF, the reaction explicitly contains free ammonium CHEBI:28938, and 2A0N contains HisF alone. The M-CSA description and PMID 11264293 also establish that the broader biological system has a HisH partner that generates ammonia.

The source handle can therefore be scoped to the HisF/free-ammonium cyclase half-reaction. HisH remains context only, with no source accession projected into the selected record. The probe does not represent ammonia-channel occupancy, intersubunit signaling, or the full coupled mechanism.

### Polymer/topology abstentions

M0064 reports CHEBI:9160 single-stranded DNA on both reaction sides and qualitatively says that DNA uncoils. Neither that identity-preserving reaction nor protein-only 1D6M gives initial and final topology. The primary paper supports a topology-changing reaction class but does not supply the missing state for the selected structure. Source annotation is allowed; topology-dependent mechanism and exact reaction-instance work are blocked.

M0970 names a polymeric acceptor with symbolic `n`, lipid II, and a leaving-group product, but the polymer product is an unnamed non-ChEBI `X00676` placeholder. Its API flag is `is_polymeric=false`. The two source proposals address local reaction alternatives, while 3VMT contains a Lipid II analog. None of those exact handles specifies n-to-n+1, initiation versus elongation, topology, or processivity. Only source annotation is allowed.

## Relationship to mechanism-record v3 and current kernels

The builder checks the live repository schema rather than assuming compatibility. Mechanism-record v3:

- rejects undeclared top-level properties;
- fixes `reaction.source_id` to Rhea;
- restricts participant IDs to numeric `CHEBI` or `RHEA-COMP` identifiers, excluding X00676;
- stores `components_summary` as a string.

The current v3 schema therefore cannot directly store the five structured probe fields. Existing `uncertainties`, `detail_abstention`, `claim_boundary`, biological-scope IDs, and reaction participants can preserve some boundaries, but prose alone cannot encode positive component/state applicability. The report is a sidecar probe and records `sidecar_probe_requires_schema_decision_before_kernel_compilation`. Atlas-3 remains on mechanism-record v2 and Atlas-10 follow-on records remain on v3.

## Evidence and limits

The exact six-entry M-CSA API response was retrieved on 2026-09-05: 97,870 bytes, SHA-256 `eb0b3cbf31dbca16a7c6be81fd5a0a7eaa6c3edbf63f030c911a01176d1cfa4e`. Eight cited PubMed records were retrieved in one official EFetch response: 68,364 bytes, SHA-256 `b64ca6a3ed37cc0950ddc5babcb2c0a6ad073cc8dfe800a336deeee8bfaa8262`. Total new external response data were 166,234 bytes, below the 30 MiB ceiling. No raw API response or article body is committed.

The RCSB conclusions reuse the URLs, byte counts, and hashes recorded in `data/atlas/atlas50/computational_review/panel_review.json`. Primary paper checks used official PubMed metadata and abstracts. They do not constitute full article-body adjudication or independent validation of M-CSA mechanism proposals.

## Build and API

Rebuild or check the report with:

```bash
python scripts/build_atlas50_state_probe.py
python scripts/build_atlas50_state_probe.py --check
PYTHONPATH=src python -m unittest tests.core.test_atlas50_state_probe -v
```

The Python API is:

```python
from catalytic_earth.atlas50_state_probe import (
    build_state_probe,
    validate_probe_spec,
    validate_state_probe,
)
```

`validate_probe_spec` checks the exact six source identities, evidence links, state catalog, representation references, clause coverage, receipt ceiling, and same-model review disclosure. `build_state_probe` derives allowed operations, missing clauses, mandatory abstentions, and dispositions. `validate_state_probe` rebuilds the full report and rejects any difference.

The canonical inputs and result are:

- `data/atlas/atlas50/state_probe/spec.json`
- `data/atlas/atlas50/state_probe/report.json`
- `src/catalytic_earth/atlas50_state_probe.py`
- `scripts/build_atlas50_state_probe.py`
- `tests/core/test_atlas50_state_probe.py`
