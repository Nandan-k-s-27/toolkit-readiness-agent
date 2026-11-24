#!/usr/bin/env python3
"""results_final.json -> patterns.json (computed, never hand-typed)."""
import json, pathlib
from collections import Counter, defaultdict
ROOT = pathlib.Path(__file__).parent
R = json.load(open(ROOT / "results_final.json", encoding="utf-8")); N = len(R)
pct = lambda n: f"{round(100 * n / N)}%"
auth = Counter(a for r in R for a in r.get("auth_methods", []))
ss = Counter(r.get("self_serve") for r in R)
bl = Counter(r.get("blocker") for r in R if r.get("blocker") not in (None, "none"))
bu = Counter(r.get("buildability") for r in R)
mcp = Counter(r.get("existing_mcp") for r in R)
cat = defaultdict(Counter)
for r in R: cat[r["category"]][r.get("self_serve")] += 1
easy = [r["app"] for r in R if r.get("buildability") == "yes" and r.get("self_serve", "").startswith("self_serve")]
outreach = [r["app"] for r in R if r.get("self_serve") in ("partner_gated", "approval_required", "paid_plan_required") or r.get("buildability") == "blocked"]
top_auth, top_n = auth.most_common(1)[0]
top_bl = bl.most_common(1)[0] if bl else ("none", 0)
gated_cat = sorted(cat.items(), key=lambda kv: -(sum(v for k, v in kv[1].items() if k and not k.startswith("self_serve")) / 10))
P = {"n": N, "auth": auth, "self_serve": ss, "blockers": bl, "buildability": bu, "mcp": mcp,
     "by_category": {c: dict(v) for c, v in cat.items()}, "easy_wins": easy, "needs_outreach": outreach,
     "headlines": [
        f"{top_auth} is the most common auth: {top_n}/{N} apps list it.",
        f"{pct(sum(v for k, v in ss.items() if k and k.startswith('self_serve')))} of apps are self-serve; {pct(len(outreach))} need payment, approval or outreach.",
        f"Most common blocker: {top_bl[0]} ({top_bl[1]} apps).",
        f"{len(easy)} easy wins (self-serve + buildable now); {bu.get('blocked', 0)} blocked today.",
        f"Most gated category: {gated_cat[0][0]}.",
        f"Existing MCP found for {mcp.get('official', 0) + mcp.get('community', 0)}/{N} apps ({mcp.get('official', 0)} official)."]}
json.dump(P, open(ROOT / "patterns.json", "w", encoding="utf-8"), indent=1); print("\n".join(P["headlines"]))
