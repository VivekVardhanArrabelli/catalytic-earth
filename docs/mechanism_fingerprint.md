# Mechanism Fingerprint Language

## Purpose

A mechanism fingerprint is a compact, auditable representation of how an enzyme
is hypothesized to catalyze chemistry. It is designed to sit below EC numbers and
above atom-level simulation.

## Minimal Fingerprint

```json
{
  "id": "ser_his_asp_hydrolase",
  "name": "Ser-His-Asp/Glu hydrolase triad",
  "enzyme_space": ["esterases", "lipases", "cutinases", "proteases"],
  "active_site_signature": [
    {"role": "nucleophile", "residue": "Ser", "constraints": ["near His"]},
    {"role": "base", "residue": "His", "constraints": ["near acid"]},
    {"role": "acid", "residue": "Asp/Glu", "constraints": ["H-bond network"]}
  ],
  "cofactors": [],
  "reaction_center": {
    "bond_changes": ["acyl heteroatom bond hydrolysis"],
    "chemical_operation": "nucleophilic acyl substitution"
  },
  "substrate_constraints": ["carbonyl accessibility", "hydrophobic pocket"],
  "evidence_features": ["conserved triad", "oxyanion hole", "fold context"],
  "counterevidence_features": ["missing nucleophile", "blocked pocket"],
  "uncertainty_axes": ["substrate scope", "accessibility", "expression"]
}
```

## Design Principles

- Represent chemistry, not labels.
- Separate evidence from conclusion.
- Track counterevidence explicitly.
- Keep provenance attached to every claim.
- Allow uncertainty instead of forcing a single annotation.
- Make the representation testable by assays and negative controls.

## What The Fingerprint Should Capture

- Catalytic residue identities and roles.
- Approximate geometry constraints.
- Metal, cofactor, or prosthetic group dependence.
- Substrate pocket shape and electrostatics.
- Reaction bond changes.
- Mechanism class.
- Known family context.
- Evidence sources.
- Failure modes.

## What It Should Avoid

- Treating EC number as ground truth.
- Treating a fold match as function proof.
- Treating a ligand dock as substrate proof.
- Hiding uncertainty inside a score.
- Claiming novelty from absence of annotation alone.
