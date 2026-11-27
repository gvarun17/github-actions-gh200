#!/usr/bin/env python3
"""Predict how GitHub Actions expands a matrix (product -> exclude -> include).

Usage: python3 matrix_expand.py matrix.json
Prints each job combination and an estimated cost in Linux-minute units
(per 10-minute job, legacy rule of thumb: Linux x1, Windows x2, macOS x10;
current per-minute prices are on the GitHub runner pricing page).
"""
import itertools
import json
import sys

MULTIPLIER = {"ubuntu": 1, "windows": 2, "macos": 10}


def matches(combo: dict, rule: dict) -> bool:
    return all(combo.get(k) == v for k, v in rule.items())


def expand(matrix: dict) -> list[dict]:
    include = matrix.get("include", [])
    exclude = matrix.get("exclude", [])
    axes = {k: v for k, v in matrix.items() if k not in ("include", "exclude")}
    original_keys = set(axes)

    keys = list(axes)
    combos = [dict(zip(keys, vals)) for vals in itertools.product(*axes.values())] if axes else []
    combos = [c for c in combos if not any(matches(c, r) for r in exclude)]

    for rule in include:
        added = False
        for c in combos:
            # Extend a combo only if no ORIGINAL matrix value would be overwritten.
            if all(c.get(k) == v for k, v in rule.items() if k in original_keys):
                c.update({k: v for k, v in rule.items() if k not in original_keys})
                added = True
        if not added:
            combos.append(dict(rule))
    return combos


def cost(combo: dict, minutes: int = 10) -> int:
    os_name = str(combo.get("os", "ubuntu"))
    for prefix, mult in MULTIPLIER.items():
        if os_name.startswith(prefix):
            return minutes * mult
    return minutes


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    with open(sys.argv[1], encoding="utf-8") as fh:
        jobs = expand(json.load(fh))
    for i, job in enumerate(jobs, 1):
        print(f"{i:>3}. {json.dumps(job)}  ~{cost(job)} units")
    print(f"Total jobs: {len(jobs)} (limit 256); est. units: {sum(cost(j) for j in jobs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
