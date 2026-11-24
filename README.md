# 100-App Toolkit Readiness Research Agent

[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-toolkit--readiness--agent.vercel.app-38bdf8?style=for-the-badge&logo=vercel)](https://toolkit-readiness-agent.vercel.app)
[![Single App Action](https://img.shields.io/badge/Run_Single_App-GitHub_Action-22c55e?style=for-the-badge&logo=githubactions)](https://github.com/Nandan-k-s-27/toolkit-readiness-agent/actions)

> **Live Platform:** [https://toolkit-readiness-agent.vercel.app](https://toolkit-readiness-agent.vercel.app)  
> **Key Finding:** 76/100 SaaS apps are buildable today with self-serve developer access, 62 have existing MCP implementations, and OAuth2 dominates authentication (60%); audited with 73% verbatim quote verification against live documentation and benchmarked across 30 hand-labeled ground-truth apps (70.0% buildability accuracy).

---

## Quick Start (with Free Google Gemini API)

1. Copy `.env.example` to `.env` (or open the provided `.env` file):
   ```bash
   cp .env.example .env
   ```
2. Paste your free Gemini API key into `.env`:
   ```ini
   GEMINI_API_KEY=your-gemini-key-here
   ```
   *(Get a free key in seconds at [Google AI Studio](https://aistudio.google.com/))*

3. Run the pipeline directly:
   ```bash
   # Single-app test
   python research.py pass1 --app Slack
   python research.py pass2 --app Slack

   # Full 100-app pipeline
   python research.py pass1
   python research.py pass2
   python analyze.py
   python build_page.py
   # open index.html in your browser
   ```

*(Anthropic Claude is also supported: set `ANTHROPIC_API_KEY=...` and `LLM_PROVIDER=anthropic` in `.env`)*

---

## Pipeline Architecture & Verification Loops

```
apps.csv (100 apps)
  → DuckDuckGo / Composio Search Tool → Fetch raw documentation
  → SPA / Headless Browser Detection: flag client-rendered JS roots (<div id="root">) to human_queue.json
  → LLM JSON Extractor (Pass 1 Baseline) + verbatim excerpt quotes
  → Code-level string match: verify extracted quote exists verbatim in raw page text
  → LLM Critic: verify quote logically supports the verdict claim
  → Targeted re-research query generation on low confidence / unverified claims (Pass 2)
  → human_queue.json for sales walls, SPA shells, and enterprise gates
  → results_final.json (100 evidence-backed records)
  → analyze.py → patterns.json
  → build_page.py → index.html (self-contained, agent-readable with SSR HTML)
```

### Extra Verification Loop: Client-Side SPA Detection
Standard HTTP fetching fails silently when documentation pages rely on client-side JavaScript rendering (Single Page Applications). Our pipeline detects SPA skeleton markers (e.g., `<div id="root"></div>`, `<div id="app"></div>`, *"enable javascript to run this app"*).
- **What it caught:** On **Paygent Connect** and **higgsfield**, client-side frameworks hid pricing and documentation behind dynamic scripts. Rather than hallucinating synthetic endpoints, the agent flagged them and routed them into `human_queue.json` for human inspection.

---

## Ground Truth Benchmark & Honest Misses

The agent's performance was evaluated against `gold_labels.csv`, containing **30 stratified applications** (3 per category across all 10 categories) hand-verified directly against official developer documentation:

| Metric | Pass 1 (Baseline) | Pass 2 (Final) | Notes |
|--------|-------------------|----------------|-------|
| **Buildability Accuracy** | 66.7% | **70.0%** | Highly reliable verdict on whether an app can be integrated |
| **Self-Serve Access Accuracy** | **70.0%** | 60.0% | Conservative critic penalizes edge-case trials |
| **Existing MCP Accuracy** | 33.3% | 30.0% | Fast-moving community vs official MCP ecosystem |
| **Authentication Methods** | 26.7% | 16.7% | Strict exact multi-label set match (`bearer_token` vs `api_key` synonyms) |
| **Verbatim Quote Validity** | 68.0% | **73.0%** | Quotes string-matched verbatim against fetched page text |

### Honest Misses: Applications That Defeated the Agent
1. **Paygent Connect & Waterfall.io**: Enterprise sales walls and partner agreements withhold public documentation entirely.
2. **Plaid**: Agent conflated the free developer sandbox with live production access (which requires underwriting and compliance review).
3. **Ahrefs & Otter AI**: Free consumer UI accounts exist, but developer API keys are gated behind bespoke enterprise contracts.
4. **Twilio**: Dual authentication scheme (HTTP Basic Account SID/Token + HMAC webhook signing) caused partial multi-label mismatch.

---

## Technical Choices & Tooling Roles

### Google Gemini vs Anthropic Claude
- **Gemini (Default):** Utilizes `gemini-2.5-flash` and `gemini-3.5-flash-lite`. Gemini offers a generous free tier with high request limits (15 RPM / 1M TPM), enabling full multi-threaded pipeline execution across 100 apps without requiring a paid subscription.
- **Claude:** Supports `claude-sonnet-5-5` for high-reasoning critic passes when an Anthropic key is configured.

### Composio SDK Role
- **Composio Search Tool:** When `COMPOSIO_API_KEY` is provided, `research.py` uses the Composio SDK to execute search via `COMPOSIO_SEARCH_DUCK_DUCK_GO_SEARCH`.
- **Direct Fallback:** When `COMPOSIO_API_KEY` is absent, the agent automatically falls back to direct DuckDuckGo search so any developer can run the pipeline without friction.

---

## Output Files

| File | Description |
|------|-------------|
| `results_pass1.json` | Baseline single-shot extraction |
| `results_final.json` | Evidence-verified final dataset (100 apps) |
| `human_queue.json` | 29 apps flagged for human review (sales walls, SPA shells, low confidence) |
| `human_notes.json` | Inspection notes detailing friction points and manual audits |
| `patterns.json` | Headline statistics and distributions generated by `analyze.py` |
| `gold_labels.csv` | 30 stratified apps hand-verified against real developer documentation |
| `accuracy.json` | Detailed pass1 vs final accuracy evaluation vs gold labels |
| `llms.txt` | Machine-readable index for AI agents and LLM crawlers |
| `index.html` | Self-contained, agent-readable dashboard with static SSR pre-rendered table and metrics |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | *(free)* | **Google Gemini API Key** ([Get free key here](https://aistudio.google.com/)) |
| `ANTHROPIC_API_KEY` | optional | Alternative Anthropic API Key |
| `LLM_PROVIDER` | `gemini` | `gemini` or `anthropic` (auto-detected if keys are set) |
| `MODEL` | `gemini-2.5-flash` | Model name (`gemini-2.5-flash`, `gemini-3.5-flash-lite`, or `claude-sonnet-5-5`) |
| `SEARCH_BACKEND` | `direct` | `direct` (Free DuckDuckGo HTML) or `composio` |
| `COMPOSIO_API_KEY` | optional | Composio API key if using Composio search backend |
| `REPO_URL` | `#` | Repository URL for page links |

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
