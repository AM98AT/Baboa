# -*- coding: utf-8 -*-
"""Doctor-facing one-page PDF for a category: concise clinical table, B&W printable.
English + numbers only — matplotlib can't shape Arabic, and doctors don't need it."""
from io import BytesIO
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lib.parsing import parse_date, parse_result, fmt_num
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
TREND_EN = {"improving": "Improving", "worsening": "Worsening",
            "stable": "Stable", "—": "New"}
FLAG = {"high": "H", "low": "L", "normal": "", "unknown": "?"}


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


def _short_date(s):
    return parse_date(s).strftime("%d/%m")


def category_pdf(tests, cat_key):
    """Bytes of a single-page A4-landscape clinical table, most-dangerous test first."""
    rows = sorted(tests, key=lambda t: -risk_score(t))
    headers = ["Test", "Result (Date)", "Unit", "Flag", "Ref. Range",
               "Previous (Date)", "Trend"]
    data, abnormal = [], []
    for t in rows:
        recs = t["records"]
        cur = (f"{fmt_num(t['val'])} ({_short_date(t['latest']['date'])})"
               if t["val"] is not None else str(t["latest"]["result"]))
        if len(recs) >= 2:
            pv = parse_result(recs[-2]["result"])
            prev = (f"{fmt_num(pv)} ({_short_date(recs[-2]['date'])})"
                    if pv is not None else str(recs[-2]["result"]))
        else:
            prev = "-"
        data.append([t["short_name"], cur, t["unit"], FLAG.get(t["status"], ""),
                     _range_str(t), prev, TREND_EN.get(t["trend"], "")])
        abnormal.append(t["status"] in ("high", "low"))

    fig, ax = plt.subplots(figsize=(11.69, 8.27))   # A4 landscape
    ax.axis("off")

    ax.text(0, 1.0, PATIENT["name"], fontsize=15, fontweight="bold",
            transform=ax.transAxes, va="top")
    ax.text(0, 0.965, f"{PATIENT['sex']}  |  DOB {PATIENT['dob']}  ({_age(PATIENT['dob'])}y)",
            fontsize=10, transform=ax.transAxes, va="top")
    ax.text(1, 1.0, CAT_EN.get(cat_key, cat_key), fontsize=13, fontweight="bold",
            transform=ax.transAxes, va="top", ha="right")
    ax.text(1, 0.965, datetime.now().strftime("Printed %Y-%m-%d %H:%M"),
            fontsize=9, color="#444", transform=ax.transAxes, va="top", ha="right")

    tbl = ax.table(cellText=data, colLabels=headers, cellLoc="left",
                   colWidths=[0.22, 0.16, 0.10, 0.06, 0.15, 0.16, 0.11],
                   bbox=[0, 0, 1, 0.92])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9.5)

    ncol = len(headers)
    for c in range(ncol):                       # header row
        cell = tbl[(0, c)]
        cell.set_text_props(fontweight="bold", color="white")
        cell.set_facecolor("#37474f")
    for i, ab in enumerate(abnormal, start=1):  # abnormal rows: shaded + bold (prints in B&W)
        for c in range(ncol):
            cell = tbl[(i, c)]
            cell.set_height(cell.get_height() * 1.4)
            if ab:
                cell.set_facecolor("#e6e6e6")
                cell.set_text_props(fontweight="bold")

    buf = BytesIO()
    fig.savefig(buf, format="pdf", bbox_inches="tight")
    plt.close(fig)
    return buf.getvalue()


if __name__ == "__main__":   # ponytail: one runnable check — valid PDF, dangerous row on top
    def mk(short, status, dev, val):
        return {"short_name": short, "status": status, "deviation": dev, "trend": "worsening",
                "val": val, "unit": "x", "lo": 1, "hi": 5, "latest": {"result": val, "date": "22/06/2026 10:00"},
                "records": [{"result": 2, "date": "20/06/2026 10:00"}, {"result": val, "date": "22/06/2026 10:00"}]}
    sample = [mk("Calm", "normal", 0, 3), mk("Danger", "high", 1.5, 12)]
    pdf = category_pdf(sample, "السكّر")
    assert pdf[:4] == b"%PDF", pdf[:8]
    assert sorted(sample, key=lambda t: -risk_score(t))[0]["short_name"] == "Danger"
    print("ok", len(pdf), "bytes")
