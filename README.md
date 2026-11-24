# 100-App Toolkit Readiness Research Agent

> **Which of 100 apps can become an AI-agent toolkit component today?**
> Automated research agent that scores every app on auth, API access, MCP availability, and buildability — with verbatim evidence for every claim.

## Quick Start

```bash
git clone https://github.com/Nandan-k-s-27/toolkit-readiness-agent.git
cd toolkit-readiness-agent
pip install -r requirements.txt

# Set your API keys
export COMPOSIO_API_KEY=<your-composio-key>
export ANTHROPIC_API_KEY=<your-anthropic-key>

# Single-app dry run
python research.py pass1 --app Slack

# Full pipeline (all 100 apps)
python research.py pass1
python research.py pass2
python analyze.py
python build_page.py
# open index.html in browser
```

## Pipeline

```
apps.csv (100 apps)
  → Composio search  →  fetch docs pages (cached)
  → LLM extract JSON + verbatim quote per claim       ← Pass 1 (baseline)
  → code checks quote exists on cited page
  → LLM critic: does quote support the claim?
  → targeted re-research on failures
  → low confidence → human_queue.json
  → results_final.json                                 ← Final
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
| `gold_labels.csv` | Hand-labeled sample for accuracy scoring |
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

## Design Decisions

- **Search** goes through Composio (`SEARCH_BACKEND=composio`) or directly via DuckDuckGo (`SEARCH_BACKEND=direct`)
- **Quote verification**: code checks the LLM-extracted quote actually appears on the fetched page → kills hallucinated evidence
- **LLM critic**: second LLM pass asks "does this quote actually support this claim?"
- **Retry loop**: failures trigger a differently-worded re-search + re-extract
- **Human queue**: apps where evidence still fails after two attempts, or confidence < 0.6

## Verification

```bash
python verify.py sample     # generates gold_labels.csv template (20 stratified apps)
# Fill gold_labels.csv by hand from real docs
python verify.py score      # writes accuracy.json (pass1 vs final vs gold)
```

## Known Limits

- JS-rendered docs (fetch returns little content) → human queue
- Login-walled docs → human queue
- Pricing pages that change frequently → may drift from gold

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `COMPOSIO_API_KEY` | required | Your Composio API key |
| `ANTHROPIC_API_KEY` | required | Your Anthropic API key |
| `SEARCH_BACKEND` | `composio` | `composio` or `direct` (DuckDuckGo fallback) |
| `COMPOSIO_SEARCH_SLUG` | `COMPOSIO_SEARCH_DUCK_DUCK_GO_SEARCH` | Composio tool slug |
| `COMPOSIO_USER_ID` | `default` | Composio user ID |
| `MODEL` | `claude-sonnet-5-5` | Anthropic model to use |
| `REPO_URL` | `#` | Your repo URL for the generated page |

## Categories Covered (100 apps)

1. CRM and Sales (10 apps)
2. Support and Helpdesk (10 apps)
3. Communications and Messaging (10 apps)
4. Marketing, Ads, Email and Social (10 apps)
5. Ecommerce (10 apps)
6. Data, SEO and Scraping (10 apps)
7. Developer, Infra and Data platforms (10 apps)
8. Productivity and Project Management (10 apps)
9. Finance and Fintech (10 apps)
10. AI, Research and Media-native (10 apps)
