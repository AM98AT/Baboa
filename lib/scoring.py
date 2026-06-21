# -*- coding: utf-8 -*-
"""Ratio text and 1-10 priority/risk scoring for a processed test dict."""
from lib.constants import CLINICAL_WEIGHT, STATUS_LABEL

STATUS_ICON = {"normal": "✅", "low": "⬇️", "high": "⬆️", "unknown": "❓"}


def _fmt_pct(p):
    s = f"{p:.1f}"
    return s[:-2] if s.endswith(".0") else s


def ratio_text(t):
    """How far the result is past the normal boundary, as a % of that boundary."""
    val, lo, hi, status = t["val"], t["lo"], t["hi"], t["status"]
    if val is None:
        return None
    if status == "high" and hi:
        return f"أعلى من الطبيعي بنسبة {_fmt_pct((val - hi) / hi * 100)}%"
    if status == "low" and lo:
        return f"أقل من الطبيعي بنسبة {_fmt_pct((lo - val) / lo * 100)}%"
    if status == "normal":
        return "ضمن المعدّل الطبيعي"
    return None


def status_line(t):
    """Status + percentage on ONE line (no repeating 'above/below normal' twice)."""
    r = ratio_text(t)
    if r is None:
        return STATUS_LABEL[t["status"]]      # unknown → "❓ بدون معدّل"
    return f"{STATUS_ICON[t['status']]} {r}"


def risk_score(t):
    """1-10 priority: how much the family should focus on this test now."""
    base = CLINICAL_WEIGHT.get(t["short_name"], 5)
    if t["status"] in ("normal", "unknown"):
        return max(1, round(base * 0.2))          # in range = low priority
    dev_factor = min(t["deviation"], 2) / 2        # 0..1 (capped at 200% outside)
    score = base * (0.5 + 0.5 * dev_factor)
    if t["trend"] == "worsening":
        score += 1.5
    elif t["trend"] == "improving":
        score -= 1.5
    return int(max(1, min(10, round(score))))


def risk_color(r):
    return "#c62828" if r >= 7 else "#f57c00" if r >= 4 else "#2e7d32"
