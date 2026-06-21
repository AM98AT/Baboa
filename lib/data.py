# -*- coding: utf-8 -*-
"""Load results.json + info.json, join by id, and compute status/trend per test."""
import json
import streamlit as st

from lib.parsing import parse_date, parse_result, parse_range, classify, deviation


def load_json_safe(path):
    """Read a JSON file; on a typo, show a clear Arabic message instead of crashing."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        st.error(
            f"⚠️ أكو غلطة كتابة بالملف **{path}** بالسطر رقم **{e.lineno}**.\n\n"
            f"غالباً فاصلة (،) أو قوس ناقص أو زايد. صلّح السطر وخزّن الملف ثم اضغط "
            f"**🔄 حمّل آخر النتائج**.\n\nتفاصيل: {e.msg}"
        )
        st.stop()
    except FileNotFoundError:
        st.error(f"⚠️ الملف **{path}** مو موجود.")
        st.stop()


@st.cache_data(ttl=30)
def load_data():
    # Two linked files, joined by `id`:
    #   results.json -> daily readings (edited every day)
    #   info.json    -> test names + Arabic guidance (stable)
    results = load_json_safe("results.json")
    info_by_id = {t["id"]: t for t in load_json_safe("info.json")}

    processed = []
    for r in results:
        info = info_by_id.get(r["id"], {})
        recs = sorted(r["records"], key=lambda x: parse_date(x["date"]))
        if not recs:
            continue

        latest = recs[-1]
        val = parse_result(latest["result"])
        lo, hi = parse_range(latest["normal_range"])
        status = classify(val, lo, hi)
        dev = deviation(val, lo, hi)

        trend = "—"
        if len(recs) >= 2:
            pv = parse_result(recs[-2]["result"])
            # Compare both readings against the SAME (latest) normal range so a
            # change of lab/units in the range string can't flip the result.
            d0 = deviation(val, lo, hi)
            d1 = deviation(pv, lo, hi)
            if d0 < d1 - 1e-6:
                trend = "improving"
            elif d0 > d1 + 1e-6:
                trend = "worsening"
            else:
                trend = "stable"

        processed.append({
            "short_name":       info.get("short_name", r.get("test", "")),
            "full_name":        info.get("full_name", r.get("test", "")),
            "family_guidance":  info.get("family_guidance", {}),
            "category":         info.get("category", ""),
            "sub_category":     info.get("sub_category", ""),
            "sub_sub_category": info.get("sub_sub_category", ""),
            "unit":             info.get("unit", r.get("unit", "")),
            "records":          recs,
            "latest":           latest,
            "val":              val,
            "lo":               lo,
            "hi":               hi,
            "status":           status,
            "deviation":        dev,
            "trend":            trend,
        })
    return processed
