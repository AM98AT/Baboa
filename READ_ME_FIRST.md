# Which file is which (so you never get confused)

The data is split into **two linked files**, joined by an `id` number.

| File | What's in it | Do you edit it? |
|------|--------------|-----------------|
| **`results.json`** | The daily readings only: `id`, test code, unit, and the list of records (date, result, lab, normal range). | ✅ **YES — this is the only file you touch every day.** |
| **`info.json`** | The Arabic info shown on the site: `id`, names, category, and all family guidance. | ❌ No (it's generated automatically). |
| `info_en.json` | The English master of the info + guidance. | ❌ Only if you want to change the guidance text. |
| `build_ar.py` | Turns `info_en.json` → `info.json` (the Arabic). | ❌ No. |
| `app.py` | The website. Joins `results.json` + `info.json` by `id`. | ❌ No. |

## How the two files connect
Each test has the same `id` in both files. Example — Hemoglobin is `id: 1`:

`results.json`
```json
{ "id": 1, "test": "Hb", "unit": "g/dl", "records": [ ... ] }
```
`info.json`
```json
{ "id": 1, "short_name": "Hb", "full_name": "الهيموغلوبين (خضاب الدم)", "family_guidance": { ... } }
```
The website looks up the `id` from `results.json` in `info.json` and shows them together.

## Your daily routine
1. Open **`results.json`**.
2. Find the test by its `id` / code, and add the new reading to its `records` list:
   ```json
   { "date": "21-06-2026 10:00:00", "result": 11.2, "lab_name": "Omed Oncology Teaching Hospital", "normal_range": "13 - 17" }
   ```
3. Save the file.
4. Double-click **`publish.bat`** → the website updates in about a minute.

> ⚠️ Keep the `id` numbers the same in both files. To add a brand-new test, give it a new `id` in **both** `results.json` and `info_en.json`, then run `publish.bat`.
