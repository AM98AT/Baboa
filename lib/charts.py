# -*- coding: utf-8 -*-
"""Static matplotlib trend chart (PNG) — reliable on Streamlit Cloud, no browser."""
from datetime import timedelta
from io import BytesIO
import math
import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from lib.parsing import parse_date, parse_result, classify
from lib.constants import STATUS_COLOR


def _nice_ticks(vmin, vmax, target=6):
    """Clean, evenly-spaced y-axis ticks with correct labels (no rounding duplicates,
    and the top/bottom ticks always enclose the data)."""
    if vmax <= vmin:
        vmax = vmin + 1
    raw = (vmax - vmin) / target
    mag = 10 ** math.floor(math.log10(raw)) if raw > 0 else 1
    step = 10 * mag
    for m in (1, 2, 2.5, 5):
        if raw <= m * mag:
            step = m * mag
            break
    start = math.floor(vmin / step) * step
    end = math.ceil(vmax / step) * step
    # decimals needed to print the step value exactly (so 0.25 -> 2, 2.5 -> 1, 5 -> 0)
    ss = f"{step:.10f}".rstrip("0").rstrip(".")
    dec = len(ss.split(".")[1]) if "." in ss else 0
    ticks, v = [], start
    while v <= end + step * 0.5:
        ticks.append(round(v, 10))
        v += step
    labels = [f"{tk:.{dec}f}" for tk in ticks]
    return ticks, labels


def _day_labels(days):
    """Day number on every tick; month (DD/MM) only on the first, the last, and on month changes."""
    out, prev, n = [], None, len(days)
    for i, d in enumerate(days):
        if i == 0 or i == n - 1 or d.month != prev:
            out.append(f"{d.day:02d}/{d.month:02d}")
        else:
            out.append(f"{d.day:02d}")
        prev = d.month
    return out


@st.cache_data(show_spinner=False, ttl=60)
def _chart_png(code, unit, rng_latin, xs, ys, colors, lo, hi):
    """Render the trend as a static PNG using matplotlib (reliable on Streamlit Cloud)."""
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=130)

    # normal-range band + dashed bounds
    if lo is not None and hi is not None:
        ax.axhspan(lo, hi, color="#2e7d32", alpha=0.10, zorder=0)
    if lo is not None:
        ax.axhline(lo, color="#2e7d32", ls="--", lw=1.3, zorder=1)
    if hi is not None:
        ax.axhline(hi, color="#2e7d32", ls="--", lw=1.3, zorder=1)

    xn = [mdates.date2num(x) for x in xs]
    ax.plot(xn, ys, color="#1565c0", lw=2.6, zorder=2)
    ax.scatter(xn, ys, c=list(colors), s=120, edgecolors="white", linewidths=1.6, zorder=3)
    for x, y in zip(xn, ys):
        ax.annotate(f"{y:g}", (x, y), textcoords="offset points", xytext=(0, 10),
                    ha="center", fontsize=11, color="#222")

    # X: one tick per calendar day (day, not time)
    day0, dayN = min(xs), max(xs)
    days, d = [], day0
    while d <= dayN:
        days.append(d); d += timedelta(days=1)
    ax.set_xticks([mdates.date2num(x) for x in days])
    ax.set_xticklabels(_day_labels(days), fontsize=11)
    ax.set_xlim(mdates.date2num(day0 - timedelta(hours=12)),
                mdates.date2num(dayN + timedelta(hours=12)))

    # Y: clean numbered ticks that enclose the data + normal band
    yvals = list(ys) + [b for b in (lo, hi) if b is not None]
    ymn, ymx = min(yvals), max(yvals)
    if ymx == ymn:
        dd = abs(ymx) * 0.3 or 1
        ymn, ymx = ymn - dd, ymx + dd
    ymx += (ymx - ymn) * 0.08      # headroom so the top value label isn't clipped
    tickvals, ticktext = _nice_ticks(ymn, ymx)
    ax.set_yticks(tickvals)
    ax.set_yticklabels(ticktext, fontsize=11)
    ax.set_ylim(tickvals[0], tickvals[-1])

    ax.set_title(f"{code}   ({unit})    normal: {rng_latin}", fontsize=13, pad=12)
    ax.grid(color="#e6e6e6", lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    return buf.getvalue()


def render_chart(t):
    recs  = t["records"]
    # Floor each date to the day (the day matters, not the time) so points sit on the day line.
    pairs = [(parse_date(r["date"]).replace(hour=0, minute=0, second=0, microsecond=0),
              parse_result(r["result"])) for r in recs]
    pairs = [(d, v) for d, v in pairs if v is not None]
    if not pairs:
        st.info("ماكو بيانات رقمية حتى نرسمها.")
        return

    xs, ys = zip(*pairs)
    lo, hi = t["lo"], t["hi"]
    if lo is not None and hi is not None:
        rng_latin = f"{lo} - {hi} {t['unit']}"
        rng_ar    = f"المعدّل الطبيعي: {lo} - {hi} {t['unit']}"
    elif hi is not None:
        rng_latin = f"< {hi} {t['unit']}"
        rng_ar    = f"المعدّل الطبيعي: أقل من {hi} {t['unit']}"
    elif lo is not None:
        rng_latin = f"> {lo} {t['unit']}"
        rng_ar    = f"المعدّل الطبيعي: أعلى من {lo} {t['unit']}"
    else:
        rng_latin = "-"
        rng_ar    = "ماكو معدّل مرجعي"
    colors = tuple(STATUS_COLOR[classify(v, lo, hi)] for v in ys)

    st.markdown(f"**📈 {t['full_name']}** — {rng_ar}")
    try:
        png = _chart_png(t["short_name"], t["unit"], rng_latin, tuple(xs), tuple(ys), colors, lo, hi)
        st.image(png, use_container_width=True)
        st.caption("📷 اضغط مطوّلاً على الصورة حتى تحفظها أو تشاركها.")
    except Exception:
        st.info("تعذّر رسم المخطط حالياً.")
