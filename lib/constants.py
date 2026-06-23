# -*- coding: utf-8 -*-
"""Static constants: status colors/labels, nav pages, clinical weights, field groups."""

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
    "low":     "⬇️ أقل من الطبيعي",
    "high":    "⬆️ أعلى من الطبيعي",
    "unknown": "❓ بدون معدّل",
}
TREND_LABEL = {
    "improving": "📈 يتحسّن",
    "worsening": "📉 يسوء",
    "stable":    "➡️ مستقر",
    "—":         "",
}

# Special pages (always first in the nav) + the 10 medical categories.
# For categories, the value == the Arabic `sub_sub_category` stored on each test.
SPECIAL_PAGES = {
    "📊 نظرة عامة":           "__overview__",
    "🆕 تحاليل اليوم":         "__today__",
    "⏰ شنو نعيد فحصه":        "__redo__",
    "📘 إرشادات عامة للعائلة": "__general__",
}
CATEGORY_PAGES = {
    "🦠 العدوى والالتهاب":          "العدوى والالتهاب",
    "🫘 وظائف الكلى":              "وظائف الكلى",
    "🩸 فقر الدم وكريات الدم الحمر": "فقر الدم وكريات الدم الحمر",
    "🛡️ خلايا الدم البيض والمناعة":  "خلايا الدم البيض والمناعة",
    "🩹 الصفيحات الدموية":          "الصفيحات الدموية",
    "❤️ التخثّر والقلب":            "التخثّر والقلب",
    "⚡ الأملاح والمعادن":          "الأملاح والمعادن",
    "🫁 وظائف الكبد":              "وظائف الكبد",
    "🥩 البروتين والتغذية":         "البروتين والتغذية",
    "🍬 السكّر":                   "السكّر",
}
# Shown as the LAST nav chip — entry page to add a new reading (writes to GitHub).
ADD_PAGES = {"➕ إضافة نتيجة": "__add__"}
PAGES = {**SPECIAL_PAGES, **CATEGORY_PAGES, **ADD_PAGES}

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

# Fields that are usually identical for every test → shown once on the general page,
# and only shown on a test if that test has its own different (specific) version.
GENERAL_FIELDS = [
    "refusal_handling", "bedridden_risks", "immune_and_hygiene",
    "communication_if_confused", "emotional_support",
]

# Relative %/Absolute sibling tests merged into one card.
PAIR_SUFFIXES = (" (Relative)", " (Absolute)")
