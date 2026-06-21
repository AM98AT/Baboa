# Deep-Research Prompt — Anemia Work-up Tests (Iron, Ferritin, Vitamin B12, Folate)

Copy everything inside the box below into your deep-research tool. Paste the result back to the assistant.

---

```
ROLE: You are a clinical educator writing for the FAMILY (non-medical, Arabic-speaking) of an
86-year-old man, bedridden in hospital, with colon cancer. Write clear, plain answers a worried
family member can act on. Do NOT use brand names — describe what things are in plain words.

STRICT SOURCING: Use ONLY these websites. If a fact is not found in them, leave that field empty —
do NOT invent or guess. Put the source domain at the end of every answer you DID find.
  1. cancer.net (ASCO)        2. cancer.gov (NCI)        3. cancer.org (American Cancer Society)
  4. mskcc.org (Memorial Sloan Kettering)   5. testing.com (Lab Tests Online)   6. healthinaging.org

PATIENT CONTEXT (use it to make every answer specific and to resolve conflicts):
- 86-year-old male, completely bedridden, colon cancer.
- Active infection / high inflammation: CRP very high, procalcitonin high.
- Kidneys impaired: high creatinine & urea (so high-potassium foods and NSAIDs are risky).
- Anemia: low hemoglobin. Low albumin (malnutrition). Low sodium. High D-dimer (clot risk).
- THESE FOUR RESULTS RIGHT NOW:
    * Serum Iron = 31.1 µg/dL   (normal 33–193)   → LOW
    * Ferritin   = 1125 ng/mL   (normal 15–150)   → VERY HIGH
    * Vitamin B12 = 291.3 pg/mL (normal 200–771)  → low-normal
    * Folate     = 4.78 ng/mL   (normal 2.5–20)   → normal
- IMPORTANT pattern to address explicitly: LOW serum iron + VERY HIGH ferritin + HIGH CRP is the
  classic picture of "anemia of inflammation" (iron is locked in storage by inflammation, not truly
  missing). Explain what this means for whether he needs iron, and why iron pills can be harmful
  with a colon tumor (constipation/obstruction risk, and they hide intestinal bleeding).

FOR EACH of the 4 tests (Iron, Ferritin, Vitamin B12, Folate), answer these 18 fields.
Keep each answer 1–4 short sentences, plain language, and end found answers with "Source: <domain>".
Write "(not found)" if the approved sources don't cover it.

meaning_high_simple:      what a HIGH result means for him
meaning_low_simple:       what a LOW result means for him
affected_system:          which organ/body system it affects and why it matters at his age + cancer
symptoms_to_watch:        visible signs the family should watch for
warning_signs_tonight:    signs in the next hours that mean call the nurse now
critical_threshold:       the number/symptom combo that is an emergency
foods_to_give:            helpful foods — BUT respect his limits (kidney = limit high-potassium like
                          banana/orange/potato; colon tumor = limit high-fiber, nuts, seeds, raw
                          produce, leafy greens; high blood sugar = limit sweets)
foods_to_avoid:           foods/drinks to avoid for this test (and why)
hydration_guidance:       fluids guidance (note: he has LOW sodium + tired kidneys, so plain water
                          is restricted — follow doctor's fluid limit)
refusal_handling:         what to do if he refuses food/drink/meds
bedridden_risks:          how being bedridden interacts with this test
supplements_safety:       is it safe to give a supplement for this (iron/B12/folate)? when is IV used
                          instead of pills? what's unsafe?
immune_and_hygiene:       any infection/hygiene relevance
communication_if_confused: how to talk to him if confused (relevant if B12 affects the brain/nerves)
emotional_support:        how to reassure the family/patient
oncologist_questions:     2–3 exact questions to ask the oncologist about THIS result
treatment_impact:         how this result affects treatment (e.g., IV iron, transfusion, delays)
palliative_care:          does this result suggest discussing comfort-focused care? (often "not found")

OUTPUT FORMAT (repeat this block for each of the 4 tests):

### TEST: <name>
meaning_high_simple: ...
meaning_low_simple: ...
affected_system: ...
symptoms_to_watch: ...
warning_signs_tonight: ...
critical_threshold: ...
foods_to_give: ...
foods_to_avoid: ...
hydration_guidance: ...
refusal_handling: ...
bedridden_risks: ...
supplements_safety: ...
immune_and_hygiene: ...
communication_if_confused: ...
emotional_support: ...
oncologist_questions: ...
treatment_impact: ...
palliative_care: ...
```

---

## Improved research plan (paste this if the tool asks "what changes to the plan?")

1. Per-test meaning & basics for Iron, Ferritin, Vitamin B12, Folate (what HIGH/LOW mean, what it
   measures, system affected) — framed for an 86-yo bedridden colon-cancer patient.
2. The inflammation pattern: low serum iron + very high ferritin + high CRP → ferritin as an
   acute-phase marker, iron "locked" by inflammation, true iron deficiency vs anemia of chronic
   disease (include soluble transferrin receptor if covered); state if he truly needs iron.
3. Supplement safety & route: oral iron risks with colon cancer (constipation/obstruction, masking
   GI bleeding, poor absorption in inflammation), when IV iron is used instead of pills, safety of
   B12/folate supplements (biotin/B-vitamins can distort lab tests); nothing without the doctor.
4. Diet — conflict-aware: helpful foods filtered against his limits (kidney→low potassium;
   colon→low fiber/no nuts-seeds-raw; high sugar→limit sweets); iron-absorption helpers/inhibitors;
   prefer animal sources for B12.
5. Hydration given low sodium + impaired kidneys (restrict free plain water; doctor's fluid limit).
6. Symptoms, tonight's warning signs, emergency thresholds per result (B12 nerve signs included).
7. Bedridden risks, infection/hygiene, and food/medication refusal handling.
8. Communication if confused (B12→brain/nerves), emotional support, palliative/comfort-care relevance.
9. Oncologist questions (2–3 per test) + treatment impact (IV iron, transfusion, treating inflammation,
   chemo timing).
10. OUTPUT as the 18 named fields per test, 1–4 plain sentences each, no brand names, each found fact
    ending with "Source: <domain>", "(not found)" where silent, and explicitly exclude any food/advice
    that conflicts with his kidney/colon/sugar limits.

---

## When you get the result
Paste the whole deep-research output back to the assistant and say:
> here is the deep research for the 4 anemia tests — update the data

The assistant will translate it to Iraqi Arabic, resolve any conflicts with his other results, and fill
the guidance fields for Iron, Ferritin, Vitamin B12, and Folate in `info_en.json` / `info.json`.
