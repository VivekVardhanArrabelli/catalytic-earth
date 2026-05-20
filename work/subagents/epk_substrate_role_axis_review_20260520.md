# ePK Substrate-Role / Substrate-Identity Axis Review

Date: 2026-05-20

Scope: review-only synthesis for ePK substrate-role / substrate-identity. No production registries, fingerprint registries, artifact migrations, tests, or git history were edited.

## Decision

No source-free substrate-role or substrate-identity axis is ready for a frozen ePK policy.

A review-only composite can be sketched that retains the current named positives and rejects the named false hits, but the evidence does not support freezing it. The apparent pass is assembled from narrow peptide identity, bounded ligand-asymmetry role, current-only protein-substrate role, and weak residue-position substrate-mode heuristics. The general substrate identity blocker is fundamental with current evidence: local topology, chain length, residue class, and author position do not yet uniquely identify substrate role across peptide, folded protein, kinase-kinase, same-chain, and transporter-like contexts.

Recommendation: continue ePK substrate-role work for one preregistered review-only experiment, then pivot if it fails. Do not calibrate thresholds, activate scoring, import labels, or edit registries.

## Features That Passed Bounded Controls

- Short peptide acceptor identity passed current and exact-query review controls. It retained `6Z3R`, `8OXM`, `8OXO`, `1O6K`, and `1O6L`, with zero nonaccepted/sibling false hits and zero imported external hard-negative non-abstentions. Blocker: it is peptide-mode only.
- Heteromeric ligand-asymmetry role passed current role controls. It retained three source-valid role hits, blocked `7M0T`, `7M0W`, and `8ZN6`, and had zero sibling role-asymmetry false hits. Blocker: it assigns role direction, not acceptor identity.
- Heteromeric acceptor-chain counteraxis passed a broader 50-structure heteromeric plus 36-row sibling control surface with zero residual nonaccepted or sibling false hits. Blocker: source-free kinase/substrate role assignment is still missing.
- Current protein-substrate role discriminator retained `1IR3`, `2PHK`, and `5HVK` with zero current protein-role control false hits. Blocker: source-expansion stress later false-hit `7B56` under relaxed protein-role logic and found no broad source-valid folded-protein positive.
- MEK/ERK Tyr or N-terminal substrate-mode retained `1IR3`, `5HVK`, `6Z3R`, `9UUR`, and `9UUX`; blocked `2JJ2`, `4HPU`, `7B56`, and `7ZDT`; and inherited topology blocking for `7CAG`, `7ZDU`, `7ZE5`, and `8BMS`. Blocker: residue class and author-position are weak identity features, fresh controls were topology-confounded, and `4EKK` is unresolved.
- Unified review-only scoring retained `1IR3`, `1O6K`, `1O6L`, `2PHK`, `5HVK`, `6Z3R`, `8OXM`, and `8OXO` on the current surface with zero current control false non-abstentions. Blocker: broad stress still produced source-validation counterexamples.

## Features That Failed Or Remain Blocked

- Nearest gamma-to-oxygen acceptor geometry false-hit 11 sibling controls: `1TZ6`, `1WKL`, `3Q86`, `3R5F`, `4XYJ`, `5C1O`, `5XZ8`, `8W2H`, `8W2J`, `9OAN`, and `9PFY`.
- Heteromeric topology plus gamma distance alone hit nonaccepted or ambiguous rows: `7M0T`, `7M0W`, and `8ZN6`.
- Source-free chain topology role inference remains unsafe against same-accession phosphosite control risks: `3Q4Z`, `4I94`, and `5XD6`.
- Naive MEK/ERK broad role failed on `2JJ2`, `4HPU`, `7B56`, `7CAG`, `7ZDT`, `7ZDU`, `7ZE5`, and `8BMS`.
- Topology ambiguity counteraxis passed the bounded `7CAG`/`8BMS` residual check, but broader stress left `2JJ2`, `4HPU`, `7B56`, and `7ZDT` as residual false hits.
- Relaxed generic polymer identity and relaxed folded-protein role both fail on `7B56`. The length-band counteraxis repairs `7B56` only in the source-expansion subset, not as a general ePK substrate identity rule.
- Unified broad stress is not clean: source-validation counterexamples include `2JJ2`, `4HPU`, `7B56`, `7T55`, `7T56`, `7T57`, `7ZDT`, `7ZDU`, `7ZE5`, `9L3M`, `9L3U`, and next-tranche `4EKK`.

## Decisive Rows

Decisive positives:

| Row | Why it matters |
| --- | --- |
| `1IR3` | Current protein-substrate positive; retained by unified and substrate-mode surfaces. |
| `5HVK` | Heteromeric protein-substrate positive and central role-direction test. |
| `6Z3R` | Current short-peptide positive retained by peptide identity and substrate-mode. |
| `8OXM` | Current short-peptide positive retained by peptide identity. |
| `8OXO` | Current short-peptide positive retained by peptide identity. |
| `9UUR` | Source-reviewed MEK/ERK Tyr phosphosite positive retained by substrate-mode. |
| `9UUX` | Source-reviewed MEK/ERK Tyr phosphosite positive retained by substrate-mode. |
| `1O6K` | Source-expansion peptide positive retained by short-peptide role axis. |
| `1O6L` | Source-expansion peptide positive retained by short-peptide role axis. |

Additional context: `2PHK` is a retained current artifact positive but was not in the requested decisive row list. `3TM0` remains ligand-analog excluded and should not be used as production-positive substrate identity evidence.

Decisive negatives and controls:

| Row | Why it matters |
| --- | --- |
| `7B56` | Most decisive blocker: mid-length folded/polymer false hit for relaxed polymer and relaxed protein-role rules. |
| `2JJ2` | Large chain context with local ligand on acceptor; blocks generic role/identity assumptions. |
| `4HPU` | Nonpositive source-expansion control blocked by peptide identity and substrate-mode. |
| `7ZDT` | Nonpositive large-chain control; residual for topology-only rule. |
| `7CAG` | Transporter/topology false hit blocked by topology ambiguity. |
| `8BMS` | Transporter/topology false hit blocked by topology ambiguity. |
| `7M0T` | Fresh nonrepeat control blocked by substrate-mode but topology-confounded. |
| `7M0W` | Fresh nonrepeat control blocked by substrate-mode but topology-confounded. |
| `9UW4` | Fresh nonrepeat control blocked by substrate-mode but topology-confounded. |

## Next Experiment

Run `epk_fresh_nonconfounded_folded_substrate_role_identity_stress_v1_review_only`.

Pre-register a fresh outside-query tranche enriched for source-reviewed heteromeric ePK or kinase-substrate co-complexes with non-peptide folded protein substrates. Exclude same-chain topology-confounded hits from success evidence and track them only as controls. Apply source validation only as labels after local features are computed.

Materialize these source-free features: gamma-to-acceptor distance, acceptor-chain nucleotide/metal context, gamma-chain nucleotide/metal context, chain/entity disjointness, acceptor chain length band (`<=40`, `41-119`, `>=120`), gamma chain size, gamma larger than acceptor, topology ambiguity, tyrosine mode, N-terminal Ser/Thr/Tyr mode, and ligand-analog exclusion.

Candidate composite to test, review-only:

```text
gamma_distance_within_candidate_cutoff
AND not_ligand_analog
AND not_topology_ambiguous
AND (
  short_peptide_acceptor_identity
  OR heteromeric_ligand_asymmetry_role_with_source_free_acceptor_identity
  OR tyr_or_n_terminal_substrate_mode
)
```

Success requires all decisive positives retained, all decisive false hits rejected, zero sibling false hits, external hard negatives abstaining or rejecting, at least one fresh non-topology-confounded source-valid folded-protein substrate positive retained, and no fresh nonpositive source-validation counterexample passing.

Failure should trigger a pivot away from substrate-role/source-free identity as the immediate ePK blocker.
