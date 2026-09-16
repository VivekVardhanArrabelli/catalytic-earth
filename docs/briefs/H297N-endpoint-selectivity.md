# Does H297N racemization nondetection establish loss of every catalytic capability?

Generated from a real query run. Source commit `57d688af01b3edfbe69c35258ddf6d61b089b18d`.

## Question

Mandelate racemase (*P. putida*, M-CSA M0187) H297N shows no detectable
racemase activity. Does that establish that the variant has lost all catalytic
capability?

## Source-scoped answer

**No.** Within the inspected published reports, H297N still catalyses
stereospecific alpha-proton exchange with solvent deuterium on **(S)**-mandelate
while racemization is undetected. The impairment is endpoint-selective, not
total. The record does not resolve the molecular cause.

This is the case's existing reviewed adjudication (`claim_status: supported`,
selected alternative `endpoint-selective-impairment`, basis discriminant
`retained-S-exchange`), quoted as a curated conclusion tied to case
`atlas10.mandelate-racemase-pputida.enolate`. The endpoint filter selected the
two observations below; **it did not recompute the adjudication** — the full and
filtered runs return the same `evidence_payload_sha256`
`dd62c8fbbde725e8567a6a2462cb456c26b5c77c4b239ed18ad3e05f468e3241`.

## Decisive observations

Filter: `--variant H297N --endpoint isotope_exchange` → 2 of 6 case observations.

| Observation | Substrate | Result | Source witness |
|---|---|---|---|
| `H297N-S-exchange` | (S)-mandelate | **measured**, 3.3 fold lower than wild type | "H297N catalyzes the stereospecific exchange"; "3.3-fold less"; "At pD 7.5"; "D2O" |
| `H297N-R-exchange` | (R)-mandelate | **not detected** | "(S)- but not (R)-mandelate" |

Conditions as reported: pD 7.5, D₂O. Both observations cite **PMID 1909893**.

The retained (S)-exchange is what counters complete abolition of catalysis.
Exchange is *not* net racemization, and the differing outcome by enantiomer
assigns no net racemization direction and no elementary proton-transfer timing.

The (R)-mandelate nondetection carries **no numeric detection limit** in the
source. It is not a rate of zero.

## Structure context

The case carries deposited structure **1MNS** (X-ray, 2.0 Å) as reference
context for site geometry, linked to `P11444:H297` and `P11444:K166`. Its
context flags record an inhibitor-bound, chemically modified static structure —
usable for site geometry, not for substrate turnover.

1MNS's own primary citation is **PMID 8292591**, a different source role from
the functional paper above. There is no H297N mutant structure here; reference
structure inspection is not an observation of the mutant.

## Sources and artifacts

- Functional observations: `paper:PMID:1909893`
- Structure reference: `1MNS`, primary citation `paper:PMID:8292591` (structural role)
- Evidence set: `atlas10-m0187-functional-evidence-v1`
- Query output sha256: `4f65dea0783252a80fc33556cd49f84a7fd093c4f0a42d40aee92be724ba2210`

## Unresolved

- The molecular cause of the selective loss.
- Any net racemization direction or proton-transfer timing.
- Whether flux is truly absent for (R)-mandelate — the detection limit is unknown.
- Any mutant structure. None exists in this record.

## Reproduce

```sh
catalytic-earth atlas-mechanism-evidence --variant H297N --endpoint isotope_exchange
```

Runs from an installed wheel in any directory. Add `--output <new file>` to save
the JSON. Drop the filters to see the full six-observation case.

*A curated demonstration case, not held-out validation and not a benchmark.*
