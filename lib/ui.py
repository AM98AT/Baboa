# -*- coding: utf-8 -*-
"""Small UI helpers and the test cards (single + merged Relative/Absolute pair)."""
from datetime import datetime
from urllib.parse import quote
import re
import streamlit as st

from lib.constants import STATUS_COLOR, STATUS_BG, STATUS_LABEL, TREND_LABEL, GENERAL_FIELDS
from lib.parsing import parse_date
from lib.scoring import ratio_text, risk_score, risk_color
from lib.units import build_units


def safe_key(s):
    return re.sub(r"[^a-zA-Z0-9_]", "_", s)


def cur_page():
    return st.query_params.get("page", "__overview__")


def detail_link(short_name):
    """Real URL link to a test's detail page (so the phone back button works)."""
    href = f"?page={quote(cur_page())}&test={quote(short_name)}"
    return f'<a class="seebtn" href="{href}" target="_self">📋 شوف التفاصيل</a>'


def val_str(t):
    return f"{t['val']:.2f}" if t["val"] is not None else str(t["latest"]["result"])


def days_ago_text(t):
    n = (datetime.now() - parse_date(t["latest"]["date"])).days
    if n <= 0:  return "انفحص اليوم"
    if n == 1:  return "قبل يوم واحد"
    if n == 2:  return "قبل يومين"
    if n <= 10: return f"قبل {n} أيام"
    return f"قبل {n} يوم"


def generic_values(tests):
    """The most common (generic) text per general field across all tests."""
    from collections import Counter
    out = {}
    for k in GENERAL_FIELDS:
        c = Counter(
            t["family_guidance"].get(k, "")
            for t in tests if t["family_guidance"].get(k, "").strip()
        )
        if c:
            out[k] = c.most_common(1)[0][0]
    return out


def render_card(t):
    status = t["status"]
    color  = STATUS_COLOR[status]
    bg     = STATUS_BG[status]
    label  = STATUS_LABEL[status]
    trend  = TREND_LABEL.get(t["trend"], "")
    ratio  = ratio_text(t)
    risk   = risk_score(t)
    rcolor = risk_color(risk)

    ratio_html = (
        f'<div style="font-size:0.82rem;font-weight:600;color:{color};margin-top:3px;">{ratio}</div>'
        if ratio else ""
    )

    st.markdown(f"""
<div style="
    background:{bg};
    border-right:6px solid {color};
    border-radius:10px;
    padding:14px 16px;
    margin-bottom:4px;
">
    <div style="font-weight:700;font-size:1rem;color:#222;">{t['short_name']}</div>
    <div style="font-size:0.75rem;color:#555;margin-bottom:6px;">{t['full_name']}</div>
    <div style="font-size:1.6rem;font-weight:700;color:{color};">
        {val_str(t)} <span style="font-size:0.85rem;font-weight:400;color:#555;">{t['unit']}</span>
    </div>
    <div style="font-size:0.84rem;font-weight:600;color:{color};margin-top:4px;">{label}</div>
    <div style="font-size:0.8rem;color:#555;margin-top:3px;">🕒 {days_ago_text(t)}{('  ·  ' + trend) if trend else ''}</div>
    {ratio_html}
    <div style="font-size:0.82rem;font-weight:700;color:{rcolor};margin-top:5px;">
        🎯 الأولوية والخطورة: {risk}/10
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown(detail_link(t["short_name"]), unsafe_allow_html=True)


def render_pair_card(u):
    rel, ab = u["rel"], u["abs"]
    status = ab["status"] if ab["status"] != "unknown" else rel["status"]
    color  = STATUS_COLOR[status]
    bg     = STATUS_BG[status]
    label  = STATUS_LABEL[status]
    risk   = max(risk_score(ab), risk_score(rel))
    rcolor = risk_color(risk)
    trend  = TREND_LABEL.get(ab["trend"], "")
    base_name = ab["full_name"].replace(" (العدد المطلق)", "").strip()
    ratio  = ratio_text(ab)
    ratio_html = (
        f'<div style="font-size:0.82rem;font-weight:600;color:{color};margin-top:3px;">{ratio}</div>'
        if ratio else ""
    )

    st.markdown(f"""
<div style="
    background:{bg};
    border-right:6px solid {color};
    border-radius:10px;
    padding:14px 16px;
    margin-bottom:4px;
">
    <div style="font-weight:700;font-size:1rem;color:#222;">{base_name}</div>
    <div style="font-size:0.72rem;color:#777;margin-bottom:8px;">يجمع: النسبة المئوية + العدد المطلق</div>
    <div style="display:flex;gap:18px;flex-wrap:wrap;">
        <div>
            <div style="font-size:0.72rem;color:#666;">النسبة المئوية</div>
            <div style="font-size:1.4rem;font-weight:700;color:{STATUS_COLOR[rel['status']]};">
                {val_str(rel)} <span style="font-size:0.75rem;font-weight:400;color:#666;">%</span>
            </div>
        </div>
        <div>
            <div style="font-size:0.72rem;color:#666;">العدد المطلق</div>
            <div style="font-size:1.4rem;font-weight:700;color:{STATUS_COLOR[ab['status']]};">
                {val_str(ab)} <span style="font-size:0.75rem;font-weight:400;color:#666;">{ab['unit']}</span>
            </div>
        </div>
    </div>
    <div style="font-size:0.84rem;font-weight:600;color:{color};margin-top:6px;">{label}</div>
    <div style="font-size:0.8rem;color:#555;margin-top:3px;">🕒 {days_ago_text(ab)}{('  ·  ' + trend) if trend else ''}</div>
    {ratio_html}
    <div style="font-size:0.82rem;font-weight:700;color:{rcolor};margin-top:5px;">
        🎯 الأولوية والخطورة: {risk}/10
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown(detail_link(ab["short_name"]), unsafe_allow_html=True)


def render_units(units):
    for u in units:
        if u["kind"] == "single":
            render_card(u["test"])
        else:
            render_pair_card(u)


def render_card_grid(tests):
    # single column = readable on a phone; pairs (Relative+Absolute) shown together
    render_units(build_units(tests))
