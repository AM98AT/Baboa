import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from urllib.parse import quote
import re

st.set_page_config(
    page_title="متابعة الصحّة اليومية",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Mobile-first + Arabic right-to-left styling ──────────────────────────────────
st.markdown("""
<style>
/* whole app right-to-left, Arabic-friendly fonts */
html, body, .stApp, .block-container, [data-testid="stMarkdownContainer"] {
    direction: rtl; text-align: right;
    font-family: "Segoe UI", Tahoma, "Noto Naskh Arabic", "Arial", sans-serif; }
/* hide Streamlit's own top toolbar (it overlaps content on mobile) */
header[data-testid="stHeader"] { display: none; }
/* our own fixed header bar */
.app-header { position: fixed; top: 0; left: 0; right: 0; height: 52px; z-index: 1000;
    background: #1565c0; color: #fff; display: flex; align-items: center;
    justify-content: center; font-size: 1.15rem; font-weight: 700;
    box-shadow: 0 2px 6px rgba(0,0,0,0.25); }
/* tighter padding + readable width on phones; top space clears the fixed header */
.block-container { padding-top: 4.3rem; padding-bottom: 3rem;
    padding-left: 0.8rem; padding-right: 0.8rem; max-width: 640px; }
/* bigger base text for older eyes */
html, body, [class*="css"] { font-size: 17px; }
/* full-width, tall, rounded buttons = easy to tap */
.stButton > button { width: 100%; padding: 0.65rem 0.8rem;
    font-size: 1.05rem; border-radius: 12px; font-weight: 600; }
/* hide menu/footer clutter */
#MainMenu, footer { visibility: hidden; }
/* expander headers larger and easier to tap */
.streamlit-expanderHeader, details summary { font-size: 1.05rem !important; }
/* metric numbers sized so 3 fit on a phone row */
[data-testid="stMetricValue"] { font-size: 1.5rem; }
[data-testid="stMetricLabel"] { font-size: 0.8rem; }
/* keep the chart itself left-to-right so numbers/dates read correctly */
[data-testid="stPlotlyChart"] { direction: ltr; }
/* link styled as a full-width "See details" button */
a.seebtn { display:block; width:100%; box-sizing:border-box; text-align:center;
    background:#1565c0; color:#fff !important; text-decoration:none;
    padding:0.6rem 0.8rem; border-radius:12px; font-weight:700; font-size:1.02rem;
    margin:2px 0 12px 0; }
/* sticky back bar that scrolls with you */
a.backbtn { position:sticky; top:52px; z-index:900; display:block; width:100%;
    box-sizing:border-box; text-align:center; background:#37474f; color:#fff !important;
    text-decoration:none; padding:0.7rem; border-radius:0 0 12px 12px; font-weight:700;
    font-size:1.08rem; margin-bottom:12px; box-shadow:0 2px 6px rgba(0,0,0,0.2); }
/* navigation chips */
a.navchip { display:inline-block; margin:3px; padding:7px 12px; border-radius:18px;
    text-decoration:none; font-weight:600; font-size:0.95rem; }
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
    "normal":  "✅ طبيعي",
    "low":     "⬇️ أوطى من الطبيعي",
    "high":    "⬆️ أعلى من الطبيعي",
    "unknown": "❓ بدون معدّل",
}
TREND_LABEL = {
    "improving": "📈 يتحسّن",
    "worsening": "📉 يسوء",
    "stable":    "➡️ مستقر",
    "—":         "",
}

PAGES = {
    "📊 نظرة عامة":          "__overview__",
    "📘 إرشادات عامة للعائلة": "__general__",
    "🩸 تحليل الدم":         "cbc",
    "🫀 وظائف الكلى":        "kidney",
    "🫁 وظائف الكبد":        "liver",
    "🔥 الالتهاب":           "inflam",
    "⚡ الأملاح (الكهارل)":  "electro",
    "❤️ القلب والتخثّر":     "cardiac",
    "🧪 تحاليل ثانية":       "other",
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

def ratio_text(t):
    """Ratio of result vs the normal range, per family's formula."""
    val, lo, hi, status = t["val"], t["lo"], t["hi"], t["status"]
    if val is None:
        return None
    if status == "high" and hi:
        return f"أعلى من الطبيعي بنسبة {val / hi * 100:.0f}%"
    if status == "low" and val and lo:
        return f"أوطى من الطبيعي بنسبة {lo / val * 100:.0f}%"
    if status == "normal":
        return "ضمن المعدّل الطبيعي"
    return None

# How serious an abnormality in each test is (1=minor, 10=life-threatening).
CLINICAL_WEIGHT = {
    "CRP": 10, "PCT": 10, "D-dimer": 10, "Troponin I": 10,
    "Na": 9, "K": 9, "S. Creatinine": 9, "Hb": 9, "Albumin": 9,
    "Neutrophils (Absolute)": 9,
    "S. Urea": 8, "S. Calcium": 8, "Ionized Ca": 8, "Platelets": 8, "WBC": 8,
    "PCV": 7, "RBC": 7, "HbA1c": 7, "Total Bilirubin": 7,
    "Cl": 6, "LDH": 6, "AST (GOT)": 6, "ALT (GPT)": 6, "ALP": 6,
    "Neutrophils (Relative)": 6, "Lymphocytes (Absolute)": 6,
    "Uric Acid": 5, "MPV": 5, "Lymphocytes (Relative)": 5,
    "MCV": 4, "MCH": 4, "MCHC": 4, "RDW": 4, "Monocytes (Absolute)": 4,
    "PDW": 3, "PCT (Plateletcrit)": 3, "Monocytes (Relative)": 3,
    "MXD (Relative)": 3, "MXD (Absolute)": 3,
}

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

# Fields that are usually identical for every test → shown once on the general page,
# and only shown on a test if that test has its own different (specific) version.
GENERAL_FIELDS = [
    "refusal_handling", "bedridden_risks", "immune_and_hygiene",
    "communication_if_confused", "emotional_support",
]

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

# ── Components ─────────────────────────────────────────────────────────────────

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


# ── Pairing of (Relative %) + (Absolute) tests into one unit ────────────────────

PAIR_SUFFIXES = (" (Relative)", " (Absolute)")

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


def render_overview(tests):
    st.title("🏥 لوحة متابعة الصحّة")
    st.caption(f"آخر تحديث للبيانات: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    units    = build_units(tests)
    normal   = [u for u in units if unit_status(u) == "normal"]
    abnormal = sorted(
        [u for u in units if unit_status(u) in ("high", "low")],
        key=lambda u: (-unit_risk(u), -unit_dev(u)),
    )
    unknown  = [u for u in units if unit_status(u) == "unknown"]

    c1, c2, c3 = st.columns(3)
    c1.metric("✅ طبيعي", len(normal))
    c2.metric("⚠️ ينتبهله", len(abnormal))
    c3.metric("❓ بدون معدّل", len(unknown))

    if abnormal:
        st.divider()
        st.subheader("⚠️ تحاليل تحتاج انتباه (الأهم بالأول)")
        render_units(abnormal)

    if normal:
        st.divider()
        st.subheader("✅ تحاليل طبيعية")
        render_units(normal)

    if unknown:
        st.divider()
        st.subheader("❓ تحاليل بدون معدّل مرجعي")
        render_units(unknown)


@st.cache_data(show_spinner=False, ttl=60)
def _chart_png(title, subtitle, unit, xs, ys, colors, lo, hi):
    """Render the trend as a static PNG image (non-interactive, downloadable)."""
    fig = go.Figure()
    if lo is not None and hi is not None:
        fig.add_hrect(y0=lo, y1=hi, fillcolor="rgba(46,125,50,0.10)", line_width=0)
    elif hi is not None:
        fig.add_hrect(y0=min(ys) * 0.85, y1=hi, fillcolor="rgba(46,125,50,0.10)", line_width=0)
    if lo is not None:
        fig.add_hline(y=lo, line=dict(color="#2e7d32", dash="dash", width=1.4))
    if hi is not None:
        fig.add_hline(y=hi, line=dict(color="#2e7d32", dash="dash", width=1.4))

    fig.add_trace(go.Scatter(
        x=list(xs), y=list(ys), mode="lines+markers+text",
        text=[f"{v:g}" for v in ys], textposition="top center",
        textfont=dict(size=15, color="#222"),
        line=dict(color="#1565c0", width=3),
        marker=dict(size=14, color=list(colors), line=dict(color="white", width=2)),
    ))
    fig.update_layout(
        title=dict(text=f"{title}<br><sub>{subtitle}</sub>", x=0.5, xanchor="center",
                   font=dict(size=22)),
        yaxis_title=unit, height=540, width=900,
        margin=dict(l=20, r=20, t=90, b=90),
        showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
        font=dict(size=15),
    )
    # One labelled tick per reading; show the DAY (date), not the time.
    fig.update_xaxes(
        tickmode="array",
        tickvals=list(xs),
        ticktext=[d.strftime("%d/%m/%Y") for d in xs],
        tickangle=-45, ticks="outside", ticklen=6,
        showgrid=True, gridcolor="#ddd", gridwidth=1,
    )
    fig.update_yaxes(gridcolor="#eee")
    return fig.to_image(format="png", scale=2)


def render_chart(t):
    recs  = t["records"]
    pairs = [(parse_date(r["date"]), parse_result(r["result"])) for r in recs]
    pairs = [(d, v) for d, v in pairs if v is not None]
    if not pairs:
        st.info("ماكو بيانات رقمية حتى نرسمها.")
        return

    xs, ys = zip(*pairs)
    lo, hi = t["lo"], t["hi"]
    if lo is not None and hi is not None:
        rng = f"المعدّل الطبيعي: {lo} - {hi}"
    elif hi is not None:
        rng = f"المعدّل الطبيعي: أوطى من {hi}"
    elif lo is not None:
        rng = f"المعدّل الطبيعي: أعلى من {lo}"
    else:
        rng = "ماكو معدّل مرجعي"
    subtitle = f"{rng}  ·  الوحدة: {t['unit']}"
    colors = tuple(STATUS_COLOR[classify(v, lo, hi)] for v in ys)

    try:
        png = _chart_png(t["full_name"], subtitle, t["unit"], tuple(xs), tuple(ys), colors, lo, hi)
        st.image(png, use_container_width=True)
        st.caption("📷 اضغط مطوّلاً على الصورة حتى تحفظها أو تشاركها.")
    except Exception:
        # Fallback: static (non-zoomable) interactive chart if image export is unavailable
        fig = go.Figure()
        if lo is not None and hi is not None:
            fig.add_hrect(y0=lo, y1=hi, fillcolor="rgba(46,125,50,0.10)", line_width=0)
        if lo is not None:
            fig.add_hline(y=lo, line=dict(color="#2e7d32", dash="dash"))
        if hi is not None:
            fig.add_hline(y=hi, line=dict(color="#2e7d32", dash="dash"))
        fig.add_trace(go.Scatter(x=list(xs), y=list(ys), mode="lines+markers",
                                 line=dict(color="#1565c0", width=2.5),
                                 marker=dict(size=11, color=list(colors))))
        fig.update_layout(title=f"{t['full_name']} — {subtitle}", height=340,
                          margin=dict(l=6, r=6, t=50, b=70), showlegend=False,
                          plot_bgcolor="white", paper_bgcolor="white")
        fig.update_xaxes(tickmode="array", tickvals=list(xs),
                         ticktext=[d.strftime("%d/%m/%Y") for d in xs],
                         tickangle=-45, showgrid=True, gridcolor="#ddd")
        st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True, "displayModeBar": False})


def render_history_table(t):
    rows = []
    for r in reversed(t["records"]):
        v = parse_result(r["result"])
        lo, hi = parse_range(r["normal_range"])
        s = classify(v, lo, hi)
        rows.append({
            "التاريخ":        parse_date(r["date"]).strftime("%Y-%m-%d %H:%M"),
            "النتيجة":        f"{v:.2f} {t['unit']}" if v is not None else str(r["result"]),
            "المعدّل الطبيعي": r["normal_range"],
            "الحالة":         STATUS_LABEL[s],
            "المختبر":        r["lab_name"],
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def render_detail(tests, short_name, back_page="__overview__"):
    t = next((x for x in tests if x["short_name"] == short_name), None)
    back_href = f"?page={quote(back_page)}"
    if t is None:
        st.markdown(f'<a class="backbtn" href="{back_href}" target="_self">→ رجوع للقائمة</a>',
                    unsafe_allow_html=True)
        st.error("التحليل مو موجود.")
        return

    # Sticky back link (real navigation → the phone back button works too)
    st.markdown(f'<a class="backbtn" href="{back_href}" target="_self">→ رجوع للقائمة</a>',
                unsafe_allow_html=True)

    status = t["status"]
    color  = STATUS_COLOR[status]
    label  = STATUS_LABEL[status]
    fg     = t.get("family_guidance", {})

    st.title(t["full_name"])
    st.caption(f"الرمز: **{t['short_name']}**  ·  {t['sub_sub_category']}")

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
    <div style="font-size:0.9rem;color:#666;margin-bottom:4px;">آخر نتيجة</div>
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
            rng = f"أوطى من {hi} {t['unit']}"
        else:
            rng = f"أعلى من {lo} {t['unit']}"
        st.info(f"**المعدّل الطبيعي:** {rng}")

    if t["trend"] != "—":
        st.markdown(f"**الاتجاه:** {TREND_LABEL[t['trend']]}")

    last_dt = parse_date(t["latest"]["date"])
    st.caption(f"وقت التسجيل: {last_dt.strftime('%Y-%m-%d %H:%M')}  ·  المختبر: {t['latest']['lab_name']}")

    # If this test has a Relative/Absolute partner, show its latest value too.
    partner = partner_of(tests, t)
    if partner:
        kind = "النسبة المئوية" if partner["short_name"].endswith("(Relative)") else "العدد المطلق"
        pcolor = STATUS_COLOR[partner["status"]]
        st.markdown(
            f"<div style='margin-bottom:8px'>القياس الآخر لنفس التحليل — "
            f"<b>{kind}:</b> <span style='color:{pcolor};font-weight:700'>"
            f"{val_str(partner)} {partner['unit']}</span> ({STATUS_LABEL[partner['status']]})</div>",
            unsafe_allow_html=True,
        )

    render_chart(t)

    st.divider()

    # ── What does this measure / affect? ──
    affected = fg.get("affected_system", "")
    if affected:
        st.subheader("📖 شنو يقيس هذا التحليل وعلى شنو يأثّر")
        st.write(affected)

    # ── Simple meaning based on direction ──
    if status == "high":
        meaning = fg.get("meaning_high_simple", "")
        if meaning:
            st.subheader("⬆️ شنو يعني لمن يكون عالي عنده؟")
            st.warning(meaning)
    elif status == "low":
        meaning = fg.get("meaning_low_simple", "")
        if meaning:
            st.subheader("⬇️ شنو يعني لمن يكون واطي عنده؟")
            st.info(meaning)
    else:
        st.success(
            "✅ هاي القيمة ضمن المعدّل الطبيعي. "
            "ماكو إجراء عاجل لهذا التحليل — بس استمرّوا بالمتابعة."
        )

    # ── Family guidance: only test-SPECIFIC info here; generic stuff lives on the
    #    "إرشادات عامة للعائلة" page so it isn't repeated on every test. ──
    generic = generic_values(tests)

    def has_field(k):
        return bool(fg.get(k, "").strip())

    def is_specific(k):
        # a general field is only shown here if this test overrides the generic text
        return has_field(k) and fg.get(k, "") != generic.get(k, "")

    _shown = []   # word-sets of fields already displayed, to skip near-duplicates

    def _norm(s):
        s = re.sub(r"المصدر:.*$", "", s)          # ignore the source tag when comparing
        return set(re.findall(r"[؀-ۿ]+", s))

    def show(label, k, box, general=False):
        v = fg.get(k, "")
        if not v or not v.strip():
            return
        if general and v == generic.get(k, ""):   # generic copy → skip (it's on general page)
            return
        words = _norm(v)
        for prev in _shown:                       # skip if it mostly repeats an earlier field
            if words and len(words & prev) / len(words | prev) > 0.7:
                return
        _shown.append(words)
        st.markdown(f"**{label}**")
        getattr(st, box)(v)

    has_watchfor = any(has_field(k) for k in ("symptoms_to_watch", "warning_signs_tonight", "critical_threshold"))
    has_diet     = any(has_field(k) for k in ("foods_to_give", "foods_to_avoid", "hydration_guidance")) or is_specific("refusal_handling")
    has_safety   = has_field("supplements_safety") or is_specific("bedridden_risks")
    has_hygiene  = is_specific("immune_and_hygiene")
    has_comms    = is_specific("communication_if_confused") or is_specific("emotional_support")
    has_medical  = any(has_field(k) for k in ("oncologist_questions", "treatment_impact", "palliative_care"))

    if has_watchfor:
        with st.expander("⚠️ شنو نراقب", expanded=(status in ("high", "low"))):
            show("أعراض نراقبها:", "symptoms_to_watch", "warning")
            show("علامات خطر هاي الليلة:", "warning_signs_tonight", "error")
            show("متى تتصل بالممرضة فوراً:", "critical_threshold", "error")

    if has_diet:
        with st.expander("🥗 الأكل والشرب", expanded=False):
            show("أكلات ممكن تساعد:", "foods_to_give", "success")
            show("أكلات لازم نتجنّبها:", "foods_to_avoid", "warning")
            show("إرشادات الترطيب (السوائل):", "hydration_guidance", "info")
            show("إذا رفض ياكل أو يشرب:", "refusal_handling", "info", general=True)

    if has_safety:
        with st.expander("🛏️ السلامة وهو طريح الفراش", expanded=False):
            show("مخاطر خاصة بهذا التحليل:", "bedridden_risks", "warning", general=True)
            show("سلامة الفيتامينات والمكمّلات:", "supplements_safety", "info")

    if has_hygiene:
        with st.expander("🧼 المناعة وقواعد النظافة (خاص بهذا التحليل)", expanded=False):
            show("قواعد النظافة والزيارة:", "immune_and_hygiene", "warning", general=True)

    if has_comms:
        with st.expander("💬 التواصل والدعم النفسي (خاص بهذا التحليل)", expanded=False):
            show("إذا صار مشوّش أو منزعج:", "communication_if_confused", "info", general=True)
            show("الدعم النفسي:", "emotional_support", "info", general=True)

    if has_medical:
        with st.expander("🩺 أسئلة للطبيب والعلاج", expanded=False):
            show("أسئلة مهمة تنطرح على طبيب الأورام:", "oncologist_questions", "info")
            show("شلون يأثّر على العلاج:", "treatment_impact", "warning")
            show("الرعاية التلطيفية والمريحة:", "palliative_care", "info")

    st.info("📘 الإرشادات العامة (الأكل عند الرفض، النظافة، الدعم النفسي، التواصل، ومخاطر الفراش) موجودة بصفحة **«إرشادات عامة للعائلة»** — تنطبق على كل التحاليل.")

    st.divider()
    st.subheader("📅 كل النتائج المسجّلة")
    render_history_table(t)

    st.markdown(
        f'<a class="seebtn" style="background:#37474f;" href="?page={quote(back_page)}" '
        f'target="_self">→ رجوع للقائمة</a>',
        unsafe_allow_html=True,
    )


def render_category_page(tests, cat_key):
    page_name = next((k for k, v in PAGES.items() if v == cat_key), cat_key)
    st.title(page_name)
    filtered = [t for t in tests if cat_filter(cat_key, t)]
    if not filtered:
        st.info("ماكو تحاليل مسجّلة بهذا القسم لحد الحين.")
        return
    render_card_grid(filtered)


def render_general(tests):
    st.title("📘 إرشادات عامة للعائلة")
    st.caption("هذي الإرشادات تنطبق على كل التحاليل — مكتوبة مرة وحدة هنا حتى ما تتكرر بكل تحليل.")

    st.error(
        "🚨 **بأي حالة طارئة:** نادوا الممرضة أو الطبيب بالجناح فوراً — لا تنتظرون. "
        "علامات الطوارئ: ضيق نفس شديد، نزيف، تشويش مفاجئ، تشنّج، أو فقدان وعي."
    )

    generic = generic_values(tests)
    sections = [
        ("🍽️ إذا رفض ياكل أو يشرب",              "refusal_handling",          "info"),
        ("🛏️ مخاطر كونه طريح الفراش وشلون نحميه", "bedridden_risks",           "warning"),
        ("🧼 المناعة وقواعد النظافة والزيارة",     "immune_and_hygiene",        "warning"),
        ("💬 شلون نحچي وياه إذا صار مشوّش",        "communication_if_confused", "info"),
        ("❤️ الدعم النفسي",                       "emotional_support",         "info"),
    ]
    for title, k, box in sections:
        v = generic.get(k, "")
        if v:
            st.subheader(title)
            getattr(st, box)(v)


# ── Main ───────────────────────────────────────────────────────────────────────

def render_nav(active):
    chips = []
    for label, key in PAGES.items():
        style = ("background:#1565c0;color:#fff;" if key == active
                 else "background:#e7eefc;color:#1565c0;")
        chips.append(f'<a class="navchip" style="{style}" href="?page={quote(key)}" '
                     f'target="_self">{label}</a>')
    st.markdown('<div style="margin-bottom:10px">' + "".join(chips) + "</div>",
                unsafe_allow_html=True)


def main():
    st.markdown('<div class="app-header">🏥 متابعة الصحّة اليومية</div>',
                unsafe_allow_html=True)
    tests = load_data()
    qp = st.query_params

    # ── A test is open: show its detail page (real URL = phone back works) ──
    test = qp.get("test")
    if test:
        render_detail(tests, test, back_page=qp.get("page", "__overview__"))
        return

    # ── List views: navigation is real URL links (chips) ──
    page = qp.get("page", "__overview__")
    if page not in PAGES.values():
        page = "__overview__"
    render_nav(page)
    if st.button("🔄 حمّل آخر النتائج"):
        st.cache_data.clear()
        st.rerun()

    if page == "__overview__":
        render_overview(tests)
    elif page == "__general__":
        render_general(tests)
    else:
        render_category_page(tests, page)


main()
