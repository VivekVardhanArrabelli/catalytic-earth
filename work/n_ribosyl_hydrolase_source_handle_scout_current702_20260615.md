# N-ribosyl hydrolase source-handle scout

Created: 2026-06-15T15:57:47Z

All handles are scope/admission only; none are predictive features.

- `current_broad_scope`: 1991 reviewed rows. current runner broad scope; live windows show low admitted yield because EC 3.2.2 is heterogeneous
- `family_name_only`: 11 reviewed rows. removes generic EC 3.2.2 DNA glycosylase/no-reaction supply
- `family_name_plus_ribose_product`: 9 reviewed rows. directly targets the counted Rhea/reaction axis used by the source wall
- `nucleosidase_synonym`: 219 reviewed rows. tests common enzyme-name synonyms not present in the first runner
- `n_ribohydrolase_spelling`: 2 reviewed rows. tests N-ribohydrolase spelling variants seen in curated names
- `ribose_reaction_without_ec`: 2395 reviewed rows. reaction-first handle that may recover entries lacking explicit family synonym in protein_name

Next: preview the highest-count narrow handle first, then aggregate only if row guardrails and >=150 clean batch supply hold.
