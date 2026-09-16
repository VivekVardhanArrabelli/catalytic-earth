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
import re
import sys
from pathlib import Path

CHECKS: list[tuple[str, bool]] = []

#: Tokens that should never reach the page. Each means a value leaked from the
#: code rather than being rendered as what the packaged data actually says.
LEAKED_TOKENS = ("undefined", "[object Object]", "NaN", "None", "{{", "}}")


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

        # 3. The whole packaged evidence set is reachable, not just one variant.
        check(
            "every packaged observation is listed by default",
            page.locator("#evidence-list .obs").count() == 6,
            str(page.locator("#evidence-list .obs").count()),
        )
        check(
            "both variants are offered",
            page.locator("#variant-select option").count() == 3,
            str(page.locator("#variant-select option").count()),
        )
        listed = page.locator("#evidence-list").inner_text()
        check("each observation names its variant", "H297N" in listed and "K166R" in listed)

        # 4. Endpoint-specific evidence for the focal variant.
        page.select_option("#variant-select", "H297N")
        page.wait_for_timeout(500)
        evidence = page.locator("#evidence-list").inner_text()
        check("four H297N observations", page.locator("#evidence-list .obs").count() == 4,
              str(page.locator("#evidence-list .obs").count()))
        check("racemization nondetection shown", "not detected" in evidence)
        check("fold value shown with its unit", "3.3 fold" in evidence)
        check("fold value shown against its comparator", "WT" in evidence)
        check("reported conditions shown", "pD 7.5" in evidence)
        check("detection floor stays unknown", "unknown" in evidence)

        # The contextual variant is reachable and is not an H297N control.
        page.select_option("#variant-select", "K166R")
        page.wait_for_timeout(500)
        check("contextual variant reachable", page.locator("#evidence-list .obs").count() == 2,
              str(page.locator("#evidence-list .obs").count()))
        check(
            "contextual variant is not bound to the focal site fragment",
            "0 matched observation(s)" in page.locator("#fragment-list").inner_text(),
        )
        page.select_option("#variant-select", "H297N")
        page.wait_for_timeout(500)

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

        # 5. Endpoint filtering, and the selected fragment must follow it.
        page.select_option("#endpoint-select", "isotope_exchange")
        page.wait_for_timeout(600)
        check("endpoint filter narrows to two rows", page.locator("#evidence-list .obs").count() == 2)

        # The inspector holds a selection made before this filter. It must show
        # the filtered evidence, not the evidence of the previous response.
        main_rows = page.locator("#evidence-list .obs").count()
        inspector_rows = len(
            re.findall(r"observation H297N-", page.locator("#inspector-body").inner_text())
        )
        check(
            "selected fragment reflects the active filter",
            inspector_rows == main_rows,
            f"main {main_rows}, inspector {inspector_rows}",
        )
        page.screenshot(path=str(shots / "04-endpoint-filter.png"))
        page.select_option("#endpoint-select", "")
        page.wait_for_timeout(400)

        # A selection the new result cannot support is dropped, not carried.
        page.select_option("#mechanism-select", "M0173")
        page.wait_for_timeout(700)
        check(
            "selection is dropped when its relation is gone",
            "H297N" not in page.locator("#inspector-body").inner_text(),
        )
        page.select_option("#mechanism-select", "M0187")
        page.wait_for_timeout(700)

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

        # 10. A slow earlier request must not overwrite a later selection.
        def delay_m0187(route):
            if "M0187" in route.request.url:
                page.wait_for_timeout(1500)
            route.continue_()

        page.click("[data-tab='replay']")
        page.route("**/api/mechanism/**", delay_m0187)
        page.route("**/api/sites/**", delay_m0187)
        page.select_option("#mechanism-select", "M0187")
        page.wait_for_timeout(120)
        page.select_option("#mechanism-select", "M0173")
        page.wait_for_timeout(4000)
        selected = page.eval_on_selector("#mechanism-select", "e => e.value")
        meta = page.locator("#mechanism-meta").inner_text()
        check(
            "the latest mechanism selection wins",
            selected in meta,
            f"selector {selected}, loaded {meta[:60]}",
        )
        page.unroute("**/api/mechanism/**")
        page.unroute("**/api/sites/**")

        # 11. A value that is not an integer is refused, never rounded.
        page.click("[data-tab='patterns']")
        page.click("[data-preset='shared']")
        page.wait_for_timeout(600)
        field = page.locator(".clause-row").first.locator("input[data-f='before']")
        field.fill("0.9")
        field.dispatch_event("change")
        page.click("#run-pattern")
        page.wait_for_timeout(700)
        refused = page.locator("#pattern-result").inner_text()
        check("a fractional clause value is refused", "not an integer" in refused)
        check("a refused query returns no result", "candidates matched" not in refused)
        field.fill("")
        field.dispatch_event("change")
        page.click("#run-pattern")
        page.wait_for_timeout(600)
        check(
            "a blank clause value is refused",
            "not an integer" in page.locator("#pattern-result").inner_text(),
        )
        page.click("[data-tab='replay']")

        # 12. The page survives a reload.
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


def sweep(base: str, executable: str | None) -> int:
    """Exhaustively visit every interface state and look for defects.

    This is a presentation defect sweep, not a demonstration: it walks every
    mechanism, every selectable atom and fragment, every variant and endpoint
    combination and every pattern preset, at several viewport widths, and
    reports leaked placeholder values and horizontal overflow.
    """
    from playwright.sync_api import sync_playwright

    problems: list[str] = []

    def scan(page, where: str) -> None:
        for line in page.locator("body").inner_text().splitlines():
            for token in LEAKED_TOKENS:
                if token in line:
                    problems.append(f"{where}: {token!r} in {line.strip()[:110]}")

    def overflow(page, where: str) -> None:
        wide, view = page.evaluate(
            "() => [document.documentElement.scrollWidth, window.innerWidth]"
        )
        if wide > view + 2:
            problems.append(f"{where}: horizontal overflow {wide} > {view}")

    with sync_playwright() as driver:
        launch: dict[str, object] = {}
        if executable:
            launch["executable_path"] = executable
        browser = driver.chromium.launch(**launch)
        for width, height in ((1600, 1100), (1280, 900), (1024, 768)):
            page = browser.new_page(viewport={"width": width, "height": height})
            tag = f"{width}x{height}"
            page.goto(base, wait_until="networkidle")
            page.wait_for_selector("#evidence-list .obs")
            page.wait_for_timeout(400)
            scan(page, f"{tag} load")
            overflow(page, f"{tag} load")

            for mechanism in ("M0187", "M0173"):
                page.select_option("#mechanism-select", mechanism)
                page.wait_for_timeout(600)
                for index in range(page.locator(".frag").count()):
                    page.locator(".frag").nth(index).click()
                    page.wait_for_timeout(160)
                    scan(page, f"{tag} {mechanism} selection {index}")
                overflow(page, f"{tag} {mechanism}")

            page.select_option("#mechanism-select", "M0187")
            page.wait_for_timeout(500)
            variants = [""] + [
                option
                for option in page.locator("#variant-select option").all_inner_texts()
                if option and not option.startswith("all")
            ]
            endpoints = [""] + [
                option
                for option in page.locator("#endpoint-select option").all_inner_texts()
                if option and not option.startswith("all")
            ]
            for variant in variants:
                for endpoint in endpoints:
                    page.select_option("#variant-select", variant)
                    page.wait_for_timeout(120)
                    page.select_option("#endpoint-select", endpoint)
                    page.wait_for_timeout(330)
                    scan(page, f"{tag} variant={variant or 'all'} endpoint={endpoint or 'all'}")

            page.click("[data-tab='patterns']")
            for preset in ("shared", "disjoint", "symmetric"):
                page.click(f"[data-preset='{preset}']")
                page.wait_for_timeout(600)
                scan(page, f"{tag} pattern {preset}")
                overflow(page, f"{tag} pattern {preset}")
            page.close()
        browser.close()

    distinct: dict[str, str] = {}
    for problem in problems:
        distinct.setdefault(problem.split(": ", 1)[1][:70], problem)
    print(f"{len(problems)} hits, {len(distinct)} distinct", flush=True)
    for problem in distinct.values():
        print("  " + problem, flush=True)
    return 1 if distinct else 0


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
    parser.add_argument(
        "--sweep",
        action="store_true",
        help="exhaustively scan every state for presentation defects instead",
    )
    args = parser.parse_args(argv)
    if args.sweep:
        return sweep(f"http://{args.host}:{args.port}/", args.browser_executable)
    return run(
        f"http://{args.host}:{args.port}/",
        args.shots,
        args.browser_executable,
        args.video,
    )


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
