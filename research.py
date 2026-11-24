#!/usr/bin/env python3
"""Research agent: search (Composio) -> fetch docs -> LLM extract with quoted evidence.
pass1: single-shot extraction (baseline).  pass2: evidence-quote check + critic + targeted re-research + human queue.
Usage: python research.py pass1 [--app Slack] | python research.py pass2 [--app Slack]"""
import os, re, json, csv, sys, hashlib, argparse, pathlib, urllib.parse
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import anthropic

ROOT = pathlib.Path(__file__).parent
CACHE = ROOT / "cache"; CACHE.mkdir(exist_ok=True)
MODEL = os.getenv("MODEL", "claude-sonnet-5-5")
UA = {"User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"}
LLM = anthropic.Anthropic()
EVIDENCE_FIELDS = ["auth_methods", "self_serve", "api_type", "existing_mcp", "buildability"]

SYSTEM = """You are a research analyst for an AI-agent toolkit company. Use ONLY the provided page excerpts.
Return ONLY a JSON object with keys:
one_liner: string (what the app does, <=20 words)
auth_methods: list from [oauth2, api_key, basic, bearer_token, jwt, request_signing, none, other]
self_serve: one of [self_serve_free, self_serve_trial, paid_plan_required, approval_required, partner_gated, no_public_api, unclear]
  (self_serve_* = developer can get credentials alone; paid_plan_required = API needs paid tier; approval_required = app/app-review/admin approval; partner_gated = partnership/contact-sales)
api_type: list from [rest, graphql, soap, sdk_only, cli_only, websocket, none]
api_breadth: one of [narrow, medium, broad, unknown]
existing_mcp: one of [official, community, none_found, unknown]; mcp_url: string or ""
buildability: one of [yes, yes_with_caveats, blocked]
blocker: one of [none, paid_gate, approval_gate, partner_gate, no_public_api, cli_or_local_only, per_tenant_setup, rate_or_cost, unclear]
blocker_note: string <=25 words
confidence: number 0-1
evidence: object mapping each of auth_methods, self_serve, api_type, existing_mcp, buildability to {"url": <one of the provided URLs>, "quote": <VERBATIM text copied from that page, <=200 chars>}.
If the pages do not support a claim, use "unclear"/"unknown" and lower confidence. Never invent quotes."""

def norm(s): return re.sub(r"\s+", " ", s or "").strip().lower()

_composio = None
def search(q, n=4):
    backend = os.getenv("SEARCH_BACKEND", "composio")
    urls = []
    if backend == "composio":
        global _composio
        from composio import Composio
        _composio = _composio or Composio()
        r = _composio.tools.execute(
            slug=os.getenv("COMPOSIO_SEARCH_SLUG", "COMPOSIO_SEARCH_DUCK_DUCK_GO_SEARCH"),
            arguments={"query": q}, user_id=os.getenv("COMPOSIO_USER_ID", "default"),
            dangerously_skip_version_check=True)
        urls = re.findall(r"https?://[^\s\"'\\<>)]+", json.dumps(r))
    else:  # direct DuckDuckGo HTML fallback
        h = requests.get("https://html.duckduckgo.com/html/", params={"q": q}, headers=UA, timeout=20).text
        for a in BeautifulSoup(h, "html.parser").select("a.result__a"):
            u = urllib.parse.parse_qs(urllib.parse.urlparse(a.get("href", "")).query).get("uddg", [a.get("href", "")])[0]
            urls.append(u)
    seen, out = set(), []
    for u in urls:
        if any(b in u for b in ("duckduckgo", "composio.dev/api", "backend.composio")) or u in seen: continue
        seen.add(u); out.append(u)
    return out[:n]

def fetch(url, cap=9000):
    p = CACHE / (hashlib.sha1(url.encode()).hexdigest() + ".txt")
    if p.exists(): return p.read_text()
    try:
        r = requests.get(url, headers=UA, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        for t in soup(["script", "style", "nav", "footer"]): t.decompose()
        txt = re.sub(r"\s+", " ", soup.get_text(" "))[:cap]
        if r.status_code >= 400: txt = ""
    except Exception:
        txt = ""
    p.write_text(txt); return txt

def gather(app, hint, queries, have=()):
    urls = []
    if hint and not have:
        urls.append(hint if hint.startswith("http") else "https://" + hint.split()[0])
    for q in queries:
        try: urls += search(q, 3)
        except Exception as e: print("search fail", app, e, file=sys.stderr)
    pages = {}
    for u in urls:
        if u in have or u in pages: continue
        t = fetch(u)
        if len(t) > 300: pages[u] = t
        if len(pages) >= 6: break
    return pages

def llm_json(system, user):
    m = LLM.messages.create(model=MODEL, max_tokens=2500, system=system, messages=[{"role": "user", "content": user}])
    t = m.content[0].text.strip()
    t = re.sub(r"^```(?:json)?|```$", "", t, flags=re.M).strip()
    return json.loads(t[t.find("{"): t.rfind("}") + 1])

def extract(app, pages, prior=None, issues=None):
    ctx = "\n\n".join(f"URL: {u}\n{t}" for u, t in pages.items())
    extra = f"\nPrevious answer: {json.dumps(prior)}\nProblems to fix: {json.dumps(issues)}" if prior else ""
    return llm_json(SYSTEM, f"App: {app}\n\nPAGES:\n{ctx}{extra}")

def check_evidence(rec, pages):
    bad = []
    for f in EVIDENCE_FIELDS:
        e = (rec.get("evidence") or {}).get(f) or {}
        q, u = norm(e.get("quote")), e.get("url")
        ok = bool(q) and u in pages and q in norm(pages[u])
        rec.setdefault("evidence_ok", {})[f] = ok
        if not ok and rec.get(f) not in ("unclear", "unknown", None): bad.append(f)
    return bad

def critic(rec):
    claims = {f: {"value": rec.get(f), "quote": (rec.get("evidence", {}).get(f) or {}).get("quote")} for f in EVIDENCE_FIELDS}
    out = llm_json("You audit research claims. For each field decide if the quote actually supports the value. "
                   'Return JSON {"unsupported": [field names]}.', json.dumps(claims))
    return [f for f in out.get("unsupported", []) if f in EVIDENCE_FIELDS]

def load_apps(only=None):
    rows = list(csv.DictReader(open(ROOT / "apps.csv")))
    return [r for r in rows if not only or r["app"].lower() == only.lower()]

def pass1(r):
    a = r["app"]
    pages = gather(a, r["hint"], [f"{a} API authentication developer docs", f"{a} API pricing free developer account", f"{a} MCP server"])
    rec = extract(a, pages) if pages else {"confidence": 0, "self_serve": "unclear", "buildability": "blocked", "blocker": "unclear", "auth_methods": [], "existing_mcp": "unknown", "api_type": []}
    rec.update(app=a, category=r["category"], id=int(r["id"]), pages=list(pages))
    check_evidence(rec, pages)  # recorded for diagnostics only; not used to fix anything in pass 1
    return rec

def pass2(rec, r):
    a = rec["app"]; pages = {u: fetch(u) for u in rec.get("pages", [])}
    rec["log"] = []
    for attempt in range(2):
        bad = check_evidence(rec, pages)
        try: bad = sorted(set(bad + critic(rec)))
        except Exception: pass
        low = rec.get("confidence", 0) < 0.6 or rec.get("self_serve") == "unclear"
        if not bad and not low: break
        rec["log"].append({"attempt": attempt + 1, "issues": bad, "low_conf": low})
        more = gather(a, "", [f"{a} developer API get API key sign up free trial", f"{a} API OAuth app approval review requirements",
                              f"{a} official MCP server", f"site:{urllib.parse.urlparse(pages and list(pages)[0] or 'https://x.com').netloc} {a} API rate limits pricing"], have=pages)
        pages.update(more)
        rec = {**rec, **extract(a, pages, {k: rec.get(k) for k in rec if k not in ("pages", "log", "evidence_ok")}, bad or ["low confidence"])}
        rec["pages"] = list(pages)
    bad = check_evidence(rec, pages)
    rec["needs_human"] = bool(bad) or rec.get("confidence", 0) < 0.6
    rec["human_reasons"] = bad
    return rec

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("stage", choices=["pass1", "pass2"]); ap.add_argument("--app"); ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args(); apps = load_apps(a.app)
    if a.stage == "pass1":
        with ThreadPoolExecutor(a.workers) as ex: res = list(ex.map(pass1, apps))
        (ROOT / "results_pass1.json").write_text(json.dumps(sorted(res, key=lambda x: x["id"]), indent=1))
    else:
        p1 = {x["app"]: x for x in json.load(open(ROOT / "results_pass1.json"))}
        with ThreadPoolExecutor(a.workers) as ex: res = list(ex.map(lambda r: pass2(p1[r["app"]], r), apps))
        res.sort(key=lambda x: x["id"])
        (ROOT / "results_final.json").write_text(json.dumps(res, indent=1))
        (ROOT / "human_queue.json").write_text(json.dumps([{"app": x["app"], "fields": x["human_reasons"], "pages": x["pages"]} for x in res if x["needs_human"]], indent=1))
    print("done", len(res))
