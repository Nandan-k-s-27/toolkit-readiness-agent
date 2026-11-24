# Submission checklist (tick every box before sending)

## Setup
- [ ] Composio account + COMPOSIO_API_KEY; Anthropic key set
- [ ] Confirm the Composio search tool slug works: `composio.tools.execute(slug=..., arguments={"query":"test"}, user_id="default")`; set COMPOSIO_SEARCH_SLUG if different
- [ ] Single-app dry run passes: `python research.py pass1 --app Slack`

## Research (per app, 100 rows)
- [ ] category + one-liner
- [ ] auth method(s)
- [ ] self-serve vs gated
- [ ] API surface (REST/GraphQL, breadth, existing MCP)
- [ ] buildability verdict + main blocker
- [ ] evidence URL + quote for each answer
- [ ] "and more": confidence, notes, needs_human flag
- [ ] results_final.json has 100 rows, no empty evidence on non-"unclear" claims

## Patterns
- [ ] analyze.py run; headline patterns stated at the TOP of the page
- [ ] auth dominance, self-serve vs gated by category, top blocker, easy wins vs outreach list
- [ ] Skim patterns.json against the table; sanity-check 3 numbers by hand

## Agent
- [ ] Uses Composio SDK/MCP (say exactly where)
- [ ] Page states what it does AND where a human was needed (human_queue.json)
- [ ] Repo README runs from a clean clone

## Verification (accuracy matters most)
- [ ] pass1 saved BEFORE pass2 (do not overwrite)
- [ ] verify.py sample -> hand-fill gold_labels.csv from real docs (>=20 apps; ideally 30)
- [ ] verify.py score -> pass1 vs final accuracy
- [ ] Misses listed honestly; apps that defeated the agent named on the page
- [ ] Optional extra loop: browser-use / manual check on JS-heavy docs
- [ ] Be ready to explain every field and every loop in the interview

## Deliverable
- [ ] build_page.py -> index.html; opens offline; understandable in ~2 min; dark+light OK
- [ ] Deployed live link works in incognito
- [ ] Repo public, README present, no API keys committed (cache/ may be gitignored)
- [ ] Submitted well under 8 hours from receipt
