# Put the Health Tracker Online (so family can open it from any phone, anywhere)

We'll use **Streamlit Community Cloud** — it's free, and it keeps the app **private** so only
people you invite can see Grandpa's results.

> 💵 **Is this really free?** Yes — 100% free, forever. GitHub is free, Streamlit Community
> Cloud is free, and you never enter a credit card. There are no hidden costs.

You only do **Part 1 and Part 2 once**. After that, daily updates are a single double-click (Part 3).

---

## ⚠️ Privacy first
This is private medical data. Follow the steps exactly so the app is locked to your family only:
- The GitHub repository must be **Private**.
- In Streamlit, set viewing to **"Only specific people"** and add your family's emails.
Do NOT share the link publicly or post it anywhere.

---

## PART 1 — Put the project on GitHub (one time)

The easiest way (no typing commands) is **GitHub Desktop**:

1. Create a free account at **https://github.com** (use your email: ameenatroshy@gmail.com).
2. Download and install **GitHub Desktop**: https://desktop.github.com
3. Open GitHub Desktop → sign in with your GitHub account.
4. Click **File → Add Local Repository** → choose this folder:
   `C:\Users\ameen\OneDrive\Other\Desktop\Baboa`
   (It's already a git repository — I set that up for you.)
5. Click **Publish repository** (top right).
   - Name: `baboa-health` (any name is fine)
   - ✅ **Keep "Keep this code private" CHECKED** — very important.
   - Click **Publish repository**.

Your project is now safely on GitHub (private).

---

## PART 2 — Turn it into a website (one time)

1. Go to **https://share.streamlit.io** and click **Sign in with GitHub**.
2. Allow Streamlit to access your GitHub (including private repos) when it asks.
3. Click **Create app** → **Deploy a public app from a repo** (don't worry, we make it private after).
   - **Repository:** `your-username/baboa-health`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - Click **Deploy**.
4. Wait ~2 minutes for it to build. You'll get a link like
   `https://baboa-health.streamlit.app`
5. **Lock it down:** open the app → bottom-right **Manage app** → **Settings → Sharing** →
   set **"Who can view this app"** to **specific people** and add each family member's
   Google or GitHub email. Save.
6. Send that link to your family. On their phones they tap it, sign in with the email you
   added, and they're in. They can **Add to Home Screen** so it feels like an app.

---

## PART 3 — Your daily update (the only thing you do from now on)

1. Edit `results.json` with the new test results (see `READ_ME_FIRST.md`).
2. **Push** with GitHub Desktop: Commit to main → **Push origin**.
3. Wait about 1 minute — the website updates by itself. Family just refreshes their phone.

That's it. No commands, no re-deploying.

---

## PART 4 — Add results from the website itself (optional, one-time setup)

The site has a **➕ إضافة نتيجة** page (last chip). Submitting there commits the new
reading straight to GitHub, so you don't have to edit `results.json` by hand. To enable it
you give the app a GitHub token + a passcode, stored as **Streamlit Secrets** (never in the repo).

1. **Make a GitHub token** (fine-grained, least privilege):
   - GitHub → Settings → **Developer settings** → **Personal access tokens → Fine-grained tokens** → **Generate new token**.
   - **Repository access:** Only select repositories → pick your repo (`AM98AT/Baboa`).
   - **Permissions:** Repository permissions → **Contents: Read and write**. Nothing else.
   - Generate and **copy** the token (starts with `github_pat_`).
2. **Add the secrets** in Streamlit: open the app → **Manage app → Settings → Secrets**, paste:
   ```toml
   github_token = "github_pat_...your token..."
   add_passcode = "choose-a-family-passcode"
   # optional overrides (defaults shown):
   # github_repo  = "AM98AT/Baboa"
   # github_branch = "main"
   ```
   Save. (Locally, put the same lines in `.streamlit/secrets.toml` — it's git-ignored.)
3. On the ➕ page, enter the passcode, pick the test, fill the reading, and **Save**. It commits
   to GitHub and the site redeploys in ~1 minute. New tests that need researched guidance still
   use the local tool (`add_results.bat`).

> Each person (grandfather / grandmother / mom / dad) is a chip at the top — switch with it.
> Their readings live in separate files (`results.json`, `data/<name>.json`); edit `users.json`
> to set each person's name / sex / date-of-birth (used on the doctor PDF).

---

## If something breaks
- **Nothing changed on the website:** make sure you actually committed *and* pushed in GitHub Desktop.
- **Website didn't update:** open the app's **Manage app → Reboot**.
- **Family can't open it:** check their email is added under **Settings → Sharing**.
- **➕ page says token/passcode not set:** add the Secrets from Part 4.
- **➕ save fails:** the token needs **Contents: Read and write** on the right repo, and must not be expired.
