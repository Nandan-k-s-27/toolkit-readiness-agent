#!/usr/bin/env python3
"""
generate_demo_data.py
Generates realistic demo results_pass1.json, results_final.json,
human_queue.json without hitting any external API.
Run: python generate_demo_data.py
"""
import json, csv, random, pathlib

ROOT = pathlib.Path(__file__).parent
random.seed(42)

APPS = list(csv.DictReader(open(ROOT / "apps.csv")))

# Realistic per-category templates
CATEGORY_PROFILES = {
    "CRM and Sales": {
        "auth_methods": [["oauth2", "api_key"], ["api_key"], ["oauth2"]],
        "self_serve": ["self_serve_free", "self_serve_trial", "paid_plan_required", "approval_required"],
        "api_type": [["rest"], ["rest", "graphql"], ["rest", "websocket"]],
        "api_breadth": ["broad", "medium", "broad"],
        "existing_mcp": ["official", "community", "none_found", "community"],
        "buildability": ["yes", "yes", "yes_with_caveats", "yes_with_caveats"],
        "blocker": ["none", "none", "rate_or_cost", "approval_gate"],
    },
    "Support and Helpdesk": {
        "auth_methods": [["api_key", "oauth2"], ["api_key"], ["bearer_token"]],
        "self_serve": ["self_serve_trial", "self_serve_free", "paid_plan_required", "paid_plan_required"],
        "api_type": [["rest"], ["rest", "websocket"]],
        "api_breadth": ["medium", "broad"],
        "existing_mcp": ["community", "none_found", "official"],
        "buildability": ["yes", "yes_with_caveats", "yes"],
        "blocker": ["none", "rate_or_cost", "none"],
    },
    "Communications and Messaging": {
        "auth_methods": [["oauth2", "bearer_token"], ["api_key", "oauth2"], ["request_signing"]],
        "self_serve": ["self_serve_free", "self_serve_free", "self_serve_trial", "approval_required"],
        "api_type": [["rest", "websocket"], ["rest"], ["sdk_only"]],
        "api_breadth": ["broad", "medium"],
        "existing_mcp": ["official", "official", "community", "none_found"],
        "buildability": ["yes", "yes", "yes_with_caveats"],
        "blocker": ["none", "none", "approval_gate"],
    },
    "Marketing, Ads, Email and Social": {
        "auth_methods": [["oauth2"], ["api_key", "oauth2"], ["oauth2", "jwt"]],
        "self_serve": ["approval_required", "self_serve_free", "self_serve_trial", "partner_gated"],
        "api_type": [["rest"], ["rest", "graphql"]],
        "api_breadth": ["medium", "broad", "narrow"],
        "existing_mcp": ["community", "none_found", "official"],
        "buildability": ["yes_with_caveats", "yes", "blocked"],
        "blocker": ["approval_gate", "none", "partner_gate"],
    },
    "Ecommerce": {
        "auth_methods": [["api_key", "oauth2"], ["api_key"], ["oauth2"]],
        "self_serve": ["self_serve_free", "self_serve_trial", "paid_plan_required"],
        "api_type": [["rest", "graphql"], ["rest"], ["rest", "websocket"]],
        "api_breadth": ["broad", "medium"],
        "existing_mcp": ["official", "community", "none_found"],
        "buildability": ["yes", "yes", "yes_with_caveats"],
        "blocker": ["none", "none", "rate_or_cost"],
    },
    "Data, SEO and Scraping": {
        "auth_methods": [["api_key"], ["basic", "api_key"]],
        "self_serve": ["paid_plan_required", "self_serve_trial", "self_serve_free"],
        "api_type": [["rest"], ["sdk_only"], ["rest", "sdk_only"]],
        "api_breadth": ["medium", "narrow"],
        "existing_mcp": ["community", "none_found", "official"],
        "buildability": ["yes_with_caveats", "yes", "yes_with_caveats"],
        "blocker": ["paid_gate", "none", "rate_or_cost"],
    },
    "Developer, Infra and Data platforms": {
        "auth_methods": [["api_key", "bearer_token"], ["oauth2", "api_key"]],
        "self_serve": ["self_serve_free", "self_serve_free", "self_serve_trial"],
        "api_type": [["rest"], ["rest", "graphql", "websocket"]],
        "api_breadth": ["broad", "medium"],
        "existing_mcp": ["official", "official", "community"],
        "buildability": ["yes", "yes", "yes_with_caveats"],
        "blocker": ["none", "none", "rate_or_cost"],
    },
    "Productivity and Project Management": {
        "auth_methods": [["oauth2", "api_key"], ["api_key"], ["oauth2"]],
        "self_serve": ["self_serve_free", "self_serve_trial", "paid_plan_required"],
        "api_type": [["rest"], ["rest", "graphql"]],
        "api_breadth": ["broad", "medium"],
        "existing_mcp": ["official", "community", "none_found"],
        "buildability": ["yes", "yes", "yes_with_caveats"],
        "blocker": ["none", "none", "rate_or_cost"],
    },
    "Finance and Fintech": {
        "auth_methods": [["oauth2", "api_key"], ["api_key", "jwt"], ["request_signing"]],
        "self_serve": ["paid_plan_required", "approval_required", "partner_gated", "self_serve_trial"],
        "api_type": [["rest"], ["rest", "websocket"]],
        "api_breadth": ["medium", "broad", "narrow"],
        "existing_mcp": ["none_found", "community", "official"],
        "buildability": ["yes_with_caveats", "blocked", "yes"],
        "blocker": ["paid_gate", "approval_gate", "none", "partner_gate"],
    },
    "AI, Research and Media-native": {
        "auth_methods": [["api_key"], ["bearer_token", "api_key"], ["oauth2"]],
        "self_serve": ["self_serve_trial", "self_serve_free", "no_public_api", "unclear"],
        "api_type": [["rest", "sdk_only"], ["rest"], ["cli_only"]],
        "api_breadth": ["narrow", "medium"],
        "existing_mcp": ["none_found", "community", "none_found"],
        "buildability": ["yes_with_caveats", "yes", "blocked"],
        "blocker": ["unclear", "none", "no_public_api"],
    },
}

BLOCKER_NOTES = {
    "none": "",
    "paid_gate": "API requires paid tier; free plan has no API access.",
    "approval_gate": "App must be approved before getting production credentials.",
    "partner_gate": "Contact sales required; no self-serve onboarding for API.",
    "no_public_api": "No documented public API; only UI/scraping possible.",
    "rate_or_cost": "API available but heavy usage costs or tight rate limits.",
    "per_tenant_setup": "Each customer must separately authorize; per-tenant setup.",
    "unclear": "API access policy unclear from public documentation.",
    "cli_or_local_only": "Only local CLI tool; no cloud API surface.",
}

ONE_LINERS = {
    "CRM and Sales": "Manages customer relationships, sales pipelines, and deal tracking.",
    "Support and Helpdesk": "Handles customer support tickets, live chat, and agent workflows.",
    "Communications and Messaging": "Provides messaging, voice, and team communication APIs.",
    "Marketing, Ads, Email and Social": "Runs marketing campaigns, email, ads, and social media automation.",
    "Ecommerce": "Powers online stores, product catalogs, orders, and payments.",
    "Data, SEO and Scraping": "Provides data enrichment, SEO analytics, and web scraping APIs.",
    "Developer, Infra and Data platforms": "Hosts infrastructure, databases, and developer tooling.",
    "Productivity and Project Management": "Manages tasks, projects, documents, and team workflows.",
    "Finance and Fintech": "Handles payments, banking data, invoicing, and financial reporting.",
    "AI, Research and Media-native": "AI-native tool for research, media, and content generation.",
}

MCP_URLS = {
    "official": "https://github.com/{slug}/mcp-server",
    "community": "https://github.com/community/{slug}-mcp",
    "none_found": "",
    "unknown": "",
}

def pick(lst): return random.choice(lst)

def make_record(row, hint_url, is_pass2=False):
    app = row["app"]
    cat = row["category"]
    prof = CATEGORY_PROFILES.get(cat, CATEGORY_PROFILES["CRM and Sales"])
    slug = app.lower().replace(" ", "-").replace("(", "").replace(")", "")
    
    auth = pick(prof["auth_methods"])
    self_serve = pick(prof["self_serve"])
    api_type = pick(prof["api_type"])
    api_breadth = pick(prof["api_breadth"])
    existing_mcp = pick(prof["existing_mcp"])
    buildability = pick(prof["buildability"])
    blocker = pick(prof["blocker"])
    
    # Ensure consistency
    if buildability == "blocked" and blocker == "none":
        blocker = "no_public_api"
    if buildability == "yes" and blocker not in ("none",):
        blocker = "none"
    if self_serve == "no_public_api":
        buildability = "blocked"
        blocker = "no_public_api"
    
    conf = round(random.uniform(0.65, 0.95), 2)
    if buildability == "blocked": conf = round(random.uniform(0.55, 0.80), 2)
    if is_pass2 and conf < 0.75: conf = round(min(conf + 0.12, 0.92), 2)
    
    mcp_url = MCP_URLS[existing_mcp].format(slug=slug) if existing_mcp in ("official","community") else ""
    
    # Realistic evidence snippets
    evidence_snippets = {
        "auth_methods": f"{app} supports {' and '.join(auth)} authentication. See developer.{slug}.com/auth.",
        "self_serve": f"Sign up for a {app} developer account to get {'free ' if 'free' in self_serve else ''}API credentials instantly.",
        "api_type": f"The {app} {', '.join(api_type).upper()} API lets you programmatically access all platform features.",
        "existing_mcp": (f"Official {app} MCP server available at {mcp_url}" if existing_mcp == "official"
                         else f"Community MCP server for {app} available on GitHub." if existing_mcp == "community"
                         else f"No MCP server found for {app} in official or community registries."),
        "buildability": (f"{app} provides {'comprehensive' if buildability=='yes' else 'limited'} API coverage for agent integration.",),
    }
    
    ev_ok = {f: (is_pass2 and conf > 0.7) for f in ["auth_methods","self_serve","api_type","existing_mcp","buildability"]}
    needs_human = not all(ev_ok.values()) or conf < 0.65
    
    rec = {
        "id": int(row["id"]),
        "app": app,
        "category": cat,
        "one_liner": ONE_LINERS.get(cat, f"{app} provides APIs for integration."),
        "auth_methods": auth,
        "self_serve": self_serve,
        "api_type": api_type,
        "api_breadth": api_breadth,
        "existing_mcp": existing_mcp,
        "mcp_url": mcp_url,
        "buildability": buildability,
        "blocker": blocker,
        "blocker_note": BLOCKER_NOTES.get(blocker, ""),
        "confidence": conf,
        "evidence": {
            "auth_methods": {"url": hint_url, "quote": evidence_snippets["auth_methods"][:200]},
            "self_serve": {"url": hint_url, "quote": evidence_snippets["self_serve"][:200]},
            "api_type": {"url": hint_url, "quote": evidence_snippets["api_type"][:200]},
            "existing_mcp": {"url": hint_url, "quote": str(evidence_snippets["existing_mcp"])[:200]},
            "buildability": {"url": hint_url, "quote": str(evidence_snippets["buildability"])[:200]},
        },
        "evidence_ok": ev_ok,
        "pages": [hint_url],
        "needs_human": needs_human,
        "human_reasons": [] if not needs_human else ["auth_methods", "self_serve"],
        "log": ([{"attempt": 1, "issues": ["self_serve"], "low_conf": conf < 0.7}]
                if is_pass2 else []),
    }
    return rec

def build_hint_url(row):
    h = row.get("hint", "")
    return h if h.startswith("http") else f"https://{h}" if h else f"https://{row['app'].lower().replace(' ', '')}.com"

results_pass1 = []
results_final = []
human_queue = []

for row in APPS:
    url = build_hint_url(row)
    p1 = make_record(row, url, is_pass2=False)
    p2 = make_record(row, url, is_pass2=True)
    # pass2 may refine values slightly
    p2["id"] = p1["id"]
    results_pass1.append(p1)
    results_final.append(p2)
    if p2["needs_human"]:
        human_queue.append({"app": p2["app"], "fields": p2["human_reasons"], "pages": p2["pages"]})

results_pass1.sort(key=lambda x: x["id"])
results_final.sort(key=lambda x: x["id"])

(ROOT / "results_pass1.json").write_text(json.dumps(results_pass1, indent=1))
(ROOT / "results_final.json").write_text(json.dumps(results_final, indent=1))
(ROOT / "human_queue.json").write_text(json.dumps(human_queue, indent=1))

print(f"Generated {len(results_pass1)} pass1 records")
print(f"Generated {len(results_final)} final records")
print(f"Human queue: {len(human_queue)} apps")
print("Files: results_pass1.json, results_final.json, human_queue.json")
