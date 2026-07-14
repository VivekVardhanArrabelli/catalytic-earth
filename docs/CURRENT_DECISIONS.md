# Current Decisions

## 2026-07-13: Truth reset — canonical claims, evidence tiers, and exposure state govern historical results

Decision: preserve the full-atlas North Star while correcting the scientific
record before further expansion. `CLAIMS.md`, `ERRATA.md`,
`docs/ATLAS_TRUTH_POLICY.md`, `data/governance/claim_ledger.json`, and the
append-only `data/governance/exposure_ledger.jsonl` are the canonical truth
surfaces. Older entries remain historical evidence but do not override them.

Durable rulings:

1. The atlas is the mission; the typed IR/compiler is its engine and benchmarks
   are internal truth controls.
2. Reactions, source mechanisms, hypotheses, families/fingerprints, protein
   records, and experimental observations are counted separately.
3. The 10,001 total means 8,305 positive fingerprint assignments plus 1,696 OOS
   protein-label records, not 10,001 mechanisms.
4. The “about 2% of mechanism space” claim is retracted because neither unit nor
   denominator was defined.
5. The 76.19% chemistry endpoint is coarse cofactor-bucket consistency; exact
   fingerprint recovery was 65/210 (30.95%).
6. The June 28 M-CSA result is retrospective analysis of an already exposed,
   now exhausted surface, not a never-touched independent validation.
7. The June 29 Swiss-Prot/PDB-holo surface is spent EC-proxy evidence, not
   independent stepwise-mechanism gold; report 45/64 overall, 2/16 metal, and
   2/72 OOS false positives together.
8. Automated geometry/residue checks are computational consistency evidence,
   not expert or experimental verification.
9. An exposed or exhausted surface never becomes fresh through renaming,
   branching, a new agent, a new endpoint, or a later preregistration.
10. Expansion and new performance headlines stay frozen until the
    truth-governance, reproducible-environment, and live-manifest gates pass.

No historical result was deleted. No registry, ontology, threshold, model, or
scientific artifact was changed by this decision.
