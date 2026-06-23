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
    """Safe secret read. st.secrets.get raises *and shows a UI error* when no secrets
    file exists; load_if_toml_exists() checks quietly first."""
    try:
        if not st.secrets.load_if_toml_exists():
            return default
        return st.secrets.get(key, default)
    except Exception:
        return default


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
    print("ok github_store merge logic")
