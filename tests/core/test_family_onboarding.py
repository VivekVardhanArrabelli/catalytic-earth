from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from catalytic_earth.execution_context import ExecutionContext
from catalytic_earth.family_onboarding import (
    FamilyOnboardingSpec,
    build_family_onboarding_plan,
    load_family_onboarding_spec,
)


class FamilyOnboardingTests(unittest.TestCase):
    def test_shared_engine_blocks_new_family_during_freeze_deterministically(self) -> None:
        root = Path(__file__).resolve().parents[2]
        spec, digest = load_family_onboarding_spec(root / "config/family_onboarding.example.json")
        context = ExecutionContext(
            seed=17,
            now=lambda: datetime(2026, 7, 13, 21, 0, tzinfo=timezone.utc),
        )

        first = build_family_onboarding_plan(
            spec,
            spec_sha256=digest,
            current_family_ids={"existing_family"},
            expansion_frozen=True,
            context=context,
        )
        second = build_family_onboarding_plan(
            spec,
            spec_sha256=digest,
            current_family_ids={"existing_family"},
            expansion_frozen=True,
            context=context,
        )

        self.assertEqual(first, second)
        self.assertEqual(first["status"], "blocked")
        self.assertFalse(first["registry_write_authorized"])
        self.assertIn("truth_reset_expansion_freeze", first["blockers"][0])

    def test_schema_rejects_ad_hoc_fields(self) -> None:
        root = Path(__file__).resolve().parents[2]
        payload = json.loads(
            (root / "config/family_onboarding.example.json").read_text(encoding="utf-8")
        )
        payload["family_specific_python"] = "scripts/source_new_family.py"

        with self.assertRaisesRegex(ValueError, "fields must match"):
            FamilyOnboardingSpec.from_dict(payload)


if __name__ == "__main__":
    unittest.main()
