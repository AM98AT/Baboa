# Family Guidance Questions — Per Lab Test
## Context: 86-year-old male, bedridden in hospital, diagnosed with colon cancer

These questions are answered per test and stored in `data.json` under `family_guidance`.
Each answer is tailored to an elderly, immobile, hospitalized cancer patient.

---

## Questions Removed and Why

| Original | Reason Removed |
|----------|----------------|
| Q5 — "Is it safe to continue usual vitamins/supplements?" | Merged into Q12 (bedridden risks) — more relevant framing |
| Q11 — "Manage physical comfort *at home*" | He is not at home. Rewritten as Q11 (bedridden hospital risks) |
| Q16 — "When to call 911" | He is already in the hospital. Rewritten as Q6 (alert nurse/doctor threshold) |

---

## Final Question List (18 Questions)

### Group A — Understanding the Result

**Q1 — meaning_high_simple**
In simple terms, what does a HIGH result mean for an 86-year-old bedridden colon cancer patient?

**Q2 — meaning_low_simple**
In simple terms, what does a LOW result mean for an 86-year-old bedridden colon cancer patient?

**Q3 — affected_system**
Which organ or body system does this result most directly affect in his current condition, and why does it matter more because of his age and cancer?

---

### Group B — What to Watch For

**Q4 — symptoms_to_watch**
What visible changes in his behavior, energy, or appearance should the family watch for because of this result?
*(e.g., increased confusion, extreme fatigue, skin color changes, swelling)*

**Q5 — warning_signs_tonight**
What are the warning signs tonight or in the next few hours that show this result is getting worse and require immediately alerting the nurse or doctor?

**Q6 — critical_threshold**
At what specific number or combination of symptoms does this result become a critical emergency requiring the family to call the nurse station immediately?

---

### Group C — Diet, Food & Hydration

**Q7 — foods_to_give**
What specific foods, drinks, or snacks can the family safely bring him or ask the hospital kitchen to include that may help improve this result?
*(Consider he is bedridden, elderly, and may have poor appetite)*

**Q8 — foods_to_avoid**
What foods, drinks, spices, or snacks must the family strictly avoid giving him right now because of this result?

**Q9 — hydration_guidance**
How does this result affect his hydration needs? How can the family gently and safely encourage him to drink more if he refuses water?

**Q10 — refusal_handling**
If he refuses to eat, drink, or take his medications because of how this result makes him feel — what is the best way for the family to handle it without forcing him?

---

### Group D — Physical Safety (Bedridden)

**Q11 — bedridden_risks**
Since he is 86, bedridden, and not moving at all — does this result increase his risk of bedsores, blood clots in the legs (DVT), lung infections, or muscle weakness? What can the family do from his bedside to help prevent these?

**Q12 — supplements_safety**
Is it safe to give him any common vitamins, herbal teas, or over-the-counter supplements alongside this result? Which ones could be harmful or interact with his condition?

---

### Group E — Immune System & Hygiene

**Q13 — immune_and_hygiene**
Does this result indicate his immune system is dangerously weakened? If so, what strict hygiene rules, visitor limits, or precautions must the family follow when entering his hospital room?

---

### Group F — Emotional Support & Communication

**Q14 — communication_if_confused**
If this result causes confusion, delirium, memory lapses, or agitation — how should the family stay calm, communicate with him gently, and avoid making it worse?

**Q15 — emotional_support**
How can the family discuss his condition and these results with him honestly, without causing unnecessary fear, or making him feel like a burden to the family?

---

### Group G — Medical & Treatment Decisions

**Q16 — oncologist_questions**
What are the 2–3 most important questions the family should ask his oncologist specifically about this lab result at the next appointment?

**Q17 — treatment_impact**
How might this result affect his upcoming chemotherapy sessions, surgical procedures, or other active treatments? Could it cause delays or cancellations?

**Q18 — palliative_care**
Does this result — especially at his age and given his cancer — suggest that the family should begin discussing palliative care, comfort-focused care, or stronger pain management options with the medical team?

---

## JSON Field Names (for `family_guidance` object in each test)

```json
"family_guidance": {
    "meaning_high_simple":       "",
    "meaning_low_simple":        "",
    "affected_system":           "",
    "symptoms_to_watch":         "",
    "warning_signs_tonight":     "",
    "critical_threshold":        "",
    "foods_to_give":             "",
    "foods_to_avoid":            "",
    "hydration_guidance":        "",
    "refusal_handling":          "",
    "bedridden_risks":           "",
    "supplements_safety":        "",
    "immune_and_hygiene":        "",
    "communication_if_confused": "",
    "emotional_support":         "",
    "oncologist_questions":      "",
    "treatment_impact":          "",
    "palliative_care":           ""
}
```
