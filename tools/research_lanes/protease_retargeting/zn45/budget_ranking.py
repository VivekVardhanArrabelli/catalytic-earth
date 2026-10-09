"""Exposed-data budget comparison; no predictive validation or inactivity labels."""
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def analyze():
    source = HERE / 'zn45_activity_af3_join.csv'
    rows = list(csv.DictReader(source.open()))
    assert len(rows) == 378 and len({r['key'] for r in rows}) == 378
    for r in rows:
        for field in ('complex_plddt', 'ipae_min', 'fold_over_wt'):
            r[field] = float(r[field])
    passing = [r for r in rows if r['complex_plddt'] > 94 and r['ipae_min'] < 1.5]
    positive = lambda r: r['fold_over_wt'] > 1.5
    assert len(passing) == 211
    assert sum(map(positive, rows)) == sum(map(positive, passing)) == 19
    outcomes = {}
    curves = []
    for name, field, direction in [('plddt_descending', 'complex_plddt', -1),
                                   ('ipae_ascending', 'ipae_min', 1)]:
        ranked = sorted(passing, key=lambda r: (direction*r[field], r['key']))
        captured = 0
        for k, r in enumerate(ranked, 1):
            captured += positive(r)
            curves.append(dict(ranking=name, budget=k, key=r['key'], score=r[field],
                               fold_over_wt=r['fold_over_wt'], signal=positive(r),
                               captured=captured, uniform211_expected=k*19/211))
        top = ranked[:19]
        count = sum(map(positive, top))
        cutoff = direction*top[-1][field]
        strictly_better = [r for r in ranked if direction*r[field] < cutoff]
        tied = [r for r in ranked if direction*r[field] == cutoff]
        slots = 19-len(strictly_better)
        positives = sum(map(positive, tied))
        base = sum(map(positive, strictly_better))
        outcomes[name] = dict(captured_at19=count, selected_keys=[r['key'] for r in top],
                             enrichment_over_uniform211=count/(19*19/211),
                             boundary_tie_size=len(tied), boundary_slots=slots,
                             tie_capture_min=base+max(0,slots-(len(tied)-positives)),
                             tie_capture_max=base+min(slots,positives))
    summary = dict(question='Does confidence ranking improve scarce retest prioritization after the existing filter?',
                   design='Retrospective exposed-data analysis; fixed top19 shortlist scenario; both ranks retained',
                   input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                   filter='five-sample mean complex_plddt >94 and ipae_min <1.5',
                   signal='executed-window fold_over_wt >1.5; not confirmed activity improvement',
                   tie_rule='lexical key; boundary tie range also retained',
                   n=378, filtered_n=211, total_signals=19, budget=19,
                   uniform211_expected=19*19/211, uniform378_expected=19*19/378,
                   outcomes=outcomes)
    return summary, curves


if __name__ == '__main__':
    summary, curves = analyze()
    (HERE/'budget_ranking_result.json').write_text(json.dumps(summary, indent=2)+'\n')
    with (HERE/'budget_ranking_curves.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(curves[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(curves)
    print(json.dumps(summary, indent=2))
