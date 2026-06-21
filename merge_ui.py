# -*- coding: utf-8 -*-
"""
Simple drag-and-drop tool to merge new lab-result JSON files into results.json.

- Existing tests (matching id): the new daily reading(s) are appended (duplicates by
  date are skipped).
- Brand-new tests (new id): added to results.json AND a blank stub is created in
  info_en.json so the website shows them right away — then it tells you to ask the
  assistant to research their guidance.

Run with: add_results.bat   (opens at http://localhost:8502)
"""
import json
import sys
import shutil
import subprocess
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).parent
RESULTS = ROOT / "results.json"
INFO_EN = ROOT / "info_en.json"

# the 18 guidance fields each test info carries (left blank for new tests)
GUIDE_FIELDS = [
    "meaning_high_simple", "meaning_low_simple", "affected_system",
    "symptoms_to_watch", "warning_signs_tonight", "critical_threshold",
    "foods_to_give", "foods_to_avoid", "hydration_guidance", "refusal_handling",
    "bedridden_risks", "supplements_safety", "immune_and_hygiene",
    "communication_if_confused", "emotional_support", "oncologist_questions",
    "treatment_impact", "palliative_care",
]

st.set_page_config(page_title="إضافة نتائج جديدة", page_icon="➕", layout="centered")
st.markdown(
    "<style>html,body,[class*='css']{direction:rtl;text-align:right;"
    "font-family:'Segoe UI',Tahoma,'Arial';}</style>",
    unsafe_allow_html=True,
)


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def save(p, obj):
    p.write_text(json.dumps(obj, indent=4, ensure_ascii=False), encoding="utf-8")


def stub_info(entry):
    return {
        "id": entry["id"],
        "short_name": entry.get("test", ""),
        "full_name": entry.get("test", ""),
        "category": "فحص الدم",
        "sub_category": "",
        "sub_sub_category": "تحت المراجعة",
        "unit": entry.get("unit", ""),
        "family_guidance": {k: "" for k in GUIDE_FIELDS},
    }


st.title("➕ إضافة نتائج جديدة")
st.caption("اسحب وأفلت ملف/ملفات JSON (مثل new.json) أو اخترها — راح ندمجها بـ results.json تلقائياً.")

files = st.file_uploader("ملفات النتائج (JSON)", type=["json"], accept_multiple_files=True)

if files:
    try:
        results = load(RESULTS)
    except Exception as e:
        st.error(f"تعذّر قراءة results.json: {e}")
        st.stop()
    by_id = {t["id"]: t for t in results}

    # ── parse uploaded files ──
    parsed, bad = [], False
    for f in files:
        try:
            parsed.append((f.name, json.loads(f.getvalue().decode("utf-8"))))
        except Exception as e:
            st.error(f"الملف «{f.name}» فيه غلطة كتابة: {e}")
            bad = True
    if bad:
        st.stop()

    # ── simulate to build a clear plan ──
    seen = {tid: {r["date"] for r in t["records"]} for tid, t in by_id.items()}
    plan_existing, plan_new, sim_new = [], [], set()
    for name, data in parsed:
        for e in data:
            tid = e["id"]
            if tid in by_id or tid in sim_new:
                ds = seen.setdefault(tid, set())
                nn = nd = 0
                for r in e["records"]:
                    if r["date"] in ds:
                        nd += 1
                    else:
                        nn += 1; ds.add(r["date"])
                plan_existing.append((tid, e.get("test", ""), nn, nd))
            else:
                sim_new.add(tid)
                seen[tid] = {r["date"] for r in e["records"]}
                plan_new.append((tid, e.get("test", ""), len(e["records"])))

    st.subheader("📋 شنو راح يصير عند الدمج:")
    if plan_existing:
        st.markdown("**تحاليل موجودة — راح نضيفلها نتائج جديدة:**")
        for tid, test, nn, nd in plan_existing:
            extra = f"  (تم تجاهل {nd} نتيجة مكررة)" if nd else ""
            st.write(f"• #{tid} {test}: +{nn} نتيجة{extra}")
    if plan_new:
        st.markdown("**🆕 تحاليل جديدة (تحتاج بحث ومعلومات):**")
        for tid, test, n in plan_new:
            st.write(f"• #{tid} {test}: {n} نتيجة")
    if not plan_existing and not plan_new:
        st.info("ماكو شي جديد للدمج (كلها مكررة).")

    st.divider()
    if st.button("✅ دمج وحفظ", type="primary"):
        shutil.copy(RESULTS, ROOT / "results.json.bak")   # safety backup
        info_en = load(INFO_EN)
        info_ids = {t["id"] for t in info_en}
        added, created = 0, []
        for name, data in parsed:
            for e in data:
                tid = e["id"]
                if tid in by_id:
                    tgt = by_id[tid]
                    ds = {r["date"] for r in tgt["records"]}
                    for r in e["records"]:
                        if r["date"] not in ds:
                            tgt["records"].append(r); ds.add(r["date"]); added += 1
                else:
                    results.append(e); by_id[tid] = e
                    created.append(e); added += len(e["records"])
                    if tid not in info_ids:
                        info_en.append(stub_info(e)); info_ids.add(tid)

        save(RESULTS, results)
        save(INFO_EN, info_en)
        # rebuild the Arabic info.json so the new stubs show up
        subprocess.run([sys.executable, "build_ar.py"], cwd=str(ROOT),
                       capture_output=True, text=True)

        st.success(f"✅ تم الدمج! أضفنا {added} نتيجة. (نسخة احتياطية: results.json.bak)")
        if created:
            st.warning("🆕 هذي تحاليل جديدة انضافت — انسخها وابعثها للمساعد حتى يسوي بحث ويضيف معلوماتها:")
            st.code("\n".join(f"#{c['id']} {c['test']} ({c.get('unit','')})" for c in created))
        st.info("بعدها شغّل **publish.bat** حتى ترفع التحديث للموقع.")
