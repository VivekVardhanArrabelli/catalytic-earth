# ePK external stress tranche review - 2026-05-20

Subagent D review-only output. No production label registries, fingerprint registries, `data/registries/mechanism_fingerprints.json`, artifact migrations, or Git history were edited.

## Answer

1. Best fresh stress candidates:

   `4EKK` is the only primary fresh nonrepeat row found in the inspected artifacts. It stresses substrate-role direction because it has ANP gamma to Ser/Thr hydroxyl geometry on partner chains but source validation does not support an explicit kinase-substrate assignment.

   The best regression-context stress rows are `7ZE5`, `7B56`, `7ZDT`, `2JJ2`, `4HPU`, `9L3U`, and `7T55`. They stress ATP/Mg or ANP/Mg false positives, tight gamma-to-Ser/Thr geometry, folded-protein or inhibitor-chain role confusion, and broad text-query source leakage. These rows were already observed in earlier broad-stress diagnostics, so they are useful controls but not clean performance evidence.

2. Freeze rule before scoring:

   Freeze the exact PDB ids, source artifacts, ligand state, acceptor chain/residue, gamma-associated chain, and nearest gamma distance before any new run. Run only already frozen review-only rules. Report every frozen row. Do not tune thresholds, role rules, ligand-analog policy, source filters, or repairs after seeing outcomes.

3. Evidence separation:

   Predictive/import evidence may include only text-free structure fields: local ATP/ANP or ATP-analog gamma context, local metal context, Ser/Thr/Tyr hydroxyl acceptor identity, gamma-to-acceptor distance, chain/entity topology, chain length, and pre-registered counteraxes.

   Review-only context includes PDB titles, RCSB/UniProt query terms, UniProt names, EC/Rhea identifiers, mechanism prose, source-validation labels, known-counterexample status, and candidate-specific repair or expert notes.

4. Leakage status:

   Current ePK review-only rules can be run on this tranche only as a review-only diagnostic. `4EKK` can be used as the primary future unified-rule probe if the list is treated as frozen now. The other rows are regression context because prior rule outcomes are already known.

5. Still forbidden:

   No candidate is import-ready or countable. No calibrated ePK score, selected threshold, clean held-out performance claim, analog/product-state activation, external hard-negative scored re-audit, registry edit, or production scoring claim is allowed.

## Candidate packet

| Candidate | Role in tranche | Main stress axis | Terminal review-only decision |
| --- | --- | --- | --- |
| `4EKK` | Primary fresh nonrepeat | ANP/Mg substrate-role direction false positive | Selected for future review-only unified-rule probe |
| `7ZE5` | Regression context | ABC transporter ATP/ANP/Mg false positive | Retain as review-only counterexample |
| `7B56` | Regression context | Folded-protein role false hit | Retain as review-only counterexample |
| `7ZDT` | Regression context | ATP-bound CydDC local role-context decoy | Retain as review-only counterexample |
| `2JJ2` | Regression context | F1-ATPase ANP false positive | Retain as review-only counterexample |
| `4HPU` | Regression context | Kinase/inhibitor partner-chain role decoy | Retain as review-only counterexample |
| `9L3U` | Regression context | Tight Thr-gamma broad-query counterexample | Retain as review-only counterexample |
| `7T55` | Regression context | ATP Thr near-gamma large/same-chain decoy | Retain as review-only counterexample |

## Recommendation

Run the tranche now only as review-only stress regression and diagnostic coverage. Do not use it as clean performance evidence. If the main loop needs clean held-out evidence, source a new not-yet-observed tranche, freeze it before any probe, then run the frozen scorer without repairs or threshold tuning.
