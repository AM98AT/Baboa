# Put the Health Tracker Online (so family can open it from any phone, anywhere)

We'll use **Streamlit Community Cloud** — it's free, and it keeps the app **private** so only
people you invite can see Grandpa's results.

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

1. Edit `data.json` with the new test results, like you do now.
2. Double-click **`publish.bat`** in this folder.
3. Wait about 1 minute — the website updates by itself. Family just refreshes their phone.

That's it. No commands, no re-deploying.

> First time you run `publish.bat` it may ask you to sign in to GitHub — say yes once,
> and it remembers you afterward.

---

## If something breaks
- **publish.bat says "nothing to commit":** you didn't change data.json, or you already published it.
- **Website didn't update:** open the app's **Manage app → Reboot**.
- **Family can't open it:** check their email is added under **Settings → Sharing**.
