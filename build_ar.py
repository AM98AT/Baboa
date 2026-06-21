# -*- coding: utf-8 -*-
"""
Re-runnable Arabic builder.
Source of truth = data_en.json (English, never edited by hand).
Output = data.json (what the website shows), regenerated every run.
As TR grows, more of the site becomes Arabic. Untranslated strings stay English.
"""
import json

# ── 16 shared paragraphs (cover 205 fields). Matched ONLY against confirmed
#    shared strings, so one-off fields can never be mis-matched. ────────────────
def shared_ar(v):
    if "soothing voice" in v:
        return ("احچي وياه بجُمَل قصيرة وبسيطة، موضوع واحد بالمرّة. استعمل صوت هادئ وليّن وحنون. "
                "انطيه وقت حتى يردّ. إذا صار مشوّش أو خايف، ذكّره بهدوء وين هو وإنّك موجود حتى تساعده. "
                "لا تتجادل وياه ولا تصحّح كلامه ولا ترفع صوتك. إذا تعلّق بشي يزعجه، حوّل الحچي لشي يريّحه. "
                "تقبّل مشاعره ولا تتجاهلها. خبّر الممرضة فوراً إذا التشويش صار فجأة أو قوي أو جديد. المصدر: mskcc.org")
    if "wash hands" in v:
        return ("كل أفراد العائلة لازم يغسلون إيديهم زين بالصابون والماي الدافي قبل ما يدخلون غرفته وبعد أي تماس وياه. "
                "أي شخص عنده زكام أو سعلة أو حرارة أو أي مرض، لا يزوره. لا تجيبون أكل ني أو مو مطبوخ زين من برّه. "
                "خلّوا الغرفة نظيفة. قلّلوا عدد الزوّار بنفس الوقت. لا تنطونه دواء ينزّل الحرارة (بنادول، بروفين) "
                "قبل ما تسألون الممرضة — لأنه يمكن يخفي علامات التهاب خطير. المصدر: cancer.gov")
    if "presence matters" in v:
        return ("اقعد ويّاه بهدوء وخلّيه يحسّ إنّك موجود — وجودك أهم من الكلام. لا تضغط عليه حتى ياكل أو يحچي أو يكون مبسوط. "
                "خلّيه هو يقرّر شيريد. احچوله أخبار بسيطة من العائلة حتى يبقى مرتبط بيكم. تجنّبوا تنقلون أخبار تزعجه أو "
                "تحچون عن كل أرقام تحاليله بالتفصيل. إذا سأل شلون حالته، كون صادق بس بهدوء وركّز على شيسوّون الأطباء حتى يساعدوه. المصدر: cancer.gov")
    if "spoonfuls" in v:
        return ("لا تجبره على الأكل أو الشرب أو الدواء. انطيه كميات صغيرة جداً — چم معلقة، چم شربة — بشكل متكرر بدل ثلاث وجبات كبيرة. "
                "إذا رفض الأكل الصلب، جرّب أشياء سائلة: حليب بالفواكه (ميلك شيك)، عصير مخفوق، مرق شوربة، أو مكمّلات غذائية مثل Ensure أو Boost. "
                "إذا رفض الدواء، خبّر الممرضة فوراً حتى الفريق الطبي يقرّر الخطوة الجاية. بالمراحل المتقدّمة، لا تجبره على الأكل أو الشرب لأنه يمكن يسبّبله انزعاج. المصدر: cancer.gov")
    if "three key risks" in v:
        return ("كونه طريح الفراش تماماً يزيد ثلاث مخاطر مهمة بغضّ النظر عن نتيجة هذا التحليل: "
                "(١) قُرَح الفراش — قلّب وضعيته كل ساعة لساعتين، احمي الكعبين ونهاية الظهر والوركين بالمخدّات، وراقب الجلد إذا صار أحمر أو بنفسجي فوق العظام وخبّر الممرضة فوراً. "
                "لا تدلّك المناطق الحمرا. خلّي الجلد نظيف وناشف. "
                "(٢) جلطات الساق — لا تدلّك ساقيه؛ اسأل الممرضة عن جوارب الضغط وتمارين خفيفة للقدم يقدر يسوّيها بالفراش. "
                "(٣) التهاب الصدر (ذات الرئة) — اسأل الممرضة عن رفع وضعيته للجلوس أحياناً حتى يساعد تنفّسه. المصدر: mskcc.org و healthinaging.org")
    if "ordered regularly" in v:
        return "هذا التحليل ممكن ينطلب بشكل منتظم لمن يكون الشخص يتعالج أو تتم متابعته بسبب حالة تخصّ خلايا الدم البيض. المصدر: testing.com"
    if "barely outside" in v:
        return ("ارتفاع أو انخفاض كبير بنوع أو أكثر من خلايا الدم البيض عادةً يستدعي إعادة التحليل؛ "
                "والنتيجة اللي بس شوية برّه المعدّل الطبيعي ممكن تكون مهمة أو لا. المصدر: testing.com")
    if "No supplements without doctor approval" in v:
        return "لا تنطيه أي مكمّلات بدون موافقة الطبيب. المصدر: cancer.gov"
    if "Red-cell results are often" in v:
        return "نتائج خلايا الدم الحمر عادةً تتم متابعتها خلال العلاج الكيمياوي، لأنه يمكن يأثّر على أعداد خلايا الدم. المصدر: testing.com"
    if "immature granulocytes" in v:
        return ('أسئلة تنطرح: شنو يعني مصطلحات بالتقرير مثل "الخلايا المحببة غير الناضجة" أو "التحوّل لليسار"، '
                "وشنو التحاليل الثانية اللي ممكن تنحتاج إذا النتائج غير طبيعية؟ المصدر: testing.com")
    if "8+ cups fluid daily" in v:
        return "٨ أكواب سوائل أو أكثر باليوم. المصدر: cancer.gov"
    if "body aches" in v:
        return "هذا التحليل عادةً ينعمل لمن تكون أكو علامات التهاب أو عدوى مثل الحرارة، القشعريرة، آلام الجسم، الوجع، أو الصداع. المصدر: testing.com"
    if "what do these red-cell numbers" in v:
        return "أسئلة تنطرح: شنو تكَول هاي الأرقام عن صحته، هل هي غير طبيعية وشنو لازم نسوّي، وهل أكو حاجة لتحاليل متابعة؟ المصدر: testing.com"
    if "Normal hydration" in v:
        return "ترطيب طبيعي — اتبع تعليمات الطبيب. المصدر: cancer.gov"
    if "No aspirin or ibuprofen" in v:
        return "لا أسبرين ولا بروفين. المصدر: cancer.org"
    if "call nurse immediately" in v:
        return "الحرارة ٣٨ درجة أو أكثر = اتصل بالممرضة فوراً. المصدر: cancer.gov"
    return None

# ── Test names (full_name) ────────────────────────────────────────────────────
FULL = {
    "Hb": "الهيموغلوبين (خضاب الدم)",
    "PCV": "نسبة حجم خلايا الدم الحمر (الهيماتوكريت)",
    "RBC": "عدد خلايا الدم الحمر",
    "MCV": "متوسّط حجم الكرية الحمرا",
    "MCH": "متوسّط هيموغلوبين الكرية الحمرا",
    "MCHC": "متوسّط تركيز هيموغلوبين الكرية الحمرا",
    "RDW": "مدى توزّع حجم خلايا الدم الحمر",
    "Platelets": "عدد الصفيحات الدموية",
    "WBC": "عدد خلايا الدم البيض",
    "Neutrophils (Relative)": "العدلات (نسبة مئوية)",
    "Neutrophils (Absolute)": "العدلات (العدد المطلق)",
    "Lymphocytes (Relative)": "اللمفاويات (نسبة مئوية)",
    "Lymphocytes (Absolute)": "اللمفاويات (العدد المطلق)",
    "Monocytes (Relative)": "الوحيدات (نسبة مئوية)",
    "Monocytes (Absolute)": "الوحيدات (العدد المطلق)",
    "S. Urea": "يوريا الدم",
    "S. Creatinine": "الكرياتينين",
    "S. Calcium": "الكالسيوم",
    "CRP": "بروتين سي التفاعلي (CRP) — مؤشّر الالتهاب",
    "Na": "الصوديوم",
    "K": "البوتاسيوم",
    "AST (GOT)": "إنزيم الكبد AST",
    "ALT (GPT)": "إنزيم الكبد ALT",
    "ALP": "الفوسفاتيز القلوي (ALP)",
    "Troponin I": "التروبونين (Troponin I) — مؤشّر القلب",
    "MPV": "متوسّط حجم الصفيحة الدموية",
    "Uric Acid": "حمض اليوريك",
    "Albumin": "الألبومين (بروتين الدم)",
    "Cl": "الكلورايد",
    "Ionized Ca": "الكالسيوم المتأيّن",
    "PCT": "البروكالسيتونين (PCT) — مؤشّر العدوى",
    "D-dimer": "دي-دايمر (D-dimer) — مؤشّر الجلطات",
    "HbA1c": "السكّر التراكمي (HbA1c)",
    "Total Bilirubin": "البيليروبين الكلّي (الصُّفار)",
    "PDW": "مدى توزّع حجم الصفيحات",
    "PCT (Plateletcrit)": "نسبة حجم الصفيحات (Plateletcrit)",
    "MXD (Relative)": "الخلايا المختلطة MXD (نسبة مئوية)",
    "MXD (Absolute)": "الخلايا المختلطة MXD (العدد المطلق)",
    "LDH": "نازعة هيدروجين اللاكتات (LDH)",
}

# ── Per-test one-off field translations (filled in batches). ───────────────────
# TR[short_name][field] = arabic
TR = {}

# ── Build ─────────────────────────────────────────────────────────────────────
def main():
    with open("data_en.json", encoding="utf-8") as f:
        data = json.load(f)

    # which strings are actually shared (appear >1)?
    counts = {}
    for t in data:
        for v in t.get("family_guidance", {}).values():
            if v and v.strip():
                counts[v] = counts.get(v, 0) + 1
    shared_set = {v for v, c in counts.items() if c > 1}

    total = done = 0
    for t in data:
        sn = t["short_name"]
        if sn in FULL:
            t["full_name"] = FULL[sn]
        fg = t.get("family_guidance", {})
        for k, v in fg.items():
            if not v or not v.strip():
                continue
            total += 1
            ar = None
            if v in shared_set:
                ar = shared_ar(v)
            if ar is None:
                ar = TR.get(sn, {}).get(k)
            if ar:
                fg[k] = ar
                done += 1

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Translated {done}/{total} guidance fields  ({100*done//total}%).")
    print(f"Remaining English fields: {total - done}")

if __name__ == "__main__":
    main()
