"""End-to-end browser check for the Mechanism Workbench.

This is a demonstration harness, not part of any test tier: it needs a real
browser and a running server, so it is kept out of ``tests/`` and out of the
packaged runtime. It drives the actual application and asserts that the
scientific boundaries survive the interface.

    python -m catalytic_earth.workbench --port 8766 &
    pip install playwright            # not a project dependency
    python -m catalytic_earth.workbench.demo_check --port 8766 --shots ./shots
    python -m catalytic_earth.workbench.demo_check --port 8766 --video ./video

Screenshots and recordings it writes are captures of the running application.
Do not present any other image or video as an application capture.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

CHECKS: list[tuple[str, bool]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    CHECKS.append((name, bool(condition)))
    status = "PASS" if condition else "FAIL"
    suffix = f" :: {detail}" if detail and not condition else ""
    print(f"{status} {name}{suffix}", flush=True)


def run(
    base: str, shots: Path, executable: str | None, video: Path | None = None
) -> int:
    from playwright.sync_api import sync_playwright

    shots.mkdir(parents=True, exist_ok=True)
    console_errors: list[str] = []

    with sync_playwright() as driver:
        launch: dict[str, object] = {}
        if executable:
            launch["executable_path"] = executable
        browser = driver.chromium.launch(**launch)
        context_options: dict[str, object] = {"viewport": {"width": 1600, "height": 1150}}
        if video is not None:
            video.mkdir(parents=True, exist_ok=True)
            context_options["record_video_dir"] = str(video)
            context_options["record_video_size"] = {"width": 1600, "height": 1150}
        context = browser.new_context(**context_options)
        page = context.new_page()
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: console_errors.append(str(e)))
        page.goto(base, wait_until="networkidle")
        page.wait_for_selector("#edit-list li")

        # 1. The first mechanism loads and is labelled honestly.
        check("M0187 lists its reviewed edits", page.locator("#edit-list li").count() == 9)
        check("graph renders every depiction node", page.locator(".atom-node").count() == 26)
        check(
            "layout is labelled computed, not measured",
            "not experimentally measured geometry" in page.locator("#layout-caveat").inner_text(),
        )
        check(
            "replay is labelled symbolic, not a trajectory",
            "not a molecular trajectory" in page.locator("#replay-note").inner_text(),
        )
        page.screenshot(path=str(shots / "01-m0187-before.png"))

        # 2. Stepping the replay.
        for _ in range(9):
            page.click("#btn-step-fwd")
            page.wait_for_timeout(450 if video is not None else 0)
        check("replay steps to the final edit", "9 of 9" in page.locator("#step-readout").inner_text())
        check("stepping stops at the after panel", page.locator("#btn-step-fwd").is_disabled())
        page.screenshot(path=str(shots / "02-m0187-replayed.png"))

        # 3. Endpoint-specific evidence.
        evidence = page.locator("#evidence-list").inner_text()
        check("four H297N observations", page.locator("#evidence-list .obs").count() == 4)
        check("racemization nondetection shown", "not detected" in evidence)
        check("fold value shown with its unit", "3.3 fold" in evidence)
        check("fold value shown against its comparator", "WT" in evidence)
        check("reported conditions shown", "pD 7.5" in evidence)
        check("detection floor stays unknown", "unknown" in evidence)

        # 4. Fragment selection exposes residue context and bound evidence.
        page.locator(".frag").first.click()
        page.wait_for_timeout(250)
        inspector = page.locator("#inspector-body").inner_text()
        check("fragment resolves to its atlas site", "P11444:H297" in inspector)
        check("numbering systems stay distinct", "mmCIF label" in inspector)
        check("structure is labelled a reference structure", "reference structure" in inspector)
        check("retained depiction coordinates reported", "retained source x2/y2" in inspector)
        check(
            "endpoint evidence bound to the site",
            "endpoint-specific evidence" in inspector.lower(),
        )
        page.screenshot(path=str(shots / "03-m0187-fragment-evidence.png"))

        # 5. Endpoint filtering.
        page.select_option("#endpoint-select", "isotope_exchange")
        page.wait_for_timeout(500)
        check("endpoint filter narrows to two rows", page.locator("#evidence-list .obs").count() == 2)
        page.screenshot(path=str(shots / "04-endpoint-filter.png"))
        page.select_option("#endpoint-select", "")
        page.wait_for_timeout(400)

        # 6. The second mechanism uses the same renderer.
        page.select_option("#mechanism-select", "M0173")
        page.wait_for_timeout(700)
        check("M0173 lists its reviewed edits", page.locator("#edit-list li").count() == 6)
        check("M0173 renders every depiction node", page.locator(".atom-node").count() == 50)
        fragments = page.locator("#fragment-list").inner_text()
        check("M0173 resolves its labelled site", "P35049:S204" in fragments)
        check("M0173 keeps unlabelled atoms unresolved", "unresolved" in fragments)
        page.screenshot(path=str(shots / "05-m0173.png"))

        page.locator("[data-site-atom='a44']").click()
        page.wait_for_timeout(300)
        site = page.locator("#inspector-body").inner_text()
        check("changed atom resolves to its site", "P35049:S204" in site)
        check("PDB author numbering shown", "1PQ5" in site and "195" in site)
        check("mmCIF label numbering shown", "180" in site)
        check("locator is not a physical atom", "not a physical atom identity" in site)
        page.screenshot(path=str(shots / "06-m0173-site.png"))

        # 7-9. Shared-atom pattern query, its negative case and its symmetry case.
        page.click("[data-tab='patterns']")
        page.click("[data-preset='shared']")
        page.wait_for_timeout(700)
        shared = page.locator("#pattern-result").inner_text()
        check("shared-atom query binds one candidate", "x = a10" in shared and "y = a28" in shared)
        check("catalog status shown as unreviewed", "unreviewed" in shared)
        check("bindings are not mechanism counts", "not mechanism counts" in shared)
        page.screenshot(path=str(shots / "07-pattern-match.png"))

        page.click("[data-preset='disjoint']")
        page.wait_for_timeout(700)
        disjoint = page.locator("#pattern-result").inner_text()
        check("disjoint-atom query returns no match",
              "No match in the declared searched collection" in disjoint)
        check("empty result is not absence of chemistry",
              "does not mean the chemistry is absent" in disjoint)
        page.screenshot(path=str(shots / "08-pattern-nomatch.png"))

        page.click("[data-preset='symmetric']")
        page.wait_for_timeout(700)
        page.screenshot(path=str(shots / "09-pattern-symmetric.png"))

        # 10. The page survives a reload.
        page.reload(wait_until="networkidle")
        page.wait_for_selector("#edit-list li")
        check("reload restores the first mechanism", page.locator("#edit-list li").count() == 9)

        context.close()
        browser.close()
        if video is not None:
            written = sorted(video.glob("*.webm"))
            check("recording written", bool(written),
                  "no video file produced")
            for path in written:
                print(f"recording: {path}", flush=True)

    check("no console errors", not console_errors, "; ".join(console_errors[:3]))
    failed = [name for name, ok in CHECKS if not ok]
    print(f"\n{len(CHECKS) - len(failed)}/{len(CHECKS)} checks passed", flush=True)
    if failed:
        print("failed: " + ", ".join(failed), flush=True)
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--shots", type=Path, default=Path("workbench-shots"))
    parser.add_argument(
        "--video",
        type=Path,
        default=None,
        help="record the whole run to this directory as a .webm capture",
    )
    parser.add_argument(
        "--browser-executable",
        default=None,
        help="path to a Chromium build, when Playwright's own download is absent",
    )
    args = parser.parse_args(argv)
    return run(
        f"http://{args.host}:{args.port}/",
        args.shots,
        args.browser_executable,
        args.video,
    )


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
