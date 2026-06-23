# -*- coding: utf-8 -*-
"""Write a new lab reading straight to the GitHub repo via the Contents API.

Streamlit Cloud's filesystem is ephemeral, so the only way to *persist* a reading
(and update the downloadable JSON) is to commit it. Pushing to GitHub also triggers
the Cloud redeploy that makes it show up. Token/repo come from st.secrets.

# ponytail: GitHub Contents API + requests (already installed via streamlit) — no
# PyGithub/git dependency. One file per commit is plenty at this volume.
"""
import base64
import json
import requests
import streamlit as st

API = "https://api.github.com"


def get_secret(key, default=""):
    """Safe secret read. Accessing a missing st.secrets key raises *and* shows a UI
    error; we read directly (works however Cloud provides secrets) with that print
    suppressed, and fall back to `default` on any miss."""
    try:
        st.secrets.set_suppress_print_error_on_exception(True)
    except Exception:
        pass
    try:
        return st.secrets[key]
    except Exception:
        return default
    finally:
        try:
            st.secrets.set_suppress_print_error_on_exception(False)
        except Exception:
            pass


def _cfg():
    return (get_secret("github_token"),
            get_secret("github_repo", "AM98AT/Baboa"),
            get_secret("github_branch", "main"))


def configured():
    return bool(get_secret("github_token"))


def _headers(token):
    return {"Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"}


def get_file(path):
    """(text, sha) for `path`; ("", None) if it doesn't exist yet (new user)."""
    token, repo, branch = _cfg()
    r = requests.get(f"{API}/repos/{repo}/contents/{path}",
                     headers=_headers(token), params={"ref": branch}, timeout=20)
    if r.status_code == 404:
        return "", None
    r.raise_for_status()
    j = r.json()
    return base64.b64decode(j["content"]).decode("utf-8"), j["sha"]


def put_file(path, text, sha, message):
    """Commit `text` to `path`; returns the commit's html_url."""
    token, repo, branch = _cfg()
    body = {"message": message, "branch": branch,
            "content": base64.b64encode(text.encode("utf-8")).decode("ascii")}
    if sha:
        body["sha"] = sha
    r = requests.put(f"{API}/repos/{repo}/contents/{path}",
                     headers=_headers(token), json=body, timeout=20)
    r.raise_for_status()
    return r.json()["commit"]["html_url"]


def _merge_record(results, test_id, record, test_meta):
    """Pure: append `record` to the test with `test_id`, deduping by exact date.
    Creates the test row from `test_meta` if absent. Returns (new_list, added)."""
    out = [dict(t) for t in results]
    for t in out:
        if t.get("id") == test_id:
            if any(r.get("date") == record["date"] for r in t.get("records", [])):
                return out, False                      # same-date reading already there
            t["records"] = list(t.get("records", [])) + [record]   # don't mutate input
            return out, True
    out.append({"id": test_id, "test": test_meta.get("short_name", ""),
                "unit": test_meta.get("unit", ""), "records": [record]})
    return out, True


def add_reading(results_file, test_id, record, test_meta, label=""):
    """Get the user's results file → merge the reading → commit. Returns commit url.
    Raises ValueError if the reading is a duplicate (nothing to commit)."""
    text, sha = get_file(results_file)
    results = json.loads(text) if text.strip() else []
    merged, added = _merge_record(results, test_id, record, test_meta)
    if not added:
        raise ValueError("هذي النتيجة بنفس التاريخ موجودة من قبل.")
    body = json.dumps(merged, indent=4, ensure_ascii=False) + "\n"
    msg = f"Add {test_meta.get('short_name', test_id)} reading for {label or results_file}"
    return put_file(results_file, body, sha, msg), body


def merge_json(results_file, new_list, label=""):
    """Merge a pasted results-style list (many tests, each with many records) into the
    user's file in ONE commit. Dedupes records by date; creates rows for new test ids.
    Returns (commit_url, body, added_count, new_test_labels). Raises ValueError if
    nothing new. The same engine as add_reading (`_merge_record`), looped."""
    text, sha = get_file(results_file)
    results = json.loads(text) if text.strip() else []
    added, new_tests = 0, []
    for entry in new_list:
        tid = entry.get("id")
        meta = {"short_name": entry.get("test", ""), "unit": entry.get("unit", "")}
        if not any(t.get("id") == tid for t in results):
            new_tests.append(f"#{tid} {entry.get('test', '')}".strip())
        for rec in entry.get("records", []):
            results, ok = _merge_record(results, tid, rec, meta)
            added += int(ok)
    if added == 0:
        raise ValueError("ماكو نتائج جديدة — كلها موجودة من قبل.")
    body = json.dumps(results, indent=4, ensure_ascii=False) + "\n"
    msg = f"Merge {added} reading(s) across {len(new_list)} test(s) for {label or results_file}"
    return put_file(results_file, body, sha, msg), body, added, new_tests


if __name__ == "__main__":   # ponytail: one runnable check — the merge logic, no network
    meta = {"short_name": "Hb", "unit": "g/dl"}
    base = [{"id": 1, "test": "Hb", "unit": "g/dl",
             "records": [{"date": "01-01-2026 10:00:00", "result": 11}]}]
    rec = {"date": "02-01-2026 10:00:00", "result": 12}

    out, added = _merge_record(base, 1, rec, meta)            # append to existing
    assert added and len(out[0]["records"]) == 2

    out2, added2 = _merge_record(out, 1, rec, meta)           # dedupe same date
    assert not added2 and len(out2[0]["records"]) == 2

    out3, added3 = _merge_record(base, 99, rec, meta)         # create stub for new id
    assert added3 and out3[-1]["id"] == 99 and out3[-1]["test"] == "Hb"

    # original list not mutated
    assert len(base[0]["records"]) == 1

    # merge_json's engine: many tests/records in one pass (dedupe + new-test rows)
    def merge_pure(results, new_list):
        added, new_tests = 0, []
        for e in new_list:
            tid = e.get("id")
            m = {"short_name": e.get("test", ""), "unit": e.get("unit", "")}
            if not any(t.get("id") == tid for t in results):
                new_tests.append(tid)
            for r in e.get("records", []):
                results, ok = _merge_record(results, tid, r, m)
                added += int(ok)
        return results, added, new_tests
    incoming = [
        {"id": 1, "test": "Hb", "records": [
            {"date": "01-01-2026 10:00:00", "result": 11},      # dup -> skip
            {"date": "03-01-2026 10:00:00", "result": 13}]},    # new -> add
        {"id": 50, "test": "New", "unit": "x", "records": [
            {"date": "03-01-2026 10:00:00", "result": 7}]},      # new test -> add + stub
    ]
    res, added, new_tests = merge_pure([dict(t) for t in base], incoming)
    assert added == 2, added
    assert new_tests == [50], new_tests
    assert any(t["id"] == 50 and t["test"] == "New" for t in res)
    print("ok github_store merge logic")
