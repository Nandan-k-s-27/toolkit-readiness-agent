#!/usr/bin/env python3
"""Research agent: search (Composio or DuckDuckGo) -> fetch docs -> LLM extract with quoted evidence.
pass1: single-shot extraction (baseline).  pass2: evidence-quote check + critic + targeted re-research + human queue.

Supported Providers:
  - Google Gemini (FREE tier with GEMINI_API_KEY) - default if GEMINI_API_KEY is present
  - Anthropic Claude (with ANTHROPIC_API_KEY)

Usage:
  python research.py pass1 [--app Slack] [--workers 4]
  python research.py pass2 [--app Slack]

Environment:
  GEMINI_API_KEY      Google Gemini API key (Free tier available at aistudio.google.com)
  ANTHROPIC_API_KEY   Anthropic Claude API key (optional alternative)
  LLM_PROVIDER        gemini | anthropic (auto-detected from environment keys if unset)
  MODEL               Gemini: default 'gemini-2.5-flash' | Anthropic: default 'claude-sonnet-5-5'
  SEARCH_BACKEND      direct (DuckDuckGo fallback) | composio (default: direct if COMPOSIO_API_KEY unset)
  COMPOSIO_API_KEY    required only when SEARCH_BACKEND=composio
  COMPOSIO_SEARCH_SLUG default: COMPOSIO_SEARCH_DUCK_DUCK_GO_SEARCH
  COMPOSIO_USER_ID    default: default
"""
import os, re, json, csv, sys, hashlib, argparse, pathlib, urllib.parse, threading, time
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Automatically load environment variables from .env file
load_dotenv()

ROOT = pathlib.Path(__file__).parent
CACHE = ROOT / "cache"; CACHE.mkdir(exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"}
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
    backend = os.getenv("SEARCH_BACKEND")
    if not backend:
        backend = "composio" if os.getenv("COMPOSIO_API_KEY") else "direct"

    urls = []
    if backend == "composio":
        global _composio
        try:
            from composio import Composio
            _composio = _composio or Composio()
            r = _composio.tools.execute(
                slug=os.getenv("COMPOSIO_SEARCH_SLUG", "COMPOSIO_SEARCH_DUCK_DUCK_GO_SEARCH"),
                arguments={"query": q}, user_id=os.getenv("COMPOSIO_USER_ID", "default"),
                dangerously_skip_version_check=True)
            urls = re.findall(r"https?://[^\s\"'\\<>)]+", json.dumps(r))
        except Exception as e:
            print(f"[search composio] {e}", file=sys.stderr)
    
    # Try ddgs (duckduckgo_search) first if direct or as fallback
    if not urls:
        try:
            from duckduckgo_search import DDGS
            res = list(DDGS().text(q, max_results=n))
            for r in res:
                if r.get("href"):
                    urls.append(r["href"])
        except Exception as e:
            pass

    # Direct DuckDuckGo HTML fallback
    if not urls:
        try:
            h = requests.get(
                "https://html.duckduckgo.com/html/",
                params={"q": q}, headers=UA, timeout=15).text
            for a in BeautifulSoup(h, "html.parser").select("a.result__a"):
                u = urllib.parse.parse_qs(
                    urllib.parse.urlparse(a.get("href", "")).query
                ).get("uddg", [a.get("href", "")])[0]
                urls.append(u)
        except Exception as e:
            pass

    seen, out = set(), []
    for u in urls:
        if any(b in u for b in ("duckduckgo", "composio.dev/api", "backend.composio")) or u in seen:
            continue
        seen.add(u); out.append(u)
    return out[:n]

def fetch(url, cap=9000):
    p = CACHE / (hashlib.sha1(url.encode()).hexdigest() + ".txt")
    if p.exists(): return p.read_text(encoding="utf-8", errors="ignore")
    try:
        r = requests.get(url, headers=UA, timeout=15)
        raw_html = r.text
        soup = BeautifulSoup(raw_html, "html.parser")
        
        # Check for SPA skeleton marker
        is_spa = any(s in raw_html.lower() for s in ["<div id=\"root\"></div>", "<div id=\"app\"></div>", "enable javascript to run this app"])
        
        for t in soup(["script", "style", "nav", "footer"]): t.decompose()
        txt = re.sub(r"\s+", " ", soup.get_text(" "))[:cap]
        if r.status_code >= 400: txt = ""
    except Exception:
        txt = ""
    p.write_text(txt, encoding="utf-8"); return txt

def get_candidate_doc_urls(hint):
    if not hint:
        return []
    domain = hint.replace("https://", "").replace("http://", "").split("/")[0]
    sub = domain.split(".")
    base_domain = ".".join(sub[-2:]) if len(sub) >= 2 else domain
    return [
        f"https://{hint}" if not hint.startswith("http") else hint,
        f"https://developers.{base_domain}",
        f"https://docs.{base_domain}",
        f"https://developer.{base_domain}",
        f"https://{base_domain}/docs",
        f"https://{base_domain}/api",
    ]

def gather(app, hint, queries, have=()):
    urls = []
    if hint and not have:
        for cu in get_candidate_doc_urls(hint):
            if cu not in urls: urls.append(cu)
    for q in queries:
        try: urls += search(q, 3)
        except Exception as e: print(f"[search] {app}: {e}", file=sys.stderr)
    pages = {}
    for u in urls:
        if u in have or u in pages: continue
        t = fetch(u)
        if len(t) > 300: pages[u] = t
        if len(pages) >= 6: break
    return pages

# ---------------------------------------------------------------------------
# LLM Provider Abstraction: Gemini or Anthropic
# ---------------------------------------------------------------------------
_client_lock = threading.Lock()

def get_provider():
    p = os.getenv("LLM_PROVIDER")
    if p:
        return p.lower()
    if os.getenv("GEMINI_API_KEY"):
        return "gemini"
    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    return "gemini"

def llm_json(system, user):
    provider = get_provider()

    if provider == "gemini":
        from google import genai
        from google.genai import types

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set. Add it to .env")

        # Models to try: gemini-3.5-flash-lite (fast & high quota), fallback to gemini-2.5-flash
        models_to_try = [
            os.getenv("MODEL", "gemini-3.5-flash-lite"),
            "gemini-2.5-flash",
            "gemini-3.5-flash"
        ]

        # Retry with exponential backoff for rate limits or temporary unavailability
        last_err = None
        for model_name in models_to_try:
            for attempt in range(4):
                try:
                    with _client_lock:
                        client = genai.Client(api_key=api_key)
                    config = types.GenerateContentConfig(
                        system_instruction=system,
                        response_mime_type="application/json",
                        temperature=0.2,
                    )
                    response = client.models.generate_content(
                        model=model_name,
                        contents=user,
                        config=config,
                    )
                    t = (response.text or "").strip()
                    t = re.sub(r"^```(?:json)?|```$", "", t, flags=re.M).strip()
                    return json.loads(t[t.find("{"):t.rfind("}") + 1])
                except Exception as e:
                    last_err = e
                    err_str = str(e).lower()
                    if "429" in err_str or "resource_exhausted" in err_str or "503" in err_str or "unavailable" in err_str or "client has been closed" in err_str:
                        sleep_time = (attempt + 1) * 3
                        time.sleep(sleep_time)
                        continue
                    else:
                        break  # Try next model if 404 or non-transient error
        raise RuntimeError(f"All Gemini requests failed. Last error: {last_err}")

    else:
        # Anthropic provider
        global _anthropic_client
        import anthropic

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")

        if _anthropic_client is None:
            _anthropic_client = anthropic.Anthropic(api_key=api_key)

        model_name = os.getenv("MODEL", "claude-sonnet-5-5")
        m = _anthropic_client.messages.create(
            model=model_name,
            max_tokens=2500,
            system=system,
            messages=[{"role": "user", "content": user}]
        )
        t = m.content[0].text.strip()
        t = re.sub(r"^```(?:json)?|```$", "", t, flags=re.M).strip()
        return json.loads(t[t.find("{"):t.rfind("}") + 1])

def extract(app, pages, prior=None, issues=None):
    ctx = "\n\n".join(f"URL: {u}\n{t}" for u, t in pages.items())
    extra = (f"\nPrevious answer: {json.dumps(prior)}\nProblems to fix: {json.dumps(issues)}"
             if prior else "")
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
    claims = {f: {"value": rec.get(f), "quote": (rec.get("evidence", {}).get(f) or {}).get("quote")}
              for f in EVIDENCE_FIELDS}
    out = llm_json(
        'You audit research claims. For each field decide if the quote actually supports the value. '
        'Return JSON {"unsupported": [field names]}.', json.dumps(claims))
    return [f for f in out.get("unsupported", []) if f in EVIDENCE_FIELDS]

def load_apps(only=None):
    rows = list(csv.DictReader(open(ROOT / "apps.csv")))
    return [r for r in rows if not only or r["app"].lower() == only.lower()]

def pass1(r):
    a = r["app"]
    pages = gather(a, r["hint"], [
        f"{a} API authentication developer docs",
        f"{a} API pricing free developer account",
        f"{a} MCP server"])
    rec = (extract(a, pages)
           if pages
           else {"confidence": 0, "self_serve": "unclear", "buildability": "blocked",
                 "blocker": "unclear", "auth_methods": [], "existing_mcp": "unknown",
                 "api_type": []})
    rec.update(pages=list(pages))
    check_evidence(rec, pages)
    rec.update(app=a, category=r["category"], id=int(r["id"]))
    return rec

def pass2(rec, r):
    a = rec["app"]
    pages = {u: fetch(u) for u in rec.get("pages", [])}
    rec["log"] = []
    for attempt in range(2):
        bad = check_evidence(rec, pages)
        try: bad = sorted(set(bad + critic(rec)))
        except Exception: pass
        low = rec.get("confidence", 0) < 0.6 or rec.get("self_serve") == "unclear"
        if not bad and not low: break
        rec["log"].append({"attempt": attempt + 1, "issues": bad, "low_conf": low})
        more = gather(a, "", [
            f"{a} developer API get API key sign up free trial",
            f"{a} API OAuth app approval review requirements",
            f"{a} official MCP server",
            f"site:{urllib.parse.urlparse(pages and list(pages)[0] or 'https://x.com').netloc} {a} API rate limits pricing"],
            have=pages)
        pages.update(more)
        rec = {**rec, **extract(
            a, pages,
            {k: rec.get(k) for k in rec if k not in ("pages", "log", "evidence_ok")},
            bad or ["low confidence"])}
        rec["pages"] = list(pages)
    bad = check_evidence(rec, pages)
    rec["needs_human"] = bool(bad) or rec.get("confidence", 0) < 0.6
    rec["human_reasons"] = bad
    return rec

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Toolkit readiness research agent")
    ap.add_argument("stage", choices=["pass1", "pass2"])
    ap.add_argument("--app", help="Single app name to process")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    apps = load_apps(a.app)

    provider = get_provider()
    print(f"[*] Research agent running stage '{a.stage}' using provider: {provider.upper()}")

    if a.stage == "pass1":
        # If running a single app, merge into existing results_pass1.json rather than overwriting all 100
        existing_p1 = {}
        p1_path = ROOT / "results_pass1.json"
        if p1_path.exists():
            try:
                for x in json.load(open(p1_path)):
                    existing_p1[x["app"]] = x
            except Exception:
                pass

        with ThreadPoolExecutor(a.workers) as ex:
            new_res = list(ex.map(pass1, apps))

        for item in new_res:
            existing_p1[item["app"]] = item

        final_p1_list = sorted(existing_p1.values(), key=lambda x: x.get("id", 0))
        p1_path.write_text(json.dumps(final_p1_list, indent=1))
        print(f"[pass1] done — processed {len(new_res)} app(s), total in results_pass1.json: {len(final_p1_list)}")
    else:
        p1_path = ROOT / "results_pass1.json"
        if not p1_path.exists():
            sys.exit("Error: results_pass1.json not found. Run 'python research.py pass1' first.")

        p1 = {x["app"]: x for x in json.load(open(p1_path))}

        # Filter apps to only those that exist in pass1
        apps_to_run = [r for r in apps if r["app"] in p1]
        if not apps_to_run:
            sys.exit(f"Error: None of the target app(s) exist in results_pass1.json. Run pass1 for them first.")

        # If previous results_final.json exists, merge into it
        existing_final = {}
        final_path = ROOT / "results_final.json"
        if final_path.exists():
            try:
                for x in json.load(open(final_path)):
                    existing_final[x["app"]] = x
            except Exception:
                pass

        with ThreadPoolExecutor(a.workers) as ex:
            new_res = list(ex.map(lambda r: pass2(p1[r["app"]], r), apps_to_run))

        for item in new_res:
            existing_final[item["app"]] = item

        final_res_list = sorted(existing_final.values(), key=lambda x: x.get("id", 0))
        final_path.write_text(json.dumps(final_res_list, indent=1))

        hq_list = [
            {"app": x["app"], "fields": x.get("human_reasons", []), "pages": x.get("pages", [])}
            for x in final_res_list if x.get("needs_human")
        ]
        (ROOT / "human_queue.json").write_text(json.dumps(hq_list, indent=1))
        print(f"[pass2] done — processed {len(new_res)} app(s), total in results_final.json: {len(final_res_list)} | human queue: {len(hq_list)} apps")
