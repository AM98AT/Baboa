# -*- coding: utf-8 -*-
"""Group Relative%/Absolute sibling tests into one 'unit' and score those units."""
from lib.constants import PAIR_SUFFIXES
from lib.scoring import risk_score


def _base(short):
    for suf in PAIR_SUFFIXES:
        if short.endswith(suf):
            return short[: -len(suf)]
    return None


def build_units(tests):
    """Group Relative+Absolute siblings into one unit; everything else stays single."""
    by_short = {t["short_name"]: t for t in tests}
    used, units = set(), []
    for t in tests:
        sn = t["short_name"]
        if sn in used:
            continue
        base = _base(sn)
        if base:
            rel = by_short.get(base + " (Relative)")
            ab  = by_short.get(base + " (Absolute)")
            if rel and ab:
                used.add(rel["short_name"]); used.add(ab["short_name"])
                units.append({"kind": "pair", "rel": rel, "abs": ab})
                continue
        used.add(sn)
        units.append({"kind": "single", "test": t})
    return units


def unit_status(u):
    if u["kind"] == "single":
        return u["test"]["status"]
    a, r = u["abs"]["status"], u["rel"]["status"]
    return a if a != "unknown" else r


def unit_risk(u):
    if u["kind"] == "single":
        return risk_score(u["test"])
    return max(risk_score(u["abs"]), risk_score(u["rel"]))


def unit_dev(u):
    if u["kind"] == "single":
        return u["test"]["deviation"]
    return max(u["abs"]["deviation"], u["rel"]["deviation"])


def partner_of(tests, t):
    base = _base(t["short_name"])
    if not base:
        return None
    other = base + (" (Absolute)" if t["short_name"].endswith("(Relative)") else " (Relative)")
    return next((x for x in tests if x["short_name"] == other), None)
