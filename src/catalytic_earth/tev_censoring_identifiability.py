"""Check identifiability of censored TEV interaction measurements.

This module deliberately separates a Michaelis--Menten specificity constant
from a directly bounded, fixed-condition product observation. A finite set of
nondetections at positive substrate concentrations does not, by itself, place a
finite upper bound on kcat/Km when both kcat and Km are unknown.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def michaelis_menten_rate(
    efficiency: float, km: float, substrate: float, enzyme: float = 1.0
) -> float:
    """Return v0 for kcat/Km=efficiency and kcat=efficiency*km."""
    if min(efficiency, km, substrate, enzyme) <= 0:
        raise ValueError("all Michaelis-Menten inputs must be positive")
    return enzyme * efficiency * km * substrate / (km + substrate)


def witness_unbounded_efficiency(
    efficiency: float,
    substrate_concentrations: list[float],
    rate_upper_bounds: list[float],
    enzyme: float = 1.0,
) -> dict[str, float | list[float]]:
    """Construct Km/kcat whose rates evade every supplied detection limit.

    Since v0 < E*(kcat/Km)*Km at every positive substrate concentration,
    choosing Km below every rate limit divided by E*(kcat/Km) proves that an
    arbitrarily large specificity constant remains compatible with the finite
    nondetection set.
    """
    if len(substrate_concentrations) != len(rate_upper_bounds) or not rate_upper_bounds:
        raise ValueError("supply one positive rate bound per substrate concentration")
    if min(substrate_concentrations + rate_upper_bounds + [efficiency, enzyme]) <= 0:
        raise ValueError("all inputs must be positive")
    km = min(rate_upper_bounds) / (2.0 * enzyme * efficiency)
    kcat = efficiency * km
    rates = [
        michaelis_menten_rate(efficiency, km, substrate, enzyme)
        for substrate in substrate_concentrations
    ]
    if not all(rate < bound for rate, bound in zip(rates, rate_upper_bounds)):
        raise AssertionError("constructed witness did not satisfy the nondetections")
    return {"efficiency": efficiency, "km": km, "kcat": kcat, "rates": rates}


def interaction_interval(
    aa: tuple[float, float],
    bb: tuple[float, float],
    ab: tuple[float, float],
    ba: tuple[float, float],
) -> tuple[float, float]:
    """Sharp interval for I=AA+BB-AB-BA from rectangular cell intervals."""
    intervals = (aa, bb, ab, ba)
    if any(lo > hi for lo, hi in intervals):
        raise ValueError("interval lower bound exceeds upper bound")
    return aa[0] + bb[0] - ab[1] - ba[1], aa[1] + bb[1] - ab[0] - ba[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    demonstrations = [
        witness_unbounded_efficiency(value, [1.0, 10.0, 100.0], [1e-3] * 3)
        for value in (1.0, 1e3, 1e6)
    ]
    fixed_intervals = {
        "PA_A": (math.log(8.0), math.log(12.0)),
        "PB_B": (math.log(8.0), math.log(12.0)),
        "PA_B": (-math.inf, math.log(2.0)),
        "PB_A": (-math.inf, math.log(2.0)),
    }
    fixed_bounds = interaction_interval(
        fixed_intervals["PA_A"],
        fixed_intervals["PB_B"],
        fixed_intervals["PA_B"],
        fixed_intervals["PB_A"],
    )

    def encode(value: float) -> float | str:
        if math.isfinite(value):
            return value
        return "Infinity" if value > 0 else "-Infinity"

    result = {
        "claim": "finite all-nondetected Michaelis-Menten observations do not upper-bound kcat/Km without an additional Km constraint",
        "witnesses": demonstrations,
        "fixed_condition_example": {
            "cell_intervals_log_fixed_interval_product_per_enzyme": {
                key: [encode(value) for value in interval]
                for key, interval in fixed_intervals.items()
            },
            "signed_interaction_interval": [encode(value) for value in fixed_bounds],
        },
    }
    payload = json.dumps(result, indent=2) + "\n"
    if args.out:
        args.out.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
