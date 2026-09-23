#!/usr/bin/env python3
"""Check that the RA95 translation uses source values and preserves native input."""
import copy
import json
import tarfile

import build_input as build


def main():
    projection = build.check_deposit_context(build.PACKET, build.ROOT)
    audit = json.loads((build.LANE / "input_state.json").read_text())
    interface = audit["native_control"]["interface"]
    rows = build.select_rows(projection, interface)
    with tarfile.open(build.BUNDLE) as archive:
        template = archive.extractfile(build.TEMPLATE_MEMBER).read()
        config = json.load(archive.extractfile("logs/resolved-inference-config.json"))
    build.verify_interface(interface, config)
    # Zero all selected template coordinates and occupancies: the source must
    # restore all of them. This catches a no-op that simply copies the template.
    keys = {build.atom_key(row) for row in rows}
    zeroed = []
    count = 0
    for line in template.decode().splitlines(keepends=True):
        key = (line[:6].strip(), line[21:22], line[22:26].strip(),
               line[17:20], line[12:16].strip(), line[16:17])
        if key in keys:
            line = line[:30] + f"{0:8.3f}" * 3 + f"{0:6.2f}" + line[60:]
            count += 1
        zeroed.append(line)
    restored, _ = build.rebuild("".join(zeroed).encode(), rows)
    assert count == 26 and restored == template
    modified = copy.deepcopy(rows)
    modified[0]["cartn_x"] = str(float(modified[0]["cartn_x"]) + 1)
    perturbed, _ = build.rebuild(template, modified)
    assert sum(a != b for a, b in zip(perturbed.splitlines(), template.splitlines())) == 1
    rejected = []
    cases = {
        "duplicate_source": rows + [rows[0]],
        "nonfinite_coordinate": [dict(rows[0], cartn_x="nan")] + rows[1:],
        "missing_template_atom": [dict(rows[0], auth_seq_id="9999")] + rows[1:],
        "element_mismatch": [dict(rows[0], type_symbol="Xe")] + rows[1:],
    }
    for name, candidate in cases.items():
        try:
            build.rebuild(template, candidate)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(name)
    missing = copy.deepcopy(projection)
    for group in missing["row_selections"]:
        if group["selection_id"] == "tyr51-atoms":
            group["rows"] = [r for r in group["rows"] if not
                             (r["label_atom_id"] == "OH" and r["label_alt_id"] == "A")]
    try:
        build.select_rows(missing, interface)
    except ValueError:
        rejected.append("missing_selected_alternate")
    else:
        raise AssertionError("missing selected alternate")
    print(json.dumps({"status": "passed", "interface_matches_executed_reference_config": True,
                      "template_atom_records_restored_from_atlas": count,
                      "one_source_coordinate_changes_exactly_one_output_atom": True,
                      "rejected_cases": rejected}, indent=2))


if __name__ == "__main__":
    main()
