# Webpage Q&A — Anemia Work-up Tests (Iron, Ferritin, Vitamin B12, Folate)

These pages are **blocked** for the assistant, so please open each one, run the MASTER PROMPT on it,
and paste the answer between the `<<<ANSWER … ANSWER>>>` markers. Send the file back when done.

| Domain | Why blocked |
|--------|-------------|
| testing.com | HTTP 403 |
| cancer.org | HTTP 406 |
| cancer.net | redirects to cancer.org (blocked) |

(The assistant CAN already read cancer.gov and mskcc.org, so those aren't listed here.)

---

## MASTER PROMPT (copy this; replace `[TEST]` and `[URL]`)

```
You are helping the family (non-medical, Arabic-speaking) of an 86-year-old man, bedridden in
hospital with colon cancer. He also has: active infection (high CRP), impaired kidneys (high
creatinine), anemia, low albumin, low sodium, high clot risk.
His relevant results now: Iron 31.1 µg/dL (low), Ferritin 1125 ng/mL (very high),
Vitamin B12 291.3 pg/mL (low-normal), Folate 4.78 ng/mL (normal).

Read ONLY this page: [URL]
For the test/topic "[TEST]", give short, plain-language answers to the fields below, based ONLY on
what THIS page says. If the page doesn't cover a field, write exactly: (not found). No brand names.
End each found answer with: Source: <domain>

meaning_high_simple:
meaning_low_simple:
affected_system:
symptoms_to_watch:
warning_signs_tonight:
critical_threshold:
foods_to_give:
foods_to_avoid:
hydration_guidance:
refusal_handling:
bedridden_risks:
supplements_safety:
immune_and_hygiene:
communication_if_confused:
emotional_support:
oncologist_questions:
treatment_impact:
palliative_care:
```

---

# PAGES TO RESEARCH

### 1. TEST: Iron  — testing.com (Iron tests)
**URL:** https://www.testing.com/tests/iron-tests/
<<<ANSWER

ANSWER>>>

---

### 2. TEST: Ferritin  — testing.com (Ferritin)
**URL:** https://www.testing.com/tests/ferritin/
<<<ANSWER

ANSWER>>>

---

### 3. TEST: Folate  — testing.com (Folate test)
**URL:** https://www.testing.com/tests/folate-test/
<<<ANSWER

ANSWER>>>

---

### 4. TEST: Vitamin B12  — testing.com (Vitamin B12 & Folate)
**URL:** https://www.testing.com/tests/vitamin-b12-and-folate/
<<<ANSWER

ANSWER>>>

---

### 5. TOPIC: Anemia / iron in cancer  — cancer.org (Managing Anemia)
**URL:** https://www.cancer.org/cancer/managing-cancer/side-effects/low-blood-counts/anemia.html
*(Covers Iron, Ferritin, B12, Folate as causes of anemia — answer generally for "anemia work-up".)*
<<<ANSWER

ANSWER>>>

---

### 6. TOPIC: Blood transfusion / IV iron  — cancer.org (Blood Transfusions)
**URL:** https://www.cancer.org/cancer/supportive-care/blood-transfusions.html
<<<ANSWER

ANSWER>>>

---

### 7. TOPIC: Anemia  — cancer.net (ASCO)
**URL:** https://www.cancer.net/coping-with-cancer/physical-emotional-and-social-effects-cancer/managing-physical-side-effects/anemia
<<<ANSWER

ANSWER>>>

---

## When you're done
Save this file and tell the assistant:
> here are the webpage answers for the 4 anemia tests — update the data

The assistant will merge every real answer (skipping "(not found)") into the Arabic guidance for
Iron, Ferritin, Vitamin B12, and Folate.
