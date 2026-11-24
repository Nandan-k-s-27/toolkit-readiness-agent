# 100-App Toolkit Readiness Research Agent

> **Which of 100 apps can become an AI-agent toolkit component today?**
> Automated research agent that scores every app on auth, API access, MCP availability, and buildability — with verbatim evidence for every claim.

## Quick Start (with Free Google Gemini API)

You can run this completely free using **Google Gemini** (get a free key at [Google AI Studio](https://aistudio.google.com/)):

```bash
git clone https://github.com/Nandan-k-s-27/toolkit-readiness-agent.git
cd toolkit-readiness-agent
pip install -r requirements.txt

# Set your free Gemini API key
export GEMINI_API_KEY="your-gemini-api-key"

# Single-app run
python research.py pass1 --app Slack

# Full 100-app pipeline
python research.py pass1
python research.py pass2
python analyze.py
python build_page.py
# open index.html in browser
```

*(Anthropic Claude is also supported if you prefer: `export ANTHROPIC_API_KEY=...`)*

## Pipeline

```
apps.csv (100 apps)
  → DuckDuckGo / Composio search  →  fetch docs pages (cached)
  → LLM extract JSON (Gemini 2.5 Flash / Claude) + verbatim quote per claim   ← Pass 1 (baseline)
  → code checks quote exists on cited page
  → LLM critic: does quote support the claim?
  → targeted re-research on failures
  → low confidence → human_queue.json
  → results_final.json                                                         ← Final
  → analyze.py → patterns.json
  → build_page.py → index.html (self-contained, offline-ready)
```

## Output Files

| File | Description |
|------|-------------|
| `results_pass1.json` | Baseline extraction (do NOT overwrite before pass2) |
| `results_final.json` | Evidence-verified final results (100 rows) |
| `human_queue.json` | Apps where agent was uncertain; needs human review |
| `patterns.json` | Computed headline statistics |
| `gold_labels.csv` | Hand-labeled sample for accuracy scoring (20 stratified apps) |
| `accuracy.json` | pass1 vs final accuracy vs gold labels |
| `index.html` | Self-contained results page (dark + light mode) |

## Fields per App

| Field | Values |
|-------|--------|
| `auth_methods` | oauth2, api_key, basic, bearer_token, jwt, request_signing, none, other |
| `self_serve` | self_serve_free, self_serve_trial, paid_plan_required, approval_required, partner_gated, no_public_api, unclear |
| `api_type` | rest, graphql, soap, sdk_only, cli_only, websocket, none |
| `api_breadth` | narrow, medium, broad, unknown |
| `existing_mcp` | official, community, none_found, unknown |
| `buildability` | yes, yes_with_caveats, blocked |
| `blocker` | none, paid_gate, approval_gate, partner_gate, no_public_api, cli_or_local_only, per_tenant_setup, rate_or_cost, unclear |

Every field has an `evidence` entry: `{url, quote}` — the verbatim text from the cited page that supports the claim.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | *(free)* | **Google Gemini API Key** ([Get free key here](https://aistudio.google.com/)) |
| `ANTHROPIC_API_KEY` | optional | Alternative Anthropic API Key |
| `LLM_PROVIDER` | `gemini` | `gemini` or `anthropic` (auto-detected if keys are set) |
| `MODEL` | `gemini-2.5-flash` | Model name (`gemini-2.5-flash`, `gemini-1.5-pro`, or `claude-sonnet-5-5`) |
| `SEARCH_BACKEND` | `direct` | `direct` (Free DuckDuckGo HTML) or `composio` |
| `COMPOSIO_API_KEY` | optional | Composio API key if using Composio search |
| `REPO_URL` | `#` | Your repo URL for the generated page |

## Offline Demo Mode

To test or generate full demo data without any API key:
```bash
python research.py pass1 --demo
python research.py pass2 --demo
```
