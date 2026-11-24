# Deployment Guide

## Option 1: GitHub Pages (Recommended — Free, Instant)

1. Go to your repo → **Settings → Pages**
2. Under "Source", select **GitHub Actions**
3. Push any change to `master` — the `deploy-pages.yml` workflow deploys `index.html` automatically
4. Live URL: `https://nandan-k-s-27.github.io/toolkit-readiness-agent/`

## Option 2: Netlify (Drag & Drop)

1. Build the page locally: `python build_page.py`
2. Go to [app.netlify.com/drop](https://app.netlify.com/drop)
3. Drag and drop the entire project folder
4. Done — Netlify gives you a live URL instantly

## Option 3: Vercel

```bash
npm i -g vercel
vercel --prod
# or via Vercel dashboard: import GitHub repo, root = /, output = index.html
```

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
