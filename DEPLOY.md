# Deployment Guide

## Option 1: Vercel (Recommended — Instant 10-Second Deploy)

Since `index.html` is a self-contained, high-performance static web application, Vercel gives you instant edge global delivery, free SSL, and zero configuration:

### Method A: Via Vercel Dashboard (Zero CLI)
1. Go to [vercel.com/new](https://vercel.com/new).
2. Import your GitHub repository: `https://github.com/Nandan-k-s-27/toolkit-readiness-agent`.
3. Keep default settings:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: `python build_page.py` (or leave empty)
   - **Output Directory**: `./`
4. Click **Deploy**. Done!

### Method B: Via Vercel CLI
```bash
npm i -g vercel
vercel --prod
```

---

## Option 2: Render (Static Site)

Render is great if you want to host both the frontend and optionally schedule background worker research jobs:

1. Log into [dashboard.render.com](https://dashboard.render.com/).
2. Click **New +** → **Static Site**.
3. Connect your repository: `https://github.com/Nandan-k-s-27/toolkit-readiness-agent`.
4. Configure:
   - **Name**: `toolkit-readiness-agent`
   - **Build Command**: `python build_page.py`
   - **Publish Directory**: `.`
5. Click **Create Static Site**.
*(A `render.yaml` blueprint is already included in the repo for 1-click infrastructure deployment!)*

---

## Option 3: GitHub Pages (Already Configured)
1. Go to your repo → **Settings → Pages**.
2. Under **Source**, select **GitHub Actions**.
3. It will deploy automatically via `.github/workflows/deploy-pages.yml` to:
   `https://nandan-k-s-27.github.io/toolkit-readiness-agent/`

## Option 4: Local Preview

```bash
python -m http.server 8080
# Open http://localhost:8080
```

## Running the Real Pipeline

Once you have API keys:

```bash
# Set keys
export ANTHROPIC_API_KEY=sk-ant-...
export COMPOSIO_API_KEY=...          # optional if using SEARCH_BACKEND=direct
export SEARCH_BACKEND=direct         # DuckDuckGo fallback, no Composio key needed

# Run full pipeline
python research.py pass1 --workers 8
python research.py pass2 --workers 8
python analyze.py
REPO_URL=https://github.com/Nandan-k-s-27/toolkit-readiness-agent python build_page.py

# Score accuracy (after hand-filling gold_labels.csv)
python verify.py sample   # generates 20-app sample template
# ... fill gold_labels.csv manually from real docs ...
python verify.py score    # writes accuracy.json
```

## GitHub Actions (Automated)

Trigger the full pipeline from GitHub:
1. Go to your repo → **Actions → Research Agent Pipeline**
2. Click **Run workflow**
3. Optionally set a single app name and search backend
4. Results are committed back to `master` and re-deploy via Pages

## Secrets Required for CI

In GitHub repo → **Settings → Secrets and variables → Actions**:

| Secret | Required? | Description |
|--------|-----------|-------------|
| `ANTHROPIC_API_KEY` | Yes (for real run) | Your Anthropic Claude API key |
| `COMPOSIO_API_KEY` | Only if using Composio backend | Your Composio API key |
