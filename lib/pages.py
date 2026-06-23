# -*- coding: utf-8 -*-
"""Page renderers, navigation, and the main() router."""
import re
import json
from urllib.parse import quote
from datetime import datetime
import streamlit as st
import pandas as pd

from lib.constants import (STATUS_COLOR, STATUS_BG, STATUS_LABEL, TREND_LABEL,
                           SPECIAL_PAGES, CATEGORY_PAGES, ADD_PAGES, PAGES)
from lib.parsing import parse_date, parse_result, parse_range, classify, fmt_num
from lib.scoring import risk_score
from lib.units import build_units, unit_status, unit_risk, unit_dev, partner_of
from lib.charts import render_chart
from lib.data import load_data, load_users, load_catalog
from lib.ui import val_str, generic_values, render_units
from lib.report import category_pdf, file_slug, CAT_EN
from lib import github_store

# Identity for the active user's PDF header — set by main() each run so the four
# pdf_button() call sites don't all need a `patient` argument. ponytail: a 1-run global.
_PATIENT = None


def pdf_button(tests, title, slug, label, ordered=False):
    """Doctor-PDF download (B&W, most-dangerous-first unless `ordered`). Two buttons:
    one with dates relative to today, one relative to tomorrow (print now, show the
    doctor tomorrow → today's labs read 'Yesterday')."""
    if not tests:
        return
    st.divider()
    st.markdown(f"**{label}**")
    c1, c2 = st.columns(2)
    c1.download_button(
        "⬇️ للعرض اليوم",
        data=category_pdf(tests, title, ordered=ordered, patient=_PATIENT),
        file_name=f"{slug}.pdf", mime="application/pdf",
        use_container_width=True, key=f"pdf_{slug}_today",
    )
    c2.download_button(
        "⬇️ للعرض باجر",
        data=category_pdf(tests, title, ordered=ordered, ref_offset=1, patient=_PATIENT),
        file_name=f"{slug}_tomorrow.pdf", mime="application/pdf",
        use_container_width=True, key=f"pdf_{slug}_tomorrow",
    )


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

    pdf_button(tests, "All Tests - Overview", "all_tests",
               "⬇️ نزّل تقرير كل التحاليل للطبيب (PDF — للطباعة)")


def render_history_table(t):
    rows = []
    for r in reversed(t["records"]):
        v = parse_result(r["result"])
        lo, hi = parse_range(r["normal_range"])
        s = classify(v, lo, hi)
        rows.append({
            "التاريخ":        parse_date(r["date"]).strftime("%Y-%m-%d %H:%M"),
            "النتيجة":        f"{fmt_num(v)} {t['unit']}" if v is not None else str(r["result"]),
            "المعدّل الطبيعي": r["normal_range"],
            "الحالة":         STATUS_LABEL[s],
            "المختبر":        r["lab_name"],
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def render_detail(tests, short_name, back_page="__overview__"):
    t = next((x for x in tests if x["short_name"] == short_name), None)
    u = st.query_params.get("user", "")
    back_href = f"?page={quote(back_page)}" + (f"&user={quote(u)}" if u else "")
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
    st.caption(f"الرمز: **{t['display_name']}**  ·  {t['sub_sub_category']}")

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
            rng = f"{fmt_num(lo)} – {fmt_num(hi)}"
        elif hi is not None:
            rng = f"أقل من {fmt_num(hi)}"
        else:
            rng = f"أعلى من {fmt_num(lo)}"
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
            st.subheader("⬇️ شنو يعني لمن يكون قليل عنده؟")
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
        f'<a class="seebtn" style="background:#37474f;" href="{back_href}" '
        f'target="_self">→ رجوع للقائمة</a>',
        unsafe_allow_html=True,
    )


def render_today(tests):
    st.title("🆕 تحاليل اليوم")
    dated = [(parse_date(t["latest"]["date"]).date(), t) for t in tests if t.get("latest")]
    if not dated:
        st.info("ماكو فحوصات مسجّلة لحد الحين.")
        return

    recent = max(d for d, _ in dated)
    todays = [t for d, t in dated if d == recent]
    gap = (datetime.now().date() - recent).days
    ds = recent.strftime("%d/%m/%Y")

    if gap <= 0:
        st.success(f"✅ فحوصات اليوم ({ds}) — عددها {len(todays)}")
    else:
        if gap == 1:    g = "يوم واحد"
        elif gap == 2:  g = "يومين"
        elif gap <= 10: g = f"{gap} أيام"
        else:           g = f"{gap} يوم"
        st.warning(f"⚠️ ماكو فحوصات جديدة من {g}. هذي آخر فحوصات اللي انعملت (بتاريخ {ds}):")

    units = sorted(build_units(todays), key=lambda u: -unit_risk(u))
    render_units(units)
    pdf_button(todays, f"Latest Labs {ds}", "latest_labs",
               "⬇️ نزّل تقرير فحوصات اليوم للطبيب (PDF — للطباعة)")


def render_redo(tests):
    st.title("⏰ شنو نعيد فحصه")
    st.caption(
        "التحاليل اللي نتيجتها مو طبيعية (عالية أو قليلة) أول — حتى لو انفحصت اليوم — "
        "وداخل كل مجموعة الأقدم فحصاً أول. هيچ تعرفون شنو الأهم تعيدون فحصه."
    )
    today = datetime.now().date()

    def days_since(u):
        rep = u["test"] if u["kind"] == "single" else u["abs"]
        return (today - parse_date(rep["latest"]["date"]).date()).days

    def is_normal(u):
        # abnormal (high/low) → 0 = on top; normal/unknown → 1 = below
        return 0 if unit_status(u) in ("high", "low") else 1

    # same key on individual tests, for the PDF (which lists each test as its own row)
    ordered = sorted(
        tests,
        key=lambda t: (0 if t["status"] in ("high", "low") else 1,
                       -(today - parse_date(t["latest"]["date"]).date()).days),
    )
    # abnormal first, then longest-since-tested first within each group
    units = sorted(build_units(tests), key=lambda u: (is_normal(u), -days_since(u)))
    render_units(units)
    pdf_button(ordered, "Re-test Priority", "retest_priority",
               "⬇️ نزّل تقرير الإعادة للطبيب (PDF — للطباعة)", ordered=True)


def render_category_page(tests, cat_key):
    page_name = next((k for k, v in PAGES.items() if v == cat_key), cat_key)
    st.title(page_name)
    filtered = [t for t in tests if t["sub_sub_category"] == cat_key]
    if not filtered:
        st.info("ماكو تحاليل مسجّلة بهذا القسم لحد الحين.")
        return
    # most important (highest risk) test first
    units = sorted(build_units(filtered), key=lambda u: -unit_risk(u))
    render_units(units)
    pdf_button(filtered, CAT_EN.get(cat_key, page_name), file_slug(cat_key),
               "⬇️ نزّل تقرير هذا القسم للطبيب (PDF — للطباعة)")


def render_personal_reco(tests):
    """One consolidated, conflict-resolved set of recommendations from ALL current results."""
    highs = [t for t in tests if t["status"] == "high"]
    lows  = [t for t in tests if t["status"] == "low"]

    st.subheader("🧭 توصيات مجمّعة حسب تحاليله الحالية")
    st.caption(
        "هاي التوصيات مبنية على آخر نتائج كل تحاليله سوا، وحليّنا التعارضات: "
        "أي شي مفيد لتحليل بس يضرّ تحليل ثاني ما حطّيناه. راجعوها وية الطبيب لمن تتغيّر النتائج."
    )
    if highs:
        st.markdown("**عالية حالياً:** " + "، ".join(t["full_name"] for t in highs))
    if lows:
        st.markdown("**قليلة حالياً:** " + "، ".join(t["full_name"] for t in lows))

    st.markdown("#### ✅ أكل مسموح ومفيد إله")
    st.success(
        "• بروتين عالي الجودة وسهل الهضم بكميات معتدلة: بيض، دجاج بدون جلد، سمك — مفيد لرفع بروتين الدم (الألبومين) ولفقر الدم. "
        "**مهم:** اسألوا الطبيب أو أخصائي التغذية عن الكمية لأن كليته متعبة.\n\n"
        "• منتجات حليب باعتدال: لبن (روب) ناعم، حليب، جبن — مفيدة للكالسيوم والبروتين.\n\n"
        "• دهون صحية تعطي طاقة بدون سكّر: زيت الزيتون والزبدة — تساعد تمنع نقص الوزن بدون ما ترفع السكّر.\n\n"
        "• وجبات صغيرة ومتكررة (٥–٦ بال يوم) بدل ٣ وجبات كبيرة.\n\n"
        "• كل الأكل لازم يكون مطبوخ زين."
    )

    st.markdown("#### ⛔ أكل نتجنّبه (لأنه مفيد لتحليل بس يضرّ غيره)")
    st.warning(
        "• **حبوب الحديد من الصيدلية:** ممنوعة — ما تنمتصّ، تسبّب إمساك خطير وية ورم القولون، وتخفي النزيف الداخلي.\n\n"
        "• **الخضار الورقية الغامقة** (سبانغ، كرنب) بكميات كبيرة: مفيدة للحديد بس عالية بالبوتاسيوم (تضرّ الكلى) وفيتامين K (تتعارض وية مميّعات الدم) وألياف (خطر انسداد القولون).\n\n"
        "• **الأكلات والعصائر العالية بالبوتاسيوم:** موز، برتقال، عصير الفواكه، بطاطا — تضرّ الكلى، والعصير يرفع السكّر بعد.\n\n"
        "• **السكّريات والحلويات والمشروبات السكّرية:** سكّره التراكمي مرتفع.\n\n"
        "• **الملح الزائد و«بديل الملح»:** لا تضيفون ملح أو بديل ملح بدون الطبيب (بديل الملح بوتاسيوم خطير للكلى).\n\n"
        "• **المكسّرات والبذور والحبوب الكاملة والأكل عالي الألياف:** خطر انسداد القولون.\n\n"
        "• **الأكل الني أو سلطات برّه أو منتجات غير مبسترة:** مناعته ضعيفة.\n\n"
        "• **الكحول والأكل المقلي الدهني الثقيل.**"
    )

    st.markdown("#### 💧 السوائل (مهم جداً)")
    st.info(
        "عنده صوديوم قليل + كلى متعبة، فالماي الزايد يكدر يكون خطير. "
        "لا تنطونه ماي صافي بكثرة من راسكم — اتبعوا كمية السوائل اللي يحددها الطبيب بالضبط. "
        "للعطش وجفاف الفم: قطع ثلج صغيرة، حلوى حامضة بدون سكّر، وترطيب الشفايف."
    )

    st.markdown("#### 💊 الأدوية والمكمّلات")
    st.warning(
        "• ماكو أي مكمّل أو فيتامين أو عشبة بدون موافقة الطبيب (لا حديد، لا كالسيوم، لا أعشاب «تقوّي المناعة»).\n\n"
        "• ممنوع مسكّنات بروفين/أسبرين/نابروكسين — تضرّ الكلى وتزيد النزيف. للوجع بس اللي يسمحه الطبيب (عادةً باراسيتامول بجرعة محددة).\n\n"
        "• لا تنطونه دواء حرارة قبل ما تخبرون الممرضة (يكدر يخفي العدوى)."
    )

    st.markdown("#### 🛡️ الوقاية اليومية")
    st.info(
        "• نظافة صارمة: غسل الإيدين قبل وبعد أي تماس، وماكو زوّار مرضى (مناعته ضعيفة والالتهاب عالي).\n\n"
        "• قلّبوا وضعيته كل ساعة–ساعتين لحماية الجلد من القُرَح (أهم لأن بروتين دمه قليل).\n\n"
        "• لا تدلّكون ساقيه (خطر جلطة لأن الدي-دايمر عالي)؛ سوّوله تمارين كاحل خفيفة بالفراش وارفعوا ساقيه على مخدّة.\n\n"
        "• استعملوا فرشاة أسنان ناعمة وراقبوا أي نزيف (لثة، خشم، بول، أو براز)."
    )

    st.caption(
        "⚠️ هذي توصيات عامة للمساعدة فقط — الكميات (خاصة البروتين والسوائل والكالسيوم) "
        "لازم تتأكّدونها وية الطبيب أو أخصائي التغذية."
    )
    st.divider()


def render_general(tests, user=None):
    st.title("📘 إرشادات عامة للعائلة")
    st.caption("هذي الإرشادات تنطبق على كل التحاليل — مكتوبة مرة وحدة هنا حتى ما تتكرر بكل تحليل.")

    st.error(
        "🚨 **بأي حالة طارئة:** نادوا الممرضة أو الطبيب بالجناح فوراً — لا تنتظرون. "
        "علامات الطوارئ: ضيق نفس شديد، نزيف، تشويش مفاجئ، تشنّج، أو فقدان وعي."
    )

    # The consolidated recommendations are written specifically for the grandfather.
    # Other users see only the generic per-test guidance until their own is written.
    if user is None or user.get("primary"):
        render_personal_reco(tests)

    st.subheader("📋 إرشادات عامة تنطبق على كل التحاليل")
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


def render_add(tests, user):
    st.title("➕ إضافة نتيجة جديدة")
    st.caption(f"المستخدم الحالي: {user.get('label','')} — النتيجة تنحفظ مباشرة على GitHub ويتحدث الموقع خلال دقيقة.")

    # ── passcode gate (trust boundary: the live site is public) ──
    need = github_store.get_secret("add_passcode")
    if not need:
        st.error("ما تم ضبط **add_passcode** بإعدادات الموقع (Secrets). راجع `docs/DEPLOY.md`.")
        return
    pw = st.text_input("🔒 كلمة السر للإضافة", type="password")
    if pw != need:
        st.info("اكتب كلمة السر حتى تكدر تضيف نتيجة.") if not pw else st.error("كلمة السر غلط.")
        return

    if not github_store.configured():
        st.error("ما تم ضبط **github_token** بإعدادات الموقع، فما نكدر نحفظ على GitHub. راجع `docs/DEPLOY.md`.")
        return

    catalog = load_catalog()
    if not catalog:
        st.error("ماكو كتالوج فحوصات (info.json).")
        return

    tab_form, tab_json = st.tabs(["➕ نتيجة وحدة (نموذج)", "📋 لصق JSON (دفعة وحدة)"])
    with tab_form:
        _add_form(tests, user, catalog)
    with tab_json:
        _add_json(user)


def _reflect_local(results_file, body):
    """Write the merged file locally + clear cache so this session shows it now.
    (On the Cloud the file is ephemeral, but the commit drives the redeploy.)"""
    try:
        with open(results_file, "w", encoding="utf-8") as f:
            f.write(body)
    except OSError:
        pass
    load_data.clear()


def _add_form(tests, user, catalog):
    def disp(c):
        return f"{c.get('full_name') or c.get('short_name','')} ({c.get('short_name','')})"
    options = sorted(catalog, key=lambda c: c.get("short_name", ""))
    by_label = {disp(c): c for c in options}
    # load_data's processed tests key on short_name (not id) — use it for prefill
    prev_by_name = {t["short_name"]: t for t in tests}

    with st.form("add_reading"):
        choice = st.selectbox("الفحص", list(by_label.keys()))
        meta = by_label[choice]
        prev = prev_by_name.get(meta.get("short_name", ""))
        default_unit  = (prev["unit"] if prev else meta.get("unit", "")) or ""
        default_range = prev["latest"].get("normal_range", "") if prev else ""
        default_lab   = prev["latest"].get("lab_name", "") if prev else ""

        c1, c2 = st.columns(2)
        d  = c1.date_input("تاريخ الفحص", value=datetime.now().date())
        tm = c2.time_input("الوقت", value=datetime.now().time())
        result = st.text_input("النتيجة", placeholder="مثال: 11.4 أو Positive")
        unit   = st.text_input("الوحدة", value=default_unit)
        rng    = st.text_input("المعدّل الطبيعي", value=default_range, placeholder="مثال: 13.0 - 17.0")
        lab    = st.text_input("اسم المختبر", value=default_lab)
        submitted = st.form_submit_button("✅ احفظ وارفع لـ GitHub", type="primary")

    if not submitted:
        return
    if not result.strip():
        st.error("لازم تكتب النتيجة.")
        return

    date_str = datetime.combine(d, tm).strftime("%d-%m-%Y %H:%M:%S")
    rv = parse_result(result)        # numeric if possible, otherwise keep the text
    record = {"date": date_str, "result": rv if rv is not None else result.strip(),
              "lab_name": lab.strip(), "normal_range": rng.strip()}
    meta_use = {**meta, "unit": unit.strip() or meta.get("unit", "")}
    try:
        commit_url, body = github_store.add_reading(
            user["results_file"], meta["id"], record, meta_use, label=user.get("label", ""))
    except ValueError as e:        # duplicate (same-date reading already there)
        st.warning(str(e))
        return
    except Exception as e:
        st.error(f"تعذّر الحفظ على GitHub: {e}")
        return

    _reflect_local(user["results_file"], body)
    st.success("✅ انحفظت وارتفعت لـ GitHub. الموقع راح يتحدث خلال دقيقة تقريباً.")
    st.markdown(f"[شوف التغيير على GitHub]({commit_url})")


def _add_json(user):
    st.caption(
        "الصق نص JSON بنفس صيغة `results.json`: قائمة فحوصات، كل فحص بداخله `id` و`records`. "
        "نقدر نلصق عدة فحوصات سوا — راح ندمجها كلها بضغطة وحدة (النتائج المكررة بنفس التاريخ تنتجاهل)."
    )
    st.code(
        '[\n'
        '  { "id": 1, "test": "Hb", "unit": "g/dl", "records": [\n'
        '      { "date": "20-06-2026 10:00:00", "result": 11.4,\n'
        '        "lab_name": "...", "normal_range": "13.0 - 17.0" }\n'
        '  ] }\n'
        ']', language="json")
    raw = st.text_area("JSON", height=260, key="merge_json_text",
                       placeholder='[ { "id": 1, "test": "Hb", "records": [ ... ] } ]')
    if not st.button("📥 ادمج وارفع لـ GitHub", type="primary", key="merge_json_btn"):
        return

    if not raw.strip():
        st.error("الصق JSON أول.")
        return
    try:
        data = json.loads(raw)
    except Exception as e:
        st.error(f"JSON غلط (غالباً فاصلة أو قوس): {e}")
        return
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list) or not data or any(
            not isinstance(e, dict) or "id" not in e or "records" not in e for e in data):
        st.error("لازم يكون قائمة فحوصات، وكل فحص بيه `id` و`records`.")
        return

    try:
        url, body, added, new_tests = github_store.merge_json(
            user["results_file"], data, label=user.get("label", ""))
    except ValueError as e:
        st.warning(str(e))
        return
    except Exception as e:
        st.error(f"تعذّر الحفظ على GitHub: {e}")
        return

    _reflect_local(user["results_file"], body)
    st.success(f"✅ ادمجنا {added} نتيجة من {len(data)} فحص وارتفعت لـ GitHub.")
    if new_tests:
        st.warning("🆕 فحوصات جديدة انضافت (تحتاج معلومات لاحقاً): " + "، ".join(new_tests))
    st.markdown(f"[شوف التغيير على GitHub]({url})")


def render_nav(active, tests):
    u = st.query_params.get("user", "")
    user_q = f"&user={quote(u)}" if u else ""

    def chip(label, key):
        style = ("background:#1565c0;color:#fff;" if key == active
                 else "background:#e7eefc;color:#1565c0;")
        return (f'<a class="navchip" style="{style}" href="?page={quote(key)}{user_q}" '
                f'target="_self">{label}</a>')

    # special pages first (fixed order)
    chips = [chip(label, key) for label, key in SPECIAL_PAGES.items()]

    # category pages ordered by current importance (highest test risk first)
    def cat_importance(key):
        risks = [risk_score(t) for t in tests if t["sub_sub_category"] == key]
        return max(risks) if risks else 0
    cats = sorted(CATEGORY_PAGES.items(), key=lambda kv: -cat_importance(kv[1]))
    chips += [chip(label, key) for label, key in cats]

    # add-data page always last
    chips += [chip(label, key) for label, key in ADD_PAGES.items()]

    st.markdown('<div style="margin-bottom:10px">' + "".join(chips) + "</div>",
                unsafe_allow_html=True)


def render_user_picker(users, active_key):
    """User chips (own ?user= links so the phone back-button works), under the header."""
    def chip(u):
        on = u["key"] == active_key
        style = ("background:#2e7d32;color:#fff;" if on
                 else "background:#e8f5e9;color:#2e7d32;")
        href = f"?user={quote(u['key'])}"
        return (f'<a class="navchip" style="{style}" href="{href}" '
                f'target="_self">{u.get("label", u["key"])}</a>')
    st.markdown('<div style="margin-bottom:8px">' + "".join(chip(u) for u in users) + "</div>",
                unsafe_allow_html=True)


def main():
    global _PATIENT
    st.markdown('<div class="app-header">🏥 متابعة الصحّة اليومية</div>',
                unsafe_allow_html=True)
    qp = st.query_params

    # ── pick the active user (each has their own results file; info is shared) ──
    users = load_users()
    by_key = {u["key"]: u for u in users}
    user = by_key.get(qp.get("user", ""), users[0] if users else None)
    if user is None:
        st.error("ماكو مستخدمين بـ users.json.")
        return
    _PATIENT = user                                 # used by pdf_button for the PDF header
    if len(users) > 1:                              # only show the picker once there's a choice
        render_user_picker(users, user["key"])
    tests = load_data(user["results_file"])

    # ── A test is open: show its detail page (real URL = phone back works) ──
    test = qp.get("test")
    if test:
        render_detail(tests, test, back_page=qp.get("page", "__overview__"))
        return

    # ── List views: navigation is real URL links (chips) ──
    page = qp.get("page", "__overview__")
    if page not in PAGES.values():
        page = "__overview__"
    render_nav(page, tests)
    if page == "__overview__":
        render_overview(tests)
    elif page == "__today__":
        render_today(tests)
    elif page == "__redo__":
        render_redo(tests)
    elif page == "__general__":
        render_general(tests, user)
    elif page == "__add__":
        render_add(tests, user)
    else:
        render_category_page(tests, page)
