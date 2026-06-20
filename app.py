import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import re

st.set_page_config(
    page_title="Grandpa's Health Tracker",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Mobile-first styling ─────────────────────────────────────────────────────────
st.markdown("""
<style>
/* tighter padding + readable width on phones */
.block-container { padding-top: 1rem; padding-bottom: 3rem;
    padding-left: 0.8rem; padding-right: 0.8rem; max-width: 640px; }
/* bigger base text for older eyes */
html, body, [class*="css"] { font-size: 17px; }
/* full-width, tall, rounded buttons = easy to tap */
.stButton > button { width: 100%; padding: 0.65rem 0.8rem;
    font-size: 1.02rem; border-radius: 12px; font-weight: 600; }
/* hide the tiny sidebar hamburger leftovers / menu clutter */
#MainMenu, footer { visibility: hidden; }
/* make expander headers larger and easier to tap */
.streamlit-expanderHeader, details summary { font-size: 1.02rem !important; }
/* metric numbers a touch smaller so 3 fit on a phone row */
[data-testid="stMetricValue"] { font-size: 1.5rem; }
[data-testid="stMetricLabel"] { font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ── Utilities ──────────────────────────────────────────────────────────────────

def parse_date(s):
    for fmt in ("%d/%m/%Y %H:%M", "%d-%m-%Y %H:%M:%S", "%d-%m-%Y %H:%M"):
        try:
            return datetime.strptime(s.strip(), fmt)
        except ValueError:
            pass
    return datetime(2000, 1, 1)

def parse_result(v):
    if isinstance(v, (int, float)):
        return float(v)
    m = re.match(r"[<>≤≥]?\s*([\d.]+)", str(v).strip())
    return float(m.group(1)) if m else None

def parse_range(s):
    """Returns (lo, hi). None means unbounded."""
    if not s or s.strip() in ("Not Specified", ""):
        return None, None
    s = s.strip()
    # "X - Y"
    m = re.match(r"^([\d.]+)\s*[-–]\s*([\d.]+)$", s)
    if m:
        return float(m.group(1)), float(m.group(2))
    # "< X" or "<= X"
    m = re.match(r"^[<≤]=?\s*([\d.]+)", s)
    if m:
        return 0.0, float(m.group(1))
    # "> X" or ">= X"
    m = re.match(r"^[>≥]=?\s*([\d.]+)", s)
    if m:
        return float(m.group(1)), None
    # "Up to X"
    m = re.match(r"[Uu]p\s+to\s+([\d.]+)", s)
    if m:
        return 0.0, float(m.group(1))
    # Complex ranges: PCT "Normal: 0.0-0.5, ..." or "Normal < 0.046, ..."
    m = re.search(r"Normal[:\s]+<\s*([\d.]+)", s, re.I)
    if m:
        return 0.0, float(m.group(1))
    m = re.search(r"Normal[:\s]+([\d.]+)\s*[-–]\s*([\d.]+)", s, re.I)
    if m:
        return float(m.group(1)), float(m.group(2))
    # HbA1c "Non diabetic < 5.8, ..."
    m = re.search(r"Non.diabetic\s*<\s*([\d.]+)", s, re.I)
    if m:
        return 0.0, float(m.group(1))
    return None, None

def classify(val, lo, hi):
    if val is None or (lo is None and hi is None):
        return "unknown"
    if lo is not None and val < lo:
        return "low"
    if hi is not None and val > hi:
        return "high"
    return "normal"

def deviation(val, lo, hi):
    """Fractional distance outside normal range (0 if inside)."""
    if val is None or (lo is None and hi is None):
        return 0.0
    if lo is not None and val < lo and lo != 0:
        return (lo - val) / lo
    if hi is not None and val > hi and hi != 0:
        return (val - hi) / hi
    return 0.0

# ── Data Loading ───────────────────────────────────────────────────────────────

@st.cache_data(ttl=30)
def load_data():
    with open("data.json", encoding="utf-8") as f:
        raw = json.load(f)

    processed = []
    for t in raw:
        recs = sorted(t["records"], key=lambda r: parse_date(r["date"]))
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
            pl, ph = parse_range(recs[-2]["normal_range"])
            d0 = deviation(val, lo, hi)
            d1 = deviation(pv, pl, ph)
            if d0 < d1 - 1e-6:
                trend = "improving"
            elif d0 > d1 + 1e-6:
                trend = "worsening"
            else:
                trend = "stable"

        processed.append({
            "short_name":       t["short_name"],
            "full_name":        t["full_name"],
            "family_guidance":  t.get("family_guidance", {}),
            "category":         t["category"],
            "sub_category":     t["sub_category"],
            "sub_sub_category": t["sub_sub_category"],
            "unit":             t["unit"],
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

# ── Constants ──────────────────────────────────────────────────────────────────

STATUS_COLOR = {
    "normal":  "#2e7d32",
    "low":     "#1565c0",
    "high":    "#c62828",
    "unknown": "#757575",
}
STATUS_BG = {
    "normal":  "#e8f5e9",
    "low":     "#e3f2fd",
    "high":    "#ffebee",
    "unknown": "#f5f5f5",
}
STATUS_LABEL = {
    "normal":  "✅ Normal",
    "low":     "⬇️ Below Normal",
    "high":    "⬆️ Above Normal",
    "unknown": "❓ No Range",
}
TREND_LABEL = {
    "improving": "📈 Improving",
    "worsening": "📉 Getting worse",
    "stable":    "➡️ Stable",
    "—":         "",
}

PAGES = {
    "📊 Overview":         "__overview__",
    "🩸 Blood Count":      "cbc",
    "🫀 Kidney Function":  "kidney",
    "🫁 Liver Function":   "liver",
    "🔥 Inflammation":     "inflam",
    "⚡ Electrolytes":     "electro",
    "❤️ Heart & Clotting": "cardiac",
    "🧪 Other Tests":      "other",
}

def cat_filter(cat_key, t):
    sub = t["sub_sub_category"]
    mapping = {
        "cbc":     sub in ("Complete Blood Count (CBC)", "Differential White Cell Count"),
        "kidney":  sub == "Kidney Function Test (RFT)",
        "liver":   sub == "Liver Function Test (LFT)",
        "inflam":  sub == "Inflammatory Markers",
        "electro": sub in ("Electrolytes", "Electrolytes and Minerals"),
        "cardiac": sub in ("Cardiac Biomarkers", "Coagulation / Vascular Markers"),
        "other":   sub in (
            "Protein Panel", "Metabolic Panel",
            "Enzyme / Tissue Damage Marker", "Endocrine / Metabolic Panel",
        ),
    }
    return mapping.get(cat_key, False)

# ── Helpers ────────────────────────────────────────────────────────────────────

def safe_key(s):
    return re.sub(r"[^a-zA-Z0-9_]", "_", s)

def val_str(t):
    return f"{t['val']:.2f}" if t["val"] is not None else str(t["latest"]["result"])

# ── Components ─────────────────────────────────────────────────────────────────

def render_card(t):
    status = t["status"]
    color  = STATUS_COLOR[status]
    bg     = STATUS_BG[status]
    label  = STATUS_LABEL[status]
    trend  = TREND_LABEL.get(t["trend"], "")

    st.markdown(f"""
<div style="
    background:{bg};
    border-left:5px solid {color};
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
    <div style="font-size:0.78rem;color:#555;margin-top:2px;">{trend}</div>
</div>
""", unsafe_allow_html=True)

    if st.button("📋 See Details", key=f"card_{safe_key(t['short_name'])}"):
        st.session_state["selected_test"] = t["short_name"]
        st.rerun()

    st.markdown("<div style='margin-bottom:10px'></div>", unsafe_allow_html=True)


def render_card_grid(tests):
    # single column = readable on a phone (no tiny side-by-side cards)
    for t in tests:
        render_card(t)


def render_overview(tests):
    st.title("🏥 Health Dashboard")
    st.caption(f"Data last loaded: {datetime.now().strftime('%d %b %Y, %H:%M')}")

    normal   = [t for t in tests if t["status"] == "normal"]
    abnormal = sorted(
        [t for t in tests if t["status"] in ("high", "low")],
        key=lambda t: -t["deviation"],
    )
    unknown  = [t for t in tests if t["status"] == "unknown"]

    c1, c2, c3 = st.columns(3)
    c1.metric("✅ Normal", len(normal))
    c2.metric("⚠️ Needs Attention", len(abnormal))
    c3.metric("❓ No Reference Range", len(unknown))

    if abnormal:
        st.divider()
        st.subheader("⚠️ Tests That Need Attention  (most abnormal first)")
        render_card_grid(abnormal)

    if normal:
        st.divider()
        st.subheader("✅ Normal Tests")
        render_card_grid(normal)

    if unknown:
        st.divider()
        st.subheader("❓ Tests Without a Reference Range")
        render_card_grid(unknown)


def render_chart(t):
    recs  = t["records"]
    dates = [parse_date(r["date"]) for r in recs]
    vals  = [parse_result(r["result"]) for r in recs]
    pairs = [(d, v) for d, v in zip(dates, vals) if v is not None]

    if not pairs:
        st.info("No numeric data to chart.")
        return

    xs, ys = zip(*pairs)
    lo, hi = t["lo"], t["hi"]

    fig = go.Figure()

    # Normal-range shading
    if lo is not None and hi is not None:
        fig.add_hrect(
            y0=lo, y1=hi,
            fillcolor="rgba(46,125,50,0.10)", line_width=0,
            annotation_text="Normal range",
            annotation_position="top right",
            annotation=dict(font_size=11, font_color="#2e7d32"),
        )
    elif hi is not None:
        y_floor = min(list(ys)) * 0.85
        fig.add_hrect(
            y0=y_floor, y1=hi,
            fillcolor="rgba(46,125,50,0.10)", line_width=0,
            annotation_text="Normal range",
            annotation_position="top right",
            annotation=dict(font_size=11, font_color="#2e7d32"),
        )

    if lo is not None:
        fig.add_hline(y=lo, line=dict(color="#2e7d32", dash="dash", width=1.2))
    if hi is not None:
        fig.add_hline(y=hi, line=dict(color="#2e7d32", dash="dash", width=1.2))

    point_colors = [STATUS_COLOR[classify(v, lo, hi)] for v in ys]

    fig.add_trace(go.Scatter(
        x=list(xs),
        y=list(ys),
        mode="lines+markers",
        line=dict(color="#1565c0", width=2.5),
        marker=dict(size=11, color=point_colors, line=dict(color="white", width=2)),
        hovertemplate=f"<b>%{{x|%d %b %H:%M}}</b><br>%{{y:.2f}} {t['unit']}<extra></extra>",
    ))

    fig.update_layout(
        title=f"{t['short_name']} over time",
        yaxis_title=t["unit"],
        height=300,
        margin=dict(l=6, r=6, t=40, b=6),
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    fig.update_xaxes(gridcolor="#f0f0f0")
    fig.update_yaxes(gridcolor="#f0f0f0")

    st.plotly_chart(fig, use_container_width=True)


def render_history_table(t):
    rows = []
    for r in reversed(t["records"]):
        v = parse_result(r["result"])
        lo, hi = parse_range(r["normal_range"])
        s = classify(v, lo, hi)
        rows.append({
            "Date":         parse_date(r["date"]).strftime("%d %b %Y, %H:%M"),
            "Result":       f"{v:.2f} {t['unit']}" if v is not None else str(r["result"]),
            "Normal Range": r["normal_range"],
            "Status":       STATUS_LABEL[s],
            "Lab":          r["lab_name"],
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def _show(label, text, box="info"):
    """Render a guidance field only if it has content."""
    if not text or not text.strip():
        return
    st.markdown(f"**{label}**")
    getattr(st, box)(text)


def render_detail(tests, short_name):
    t = next((x for x in tests if x["short_name"] == short_name), None)
    if t is None:
        st.error("Test not found.")
        return

    if st.button("← Back"):
        st.session_state["selected_test"] = None
        st.rerun()

    status = t["status"]
    color  = STATUS_COLOR[status]
    label  = STATUS_LABEL[status]
    fg     = t.get("family_guidance", {})

    st.title(t["full_name"])
    st.caption(f"Short code: **{t['short_name']}**  ·  {t['sub_sub_category']}")

    # Big result card (full width, stacks on phone)
    st.markdown(f"""
<div style="
    background:{STATUS_BG[status]};
    border:3px solid {color};
    border-radius:14px;
    padding:20px;
    text-align:center;
    margin-bottom:14px;
">
    <div style="font-size:0.9rem;color:#666;margin-bottom:4px;">Latest result</div>
    <div style="font-size:2.8rem;font-weight:700;color:{color};line-height:1.1;">{val_str(t)}</div>
    <div style="font-size:1.05rem;color:#777;margin-bottom:6px;">{t['unit']}</div>
    <div style="font-size:1.15rem;font-weight:600;color:{color};">{label}</div>
</div>
""", unsafe_allow_html=True)

    lo, hi = t["lo"], t["hi"]
    if lo is not None or hi is not None:
        if lo is not None and hi is not None:
            rng = f"{lo} – {hi} {t['unit']}"
        elif hi is not None:
            rng = f"Less than {hi} {t['unit']}"
        else:
            rng = f"More than {lo} {t['unit']}"
        st.info(f"**Normal Range:** {rng}")

    if t["trend"] != "—":
        st.markdown(f"**Trend:** {TREND_LABEL[t['trend']]}")

    last_dt = parse_date(t["latest"]["date"])
    st.caption(f"Recorded: {last_dt.strftime('%d %b %Y at %H:%M')}  ·  Lab: {t['latest']['lab_name']}")

    render_chart(t)

    st.divider()

    # ── What does this measure / affect? ──
    affected = fg.get("affected_system", "")
    if affected:
        st.subheader("📖 What this test measures & affects")
        st.write(affected)

    # ── Simple meaning based on direction ──
    if status == "high":
        meaning = fg.get("meaning_high_simple", "")
        if meaning:
            st.subheader("⬆️ What does HIGH mean for grandfather?")
            st.warning(meaning)
    elif status == "low":
        meaning = fg.get("meaning_low_simple", "")
        if meaning:
            st.subheader("⬇️ What does LOW mean for grandfather?")
            st.info(meaning)
    else:
        st.success(
            "✅ This value is within the normal range. "
            "No immediate action is needed for this test — keep monitoring."
        )

    # ── Expandable family guidance sections ──
    has_watchfor = any(fg.get(k) for k in ("symptoms_to_watch", "warning_signs_tonight", "critical_threshold"))
    has_diet     = any(fg.get(k) for k in ("foods_to_give", "foods_to_avoid", "hydration_guidance", "refusal_handling"))
    has_safety   = any(fg.get(k) for k in ("bedridden_risks", "supplements_safety"))
    has_hygiene  = bool(fg.get("immune_and_hygiene"))
    has_comms    = any(fg.get(k) for k in ("communication_if_confused", "emotional_support"))
    has_medical  = any(fg.get(k) for k in ("oncologist_questions", "treatment_impact", "palliative_care"))

    if has_watchfor:
        with st.expander("⚠️ What to Watch For", expanded=(status in ("high", "low"))):
            _show("Symptoms to watch for:", fg.get("symptoms_to_watch", ""), "warning")
            _show("Warning signs tonight:", fg.get("warning_signs_tonight", ""), "error")
            _show("When to call the nurse immediately:", fg.get("critical_threshold", ""), "error")

    if has_diet:
        with st.expander("🥗 Diet, Food & Hydration", expanded=False):
            _show("Foods that can help:", fg.get("foods_to_give", ""), "success")
            _show("Foods to strictly avoid:", fg.get("foods_to_avoid", ""), "warning")
            _show("Hydration guidance:", fg.get("hydration_guidance", ""), "info")
            _show("If he refuses to eat or drink:", fg.get("refusal_handling", ""), "info")

    if has_safety:
        with st.expander("🛏️ Bedridden Safety", expanded=False):
            _show("Risks from being completely bedridden:", fg.get("bedridden_risks", ""), "warning")
            _show("Vitamins & supplements safety:", fg.get("supplements_safety", ""), "info")

    if has_hygiene:
        with st.expander("🧼 Immune System & Hygiene Rules", expanded=False):
            _show("Hygiene & visitor rules:", fg.get("immune_and_hygiene", ""), "warning")

    if has_comms:
        with st.expander("💬 Communication & Emotional Support", expanded=False):
            _show("If he is confused or agitated:", fg.get("communication_if_confused", ""), "info")
            _show("Emotional support:", fg.get("emotional_support", ""), "info")

    if has_medical:
        with st.expander("🩺 Questions for the Doctor & Treatment", expanded=False):
            _show("Important questions to ask the oncologist:", fg.get("oncologist_questions", ""), "info")
            _show("How this affects treatment:", fg.get("treatment_impact", ""), "warning")
            _show("Palliative & comfort care:", fg.get("palliative_care", ""), "info")

    st.divider()
    st.subheader("📅 All Recorded Values")
    render_history_table(t)


def render_category_page(tests, cat_key):
    page_name = next((k for k, v in PAGES.items() if v == cat_key), cat_key)
    st.title(page_name)
    filtered = [t for t in tests if cat_filter(cat_key, t)]
    if not filtered:
        st.info("No tests recorded in this category yet.")
        return
    render_card_grid(filtered)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if "selected_test" not in st.session_state:
        st.session_state["selected_test"] = None

    tests = load_data()

    # ── Detail view takes over the whole screen ──
    if st.session_state["selected_test"]:
        render_detail(tests, st.session_state["selected_test"])
        return

    # ── Top navigation (phone-friendly: native dropdown, no hidden sidebar) ──
    labels = list(PAGES.keys())
    choice = st.selectbox("📋 Choose what to view", labels, key="nav_choice")
    if st.button("🔄 Reload latest results"):
        st.cache_data.clear()
        st.rerun()

    page = PAGES[choice]
    if page == "__overview__":
        render_overview(tests)
    else:
        render_category_page(tests, page)


main()
