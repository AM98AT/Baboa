# Research Requests — Pages I Could NOT Reach

These webpages were **blocked** when I tried to fetch them automatically:

| Domain                               | Why it failed                         |
| ------------------------------------ | ------------------------------------- |
| testing.com (Lab Tests Online)       | HTTP 403 Forbidden                    |
| cancer.org (American Cancer Society) | HTTP 406 Not Acceptable               |
| cancer.net (ASCO)                    | Redirects to cancer.org, also blocked |

The 3 reachable sources (cancer.gov, mskcc.org, healthinaging.org) are already used in `data.json`.

---

## HOW TO USE THIS FILE

1. Go to an entry below. Each entry has a **TEST**, one or more **URL(s)**, and an empty **ANSWER** block.
2. Copy the **MASTER PROMPT** (just below). Replace `[TEST]` and `[URL]` with the values from that entry.
3. Paste it into the website / AI tool that can open that page.
4. Copy the reply and paste it **between the `<<<ANSWER` and `ANSWER>>>` markers** of that entry.
5. Send the file back to me. I will read every ANSWER block and update `data.json` automatically.

**Rules to keep the data trustworthy:**

- Only accept answers taken from the URL given (or that exact domain). If the tool can't find it there, leave the field blank.
- Do NOT invent / guess. A blank field is fine and expected.
- Keep each answer in plain language a non-medical family member can understand.

---

## MASTER PROMPT (copy this, fill the two placeholders)

```
You are helping the family of an 86-year-old man who is bedridden in hospital with colon cancer.

They do not have medical training.

For this Test, write short, plain-language answers to the fields below.
- Base every answer ONLY on what that page says. If the page does not cover a field, write exactly: (not found)
- No medical jargon. 1-3 sentences per field.
- At the end of each answer you DID find, write the source like: Source: <domain>

Return your answer in EXACTLY this format (keep the field keys unchanged):

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

> Field meanings (for your reference, not part of the prompt): high/low = what an abnormal result means · affected_system = which organ it affects · symptoms_to_watch = visible changes · warning_signs_tonight = signs it's worsening fast · critical_threshold = when to call the nurse now · foods_to_give / foods_to_avoid / hydration_guidance / refusal_handling = diet · bedridden_risks = bedsores/clots/lung · supplements_safety = vitamins/herbs · immune_and_hygiene = infection precautions · communication_if_confused = how to talk to him · emotional_support = how to reassure · oncologist_questions = what to ask the doctor · treatment_impact = effect on chemo/surgery · palliative_care = comfort-care discussion.

---

# PART 1 — testing.com (Lab Tests Online) → explains what each test means

> If a URL 404s, search testing.com for the test name and use that page instead.

---

### 1. Hb — Hemoglobin

**URL:** https://www.testing.com/tests/hemoglobin/
<<<ANSWER
A note before the answers: this page is an article about the **hemoglobin blood test**. It is not about colon cancer, daily care, nutrition, or end-of-life support. Because the instructions say to base every answer only on this page and write "(not found)" for anything it doesn't cover, most fields below are "(not found)." That's expected given the page topic, not an oversight.

meaning_high_simple: High hemoglobin can be a sign of underlying problems with the lungs or heart, and can also come from dehydration, smoking, or living at a high altitude. Signs of high levels can include headache, dizziness, vision trouble, slurred speech, and a reddened face. Source: testing.com

meaning_low_simple: Low hemoglobin can be a sign of "anemia," which means too few red blood cells. It can be caused by blood loss, poor nutrition, or many other conditions. Source: testing.com

affected_system: Hemoglobin sits in the red blood cells and mainly carries oxygen to the body, so low or high levels affect how much oxygen the body is getting. Abnormal levels can also relate to the lungs, heart, liver, or kidneys. Source: testing.com

symptoms_to_watch: Signs linked to low hemoglobin include tiredness, shortness of breath with activity, dizziness, paler or more yellow skin, headaches, and an irregular heartbeat. Source: testing.com

warning_signs_tonight: (not found)

critical_threshold: (not found)

foods_to_give: (not found)

foods_to_avoid: (not found)

hydration_guidance: (not found)

refusal_handling: (not found)

bedridden_risks: (not found)

supplements_safety: (not found)

immune_and_hygiene: (not found)

communication_if_confused: (not found)

emotional_support: (not found)

oncologist_questions: Helpful questions to ask the doctor about results include whether the level was abnormal, whether that level is concerning in his case, whether it can be changed, whether it needs monitoring at home, and whether any other testing is needed. Source: testing.com

treatment_impact: A hemoglobin test may be ordered to check how someone is responding to treatment and to monitor their overall health over time. Source: testing.com

palliative_care: (not found)

One important caution: this page is general information about a blood test and is not a guide for caring for someone with advanced colon cancer. For the bedside questions you really need answered tonight (warning signs, what to feed him, hydration, comfort, and palliative care), please ask the hospital's nurses or care team directly — they know his specific situation and can give safe, personalized guidance. If you'd like, I can find a page that actually covers those caregiving and palliative-care topics so I can fill in more of these fields.
ANSWER>>>

---

### 2. PCV — Hematocrit

**URL:** https://www.testing.com/tests/hematocrit/
<<<ANSWER
A quick note before the answers: the page you have open is only about the **hematocrit (HCT) blood test** — what it measures and what high or low results can mean. It does not cover most of the caregiving topics in your list (food, hydration, bedridden risks, emotional support, palliative care, and so on), so I've honestly marked those as **(not found)** rather than guessing. For those, you'd need a different, more caregiving-focused source.

Here are the answers based only on this page:

meaning_high_simple: A high result means the blood has too many red blood cells or is too concentrated. On this page, common causes include dehydration, lung disease, heart problems, certain kidney tumors, smoking, or rare blood disorders. Source: testing.com

meaning_low_simple: A low result (called anemia) means the cells may not be getting enough oxygen. Causes listed include blood loss, poor nutrition (low iron or certain vitamins), bone marrow problems or cancers like leukemia, and too much water in the body. Source: testing.com

affected_system: This test is about the blood, specifically the red blood cells that carry oxygen to the body and bring back waste (carbon dioxide) to the lungs. Source: testing.com

symptoms_to_watch: The page lists signs that may prompt this test, including tiredness, mood changes, headaches, trouble concentrating ("brain fog"), and blood in the stool or vomit. Source: testing.com

warning_signs_tonight: (not found)

critical_threshold: (not found)

foods_to_give: (not found)

foods_to_avoid: (not found)

hydration_guidance: (not found)

refusal_handling: (not found)

bedridden_risks: (not found)

supplements_safety: (not found)

immune_and_hygiene: (not found)

communication_if_confused: (not found)

emotional_support: (not found)

oncologist_questions: The page suggests questions to ask the doctor: what the result means for his health, whether anything can be done to change the levels, and whether further testing is needed. Source: testing.com

treatment_impact: (not found)

palliative_care: (not found)

If it would help, I can search for a trustworthy caregiving or cancer-support source to fill in the many fields this page doesn't address. Just let me know and I'll find one.
ANSWER>>>

---

### 3. RBC — Red Blood Cell Count

**URL:** https://www.testing.com/tests/red-blood-cell-count-rbc/
<<<ANSWER
Here are the answers based **only** on what the testing.com RBC Count page says:

---

**meaning_high_simple:** A high RBC count means there are more red blood cells than normal in the blood. This can be caused by things like dehydration, smoking, low oxygen levels, certain cancers, or some medications. Source: testing.com

**meaning_low_simple:** A low RBC count means there are fewer red blood cells than normal, which is the main sign of anemia. It can be caused by poor nutrition, bleeding, bone marrow problems, kidney failure, or cancer-related conditions. Source: testing.com

**affected_system:** Red blood cells are made in the bone marrow and travel through the bloodstream. They carry oxygen to the body's tissues and bring carbon dioxide back to the lungs. The kidneys also play a role by producing a hormone that tells the bone marrow to make more red blood cells. Source: testing.com

**symptoms_to_watch:** The page mentions that a doctor may order this test if someone has fatigue, headache, loss of appetite, problems concentrating, fever, infection, or general weakness — these are signs that blood cell counts may be off. Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** (not found)

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** The page notes that dehydration can cause a falsely high RBC count, and overhydration can cause a falsely low one — but it gives no specific guidance on how much fluid to give. (not found)

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** The page mentions that vitamin B12 and folate deficiencies can cause a low RBC count, but does not give any advice about taking supplements. (not found)

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: What does my red blood count say about my health? Are the results abnormal, and how should we address that? Will any follow-up tests be needed? Is there anything I should do to improve my health based on these results? Source: testing.com

**treatment_impact:** The page states that RBC count is often monitored when a patient is receiving treatment that can affect blood cell counts, such as chemotherapy — meaning chemo can change these numbers. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 4. MCV / MCH / MCHC / RDW — Red Blood Cell Indices

**URL:** https://www.testing.com/tests/red-blood-cell-indices/
_(Answer applies to all four; I will split it.)_
<<<ANSWER
Here are the plain-language answers based **only** on what the testing.com RBC Count page says:

---

**meaning_high_simple:** A high RBC count means there are more red blood cells than normal in the blood. This can be caused by things like dehydration, smoking, low oxygen levels, or certain cancers and drugs. Source: testing.com

**meaning_low_simple:** A low RBC count means the blood doesn't have enough red blood cells, which is often a sign of anemia. It can be caused by things like poor nutrition, bleeding, cancer affecting the bone marrow, kidney failure, or certain medications. Source: testing.com

**affected_system:** Red blood cells are made in the bone marrow and travel through the bloodstream. They carry oxygen to the body's tissues and carry carbon dioxide back to the lungs. A problem with RBC count can affect the whole body because every organ needs oxygen. Source: testing.com

**symptoms_to_watch:** The page mentions that a doctor may order this test if a patient has fatigue, headache, loss of appetite, trouble concentrating, fever, infection, or weakness — these can all be signs that red blood cell counts are off. Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** The page states that normal RBC levels for adults generally fall between 4 and 6 million cells per microliter of blood, and that males typically have higher counts than females. It does not specify a number that would be considered a critical emergency. Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** The page notes that dehydration can cause a high RBC count, and overhydration can cause a low one, but it gives no specific advice about how much to drink. Source: testing.com

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** The page mentions that vitamin B12 and folate deficiencies can cause a low RBC count, but it does not give any advice about whether or how to take supplements safely. Source: testing.com

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: What does my red blood count say about my health? Are the results abnormal, and if so, what should be done? Will any follow-up tests be needed? Is there anything I should do to improve my health based on these results? Source: testing.com

**treatment_impact:** The page says that RBC counts are often monitored when a patient is receiving chemotherapy, because that treatment can affect blood cell counts. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 5. Platelets — Platelet Count

**URL:** https://www.testing.com/tests/platelet-count/
<<<ANSWER
Here are the answers based **only** on what the testing.com platelet count page says. Fields that the page does not cover are marked **(not found)**.

---

**meaning_high_simple:** A high platelet count means there are too many platelets in the blood, which can raise the risk of dangerous blood clots or, in extreme cases, unexpected bleeding. Source: testing.com

**meaning_low_simple:** A low platelet count means the blood cannot clot properly, making the person bleed more easily and for longer than normal — even from minor cuts or bumps. Source: testing.com

**affected_system:** Platelets are part of the blood and the body's clotting system, so a platelet problem affects the blood and the ability to stop bleeding or, if too high, to avoid harmful clots. Source: testing.com

**symptoms_to_watch:** With low platelets, watch for easy or frequent bruising (purple, red, or brown marks), tiny red or purple dots on the skin, nosebleeds, bleeding from the mouth, blood in urine or stool, and wounds that bleed longer than expected. With high platelets, watch for headache, dizziness, weakness, chest pain, and tingling in the hands or feet. Source: testing.com

**warning_signs_tonight:** If platelets are very high, watch for confusion, sudden changes in memory or behavior, shortness of breath, fever, or bleeding from many parts of the body at once — these can be serious. Source: testing.com

**critical_threshold:** The normal range is 150,000 to 450,000 platelets per microliter of blood, according to the American Board of Internal Medicine. Results outside this range — especially large drops or rises from one test to the next — may indicate a problem even if they are still technically "in range." Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** (not found)

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** (not found)

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: Was the result abnormal (too high or too low)? What does it mean for his health? Does it point to a diagnosis? Will more tests be needed? Will any medication be prescribed? Source: testing.com

**treatment_impact:** The platelet count test is used to monitor patients during treatments like chemotherapy, because these treatments can affect platelet levels and the blood's ability to clot. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 7. WBC — White Blood Cell Count

**URL:** https://www.testing.com/tests/white-blood-cell-count-wbc/
<<<ANSWER
Here are the answers based **only** on what the testing.com WBC page says:

---

**meaning_high_simple:** A high WBC count (called leukocytosis) means there are more white blood cells than normal in the blood. This can be caused by infection, inflammation, certain cancers, or some medications. Source: testing.com

**meaning_low_simple:** A low WBC count (called leukopenia) means the body has fewer white blood cells than normal, which can be caused by cancer, cancer treatment (like chemotherapy), bone marrow problems, or certain medications. Source: testing.com

**affected_system:** White blood cells are part of the immune system and are made in the bone marrow. They help the body fight infections and disease. Source: testing.com

**symptoms_to_watch:** The page mentions that a doctor may order this test if someone has excessive tiredness or weakness, weight loss, fever or signs of infection, unexpected bleeding or bruising, or signs of cancer. Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** (not found)

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** (not found)

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** (not found)

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: what is my WBC count, do other parts of the blood test explain the abnormal result, and do I need any follow-up tests? Source: testing.com

**treatment_impact:** Chemotherapy and medications that suppress the immune system can affect WBC counts, so the test is used to monitor how a patient responds to these treatments. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 8. Neutrophils / Lymphocytes / Monocytes / MXD — WBC Differential

**URL:** https://www.testing.com/tests/white-blood-cell-differential/
_(Answer applies to the differential cell types; I will split it.)_
<<<ANSWER
Based solely on the content of the page at testing.com, here are plain-language answers for each field:

---

**meaning_high_simple:** (not found)

**meaning_low_simple:** (not found)

**affected_system:** The WBC differential test measures the body's immune system — specifically the white blood cells (also called leukocytes) that travel through the blood and lymphatic system to fight infections and disease. It can also reflect the health of the bone marrow, where these cells are made. Source: testing.com

**symptoms_to_watch:** The page says the test is typically done when someone has signs of infection or inflammation, such as fever, chills, body aches, pain, or headache. Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** The page says a large rise or drop in one or more types of white blood cells "usually prompts more or repeat testing," and that a result barely outside the normal range "may or may not be significant." It does not give specific numbers to watch for. Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** (not found)

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** (not found)

**immune_and_hygiene:** The page explains that white blood cells help protect the body against infections and play a role in fighting inflammation, allergies, and cancer. It does not give hygiene advice for caregivers. Source: testing.com

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: what "immature granulocytes" in the report mean, what other tests might be needed if results are abnormal, and what a "left shift" on the report means. Source: testing.com

**treatment_impact:** The page notes the test may be ordered regularly if someone is being treated or monitored for a white blood cell–related disease, but does not discuss cancer treatment specifically. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 9. S. Urea — Blood Urea Nitrogen (BUN)

**URL:** https://www.testing.com/tests/blood-urea-nitrogen-bun/
<<<ANSWER
Here are the answers based **only** on what the testing.com BUN Blood Test page says:

---

**meaning_high_simple:** A high BUN level can mean the kidneys are not filtering waste out of the blood properly. It can also be caused by eating a lot of protein, being dehydrated, certain medications, or burns — not just kidney disease. BUN levels also tend to rise naturally with aging. Source: testing.com

**meaning_low_simple:** A low BUN level can be a sign of malnutrition, not getting enough protein in the diet, or liver disease. Source: testing.com

**affected_system:** The BUN test mainly looks at how well the kidneys are working. The kidneys are supposed to filter a waste product called urea out of the blood and remove it through urine. Source: testing.com

**symptoms_to_watch:** The page mentions that a BUN test may be ordered if someone has symptoms of kidney disease, such as changes in urination, swelling in the arms or legs, muscle cramps, or frequent tiredness. Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** The page states that a typical normal range for BUN is 8 to 20 mg/dL, but notes this can vary between labs depending on their methods and units. Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** The page only mentions that eating a lot of protein can raise BUN levels, but gives no specific dietary advice for patients. Source: testing.com

**hydration_guidance:** The page notes that dehydration can raise BUN levels, but does not give any specific guidance on how much fluid to give or avoid. Source: testing.com

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** The page says to tell the doctor about all prescription drugs, over-the-counter medications, and dietary supplements before the test, because some of them can affect BUN results. It does not name which supplements are safe or unsafe. Source: testing.com

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: whether the BUN level was normal or abnormal, what the result means for kidney function, what the most likely explanation is if it was abnormal, and whether any follow-up or repeat tests are needed. Source: testing.com

**treatment_impact:** The page notes that BUN testing can be used to monitor for kidney side effects when starting a new medication, and to track how a known kidney condition changes over time. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 10. S. Creatinine — Creatinine

**URL:** https://www.testing.com/tests/creatinine/
<<<ANSWER
Here are the answers based **only** on what the testing.com creatinine page says. Fields the page does not address are marked accordingly.

---

**meaning_high_simple:** A high creatinine level may mean the kidneys are not filtering waste out of the blood properly. It can also be caused by dehydration, muscle problems, or certain medications. Source: testing.com

**meaning_low_simple:** A lower-than-expected creatinine level may be a sign of malnutrition or loss of muscle mass. Source: testing.com

**affected_system:** This test is about the kidneys. The kidneys normally filter creatinine (a waste product from muscles) out of the blood and remove it through urine. Source: testing.com

**symptoms_to_watch:** The page lists symptoms that can point to a kidney problem, including swelling in the feet, changes in urination, loss of appetite, and tiredness. Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** The page gives normal blood creatinine ranges as 0.7–1.3 mg/dL for men and 0.5–1.1 mg/dL for women, but does not specify a critical or emergency level. Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** The page mentions avoiding eating meat for about 24 hours before a creatinine test, as it can affect results — but this is about test preparation, not general diet advice. Source: testing.com

**hydration_guidance:** The page notes that dehydration can raise creatinine levels, but gives no specific guidance on how much fluid to drink. Source: testing.com

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** The page says some medications and supplements can change creatinine levels, so the doctor may adjust them before testing. It advises reviewing all prescriptions, over-the-counter drugs, and supplements with the doctor beforehand. Source: testing.com

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: Was the result normal or abnormal? Are there individual factors (like age, diet, or muscle mass) that affect the result? Should another kidney test be done now or in the future? Are any follow-up tests recommended? Source: testing.com

**treatment_impact:** The page notes that creatinine testing may be used to watch for kidney side effects from medications. It also says a creatinine test should be done before a CT scan with contrast dye. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 11. S. Calcium / Ionized Ca — Calcium

**URL:** https://www.testing.com/tests/calcium/
<<<ANSWER
Here are plain-language answers based **only** on what the testing.com calcium blood test page states:

---

**meaning_high_simple:** A high calcium level (called hypercalcemia) means there is too much calcium circulating in the blood. For someone with cancer, this can happen when the cancer spreads to the bones and releases calcium into the blood, or when cancer produces a hormone that raises calcium levels. Source: testing.com

**meaning_low_simple:** A low calcium level (called hypocalcemia) means there is not enough calcium circulating in the blood. A very common reason in sick patients is low protein (albumin) levels in the blood, which is especially common when someone is acutely ill. Source: testing.com

**affected_system:** Calcium affects the bones, heart, nerves, kidneys, and teeth. Large swings in calcium levels can cause the heart to beat too slowly or too fast, muscles to go into painful spasm, and confusion or even coma. Source: testing.com

**symptoms_to_watch:** Signs of high calcium include tiredness, weakness, loss of appetite, nausea, vomiting, constipation, stomach pain, needing to urinate often, and being very thirsty. Signs of low calcium include stomach cramps, muscle cramps, and tingling in the fingers. Source: testing.com

**warning_signs_tonight:** If calcium levels are very far out of range, the heart can slow down or beat too fast, muscles can go into spasm, and the person can become confused or fall into a coma — these would require urgent medical attention. Source: testing.com

**critical_threshold:** The normal adult range is 8.6–10.2 mg/dL. The page notes that large fluctuations in ionized calcium (the active form) can cause serious complications including heart problems, muscle spasms, and confusion, but does not give a specific number for a "critical" threshold. Source: testing.com

**foods_to_give:** The page mentions that a doctor may advise changes to diet if calcium is abnormal, and that a low-calcium, neutral ash diet is used before certain urine tests. It does not list specific foods to give. (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** (not found)

**refusal_handling:** (not found)

**bedridden_risks:** The page lists "prolonged immobilization" as one of the causes of high blood calcium. This means that being bedridden for a long time can itself raise calcium levels, which is relevant for someone who cannot get out of bed. Source: testing.com

**supplements_safety:** Some medications and supplements can affect calcium levels and may need to be stopped before a calcium test — these include lithium, antacids, diuretics, and vitamin D supplements. A doctor should advise on any changes. Source: testing.com

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: Was the calcium level low, normal, or high? What is the most likely cause? Are follow-up tests needed? Should another calcium test be done? Should diet be changed? Source: testing.com

**treatment_impact:** When a patient is being treated for abnormal calcium, further calcium tests may be ordered to check whether the treatment (such as calcium or vitamin D supplements) is working. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 12. CRP — C-Reactive Protein

**URL:** https://www.testing.com/tests/c-reactive-protein-crp/
<<<ANSWER
Here are the plain-language answers based **only** on what the testing.com CRP page says:

---

**meaning_high_simple:** A CRP level higher than 1.0 mg/dL means there is likely inflammation happening somewhere in the body. Very high levels can be linked to infections, autoimmune diseases, some cancers, and conditions affecting the lungs or pancreas. Source: testing.com

**meaning_low_simple:** A CRP level of 0.8–1.0 mg/dL or lower is considered normal, and most healthy adults have levels below 0.3 mg/dL. A mildly elevated result (0.3–1.0 mg/dL) doesn't necessarily mean something serious is wrong. Source: testing.com

**affected_system:** CRP is a protein made by the liver and released into the bloodstream when the body detects bacteria or other threats. The test reflects inflammation anywhere in the body, but it does not tell you where or what is causing it. Source: testing.com

**symptoms_to_watch:** Signs that might prompt a CRP test include fever, chills, redness or flushing, nausea, vomiting, rapid breathing, and rapid heart rate. These can be signs of infection or serious inflammation. Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** The page does not give a single "danger number," but notes that a level above 1.0 mg/dL suggests inflammation, and very high levels are associated with serious conditions like sepsis (a life-threatening body-wide response to infection). Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** (not found)

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** The page mentions that magnesium supplements and some medications (like anti-inflammatory drugs and statins) can affect CRP levels, so doctors may review these before testing. Always tell the doctor about any supplements being taken. Source: testing.com

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: whether levels are within the normal range and how concerned to be, what might be causing any minor increase, whether anything can be done to bring the level down, and whether more tests are needed. Source: testing.com

**treatment_impact:** The page notes that CRP is used to assess whether treatment for a chronic inflammatory condition is working, and to guide treatment of sepsis. It does not specifically address cancer treatment. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 13. Na / K / Cl — Electrolytes (Sodium, Potassium, Chloride)

**URL:** https://www.testing.com/tests/electrolytes/
_(Please give a short note for sodium, potassium, and chloride each.)_
<<<ANSWER
Here are the answers based **only** on what the testing.com page says. Many fields are not covered by that page, so those are marked accordingly.

---

**meaning_high_simple:**
_(not found — the page does not explain what it means when specific electrolytes are too high)_

**meaning_low_simple:**
_(not found — the page does not explain what it means when specific electrolytes are too low)_

**affected_system:**
Electrolytes affect the kidneys, heart, lungs, muscles, and nerves. The test is used to check how well these systems are working and to spot fluid or acid imbalances in the body. Source: testing.com

**symptoms_to_watch:**
Watch for weakness or tiredness, fast or irregular heartbeat, muscle twitching or cramps, nausea, vomiting, diarrhea, headaches, and confusion or irritability. These are the symptoms the page lists as reasons a doctor might order this test. Source: testing.com

**warning_signs_tonight:**
_(not found — the page does not give specific urgent warning thresholds or overnight guidance)_

**critical_threshold:**
_(not found — the page does not list specific numbers that count as dangerous or critical)_

**foods_to_give:**
_(not found)_

**foods_to_avoid:**
_(not found)_

**hydration_guidance:**
The page notes that dehydration is one of the most common causes of electrolyte imbalances and can affect sodium, potassium, and other levels. If results are abnormal, a doctor may recommend adjusting fluid intake. Source: testing.com

**refusal_handling:**
_(not found)_

**bedridden_risks:**
_(not found — the page does not address risks specific to bedridden patients)_

**supplements_safety:**
_(not found)_

**immune_and_hygiene:**
_(not found)_

**communication_if_confused:**
_(not found)_

**emotional_support:**
_(not found)_

**oncologist_questions:**
_(not found — the page does not address cancer care specifically)_

**treatment_impact:**
The page notes that changes in electrolyte levels can show whether a treatment is working and can detect side effects of medications, so the test may be used to track how the body is responding to treatment. Source: testing.com

**palliative_care:**
_(not found)_

---

**Short notes for sodium, potassium, and chloride:**

- **Sodium:** Controls how much fluid the body holds and helps nerves and muscles work normally. Source: testing.com

- **Potassium:** Important for the healthy function of cells, muscles, and nerves throughout the body. Source: testing.com

- **Chloride:** Works together with other electrolytes to keep fluid levels balanced and to maintain the body's acid-base balance. Source: testing.com
  ANSWER>>>

---

### 14. AST (GOT) — Aspartate Aminotransferase

**URL:** https://www.testing.com/tests/aspartate-aminotransferase-ast/
<<<ANSWER
Here are the plain-language answers based **only** on what the testing.com AST page says:

---

**meaning_high_simple:** A high AST level means cells somewhere in the body have been damaged. Very high levels often point to sudden (short-term) liver damage, while smaller but ongoing high levels can point to a long-term condition. Source: testing.com

**meaning_low_simple:** (not found)

**affected_system:** AST is an enzyme found in the liver, heart, brain, pancreas, kidneys, and muscles. The test is most often used to check the liver, but a high result can also come from damage to other organs or tissues. Source: testing.com

**symptoms_to_watch:** Symptoms that might lead a doctor to order this test include jaundice (yellowing), fatigue, swelling, unexplained weight loss, itching, nausea, and vomiting. These are signs the liver may be struggling. Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** There is no single number that is dangerous for everyone — the healthy range depends on the lab used, and also on the person's age, sex, race, and weight. The page says there is no universal reference range. Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** The page only mentions that before the blood test, the patient should drink nothing except water (if fasting is required). No broader drinking guidance for patients is given. Source: testing.com

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** The page warns that prescription drugs, over-the-counter medicines, and dietary supplements can all affect AST levels, so the doctor should be told about everything being taken before the test. Source: testing.com

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking: What is the normal range for the lab that ran my test? Were my AST levels normal or abnormal? What is the most likely reason for my result? Should I repeat the test or have other follow-up tests done? Source: testing.com

**treatment_impact:** The page mentions that AST can be tested repeatedly to track how well treatment for liver problems is working, and to watch for liver damage if a new medication is started. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 15. ALT (GPT) — Alanine Aminotransferase

**URL:** https://www.testing.com/tests/alanine-aminotransferase-alt/
<<<ANSWER
Here are the answers based **only** on what the testing.com ALT page says:

---

**meaning_high_simple:** A high ALT level means that liver cells may be damaged or injured, causing the enzyme to leak into the blood. It can point to liver problems like inflammation or scarring, though it can also be elevated without any serious underlying disease. Source: testing.com

**meaning_low_simple:** The page notes that ALT levels tend to decrease with older age, though the exact reason is unknown. There is no specific explanation given for what a low result means in terms of health risk. Source: testing.com

**affected_system:** ALT is mainly found in the liver, so an abnormal result is generally linked to the liver. Small amounts can also be found in muscle and other parts of the body. Source: testing.com

**symptoms_to_watch:** Symptoms that can be connected to liver problems and may prompt ALT testing include nausea, vomiting, stomach pain, itching, yellowing of the skin (jaundice), tiredness, and loss of appetite. Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** The page does not give a specific number that counts as a dangerous or critical ALT level. It does say that very high levels may indicate an acute (sudden, serious) liver problem, while mild or moderate elevations over time may point to a chronic condition. Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** The only mention of hydration is that during the fasting period before the blood test, the patient may drink water. No broader hydration guidance is provided. Source: testing.com

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** The page warns that many medications and supplements can affect ALT levels, and the doctor should be told about all drugs and dietary supplements being taken before testing. In some cases, the doctor may ask the patient to stop certain medications before the test. Source: testing.com

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: What was the ALT level and is it in the normal range? Were other measurements taken and were they normal? What do the results mean for overall health? Are any follow-up tests recommended, and what are their benefits and risks? Source: testing.com

**treatment_impact:** The page notes that ALT testing can be used to watch for unwanted side effects when a doctor prescribes a medication that can affect the liver, and that ongoing testing can monitor how a liver condition progresses over time. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 16. ALP — Alkaline Phosphatase

**URL:** https://www.testing.com/tests/alkaline-phosphatase-alp/
<<<ANSWER
Here are the answers based **only** on what the testing.com ALP page contains:

---

**meaning_high_simple:** A high ALP level can be a sign of liver or bone problems, or blockages in the bile ducts. However, high levels are not always a sign of illness — older adults naturally tend to have higher ALP levels. Source: testing.com

**meaning_low_simple:** A low ALP level is less common and can be caused by poor nutrition, nutrient deficiencies, an underactive thyroid, or rare inherited disorders. Very persistently low levels may point to a rare genetic bone condition called hypophosphatasia. Source: testing.com

**affected_system:** ALP is an enzyme found in the liver, bones, kidneys, intestines, and other parts of the body. Abnormal levels in the blood can signal damage or disruption in any of these areas. Source: testing.com

**symptoms_to_watch:** Symptoms that might prompt an ALP test include nausea, vomiting, yellowing of the skin (jaundice), tiredness, belly pain, and unexplained weight loss — all possible signs of liver trouble. Bone pain, easy fractures, or abnormal bone shape may also lead to ALP testing. Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** The page notes that a common normal range is 44–147 IU/L, though some guidelines suggest 30–120 IU/L, and ranges can differ between labs. Very high levels are often seen with bile duct blockages, but no specific "danger number" is stated. Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** The page only mentions that fatty meals can temporarily raise ALP in people with certain blood types. No broader dietary advice for patients is given. Source: testing.com

**hydration_guidance:** (not found)

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** The page notes that before an ALP blood test, patients may be asked about any medications or supplements they take, and the doctor may advise adjusting timing or dosage. No specific supplement safety advice for patients is given beyond this. Source: testing.com

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: "What did the test show about my ALP levels?", "Were any other measurements taken, and what can you learn from them?", and "Do you recommend any follow-up tests, and what are the pros and cons?" Source: testing.com

**treatment_impact:** ALP testing can be used to monitor whether a liver disease or other condition is improving, getting worse, or staying the same in response to treatment. No specific cancer treatment information is provided. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 17. Total Bilirubin — Bilirubin

**URL:** https://www.testing.com/tests/bilirubin/
<<<ANSWER
Here are the answers based **solely** on what the testing.com bilirubin page says:

---

**meaning_high_simple:** A bilirubin result above the normal range may indicate the presence of a disease or the need for further testing. Conditions that can cause high bilirubin include jaundice (which turns the eyes and skin yellow), hepatitis, cirrhosis, gallbladder disease, or a problem with red blood cells. Source: testing.com

**meaning_low_simple:** (not found)

**affected_system:** Bilirubin problems mainly affect the liver, gallbladder, and red blood cells. The liver normally processes bilirubin so it can leave the body, and when something goes wrong with that process, bilirubin builds up in the blood. Source: testing.com

**symptoms_to_watch:** The main visible sign of high bilirubin is jaundice — yellowing of the skin and eyes. If bilirubin appears in the urine, the urine may turn a tea or cola color. Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** The page notes that very high bilirubin levels can lead to serious complications if left untreated, but it does not give a specific number to watch for in adults. Normal total bilirubin for adults is 0.3–1.0 mg/dL; anything above that upper level may signal a problem. Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** (not found)

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** The page mentions that many medications can interfere with bilirubin test results, so it is important to tell the doctor about all medicines being taken. It does not specifically mention supplements. Source: testing.com

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: "Are my results normal or abnormal?", "Were any other measurements taken and what were the results?", "What do these tests tell us about overall health?", and "Do I need any follow-up tests?" Source: testing.com

**treatment_impact:** The page says that repeated bilirubin testing can help a doctor monitor how a patient with a liver disorder is responding to treatment, so the number may change over time as care continues. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 18. Troponin I — Troponin

**URL:** https://www.testing.com/tests/troponin/
<<<ANSWER
Here are the answers based **only** on what the testing.com Troponin Test page says. Many fields are not covered by this page, which focuses on troponin as a heart test — not on colon cancer, bedridden care, or palliative support.

---

**meaning_high_simple:** A high troponin level means there may be damage or injury to the heart muscle. Even a small measurable amount is considered significant because troponin is not normally found in the blood. Source: testing.com

**meaning_low_simple:** If troponin levels stay normal over a 12-hour period after symptoms, it is unlikely that a heart attack occurred. Normal levels are a reassuring sign that the heart muscle has not been significantly damaged. Source: testing.com

**affected_system:** This test measures the health of the heart. Troponin is a protein released into the blood when the heart is damaged or under stress. Source: testing.com

**symptoms_to_watch:** Watch for chest pain, squeezing or heavy pressure on the chest, pain spreading to the arms, shoulders, neck, or jaw, sudden tiredness or weakness, nausea or vomiting, sweating, shortness of breath, feeling faint, irregular heartbeat, or unusual anxiety. Source: testing.com

**warning_signs_tonight:** The page does not give specific overnight warning signs for a bedridden patient, but it states that if any signs of a heart attack appear, you should seek medical attention immediately. Source: testing.com

**critical_threshold:** The page does not give a specific number for a dangerous troponin level. It says reference ranges vary by laboratory and type of test, so the lab report and doctor must be used to interpret the result. Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** (not found)

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** Biotin (a B vitamin found in many multivitamins and supplements) can cause troponin test results to appear falsely low. The page says to always tell the doctor if the patient is taking any supplement that contains biotin. Source: testing.com

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: "What are my troponin levels?", "Did I have a heart attack?", "Is there damage to the heart muscle?", "Do you recommend any other tests?", and "Should troponin be tested again?" Source: testing.com

**treatment_impact:** The page notes that troponin levels can rise after heart-related surgery, open-heart surgery, or cardiac defibrillation. It does not address cancer treatment specifically. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 19. Uric Acid

**URL:** https://www.testing.com/tests/uric-acid/
<<<ANSWER
Here are plain-language answers based **only** on what the testing.com uric acid page says:

---

**meaning_high_simple:** High uric acid in the blood means the body is either making too much of it or the kidneys are not removing enough. In cancer patients, it can rise because cancer therapies cause more cells to break down and release uric acid. Source: testing.com

**meaning_low_simple:** Low uric acid levels in the blood are uncommon and rarely a cause for concern on their own. They can be linked to certain liver or kidney diseases, a low-purine diet, or some medications, but doctors usually identify those causes through other tests. Source: testing.com

**affected_system:** The kidneys are the main organ involved — they are responsible for removing most uric acid from the body through urine. When uric acid builds up, it can also affect the joints and kidney tissue. Source: testing.com

**symptoms_to_watch:** High uric acid can cause gout, which shows up as joint pain and inflammation, most often in the toes and other joints. Excess uric acid can also lead to kidney stones. Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** A level below 6 mg/dL is the target recommended for people diagnosed with gout, according to guidelines from the American College of Rheumatology. The page does not specify a danger threshold for cancer patients. Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** The page mentions that certain foods can raise uric acid levels, including liver, anchovies, mackerel, dried beans and peas, and beer. Avoiding these may help. Source: testing.com

**hydration_guidance:** (not found)

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** (not found)

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor whether there are any common medications to stop to help control uric acid levels, and whether there are foods to avoid. Source: testing.com

**treatment_impact:** Chemotherapy and radiation therapy for cancer can cause uric acid levels to rise dangerously because these treatments increase cell death, which releases uric acid into the blood. Doctors order this test specifically to keep an eye on that during treatment. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 20. Albumin

**URL:** https://www.testing.com/tests/albumin/
<<<ANSWER
Here are the answers based **only** on what the testing.com albumin page says:

---

**meaning_high_simple:** A high albumin level most often means the person is dehydrated — their body doesn't have enough fluid, which can be caused by things like severe diarrhea. Source: testing.com

**meaning_low_simple:** A low albumin level can mean the liver isn't working well enough to make albumin, or that albumin is being lost through the kidneys. It can also be linked to poor nutrition, inflammation, infection, thyroid disease, or gut problems. Source: testing.com

**affected_system:** Albumin is made by the liver, so low levels are often tied to liver or kidney problems. It helps keep fluid inside blood vessels and carries hormones, vitamins, and enzymes around the body. Source: testing.com

**symptoms_to_watch:** The page mentions that a doctor might order this test if there are signs of liver disease (like yellowing skin or tiredness) or kidney disease (like unusual urination or unexplained swelling, especially of the feet and legs). Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** The normal range is 3.5 to 5.5 g/dL (grams per deciliter). Levels above or below this range may point to an underlying health problem. Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** The page notes that high albumin is most often caused by dehydration, which can result from conditions such as severe diarrhea — implying that staying adequately hydrated is important. No specific guidance for patients is given beyond this. Source: testing.com

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** The page says to tell the doctor about any medications or supplements being taken before the test, because some drugs can affect albumin levels. Source: testing.com

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking: Was the albumin level normal or abnormal, and was it high or low? Were other measurements taken alongside it, and what do those levels show? What is the most likely explanation for the result, and are any follow-up tests recommended? Source: testing.com

**treatment_impact:** The page explains that albumin testing can be used to monitor how a condition responds to treatment, and that follow-up tests can show how severe the disease is and how things change over time. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 21. PCT — Procalcitonin

**URL:** https://www.testing.com/tests/procalcitonin/
<<<ANSWER
Here are plain-language answers based **only** on what the testing.com Procalcitonin (PCT) page says. Fields the page does not cover are marked **(not found)**.

---

**meaning_high_simple:** A high procalcitonin level means there is a high chance your father has sepsis (a dangerous body-wide infection) and a greater risk it could get worse or become life-threatening. It can also be seen with serious infections like meningitis. Source: testing.com

**meaning_low_simple:** A low procalcitonin level suggests a lower risk of sepsis, but it doesn't completely rule it out. It may mean the symptoms are caused by something other than a bacterial infection, or that a bacterial infection is very early (less than 6 hours old) or still limited to one area. Source: testing.com

**affected_system:** This test mainly relates to the body's response to bacterial infection and the immune system. It is used to check whether an infection has spread into the bloodstream (sepsis), which can affect the whole body. Source: testing.com

**symptoms_to_watch:** Signs that may mean the infection is getting worse include chills or shivering, fever, clammy or sweaty skin, rapid breathing, fast heartbeat, confusion or disorientation, and urinating less than usual. Source: testing.com

**warning_signs_tonight:** Watch for sudden confusion or disorientation, very fast breathing or heartbeat, clammy/sweaty skin, and a big drop in how alert or responsive he is — these are signs sepsis may be worsening and staff should be told immediately. Source: testing.com

**critical_threshold:** (not found)

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** (not found)

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** (not found)

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** (not found)

**treatment_impact:** If procalcitonin levels go down over time while he is being treated, that means the treatment is working. If the levels stay the same or rise, it may mean treatment needs to continue or be changed. The test can also help doctors decide when it is safe to stop antibiotics. Source: testing.com

**palliative_care:** (not found)

---

**Note for the family:** This page is specifically about the PCT blood test and what its results mean for detecting infection/sepsis. It does not address cancer care, nutrition, comfort care, or family communication. For those topics, please ask the hospital's care team or palliative care nurse directly — they are the best resource for your father's specific situation.
ANSWER>>>

---

### 22. D-dimer

**URL:** https://www.testing.com/tests/d-dimer/
<<<ANSWER
Here are the answers based **only** on what the testing.com D-Dimer page says:

---

**meaning_high_simple:** A high (positive) D-dimer result means there may be significant blood clot formation and breakdown happening somewhere in the body. It does not confirm a clot is present — it just means more tests (like an ultrasound or CT scan) are needed to find out. Source: testing.com

**meaning_low_simple:** A low (negative) D-dimer result means it is very unlikely that the person has a dangerous blood clot forming right now. Doctors consider a result below 0.50 mg/L FEU to be negative. Source: testing.com

**affected_system:** The D-dimer test relates to the blood clotting system. It looks at whether the body is forming and breaking down blood clots in the veins, arteries, or lungs. Source: testing.com

**symptoms_to_watch:** Warning symptoms that might lead a doctor to order this test include leg pain, leg swelling, or skin discoloration in one leg (possible clot in the leg), and sudden shortness of breath, chest pain, coughing up blood, or a fast heart rate (possible clot in the lungs). Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** The cut-off level is 0.50 mg/L FEU — below this is considered negative (no clot likely), and above this is considered positive (further testing needed). Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** (not found)

**refusal_handling:** (not found)

**bedridden_risks:** The page notes that being in hospital or having recent surgery, trauma, infection, heart attack, or certain cancers can all raise D-dimer levels — meaning a positive result in a hospitalised patient does not necessarily mean there is a clot. The page specifically states D-dimer is typically **not** used to rule out clots in hospitalised patients for this reason. Source: testing.com

**supplements_safety:** (not found)

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: "Does an elevated D-dimer always mean I could have a clot or some type of disorder?" and "What are the next steps if I get a positive D-dimer result?" — both useful questions to raise with the care team. Source: testing.com

**treatment_impact:** If the test is being used to monitor a clotting condition called DIC, falling D-dimer levels mean treatment is working, while rising levels may mean it is not working. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

---

### 23. HbA1c — Hemoglobin A1c

**URL:** https://www.testing.com/tests/hemoglobin-a1c/
<<<ANSWER
Here are the answers based **only** on what the testing.com Hemoglobin A1c page says. Because this page is specifically about diabetes blood-sugar testing — not colon cancer, hospital care, or end-of-life support — most fields your family needs are not covered there.

---

**meaning_high_simple:** A high result (at or over 6.5%) means the person's blood sugar has been too high on average over the past few months, which may indicate diabetes. The higher the percentage, the more sugar has been sticking to the red blood cells. Source: testing.com

**meaning_low_simple:** The page defines "normal" as under 5.7%, which means blood sugar has been well-controlled. The page does not explain what an unusually low result would mean for a seriously ill or bedridden person. Source: testing.com

**affected_system:** This test measures blood sugar (glucose) control. It relates to how well the body manages sugar using the hormone insulin, and high levels can damage organs over time. Source: testing.com

**symptoms_to_watch:** Signs that blood sugar may be too high include excessive thirst, needing to urinate very often, blurry vision, tingling or numbness in the hands and feet, and feeling extremely tired. Source: testing.com

**warning_signs_tonight:** (not found)

**critical_threshold:** A result at or over 6.5% is used to diagnose diabetes. However, the page notes that doctors set personal target numbers for people already diagnosed, taking into account age, past sugar control, and other health conditions. Source: testing.com

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** (not found)

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** (not found)

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** (not found)

**treatment_impact:** The page notes that if someone already has diabetes, the doctor will consider their age, ability to control blood sugar in the past, and any complications when setting a target A1c number. This suggests illness and other health conditions can affect how results are interpreted. Source: testing.com

**palliative_care:** (not found)

---

**Important note for the family:** This page is about a diabetes blood-sugar test and does not address colon cancer, hospital care for elderly patients, or end-of-life support. For the specific concerns you have about your 86-year-old loved one, I'd strongly encourage speaking directly with his care team, or asking his hospital if they have a **palliative care team** who can walk through his comfort, nutrition, and care needs in plain language.
ANSWER>>>

---

### 24. LDH — Lactate Dehydrogenase

**URL:** https://www.testing.com/tests/lactate-dehydrogenase-ldh/
<<<ANSWER
Here are the answers based **only** on what the testing.com LDH page says. Fields not covered by that page are marked (not found).

---

**meaning_high_simple:** A high LDH result means that cells or tissues somewhere in the body are being damaged faster than normal, causing LDH to leak into the blood. For someone with cancer, a high level can help doctors understand how serious the cancer is or how well treatment is working. Source: testing.com

**meaning_low_simple:** A low LDH result is uncommon and usually not a concern. The page notes it can happen if someone is taking high doses of vitamin C or E, or in a rare genetic condition where the body cannot make LDH properly. Source: testing.com

**affected_system:** LDH is found throughout the body — the biggest amounts are in the heart, muscles, kidneys, lungs, and red blood cells. It is also present in many cancers. So a high result could point to damage in any of these areas. Source: testing.com

**symptoms_to_watch:** (not found)

**warning_signs_tonight:** (not found)

**critical_threshold:** (not found)

**foods_to_give:** (not found)

**foods_to_avoid:** (not found)

**hydration_guidance:** (not found)

**refusal_handling:** (not found)

**bedridden_risks:** (not found)

**supplements_safety:** High intake of vitamin C or E can cause LDH test results to appear lower than they actually are, which could give misleading information. It is worth telling the doctor if your father is taking these vitamins. Source: testing.com

**immune_and_hygiene:** (not found)

**communication_if_confused:** (not found)

**emotional_support:** (not found)

**oncologist_questions:** The page suggests asking the doctor: what the LDH result is and whether it is within the normal range; what might be causing an elevated level; whether other tests are needed; and what the LDH level reveals about the cancer's severity, outlook, and response to treatment. Source: testing.com

**treatment_impact:** LDH testing can be done during and after cancer treatment to see how well the treatment is working and to assess the likely outcome of the disease. A condition called "tumor lysis syndrome" — where tumor cells die rapidly after treatment starts — can also cause LDH to rise. Source: testing.com

**palliative_care:** (not found)
ANSWER>>>

## When you're done

Save this file and give it back to me. I'll merge every `(found)` answer into `data.json`,
skip every `(not found)`, and the website will show the new info automatically.
