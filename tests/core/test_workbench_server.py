"""Offline checks for the Mechanism Workbench loopback server."""

from __future__ import annotations

import json
import threading
import unittest
import urllib.error
import urllib.request

from catalytic_earth.workbench.server import build_server


class ServerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = build_server("127.0.0.1", 0)
        cls.base = "http://127.0.0.1:%d" % cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def get(self, path: str) -> tuple[int, bytes, str]:
        try:
            with urllib.request.urlopen(self.base + path, timeout=30) as response:
                return response.status, response.read(), response.headers.get("Content-Type", "")
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read(), exc.headers.get("Content-Type", "")

    def get_json(self, path: str) -> dict:
        status, body, _ = self.get(path)
        self.assertEqual(status, 200, body[:200])
        return json.loads(body)

    def post_json(self, path: str, payload: dict) -> tuple[int, dict]:
        request = urllib.request.Request(
            self.base + path,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read())


class BindingTest(unittest.TestCase):
    def test_non_loopback_bind_is_refused(self) -> None:
        for host in ("0.0.0.0", "10.0.0.5", ""):
            with self.assertRaises(ValueError):
                build_server(host, 0)


class StaticAssetTest(ServerTestCase):
    def test_page_and_assets_are_served(self) -> None:
        for path, fragment in (
            ("/", b"Mechanism Workbench"),
            ("/index.html", b"Mechanism Workbench"),
            ("/app.js", b"graphAtStep"),
            ("/style.css", b".atom-node"),
        ):
            status, body, _ = self.get(path)
            self.assertEqual(status, 200, path)
            self.assertIn(fragment, body, path)

    def test_only_allowlisted_assets_are_reachable(self) -> None:
        for path in (
            "/adapter.py",
            "/server.py",
            "/static/index.html",
            "/..%2f..%2fetc%2fpasswd",
            "/%2e%2e/%2e%2e/etc/passwd",
            "/layout.py",
        ):
            status, _, _ = self.get(path)
            self.assertEqual(status, 404, path)


class ApiRouteTest(ServerTestCase):
    def test_mechanism_list(self) -> None:
        payload = self.get_json("/api/mechanisms")
        self.assertEqual(
            {entry["mcsa_id"] for entry in payload["mechanisms"]}, {"M0187", "M0173"}
        )

    def test_both_mechanisms_load(self) -> None:
        for mcsa_id, edits in (("M0187", 9), ("M0173", 6)):
            payload = self.get_json(f"/api/mechanism/{mcsa_id}")
            self.assertEqual(len(payload["edits"]), edits)
            self.assertEqual(len(payload["layout"]["positions"]),
                             len(payload["before_graph"]["atoms"]))

    def test_sites_route(self) -> None:
        payload = self.get_json("/api/sites/M0173")
        self.assertEqual(payload["resolved_source_atom_count"], 2)

    def test_evidence_route_and_filter(self) -> None:
        unfiltered = self.get_json("/api/evidence?variant=H297N")
        self.assertEqual(unfiltered["matched_observation_count"], 4)
        filtered = self.get_json("/api/evidence?variant=H297N&endpoint=isotope_exchange")
        self.assertEqual(filtered["matched_observation_count"], 2)

    def test_unknown_routes_and_mechanisms(self) -> None:
        status, _, _ = self.get("/api/nope")
        self.assertEqual(status, 404)
        status, body, _ = self.get("/api/mechanism/M9999")
        self.assertEqual(status, 400)
        self.assertIn("no packaged transformation set", json.loads(body)["error"])


class PatternRouteTest(ServerTestCase):
    SHARED = [
        {"kind": "bond", "elements": ["C", "C"], "variables": ["x", "y"],
         "before": 0, "after": 1},
        {"kind": "charge", "elements": ["C"], "variables": ["x"],
         "before": -1, "after": 0},
    ]
    DISJOINT = [
        {"kind": "bond", "elements": ["C", "O"], "variables": ["x", "y"],
         "before": 2, "after": 1},
        {"kind": "charge", "elements": ["C"], "variables": ["x"],
         "before": -1, "after": 0},
    ]

    def test_shared_atom_match(self) -> None:
        status, payload = self.post_json("/api/patterns", {"clauses": self.SHARED})
        self.assertEqual(status, 200)
        self.assertEqual(payload["candidate_count"], 1)
        self.assertEqual(payload["binding_count"], 1)

    def test_disjoint_atom_no_match(self) -> None:
        status, payload = self.post_json("/api/patterns", {"clauses": self.DISJOINT})
        self.assertEqual(status, 200)
        self.assertEqual(payload["candidate_count"], 0)
        self.assertEqual(payload["matches"], [])

    def test_bad_requests_are_reported(self) -> None:
        for body in ({"clauses": []}, {"clauses": [{"kind": "nope"}]}, {}):
            status, payload = self.post_json("/api/patterns", body)
            self.assertEqual(status, 400, payload)
            self.assertIn("error", payload)

    def test_pattern_route_rejects_get(self) -> None:
        status, _, _ = self.get("/api/patterns")
        self.assertEqual(status, 404)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
