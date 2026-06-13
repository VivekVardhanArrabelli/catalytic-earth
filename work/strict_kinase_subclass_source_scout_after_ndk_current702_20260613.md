# Strict Kinase Subclass Source Scout After NDK (2026-06-13)

Status: non-destructive source-supply scout; no labels generated or admitted.

Guardrails: broad EC 2.7 remains blocked; EC/name/Rhea/reaction/feature handles are scout/admission context only; predictive_evidence remains empty.

## Lane Summary

### deoxynucleoside_kinase
- Reviewed total: 278
- Sampled with UniProt entry JSON: 40 / 40
- Likely wireable sample: 39 / 40 (boundary fraction 0.025)
- Mechanism handles: Rhea 40, phosphoryl reaction text 40, active/binding site 40, family text 40
- Top ECs in sample: `{'2.7.1.21': 23, '2.7.1.113': 15, '2.7.1.74': 12, '2.7.1.76': 11, '2.7.1.-': 3, '2.7.1.145': 1}`
- Recommendation: backup split; mechanism-rich sample, but smaller reviewed supply and one sampled boundary signal

### ghmp_small_molecule_kinase
- Reviewed total: 613
- Sampled with UniProt entry JSON: 40 / 40
- Likely wireable sample: 37 / 40 (boundary fraction 0.0)
- Mechanism handles: Rhea 40, phosphoryl reaction text 40, active/binding site 37, family text 40
- Top ECs in sample: `{'2.7.1.36': 21, '2.7.1.6': 11, '2.7.1.39': 7, '2.7.1.157': 1}`
- Recommendation: backup split; clean sampled boundary profile, but smaller reviewed supply and fewer sampled active/binding-site handles than ASKHA

### askha_sugar_acetate_kinase
- Reviewed total: 667
- Sampled with UniProt entry JSON: 40 / 40
- Likely wireable sample: 39 / 40 (boundary fraction 0.0)
- Mechanism handles: Rhea 40, phosphoryl reaction text 40, active/binding site 39, family text 40
- Top ECs in sample: `{'2.7.1.1': 37, '2.7.1.30': 2, '2.7.1.2': 1, '2.7.1.147': 1}`
- Recommendation: preferred next split; largest reviewed supply among sampled strict lanes, 39/40 likely wireable, and zero sampled boundary signals

## Recommendation

Prefer `askha_sugar_acetate_kinase` for the next full gated lane: it has 667 reviewed rows and the strict sample was 39/40 likely wireable with no sampled boundary signal. Keep GHMP small-molecule kinase and deoxynucleoside kinase as backups, but do not broad-wire EC 2.7 or merge subclasses.

Next exact action: implement ASKHA/sugar-acetate kinase fingerprint/ontology and disambiguation guards, re-freeze 29fp OOS preregistration, run tests, produce a non-destructive preview, and apply only if novelty/governor/dedup/trust-tier gates pass.
