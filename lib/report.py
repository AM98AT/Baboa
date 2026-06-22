# -*- coding: utf-8 -*-
"""Doctor-facing one-page PDF for a category: concise clinical table, B&W printable.
English + numbers only — matplotlib can't shape Arabic, and doctors don't need it."""
from io import BytesIO
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ROWS_PER_PAGE = 28
PAGE_W, PAGE_H = 8.27, 11.69                 # A4 portrait, inches
MARGIN_X, MARGIN_TOP, MARGIN_BOT = 0.4, 0.5, 0.6   # tight sides, room for footer
FONT_PT = 9
CHAR_W = FONT_PT / 72 * 0.62                 # ~avg glyph width (in) for sizing columns
CELL_PAD = 0.20                              # total horizontal padding per column (in)
ROW_H = 0.33                                 # fixed row height (in)

from lib.parsing import parse_date, parse_result, deviation, fmt_num
from lib.scoring import risk_score

# One patient app → fixed header (English; the app's Arabic name doesn't render in PDF).
PATIENT = {"name": "Abdullah Ahmed Abdullah", "sex": "Male", "dob": "16-06-1940"}

CAT_EN = {
    "العدوى والالتهاب":            "Infection & Inflammation",
    "وظائف الكلى":                "Kidney Function",
    "فقر الدم وكريات الدم الحمر":   "Anemia & Red Cells",
    "خلايا الدم البيض والمناعة":    "White Cells & Immunity",
    "الصفيحات الدموية":            "Platelets",
    "التخثّر والقلب":              "Coagulation & Cardiac",
    "الأملاح والمعادن":            "Electrolytes & Minerals",
    "وظائف الكبد":                "Liver Function",
    "البروتين والتغذية":           "Protein & Nutrition",
    "السكّر":                     "Glucose",
}
FLAG = {"high": "H", "low": "L", "normal": "", "unknown": "?"}


def _trend_run(t):
    """(direction, run) where run = how many consecutive readings moved that way.
    'Better' = closer to the normal range, measured against the latest range."""
    vals = [parse_result(r["result"]) for r in t["records"]]   # oldest -> newest
    if len(vals) < 2 or vals[-1] is None or vals[-2] is None:
        return "new", 0
    devs = [deviation(v, t["lo"], t["hi"]) if v is not None else None for v in vals]

    def step(a, b):
        if a is None or b is None:
            return None
        if b < a - 1e-9: return "improving"
        if b > a + 1e-9: return "worsening"
        return "stable"

    last = step(devs[-2], devs[-1])
    if last in (None, "stable"):
        return "stable", 0
    run, i = 1, len(vals) - 1
    while i - 1 >= 1 and step(devs[i - 2], devs[i - 1]) == last:
        run += 1
        i -= 1
    return last, run


def _trend_text(t):
    d, n = _trend_run(t)
    if d == "worsening": return f"Worsening ({n})", "worsening"
    if d == "improving": return f"Improving ({n})", "improving"
    if d == "stable":    return "Stable", "stable"
    return "New", "new"


def file_slug(cat_key):
    return CAT_EN.get(cat_key, "report").replace(" & ", "_").replace(" ", "_")


def _age(dob):
    b = datetime.strptime(dob, "%d-%m-%Y")
    n = datetime.now()
    return n.year - b.year - ((n.month, n.day) < (b.month, b.day))


def _range_str(t):
    lo, hi = t["lo"], t["hi"]
    if lo is not None and hi is not None:
        return f"{fmt_num(lo)} - {fmt_num(hi)}"
    if hi is not None:
        return f"< {fmt_num(hi)}"
    if lo is not None:
        return f"> {fmt_num(lo)}"
    return t["latest"].get("normal_range", "-") or "-"


def _rel_date(s):
    n = (datetime.now().date() - parse_date(s).date()).days
    if n <= 0:
        return "today"
    if n == 1:
        return "1 day ago"
    return f"{n} days ago"


def category_pdf(tests, title, ordered=False):
    """Bytes of a single-page A4-landscape clinical table. Most-dangerous test first,
    unless `ordered` (then the caller's order is kept — e.g. the re-test page)."""
    rows = tests if ordered else sorted(tests, key=lambda t: -risk_score(t))
    headers = ["Test", "Result (When)", "Unit", "Flag", "Ref. Range",
               "Previous (When)", "Trend"]
    data, abnormal, trends = [], [], []
    for t in rows:
        recs = t["records"]
        cur = (f"{fmt_num(t['val'])} ({_rel_date(t['latest']['date'])})"
               if t["val"] is not None else str(t["latest"]["result"]))
        if len(recs) >= 2:
            pv = parse_result(recs[-2]["result"])
            prev = (f"{fmt_num(pv)} ({_rel_date(recs[-2]['date'])})"
                    if pv is not None else str(recs[-2]["result"]))
        else:
            prev = "-"
        trend_txt, trend_dir = _trend_text(t)
        data.append([t["short_name"], cur, t["unit"], FLAG.get(t["status"], ""),
                     _range_str(t), prev, trend_txt])
        abnormal.append(t["status"] in ("high", "low"))
        trends.append(trend_dir)

    # Paginate so any test count stays readable (overview has ~43 tests).
    pages = [(data[i:i + ROWS_PER_PAGE], abnormal[i:i + ROWS_PER_PAGE],
              trends[i:i + ROWS_PER_PAGE])
             for i in range(0, len(data), ROWS_PER_PAGE)] or [([], [], [])]
    buf = BytesIO()
    with PdfPages(buf) as pdf:
        for idx, (pdata, pabn, ptr) in enumerate(pages, start=1):
            fig = _draw_page(pdata, pabn, ptr, headers, title, idx, len(pages))
            pdf.savefig(fig)          # full A4 sheet (no tight crop → real margins)
            plt.close(fig)
    return buf.getvalue()


def _draw_page(data, abnormal, trends, headers, title, page_no, n_pages):
    fig, ax = plt.subplots(figsize=(PAGE_W, PAGE_H))   # A4 portrait
    content_w = PAGE_W - 2 * MARGIN_X
    content_h = PAGE_H - MARGIN_TOP - MARGIN_BOT
    ax.set_position([MARGIN_X / PAGE_W, MARGIN_BOT / PAGE_H,
                     content_w / PAGE_W, content_h / PAGE_H])
    ax.axis("off")

    ax.text(0, 1.0, PATIENT["name"], fontsize=15, fontweight="bold",
            transform=ax.transAxes, va="top")
    ax.text(0, 0.965, f"{PATIENT['sex']}  |  DOB {PATIENT['dob']}  ({_age(PATIENT['dob'])}y)",
            fontsize=10, transform=ax.transAxes, va="top")
    ax.text(1, 1.0, title, fontsize=13, fontweight="bold",
            transform=ax.transAxes, va="top", ha="right")

    # Column widths from the longest cell in each column (+ padding); shrink to fit
    # if the total would exceed the printable width.
    ncol = len(headers)
    cols = list(zip(*([headers] + data))) if data else [[h] for h in headers]
    widths = [CELL_PAD + max(len(str(x)) for x in col) * CHAR_W for col in cols]
    total = sum(widths)
    if total > content_w:
        widths = [w * content_w / total for w in widths]
        total = content_w
    total_frac = total / content_w
    x0 = (1 - total_frac) / 2                    # center the table horizontally

    top = 0.93
    row_frac = ROW_H / content_h
    height = row_frac * (len(data) + 1)
    tbl = ax.table(cellText=data or [[""] * ncol], colLabels=headers, cellLoc="center",
                   colWidths=widths, bbox=[x0, top - height, total_frac, height])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(FONT_PT)
    for cell in tbl.get_celld().values():        # center text vertically too
        cell.set_text_props(va="center")
        cell.PAD = 0.04

    for c in range(ncol):                        # header row
        tbl[(0, c)].set_text_props(fontweight="bold", color="white", va="center")
        tbl[(0, c)].set_facecolor("#37474f")
    for i, ab in enumerate(abnormal, start=1):   # out-of-range rows: grey shading (B&W-safe)
        if ab:
            for c in range(ncol):
                tbl[(i, c)].set_facecolor("#e6e6e6")
    for i, tr in enumerate(trends, start=1):     # trend distinction: type style, no color
        if tr == "worsening":
            tbl[(i, ncol - 1)].set_text_props(fontweight="bold", va="center")
        elif tr == "improving":
            tbl[(i, ncol - 1)].set_text_props(fontstyle="italic", va="center")

    if n_pages > 1:                              # page number at the bottom
        fig.text(0.5, MARGIN_BOT / PAGE_H / 2, f"{page_no} / {n_pages}",
                 ha="center", va="center", fontsize=9, color="#444")
    return fig


if __name__ == "__main__":   # ponytail: one runnable check — valid PDF, dangerous row on top
    def mk(short, status, dev, val):
        return {"short_name": short, "status": status, "deviation": dev, "trend": "worsening",
                "val": val, "unit": "x", "lo": 1, "hi": 5, "latest": {"result": val, "date": "22/06/2026 10:00"},
                "records": [{"result": 2, "date": "20/06/2026 10:00"}, {"result": val, "date": "22/06/2026 10:00"}]}
    sample = [mk("Calm", "normal", 0, 3), mk("Danger", "high", 1.5, 12)]
    pdf = category_pdf(sample, "Glucose")
    assert pdf[:4] == b"%PDF", pdf[:8]
    assert sorted(sample, key=lambda t: -risk_score(t))[0]["short_name"] == "Danger"
    # run count: 3 steps worse in a row (lo=1,hi=5: 4->6->9->14 all rising past hi)
    worse = {"lo": 1, "hi": 5, "records": [{"result": v, "date": "2%d-06-2026 10:00" % i}
             for i, v in enumerate([4, 6, 9, 14], start=1)]}
    assert _trend_run(worse) == ("worsening", 3), _trend_run(worse)
    print("ok", len(pdf), "bytes")
