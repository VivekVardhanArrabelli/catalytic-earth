# HAD-like Phosphatase Lane Preregistration

Run: 2026-06-14T18:36:00Z

Design-only preregistration for the next high-yield bronze lane. No labels, fingerprints, or registries were written.

## Scale Rationale

- Reviewed scope supply: 4457.
- Non-EC corroborated supply estimate: 3477 (0.78).
- Projected clean admits under cap: 150.

## Admission Rule

- Scope query: `(reviewed:true) AND (ec:3.1.3.*)`.
- Required non-EC mechanism corroborators:
  - HAD family/domain/name handle.
  - Asp nucleophile or Mg binding-site evidence.
  - Rhea phosphomonoester hydrolysis equation where available.
- Holds:
  - protein phosphatase rows.
  - metal phosphomonoesterase rows with no HAD signal.
  - phosphodiesterase/nuclease side rows.

## Guardrails

- EC is scope-only and never a counted corroborator.
- Admission handles stay in excluded_context and never become predictive features.
- `predictive_evidence` must remain empty unless a future source-free feature is implemented under leakage tests.
- Dedup/novelty must check both current702 and external registries before apply.
- Frozen current702 SHA must be printed and unchanged before/after apply.

## Next Action

- Build the ontology node, mechanism fingerprint entry, source runner preview, and row-level guardrail tests before any apply.
