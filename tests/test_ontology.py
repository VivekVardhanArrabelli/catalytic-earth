from __future__ import annotations

import sys
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.ontology import fingerprint_family, load_mechanism_ontology
from catalytic_earth.models import RegistryError


class OntologyTests(unittest.TestCase):
    def test_load_mechanism_ontology(self) -> None:
        ontology = load_mechanism_ontology()
        self.assertGreaterEqual(len(ontology["families"]), 5)
        self.assertEqual(fingerprint_family("metal_dependent_hydrolase", ontology), "hydrolysis")
        self.assertEqual(
            fingerprint_family("flavin_dehydrogenase_reductase", ontology),
            "flavin_redox",
        )

    def test_rejects_unknown_parent(self) -> None:
        ontology = load_mechanism_ontology()
        ontology["families"][0] = {**ontology["families"][0], "parent_id": "missing"}
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "ontology.json"
            path.write_text(json.dumps(ontology), encoding="utf-8")
            with self.assertRaises(RegistryError):
                load_mechanism_ontology(path)


if __name__ == "__main__":
    unittest.main()
