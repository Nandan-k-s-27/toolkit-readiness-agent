#!/usr/bin/env python3
"""
Builds index.html — high-standard, developer-grade SaaS platform inspired by nandanks.me.
Zero emojis, crisp inline SVG icons, status micro-indicators, interactive category tabs,
multi-column sorting, CSV/JSON export, evidence modal with copy-to-clipboard, and SSR HTML table.
"""
import json, pathlib, os, html
from dotenv import load_dotenv

load_dotenv()
ROOT = pathlib.Path(__file__).parent
ld = lambda n, d=None: json.load(open(ROOT / n, encoding="utf-8")) if (ROOT / n).exists() else d

DATA = {
    "results": ld("results_final.json", []),
    "patterns": ld("patterns.json", {}),
    "accuracy": ld("accuracy.json", {}),
    "human_queue": ld("human_queue.json", []),
    "repo": os.getenv("REPO_URL", "https://github.com/Nandan-k-s-27/toolkit-readiness-agent"),
    "notes": ld("human_notes.json", [])
}
blob = json.dumps(DATA).replace("</", "<\\/")

def get_badge_build(val):
    if val == "yes":
        return '<span class="badge badge-yes"><span class="dot dot-green"></span>Yes</span>'
    elif val == "yes_with_caveats":
        return '<span class="badge badge-warn"><span class="dot dot-amber"></span>Caveats</span>'
    elif val == "blocked":
        return '<span class="badge badge-bad"><span class="dot dot-red"></span>Blocked</span>'
    return f'<span class="badge badge-neutral">{html.escape(val or "—")}</span>'

def get_badge_self_serve(val):
    v = (val or "").strip()
    if v == "self_serve_free":
        return '<span class="badge badge-yes"><span class="dot dot-green"></span>Free Tier</span>'
    elif v == "self_serve_trial":
        return '<span class="badge badge-blue"><span class="dot dot-blue"></span>Free Trial</span>'
    elif v == "paid_plan_required":
        return '<span class="badge badge-warn"><span class="dot dot-amber"></span>Paid Plan</span>'
    elif v == "approval_required":
        return '<span class="badge badge-warn"><span class="dot dot-amber"></span>Approval Gate</span>'
    elif v == "partner_gated":
        return '<span class="badge badge-bad"><span class="dot dot-red"></span>Partner Gated</span>'
    elif v == "no_public_api":
        return '<span class="badge badge-bad"><span class="dot dot-red"></span>No Public API</span>'
    return '<span class="badge badge-neutral">Unclear</span>'

def get_badge_mcp(val):
    v = (val or "").strip()
    if v == "official":
        return '<span class="badge badge-purple"><span class="dot dot-purple"></span>Official</span>'
    elif v == "community":
        return '<span class="badge badge-blue"><span class="dot dot-blue"></span>Community</span>'
    return '<span class="badge badge-neutral">None</span>'

def render_ssr_rows(apps):
    rows = []
    for r in apps:
        aid = r.get("id", 0)
        app_name = html.escape(r.get("app", ""))
        cat = html.escape(r.get("category", ""))
        auth_html = "".join([f'<span class="badge badge-subtle">{html.escape(m)}</span>' for m in (r.get("auth_methods") or [])[:2]])
        ss_html = get_badge_self_serve(r.get("self_serve", ""))
        mcp_html = get_badge_mcp(r.get("existing_mcp", ""))
        build_html = get_badge_build(r.get("buildability", ""))
        blocker = r.get("blocker", "none")
        blocker_html = '—' if blocker == "none" or not blocker else f'<span class="badge badge-bad-subtle">{html.escape(blocker.replace("_", " "))}</span>'
        conf = round((r.get("confidence") or 0) * 100)
        conf_color = "var(--ok)" if conf >= 80 else "var(--warn)" if conf >= 65 else "var(--bad)"
        
        row_str = f"""<tr onclick="openEvidenceModal({aid})">
  <td style="color:var(--text-dim);font-weight:600;font-family:'JetBrains Mono',monospace;font-size:12px;">#{aid}</td>
  <td>
    <div style="font-weight:700;color:var(--text);font-size:13.5px;">{app_name}</div>
    <div style="font-size:11.5px;color:var(--text-dim);line-height:1.3;max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{html.escape(r.get("one_liner") or "")}</div>
  </td>
  <td style="color:var(--text-muted);font-size:12.5px;">{cat}</td>
  <td>{auth_html}</td>
  <td>{ss_html}</td>
  <td>{mcp_html}</td>
  <td>{build_html}</td>
  <td style="font-size:12px;color:var(--text-muted);">{blocker_html}</td>
  <td><span style="font-weight:700;font-family:'JetBrains Mono',monospace;font-size:12px;color:{conf_color};">{conf}%</span></td>
  <td><button class="btn btn-xs" onclick="openEvidenceModal({aid}); event.stopPropagation();">Inspect</button></td>
</tr>"""
        rows.append(row_str)
    return "\n".join(rows)

STATIC_ROWS_HTML = render_ssr_rows(DATA["results"])

HTML = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ToolkitHub · 100-App Agent Readiness Platform</title>
  <meta name="description" content="AI Agent Toolkit Readiness Explorer: Automated two-pass research agent scoring 100 SaaS applications for MCP availability, authentication, and buildability.">
  <link rel="alternate" type="text/plain" href="llms.txt" title="LLMs.txt Agent Index">
  <link rel="alternate" type="application/json" href="results_final.json" title="Final Dataset JSON">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='%233b82f6'/%3E%3Cstop offset='100%25' stop-color='%238b5cf6'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='8' fill='%23090d16'/%3E%3Cpath d='M8 16h6l-2 8 12-12h-6l2-8z' fill='url(%23g)'/%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
  
  <style>
    :root {{
      --bg: #090d16;
      --surface: #0f1422;
      --surface-card: #141b2d;
      --surface-hover: #192338;
      --border: rgba(255, 255, 255, 0.08);
      --border-subtle: rgba(255, 255, 255, 0.04);
      --border-focus: #3b82f6;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --accent: #3b82f6;
      --accent-light: #60a5fa;
      --accent-glow: rgba(59, 130, 246, 0.15);
      --ok: #10b981;
      --ok-bg: rgba(16, 185, 129, 0.12);
      --warn: #f59e0b;
      --warn-bg: rgba(245, 158, 11, 0.12);
      --bad: #ef4444;
      --bad-bg: rgba(239, 68, 68, 0.12);
      --purple: #8b5cf6;
      --purple-bg: rgba(139, 92, 246, 0.12);
      --blue: #3b82f6;
      --blue-bg: rgba(59, 130, 246, 0.12);
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
      --shadow-lg: 0 12px 36px rgba(0, 0, 0, 0.5);
    }}
    [data-theme="light"] {{
      --bg: #f8fafc;
      --surface: #ffffff;
      --surface-card: #f1f5f9;
      --surface-hover: #e2e8f0;
      --border: rgba(0, 0, 0, 0.08);
      --border-subtle: rgba(0, 0, 0, 0.04);
      --border-focus: #3b82f6;
      --text: #0f172a;
      --text-muted: #64748b;
      --text-dim: #94a3b8;
      --shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
      --shadow-lg: 0 12px 36px rgba(0, 0, 0, 0.1);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 14px;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      min-height: 100vh;
    }}
    a {{ color: inherit; text-decoration: none; }}
    button, input, select {{ font-family: inherit; }}

    /* Layout */
    .container {{ max-width: 1280px; margin: 0 auto; padding: 0 24px; }}
    
    /* Header */
    header {{
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(9, 13, 22, 0.85);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
    }}
    [data-theme="light"] header {{ background: rgba(255, 255, 255, 0.88); }}
    .header-inner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 64px;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 700;
      font-size: 15px;
      letter-spacing: -0.02em;
    }}
    .brand-icon {{
      width: 28px;
      height: 28px;
      background: linear-gradient(135deg, var(--blue), var(--purple));
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
    }}
    .brand-badge {{
      font-size: 11px;
      font-weight: 600;
      padding: 2px 7px;
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      color: var(--text-muted);
    }}
    .nav-links {{
      display: flex;
      gap: 22px;
      align-items: center;
      font-size: 13px;
      font-weight: 500;
      color: var(--text-muted);
    }}
    .nav-links a:hover {{ color: var(--text); }}
    .header-actions {{ display: flex; align-items: center; gap: 10px; }}

    /* Buttons */
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 7px 14px;
      font-size: 12.5px;
      font-weight: 600;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text);
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .btn:hover {{
      background: var(--surface-hover);
      border-color: rgba(255, 255, 255, 0.16);
    }}
    [data-theme="light"] .btn:hover {{ border-color: rgba(0, 0, 0, 0.16); }}
    .btn-primary {{
      background: var(--accent);
      border-color: var(--accent);
      color: #fff;
    }}
    .btn-primary:hover {{ background: #2563eb; border-color: #2563eb; }}
    .btn-xs {{
      padding: 3px 9px;
      font-size: 11px;
      border-radius: 4px;
    }}

    /* Hero Section */
    .hero {{
      padding: 56px 0 36px;
      border-bottom: 1px solid var(--border);
    }}
    .tagline-pill {{
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 4px 12px;
      border-radius: 20px;
      background: var(--blue-bg);
      border: 1px solid rgba(59, 130, 246, 0.25);
      color: var(--blue);
      margin-bottom: 16px;
    }}
    .hero-title {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 38px;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.15;
      margin-bottom: 14px;
    }}
    .grad-text {{
      background: linear-gradient(135deg, var(--accent) 0%, var(--purple) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .hero-desc {{
      color: var(--text-muted);
      font-size: 15px;
      line-height: 1.6;
      max-width: 820px;
      margin-bottom: 32px;
    }}

    /* Metric Grid */
    .metric-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 12px;
      margin-bottom: 24px;
    }}
    @media (max-width: 900px) {{ .metric-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (max-width: 500px) {{ .metric-grid {{ grid-template-columns: 1fr; }} }}
    .metric-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 16px 18px;
      cursor: pointer;
      transition: all 0.15s ease;
      position: relative;
    }}
    .metric-card:hover {{
      background: var(--surface-hover);
      border-color: rgba(255, 255, 255, 0.18);
      transform: translateY(-1px);
    }}
    .metric-card.active {{
      border-color: var(--accent);
      background: var(--surface-card);
      box-shadow: 0 0 0 1px var(--accent);
    }}
    .metric-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}
    .metric-icon-wrap {{
      width: 32px;
      height: 32px;
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--surface-card);
      color: var(--text-muted);
    }}
    .metric-val {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 26px;
      font-weight: 700;
      letter-spacing: -0.02em;
      line-height: 1.2;
    }}
    .metric-lbl {{
      font-size: 13px;
      font-weight: 600;
      color: var(--text);
      margin-top: 4px;
    }}
    .metric-sub {{
      font-size: 11.5px;
      color: var(--text-dim);
      margin-top: 2px;
    }}

    /* Accuracy Callout Banner */
    .accuracy-callout {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 3px solid var(--accent);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }}

    /* Sections */
    .section-wrap {{ padding: 48px 0; border-bottom: 1px solid var(--border); }}
    .section-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 24px;
    }}
    .section-title-wrap {{ display: flex; align-items: center; gap: 10px; }}
    .section-num {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      color: var(--accent);
      background: var(--blue-bg);
      border: 1px solid rgba(59, 130, 246, 0.25);
      border-radius: 4px;
      padding: 2px 7px;
    }}
    .section-title {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 20px;
      font-weight: 700;
      letter-spacing: -0.02em;
    }}

    /* Card Grids */
    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }}
    @media (max-width: 900px) {{ .grid-3 {{ grid-template-columns: 1fr; }} }}
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 20px;
    }}
    .card-title {{
      font-size: 14px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 4px;
    }}
    .card-subtitle {{
      font-size: 12px;
      color: var(--text-dim);
      margin-bottom: 16px;
    }}

    /* Bars */
    .bar-row {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
      font-size: 12.5px;
    }}
    .bar-name {{ width: 110px; color: var(--text-muted); font-size: 12px; }}
    .bar-track {{ flex: 1; height: 6px; background: var(--surface-card); border-radius: 3px; overflow: hidden; }}
    .bar-fill {{ height: 100%; border-radius: 3px; background: var(--accent); }}
    .bar-count {{ width: 36px; text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 11.5px; color: var(--text-dim); }}

    /* Category Tab Bar */
    .category-tabs {{
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 12px;
      margin-bottom: 16px;
      scrollbar-width: thin;
    }}
    .tab-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      font-size: 12.5px;
      font-weight: 600;
      border-radius: 20px;
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--text-muted);
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s ease;
    }}
    .tab-pill:hover {{
      background: var(--surface-hover);
      color: var(--text);
    }}
    .tab-pill.active {{
      background: var(--accent);
      border-color: var(--accent);
      color: #fff;
    }}
    .tab-pill .tab-count {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      padding: 1px 6px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.15);
    }}

    /* Filter Toolbar */
    .toolbar {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
      margin-bottom: 16px;
    }}
    .search-box {{
      position: relative;
      flex: 1;
      min-width: 220px;
    }}
    .search-icon {{
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      pointer-events: none;
    }}
    .search-input {{
      width: 100%;
      padding: 8px 36px 8px 36px;
      font-size: 13px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text);
      outline: none;
      transition: border-color 0.15s ease;
    }}
    .search-input:focus {{ border-color: var(--border-focus); }}
    .search-kbd {{
      position: absolute;
      right: 10px;
      top: 50%;
      transform: translateY(-50%);
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      padding: 2px 5px;
      border: 1px solid var(--border);
      border-radius: 3px;
      color: var(--text-dim);
      background: var(--surface-card);
    }}
    .filter-select {{
      padding: 8px 12px;
      font-size: 12.5px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text);
      outline: none;
      cursor: pointer;
    }}

    /* Table */
    .table-viewport {{
      overflow-x: auto;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      background: var(--surface);
    }}
    .data-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }}
    .data-table th {{
      padding: 12px 14px;
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      background: var(--surface-card);
      border-bottom: 1px solid var(--border);
      cursor: pointer;
      user-select: none;
      white-space: nowrap;
    }}
    .data-table th:hover {{ color: var(--text); }}
    .data-table td {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--border-subtle);
      font-size: 13px;
      vertical-align: middle;
    }}
    .data-table tbody tr {{ cursor: pointer; transition: background 0.1s ease; }}
    .data-table tbody tr:hover {{ background: var(--surface-hover); }}

    /* Status Indicator Dots & Badges */
    .dot {{
      display: inline-block;
      width: 6px;
      height: 6px;
      border-radius: 50%;
      margin-right: 6px;
      vertical-align: middle;
    }}
    .dot-green {{ background: var(--ok); box-shadow: 0 0 6px var(--ok); }}
    .dot-amber {{ background: var(--warn); box-shadow: 0 0 6px var(--warn); }}
    .dot-red {{ background: var(--bad); box-shadow: 0 0 6px var(--bad); }}
    .dot-blue {{ background: var(--blue); box-shadow: 0 0 6px var(--blue); }}
    .dot-purple {{ background: var(--purple); box-shadow: 0 0 6px var(--purple); }}

    .badge {{
      display: inline-flex;
      align-items: center;
      padding: 3px 8px;
      border-radius: var(--radius-sm);
      font-size: 11.5px;
      font-weight: 600;
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: -0.01em;
      white-space: nowrap;
    }}
    .badge-yes {{ background: var(--ok-bg); color: var(--ok); border: 1px solid rgba(16, 185, 129, 0.25); }}
    .badge-warn {{ background: var(--warn-bg); color: var(--warn); border: 1px solid rgba(245, 158, 11, 0.25); }}
    .badge-bad {{ background: var(--bad-bg); color: var(--bad); border: 1px solid rgba(239, 68, 68, 0.25); }}
    .badge-purple {{ background: var(--purple-bg); color: var(--purple); border: 1px solid rgba(139, 92, 246, 0.25); }}
    .badge-blue {{ background: var(--blue-bg); color: var(--blue); border: 1px solid rgba(59, 130, 246, 0.25); }}
    .badge-neutral {{ background: var(--surface-card); color: var(--text-dim); border: 1px solid var(--border); }}
    .badge-subtle {{ background: var(--surface-card); color: var(--text-muted); border: 1px solid var(--border-subtle); margin-right: 4px; }}
    .badge-bad-subtle {{ background: var(--bad-bg); color: var(--bad); border: 1px solid rgba(239, 68, 68, 0.2); }}

    /* Flow Steps */
    .flow-grid {{
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 10px;
      margin-top: 20px;
    }}
    @media (max-width: 1000px) {{ .flow-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    .flow-step {{
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 12px 14px;
    }}
    .flow-step-num {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 10.5px;
      font-weight: 700;
      color: var(--accent);
      margin-bottom: 4px;
    }}
    .flow-step-title {{
      font-size: 12.5px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 2px;
    }}
    .flow-step-desc {{
      font-size: 11px;
      color: var(--text-dim);
      line-height: 1.35;
    }}

    /* Modal */
    .modal-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(8px);
      z-index: 100;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}
    .modal-box {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      max-width: 760px;
      width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      box-shadow: var(--shadow-lg);
      padding: 24px 28px;
      position: relative;
    }}
    .modal-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 20px;
    }}
    .modal-close {{
      background: transparent;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text-muted);
      cursor: pointer;
    }}
    .modal-close:hover {{ background: var(--surface-hover); color: var(--text); }}
    .evidence-block {{
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 14px 16px;
      margin-bottom: 12px;
    }}
    .evidence-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
      font-size: 12px;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .evidence-quote {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      color: var(--text);
      line-height: 1.5;
      background: var(--surface);
      border-left: 2px solid var(--accent);
      padding: 8px 12px;
      border-radius: 0 4px 4px 0;
      margin-top: 6px;
      word-break: break-word;
    }}
    .evidence-url {{
      font-size: 11.5px;
      color: var(--text-dim);
      margin-top: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .evidence-url a {{ color: var(--accent); text-decoration: underline; }}

    /* Footer */
    footer {{
      padding: 40px 0;
      border-top: 1px solid var(--border);
      font-size: 12.5px;
      color: var(--text-dim);
    }}
    .footer-inner {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
  </style>
</head>
<body>

<header>
  <div class="container header-inner">
    <a href="#" class="brand">
      <div class="brand-icon">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>
      </div>
      <span>ToolkitHub</span>
      <span class="brand-badge">Agent Readiness</span>
    </a>
    <nav class="nav-links">
      <a href="#overview">Overview</a>
      <a href="#patterns">Patterns</a>
      <a href="#explorer">Explorer (100)</a>
      <a href="#architecture">Architecture</a>
      <a href="#verification">Benchmark</a>
      <a href="llms.txt" target="_blank">llms.txt</a>
      <a href="results_final.json" target="_blank">Data JSON</a>
    </nav>
    <div class="header-actions">
      <button class="btn btn-xs" id="themeSwitcher" title="Toggle theme">
        <span id="themeIcon">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
        </span>
      </button>
      <a class="btn btn-xs" href="https://github.com/Nandan-k-s-27/toolkit-readiness-agent/actions" target="_blank" rel="noopener">
        <span>Run Single App</span>
      </a>
      <a class="btn btn-xs btn-primary" id="repoButton" href="https://github.com/Nandan-k-s-27/toolkit-readiness-agent" target="_blank" rel="noopener">
        <span>GitHub Repo</span>
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
      </a>
    </div>
  </div>
</header>

<main>
  <!-- Hero Section -->
  <section class="hero" id="overview">
    <div class="container">
      <div class="tagline-pill">Evidence-Grounded Research Pipeline</div>
      <h1 class="hero-title">Which of 100 Apps Can Become <span class="grad-text">AI Agent Toolkits</span> Today?</h1>
      <p class="hero-desc">
        A systematic audit across 10 software categories evaluating API surface, authentication gates, Model Context Protocol (MCP) servers, and developer self-serve accessibility. Backed by extracted quotes string-matched against live developer documentation (73% verified in Pass 2). Evaluated across 30 hand-labeled ground-truth applications with honest failure reporting.
      </p>

      <!-- Plain-Text Patterns Summary -->
      <div style="font-family:'JetBrains Mono',monospace;font-size:12.5px;color:var(--text);background:var(--surface);border:1px solid var(--border);border-left:3px solid var(--ok);padding:10px 16px;border-radius:var(--radius-sm);margin-bottom:24px;line-height:1.5;">
        <strong>Patterns Summary:</strong> OAuth2 dominates at 60/100 apps; 85% self-serve accessible; 12% gated by payment, approval or sales outreach; 62% have existing MCP servers (52 official); top blocker is unclear or custom enterprise pricing.
      </div>

      <!-- Metric Grid -->
      <div class="metric-grid">
        <div class="metric-card active" onclick="filterByQuickStat('all')">
          <div class="metric-top">
            <span class="metric-lbl">Apps Audited</span>
            <div class="metric-icon-wrap">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
            </div>
          </div>
          <div class="metric-val" id="valTotal">100</div>
          <div class="metric-sub">Across 10 categories</div>
        </div>

        <div class="metric-card" onclick="filterByQuickStat('easy_wins')">
          <div class="metric-top">
            <span class="metric-lbl">Easy Wins</span>
            <div class="metric-icon-wrap" style="color:var(--ok);">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            </div>
          </div>
          <div class="metric-val" id="valEasy" style="color:var(--ok);">76</div>
          <div class="metric-sub">Self-serve and buildable now</div>
        </div>

        <div class="metric-card" onclick="filterByQuickStat('mcp')">
          <div class="metric-top">
            <span class="metric-lbl">MCP Servers</span>
            <div class="metric-icon-wrap" style="color:var(--purple);">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>
            </div>
          </div>
          <div class="metric-val" id="valMcp" style="color:var(--purple);">62</div>
          <div class="metric-sub">Official and community</div>
        </div>

        <div class="metric-card" onclick="filterByQuickStat('self_serve')">
          <div class="metric-top">
            <span class="metric-lbl">Self-Serve Rate</span>
            <div class="metric-icon-wrap" style="color:var(--blue);">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6"/><path d="m15.5 7.5 3 3L22 7l-3-3"/></svg>
            </div>
          </div>
          <div class="metric-val" id="valSelfServe" style="color:var(--blue);">85%</div>
          <div class="metric-sub">Instant developer access</div>
        </div>

        <div class="metric-card" onclick="filterByQuickStat('blocked')">
          <div class="metric-top">
            <span class="metric-lbl">Blocked Today</span>
            <div class="metric-icon-wrap" style="color:var(--bad);">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></svg>
            </div>
          </div>
          <div class="metric-val" id="valBlocked" style="color:var(--bad);">4</div>
          <div class="metric-sub">Sales walls or no public API</div>
        </div>
      </div>

      <!-- Accuracy Callout Banner -->
      <div class="accuracy-callout">
        <div>
          <div style="font-size:13.5px;font-weight:700;color:var(--text);margin-bottom:3px;">
            Ground-Truth Evaluation: Pass 1: 49.2% → Final: 44.2% on 30 Hand-Checked Applications
          </div>
          <div style="font-size:12.5px;color:var(--text-muted);line-height:1.5;">
            Buildability Accuracy: <strong>70.0%</strong> · Access Model: <strong>60.0%</strong> · Verbatim Quote Match: <strong>73.0%</strong>.<br>
            Honest Misses (Defeated the Agent): <em>Paygent Connect, Waterfall.io, Plaid, Ahrefs, Otter AI</em>.
          </div>
          <div style="margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--text-dim);display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
            <span>Run Single App:</span>
            <code style="background:var(--surface-card);border:1px solid var(--border);padding:2px 7px;border-radius:3px;color:var(--accent);">python research.py pass1 --app Slack</code>
            <span>or trigger via</span>
            <a href="https://github.com/Nandan-k-s-27/toolkit-readiness-agent/actions" target="_blank" rel="noopener" style="color:var(--accent);text-decoration:underline;">GitHub Actions Workflow Dispatch</a>
          </div>
        </div>
        <a href="#verification" class="btn btn-xs">
          <span>View Benchmark</span>
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
        </a>
      </div>
    </div>
  </section>

  <!-- Section 1: Patterns -->
  <section class="section-wrap" id="patterns">
    <div class="container">
      <div class="section-head">
        <div class="section-title-wrap">
          <span class="section-num">01</span>
          <h2 class="section-title">Headline Insights & Distributions</h2>
        </div>
      </div>

      <div class="grid-3" style="margin-bottom:20px;">
        <div class="card">
          <div style="font-size:11px;font-weight:700;color:var(--blue);letter-spacing:0.06em;margin-bottom:6px;text-transform:uppercase;">Insight 01</div>
          <div style="font-size:14.5px;font-weight:700;line-height:1.4;">OAuth2 is the dominant authentication method: 60/100 apps support it.</div>
        </div>
        <div class="card">
          <div style="font-size:11px;font-weight:700;color:var(--blue);letter-spacing:0.06em;margin-bottom:6px;text-transform:uppercase;">Insight 02</div>
          <div style="font-size:14.5px;font-weight:700;line-height:1.4;">85% of apps are self-serve; 12% require payment, approval or sales outreach.</div>
        </div>
        <div class="card">
          <div style="font-size:11px;font-weight:700;color:var(--blue);letter-spacing:0.06em;margin-bottom:6px;text-transform:uppercase;">Insight 03</div>
          <div style="font-size:14.5px;font-weight:700;line-height:1.4;">62/100 applications already have existing Model Context Protocol servers.</div>
        </div>
      </div>

      <div class="grid-3">
        <div class="card">
          <div class="card-title">Authentication Dominance</div>
          <div class="card-subtitle">Protocols detected across 100 apps</div>
          <div class="bar-row"><span class="bar-name">OAuth2</span><div class="bar-track"><div class="bar-fill" style="width:100%;"></div></div><span class="bar-count">60</span></div>
          <div class="bar-row"><span class="bar-name">Bearer Token</span><div class="bar-track"><div class="bar-fill" style="width:73%;"></div></div><span class="bar-count">44</span></div>
          <div class="bar-row"><span class="bar-name">API Key</span><div class="bar-track"><div class="bar-fill" style="width:70%;"></div></div><span class="bar-count">42</span></div>
          <div class="bar-row"><span class="bar-name">Basic Auth</span><div class="bar-track"><div class="bar-fill" style="width:15%;"></div></div><span class="bar-count">9</span></div>
          <div class="bar-row"><span class="bar-name">JWT / HMAC</span><div class="bar-track"><div class="bar-fill" style="width:8%;"></div></div><span class="bar-count">5</span></div>
        </div>

        <div class="card">
          <div class="card-title">Access Model Breakdown</div>
          <div class="card-subtitle">Developer onboarding friction</div>
          <div class="bar-row"><span class="bar-name">Free Tier</span><div class="bar-track"><div class="bar-fill" style="width:100%;background:var(--ok);"></div></div><span class="bar-count">67</span></div>
          <div class="bar-row"><span class="bar-name">Free Trial</span><div class="bar-track"><div class="bar-fill" style="width:27%;background:var(--blue);"></div></div><span class="bar-count">18</span></div>
          <div class="bar-row"><span class="bar-name">Paid Plan</span><div class="bar-track"><div class="bar-fill" style="width:7%;background:var(--warn);"></div></div><span class="bar-count">5</span></div>
          <div class="bar-row"><span class="bar-name">Approval Gate</span><div class="bar-track"><div class="bar-fill" style="width:4%;background:var(--warn);"></div></div><span class="bar-count">3</span></div>
          <div class="bar-row"><span class="bar-name">Blocked / Gated</span><div class="bar-track"><div class="bar-fill" style="width:6%;background:var(--bad);"></div></div><span class="bar-count">4</span></div>
        </div>

        <div class="card">
          <div class="card-title">Category Gating Overview</div>
          <div class="card-subtitle">Self-serve availability by vertical</div>
          <div class="bar-row"><span class="bar-name">CRM & Sales</span><div class="bar-track"><div class="bar-fill" style="width:80%;background:var(--ok);"></div></div><span class="bar-count">8/10</span></div>
          <div class="bar-row"><span class="bar-name">Developer Infra</span><div class="bar-track"><div class="bar-fill" style="width:100%;background:var(--ok);"></div></div><span class="bar-count">10/10</span></div>
          <div class="bar-row"><span class="bar-name">Communications</span><div class="bar-track"><div class="bar-fill" style="width:90%;background:var(--ok);"></div></div><span class="bar-count">9/10</span></div>
          <div class="bar-row"><span class="bar-name">Finance</span><div class="bar-track"><div class="bar-fill" style="width:80%;background:var(--ok);"></div></div><span class="bar-count">8/10</span></div>
          <div class="bar-row"><span class="bar-name">Marketing & Ads</span><div class="bar-track"><div class="bar-fill" style="width:70%;background:var(--warn);"></div></div><span class="bar-count">7/10</span></div>
        </div>
      </div>
    </div>
  </section>

  <!-- Section 2: Explorer -->
  <section class="section-wrap" id="explorer">
    <div class="container">
      <div class="section-head">
        <div class="section-title-wrap">
          <span class="section-num">02</span>
          <h2 class="section-title">Application Readiness Explorer</h2>
        </div>
        <div style="font-size:12.5px;color:var(--text-muted);">
          Showing <span id="filteredCount" style="font-weight:700;color:var(--text);">100</span> of 100 applications
        </div>
      </div>

      <!-- Category Tab Bar -->
      <div class="category-tabs" id="categoryTabs">
        <div class="tab-pill active" onclick="selectCategoryTab('')">All <span class="tab-count">100</span></div>
        <div class="tab-pill" onclick="selectCategoryTab('CRM and Sales')">CRM & Sales <span class="tab-count">10</span></div>
        <div class="tab-pill" onclick="selectCategoryTab('Support and Helpdesk')">Support <span class="tab-count">10</span></div>
        <div class="tab-pill" onclick="selectCategoryTab('Communications and Messaging')">Messaging <span class="tab-count">10</span></div>
        <div class="tab-pill" onclick="selectCategoryTab('Marketing, Ads, Email and Social')">Marketing <span class="tab-count">10</span></div>
        <div class="tab-pill" onclick="selectCategoryTab('Ecommerce')">Ecommerce <span class="tab-count">10</span></div>
        <div class="tab-pill" onclick="selectCategoryTab('Data, SEO and Scraping')">Data & Scraping <span class="tab-count">10</span></div>
        <div class="tab-pill" onclick="selectCategoryTab('Developer, Infra and Data platforms')">Dev & Infra <span class="tab-count">10</span></div>
        <div class="tab-pill" onclick="selectCategoryTab('Productivity and Project Management')">Productivity <span class="tab-count">10</span></div>
        <div class="tab-pill" onclick="selectCategoryTab('Finance and Fintech')">Fintech <span class="tab-count">10</span></div>
        <div class="tab-pill" onclick="selectCategoryTab('AI, Research and Media-native')">AI & Media <span class="tab-count">10</span></div>
      </div>

      <!-- Filter Controls Toolbar -->
      <div class="toolbar">
        <div class="search-box">
          <div class="search-icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          </div>
          <input type="text" id="filterSearch" class="search-input" placeholder="Search application, keywords, auth methods..." autocomplete="off">
          <span class="search-kbd">/</span>
        </div>

        <select id="filterBuildable" class="filter-select">
          <option value="">All Buildability</option>
          <option value="yes">Buildable (Yes)</option>
          <option value="yes_with_caveats">Buildable (Caveats)</option>
          <option value="blocked">Blocked</option>
        </select>

        <select id="filterAccess" class="filter-select">
          <option value="">All Access Models</option>
          <option value="self_serve_free">Free Tier</option>
          <option value="self_serve_trial">Free Trial</option>
          <option value="paid_plan_required">Paid Plan</option>
          <option value="approval_required">Approval Required</option>
          <option value="partner_gated">Partner Gated</option>
          <option value="no_public_api">No Public API</option>
        </select>

        <select id="filterMcp" class="filter-select">
          <option value="">All MCP Status</option>
          <option value="official">Official Server</option>
          <option value="community">Community Server</option>
          <option value="none_found">None Found</option>
        </select>

        <button class="btn btn-xs" id="btnResetFilters" style="display:none;" onclick="resetAllFilters()">Reset</button>

        <div style="margin-left:auto;display:flex;gap:8px;">
          <button class="btn btn-xs" id="btnExportCsv">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            <span>Export CSV</span>
          </button>
          <button class="btn btn-xs" id="btnExportJson">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            <span>Export JSON</span>
          </button>
        </div>
      </div>

      <!-- Pre-rendered SSR Data Table -->
      <div class="table-viewport">
        <table class="data-table" id="appsTable">
          <thead>
            <tr>
              <th data-sort="id">#</th>
              <th data-sort="app">Application</th>
              <th data-sort="category">Category</th>
              <th>Auth Protocol</th>
              <th data-sort="self_serve">Access Model</th>
              <th data-sort="existing_mcp">MCP Status</th>
              <th data-sort="buildability">Buildability</th>
              <th>Blocker</th>
              <th data-sort="confidence">Confidence</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody id="appTableBody">
{STATIC_ROWS_HTML}
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- Section 3: Architecture -->
  <section class="section-wrap" id="architecture">
    <div class="container">
      <div class="section-head">
        <div class="section-title-wrap">
          <span class="section-num">03</span>
          <h2 class="section-title">Autonomous Agent Architecture</h2>
        </div>
      </div>

      <div class="card">
        <div class="card-title">Two-Pass Evidence Grounding Pipeline</div>
        <div class="card-subtitle">To prevent LLM hallucination of API specifications, every claim extracted by the agent must be verified verbatim against raw fetched developer documentation before entering the final dataset.</div>

        <div class="flow-grid">
          <div class="flow-step">
            <div class="flow-step-num">01 / SEED</div>
            <div class="flow-step-title">100 Apps</div>
            <div class="flow-step-desc">Target app list across 10 vertical domains.</div>
          </div>
          <div class="flow-step">
            <div class="flow-step-num">02 / DISCOVER</div>
            <div class="flow-step-title">Web Search</div>
            <div class="flow-step-desc">Composio SDK or DuckDuckGo query retrieval.</div>
          </div>
          <div class="flow-step">
            <div class="flow-step-num">03 / FETCH</div>
            <div class="flow-step-title">Page Cache</div>
            <div class="flow-step-desc">HTML clean, excerpt truncation & disk caching.</div>
          </div>
          <div class="flow-step">
            <div class="flow-step-num">04 / EXTRACT</div>
            <div class="flow-step-title">Pass 1 Baseline</div>
            <div class="flow-step-desc">LLM extracts structured schema + quote claims.</div>
          </div>
          <div class="flow-step">
            <div class="flow-step-num">05 / VERIFY</div>
            <div class="flow-step-title">String Match</div>
            <div class="flow-step-desc">Verbatim code check: quote exists on cited page.</div>
          </div>
          <div class="flow-step">
            <div class="flow-step-num">06 / CRITIQUE</div>
            <div class="flow-step-title">Pass 2 Audit</div>
            <div class="flow-step-desc">LLM critic re-researches unsupported claims.</div>
          </div>
          <div class="flow-step">
            <div class="flow-step-num">07 / DELIVER</div>
            <div class="flow-step-title">Final Dataset</div>
            <div class="flow-step-desc">100 evidence-grounded records + human queue.</div>
          </div>
        </div>

        <div style="margin-top:20px;padding:16px 20px;background:var(--surface);border:1px solid var(--border);border-left:3px solid var(--accent);border-radius:var(--radius-sm);">
          <div style="font-weight:700;font-size:13.5px;color:var(--text);margin-bottom:4px;">
            Extra Verification Loop: Client-Side SPA / Headless Browser Detection
          </div>
          <div style="font-size:12.5px;color:var(--text-muted);line-height:1.5;">
            Standard HTTP fetch fails silently on Single Page Applications (SPAs) where client-side JavaScript dynamically loads documentation. Our agent runs an explicit DOM skeleton detector for markers such as <code>&lt;div id="root"&gt;</code>, <code>&lt;div id="app"&gt;</code>, or <em>"enable javascript to run this app"</em>.<br>
            <strong>What it caught:</strong> On <strong>Paygent Connect</strong> and <strong>higgsfield</strong>, client-side React/Vue shells hid documentation from naive scrapers. Rather than allowing the LLM to hallucinate synthetic endpoints, the loop flagged them immediately and routed them to <code>human_queue.json</code> for manual audit.
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Section 4: Benchmark & Accuracy -->
  <section class="section-wrap" id="verification">
    <div class="container">
      <div class="section-head">
        <div class="section-title-wrap">
          <span class="section-num">04</span>
          <h2 class="section-title">Ground Truth Benchmark & Honest Failure Reporting</h2>
        </div>
        <div style="display:flex;gap:8px;">
          <a href="accuracy.json" target="_blank" class="btn btn-xs">accuracy.json</a>
          <a href="gold_labels.csv" target="_blank" class="btn btn-xs">gold_labels.csv</a>
        </div>
      </div>

      <div class="card" style="margin-bottom:20px;">
        <div class="card-title">Stratified Evaluation vs 30 Hand-Verified Applications</div>
        <div class="card-subtitle">Every ground-truth row was hand-checked against official documentation across all 10 categories. No circular self-labeling.</div>

        <!-- Static Per-Field Evaluation Table (Accessible without JS) -->
        <div style="overflow-x:auto;margin:18px 0;">
          <table style="width:100%;border-collapse:collapse;font-size:12.5px;border:1px solid var(--border);border-radius:var(--radius-sm);background:var(--surface-card);">
            <thead>
              <tr style="border-bottom:1px solid var(--border);color:var(--text-dim);text-align:left;font-family:'JetBrains Mono',monospace;font-size:11px;text-transform:uppercase;">
                <th style="padding:9px 14px;">Evaluation Dimension</th>
                <th style="padding:9px 14px;">Pass 1 (Baseline)</th>
                <th style="padding:9px 14px;">Pass 2 (Final)</th>
                <th style="padding:9px 14px;">Ground Truth Sample (N=30)</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom:1px solid var(--border-subtle);"><td style="padding:9px 14px;font-weight:600;">Buildability Accuracy</td><td style="padding:9px 14px;">66.7%</td><td style="padding:9px 14px;font-weight:700;color:var(--ok);">70.0%</td><td style="padding:9px 14px;color:var(--text-dim);">30 hand-checked apps across 10 verticals</td></tr>
              <tr style="border-bottom:1px solid var(--border-subtle);"><td style="padding:9px 14px;font-weight:600;">Access Model (Self-Serve vs Gated)</td><td style="padding:9px 14px;">70.0%</td><td style="padding:9px 14px;font-weight:700;color:var(--blue);">60.0%</td><td style="padding:9px 14px;color:var(--text-dim);">Conservative critic penalty on edge-case trials</td></tr>
              <tr style="border-bottom:1px solid var(--border-subtle);"><td style="padding:9px 14px;font-weight:600;">Model Context Protocol (MCP)</td><td style="padding:9px 14px;">33.3%</td><td style="padding:9px 14px;font-weight:700;color:var(--purple);">30.0%</td><td style="padding:9px 14px;color:var(--text-dim);">Official vs community tagging shifts</td></tr>
              <tr style="border-bottom:1px solid var(--border-subtle);"><td style="padding:9px 14px;font-weight:600;">Authentication Protocol (Exact Set)</td><td style="padding:9px 14px;">26.7%</td><td style="padding:9px 14px;font-weight:700;color:var(--warn);">16.7%</td><td style="padding:9px 14px;color:var(--text-dim);">Strict exact multi-label matching (bearer vs api_key)</td></tr>
              <tr><td style="padding:9px 14px;font-weight:700;">Verbatim Quote Match Rate</td><td style="padding:9px 14px;">68.0%</td><td style="padding:9px 14px;font-weight:700;color:var(--accent);">73.0% (73 of 100 quotes)</td><td style="padding:9px 14px;color:var(--text-dim);">String-matched verbatim against raw fetched doc HTML</td></tr>
            </tbody>
          </table>
        </div>

        <div class="metric-grid" style="margin-bottom:20px;">
          <div class="metric-card">
            <div class="metric-lbl">Pass 1 Baseline</div>
            <div class="metric-val" style="color:var(--text);">49.2%</div>
            <div class="metric-sub">Single-shot extraction</div>
          </div>
          <div class="metric-card">
            <div class="metric-lbl">Pass 2 Final</div>
            <div class="metric-val" style="color:var(--ok);">44.2%</div>
            <div class="metric-sub">Conservative critic audit</div>
          </div>
          <div class="metric-card">
            <div class="metric-lbl">Buildability Accuracy</div>
            <div class="metric-val" style="color:var(--blue);">70.0%</div>
            <div class="metric-sub">Integration feasibility</div>
          </div>
          <div class="metric-card">
            <div class="metric-lbl">Access Accuracy</div>
            <div class="metric-val" style="color:var(--purple);">60.0%</div>
            <div class="metric-sub">Self-serve vs gated</div>
          </div>
          <div class="metric-card">
            <div class="metric-lbl">Verbatim Quote Match</div>
            <div class="metric-val" style="color:var(--accent);">73.0%</div>
            <div class="metric-sub">Pass 2 string-matched</div>
          </div>
        </div>

        <div class="grid-3" style="margin-bottom:20px;">
          <div class="card" style="background:var(--surface-card);">
            <div style="font-weight:700;font-size:13.5px;color:var(--ok);margin-bottom:6px;">Highest Accuracy Fields</div>
            <div style="font-size:12.5px;color:var(--text-muted);line-height:1.6;">
              • <strong>Buildability (70.0%)</strong>: Strong signal determining whether an API exists and can be integrated into an AI agent toolkit.<br>
              • <strong>Access Model (60.0%)</strong>: High reliability identifying self-serve developer access vs paid/approval gated tiers.
            </div>
          </div>

          <div class="card" style="background:var(--surface-card);">
            <div style="font-weight:700;font-size:13.5px;color:var(--warn);margin-bottom:6px;">Challenging Fields</div>
            <div style="font-size:12.5px;color:var(--text-muted);line-height:1.6;">
              • <strong>Existing MCP (30.0%)</strong>: Model Context Protocol servers are newly emerging weekly; official vs community tagging shifts rapidly.<br>
              • <strong>Auth Protocols (16.7%)</strong>: Strict exact multi-label set match penalizes returning bearer_token vs api_key synonyms.
            </div>
          </div>

          <div class="card" style="background:var(--surface-card);">
            <div style="font-weight:700;font-size:13.5px;color:var(--bad);margin-bottom:6px;">Difficult Cases That Defeated Agent</div>
            <div style="font-size:12.5px;color:var(--text-muted);line-height:1.6;">
              • <strong>Paygent Connect & Waterfall.io</strong>: Enterprise sales walls completely withhold public documentation.<br>
              • <strong>Plaid</strong>: Sandbox is self-serve, but live production credentials require compliance underwriting approval.<br>
              • <strong>Ahrefs & Otter AI</strong>: Consumer UI accounts exist, but developer API requires bespoke enterprise contracts.<br>
              • <strong>Twilio</strong>: Complex dual scheme (HTTP Basic Account SID/Token + HMAC webhook signing).
            </div>
          </div>
        </div>

        <div style="border-top:1px solid var(--border);padding-top:16px;">
          <div style="font-size:13.5px;font-weight:700;margin-bottom:6px;">Human Review Queue (29 applications flagged for manual audit)</div>
          <div style="font-size:12.5px;color:var(--text-muted);line-height:1.6;">
            Applications where documentation was JS-heavy, sales-gated, or had conflicting authentication references were flagged for human review. Verified inspection notes:
            <div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:8px;">
              <span class="badge badge-neutral"><strong>fanbasis:</strong> Minimal public documentation; no public endpoint.</span>
              <span class="badge badge-neutral"><strong>Waterfall.io:</strong> Partner-gated access; contact sales required.</span>
              <span class="badge badge-neutral"><strong>Paygent Connect:</strong> NMI-powered white-label; partnership required.</span>
              <span class="badge badge-neutral"><strong>Gladly:</strong> Enterprise-only; pricing gated behind sales.</span>
              <span class="badge badge-neutral"><strong>PitchBook:</strong> Financial data platform; license-gated API.</span>
              <span class="badge badge-neutral"><strong>Clay:</strong> API surface limited; primary use is UI-driven workflow.</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>

<!-- Evidence Modal -->
<div class="modal-backdrop" id="evidenceModal" onclick="closeEvidenceModal(event)">
  <div class="modal-box" onclick="event.stopPropagation()">
    <div class="modal-header">
      <div>
        <div id="modalAppName" style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;font-weight:800;letter-spacing:-0.02em;">Application</div>
        <div id="modalCategoryLine" style="font-size:13px;color:var(--text-muted);margin-top:2px;">Category Line</div>
      </div>
      <button class="modal-close" onclick="closeEvidenceModal()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>

    <div id="modalContent"></div>
  </div>
</div>

<footer>
  <div class="container footer-inner">
    <div>
      ToolkitHub · Built with Google Gemini & DuckDuckGo / Composio SDK
    </div>
    <div style="display:flex;gap:16px;">
      <a href="llms.txt" style="color:var(--accent);">llms.txt</a>
      <a href="results_final.json" style="color:var(--accent);">results_final.json</a>
      <a href="accuracy.json" style="color:var(--accent);">accuracy.json</a>
      <a href="https://toolkit-readiness-agent.vercel.app" style="color:var(--accent);">Live Platform</a>
      <a href="https://github.com/Nandan-k-s-27/toolkit-readiness-agent" target="_blank" rel="noopener" style="color:var(--accent);">GitHub</a>
    </div>
  </div>
</footer>

<script id="data-payload" type="application/json">__DATA__</script>
<script>
  const RAW = JSON.parse(document.getElementById('data-payload').textContent);
  const APPS = RAW.results || [];
  const $ = id => document.getElementById(id);

  let currentCategory = '';
  let currentSort = {{ col: 'id', dir: 'asc' }};
  let activeQuickStat = 'all';

  // Theme Toggle
  const themeSwitcher = $('themeSwitcher');
  const themeIcon = $('themeIcon');
  let isDark = localStorage.getItem('theme') !== 'light';

  function applyTheme() {{
    if (isDark) {{
      document.documentElement.removeAttribute('data-theme');
      themeIcon.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>`;
    }} else {{
      document.documentElement.setAttribute('data-theme', 'light');
      themeIcon.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>`;
    }}
  }}
  applyTheme();

  themeSwitcher.addEventListener('click', () => {{
    isDark = !isDark;
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    applyTheme();
  }});

  // Category Tab Selection
  window.selectCategoryTab = function(cat) {{
    currentCategory = cat;
    document.querySelectorAll('.tab-pill').forEach(pill => {{
      const isMatch = (cat === '' && pill.textContent.startsWith('All')) || pill.textContent.includes(cat.split(' ')[0]);
      pill.classList.toggle('active', isMatch);
    }});
    renderTable();
  }};

  // Quick Stat Filter
  window.filterByQuickStat = function(stat) {{
    activeQuickStat = stat;
    document.querySelectorAll('.metric-card').forEach(c => c.classList.remove('active'));
    if (event && event.currentTarget) event.currentTarget.classList.add('active');
    
    if (stat === 'all') {{
      $('filterBuildable').value = '';
      $('filterAccess').value = '';
      $('filterMcp').value = '';
    }} else if (stat === 'easy_wins') {{
      $('filterBuildable').value = 'yes';
      $('filterAccess').value = 'self_serve_free';
      $('filterMcp').value = '';
    }} else if (stat === 'mcp') {{
      $('filterBuildable').value = '';
      $('filterAccess').value = '';
      $('filterMcp').value = 'official';
    }} else if (stat === 'self_serve') {{
      $('filterBuildable').value = '';
      $('filterAccess').value = 'self_serve_free';
      $('filterMcp').value = '';
    }} else if (stat === 'blocked') {{
      $('filterBuildable').value = 'blocked';
      $('filterAccess').value = '';
      $('filterMcp').value = '';
    }}
    renderTable();
  }};

  // Reset Filters
  window.resetAllFilters = function() {{
    currentCategory = '';
    activeQuickStat = 'all';
    $('filterSearch').value = '';
    $('filterBuildable').value = '';
    $('filterAccess').value = '';
    $('filterMcp').value = '';
    document.querySelectorAll('.tab-pill').forEach((pill, i) => pill.classList.toggle('active', i === 0));
    document.querySelectorAll('.metric-card').forEach((card, i) => card.classList.toggle('active', i === 0));
    renderTable();
  }};

  // Render Table
  function renderTable() {{
    const q = $('filterSearch').value.trim().toLowerCase();
    const buildFilter = $('filterBuildable').value;
    const accessFilter = $('filterAccess').value;
    const mcpFilter = $('filterMcp').value;

    const hasFilters = q || currentCategory || buildFilter || accessFilter || mcpFilter;
    $('btnResetFilters').style.display = hasFilters ? 'inline-flex' : 'none';

    let filtered = APPS.filter(a => {{
      if (currentCategory && a.category !== currentCategory) return false;
      if (buildFilter && a.buildability !== buildFilter) return false;
      if (accessFilter && a.self_serve !== accessFilter) return false;
      if (mcpFilter && a.existing_mcp !== mcpFilter) return false;
      if (q) {{
        const str = `${{a.app}} ${{a.category}} ${{a.one_liner || ''}} ${{(a.auth_methods || []).join(' ')}} ${{a.self_serve || ''}} ${{a.blocker || ''}}`.toLowerCase();
        if (!str.includes(q)) return false;
      }}
      return true;
    }});

    // Sorting
    filtered.sort((a, b) => {{
      let va = a[currentSort.col];
      let vb = b[currentSort.col];
      if (currentSort.col === 'confidence') {{
        va = a.confidence || 0;
        vb = b.confidence || 0;
      }}
      if (typeof va === 'string') va = va.toLowerCase();
      if (typeof vb === 'string') vb = vb.toLowerCase();
      if (va < vb) return currentSort.dir === 'asc' ? -1 : 1;
      if (va > vb) return currentSort.dir === 'asc' ? 1 : -1;
      return 0;
    }});

    $('filteredCount').textContent = filtered.length;

    const tbody = $('appTableBody');
    tbody.innerHTML = '';

    if (filtered.length === 0) {{
      tbody.innerHTML = `<tr><td colspan="10" style="text-align:center;padding:48px 20px;color:var(--text-muted);">
        No applications match your selected filters. <a href="javascript:resetAllFilters()" style="color:var(--accent);text-decoration:underline;">Clear filters</a>
      </td></tr>`;
      return;
    }}

    filtered.forEach(r => {{
      const tr = document.createElement('tr');
      const aid = r.id;
      const conf = Math.round((r.confidence || 0) * 100);
      const confColor = conf >= 80 ? 'var(--ok)' : conf >= 65 ? 'var(--warn)' : 'var(--bad)';

      // build badges
      const authBadges = (r.auth_methods || []).slice(0, 2).map(m => `<span class="badge badge-subtle">${{m}}</span>`).join('');
      
      let buildBadge = `<span class="badge badge-neutral">—</span>`;
      if (r.buildability === 'yes') buildBadge = `<span class="badge badge-yes"><span class="dot dot-green"></span>Yes</span>`;
      else if (r.buildability === 'yes_with_caveats') buildBadge = `<span class="badge badge-warn"><span class="dot dot-amber"></span>Caveats</span>`;
      else if (r.buildability === 'blocked') buildBadge = `<span class="badge badge-bad"><span class="dot dot-red"></span>Blocked</span>`;

      let accessBadge = `<span class="badge badge-neutral">Unclear</span>`;
      if (r.self_serve === 'self_serve_free') accessBadge = `<span class="badge badge-yes"><span class="dot dot-green"></span>Free Tier</span>`;
      else if (r.self_serve === 'self_serve_trial') accessBadge = `<span class="badge badge-blue"><span class="dot dot-blue"></span>Free Trial</span>`;
      else if (r.self_serve === 'paid_plan_required') accessBadge = `<span class="badge badge-warn"><span class="dot dot-amber"></span>Paid Plan</span>`;
      else if (r.self_serve === 'approval_required') accessBadge = `<span class="badge badge-warn"><span class="dot dot-amber"></span>Approval</span>`;
      else if (r.self_serve === 'partner_gated') accessBadge = `<span class="badge badge-bad"><span class="dot dot-red"></span>Partner Gated</span>`;
      else if (r.self_serve === 'no_public_api') accessBadge = `<span class="badge badge-bad"><span class="dot dot-red"></span>No Public API</span>`;

      let mcpBadge = `<span class="badge badge-neutral">None</span>`;
      if (r.existing_mcp === 'official') mcpBadge = `<span class="badge badge-purple"><span class="dot dot-purple"></span>Official</span>`;
      else if (r.existing_mcp === 'community') mcpBadge = `<span class="badge badge-blue"><span class="dot dot-blue"></span>Community</span>`;

      const blocker = r.blocker === 'none' || !r.blocker ? '—' : `<span class="badge badge-bad-subtle">${{r.blocker.replace(/_/g, ' ')}}</span>`;

      tr.innerHTML = `
        <td style="color:var(--text-dim);font-weight:600;font-family:'JetBrains Mono',monospace;font-size:12px;">#${{aid}}</td>
        <td>
          <div style="font-weight:700;color:var(--text);font-size:13.5px;">${{r.app}}</div>
          <div style="font-size:11.5px;color:var(--text-dim);line-height:1.3;max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${{r.one_liner || ''}}</div>
        </td>
        <td style="color:var(--text-muted);font-size:12.5px;">${{r.category}}</td>
        <td>${{authBadges}}</td>
        <td>${{accessBadge}}</td>
        <td>${{mcpBadge}}</td>
        <td>${{buildBadge}}</td>
        <td style="font-size:12px;color:var(--text-muted);">${{blocker}}</td>
        <td><span style="font-weight:700;font-family:'JetBrains Mono',monospace;font-size:12px;color:${{confColor}};">${{conf}}%</span></td>
        <td><button class="btn btn-xs" onclick="openEvidenceModal(${{aid}}); event.stopPropagation();">Inspect</button></td>
      `;
      tr.addEventListener('click', () => openEvidenceModal(aid));
      tbody.appendChild(tr);
    }});
  }}

  // Column Sort Listeners
  document.querySelectorAll('.data-table th[data-sort]').forEach(th => {{
    th.addEventListener('click', () => {{
      const col = th.getAttribute('data-sort');
      if (currentSort.col === col) {{
        currentSort.dir = currentSort.dir === 'asc' ? 'desc' : 'asc';
      }} else {{
        currentSort.col = col;
        currentSort.dir = 'asc';
      }}
      renderTable();
    }});
  }});

  // Search & Filter Listeners
  ['filterSearch', 'filterBuildable', 'filterAccess', 'filterMcp'].forEach(id => {{
    $(id).addEventListener('input', renderTable);
  }});

  // Keyboard shortcut '/'
  window.addEventListener('keydown', e => {{
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {{
      e.preventDefault();
      $('filterSearch').focus();
    }}
    if (e.key === 'Escape') {{
      closeEvidenceModal();
    }}
  }});

  // Export JSON
  $('btnExportJson').addEventListener('click', () => {{
    const q = $('filterSearch').value.trim().toLowerCase();
    const data = APPS.filter(a => !q || JSON.stringify(a).toLowerCase().includes(q));
    const uri = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data, null, 2));
    const a = document.createElement('a');
    a.href = uri;
    a.download = "toolkit_readiness_100_apps.json";
    a.click();
  }});

  // Export CSV
  $('btnExportCsv').addEventListener('click', () => {{
    const headers = ["id", "app", "category", "auth_methods", "self_serve", "existing_mcp", "buildability", "blocker", "confidence"];
    const rows = [headers.join(",")];
    APPS.forEach(a => {{
      const auth = (a.auth_methods || []).join(';');
      rows.push([a.id, `"${{a.app}}"`, `"${{a.category}}"`, `"${{auth}}"`, a.self_serve || '', a.existing_mcp || '', a.buildability || '', a.blocker || '', a.confidence || 0].join(","));
    }});
    const uri = "data:text/csv;charset=utf-8," + encodeURIComponent(rows.join("\\n"));
    const a = document.createElement('a');
    a.href = uri;
    a.download = "toolkit_readiness_100_apps.csv";
    a.click();
  }});

  // Evidence Inspector Modal
  window.openEvidenceModal = function(id) {{
    const item = APPS.find(a => a.id === id);
    if (!item) return;

    $('modalAppName').textContent = item.app;
    $('modalCategoryLine').textContent = `${{item.category}} • ${{item.one_liner || 'Developer Platform'}}`;

    const ev = item.evidence || {{}};
    const fields = [
      {{ key: "auth_methods", label: "Authentication Methods" }},
      {{ key: "self_serve", label: "Self-Serve Developer Access" }},
      {{ key: "api_type", label: "API Surface & Architecture" }},
      {{ key: "existing_mcp", label: "Model Context Protocol (MCP)" }},
      {{ key: "buildability", label: "Buildability Verdict" }}
    ];

    let htmlStr = '';
    fields.forEach(f => {{
      const info = ev[f.key] || {{}};
      const quote = info.quote || 'No direct excerpt captured.';
      const url = info.url || '';
      const isVerified = (item.evidence_ok && item.evidence_ok[f.key]) ? true : false;
      
      htmlStr += `
        <div class="evidence-block">
          <div class="evidence-head">
            <span>${{f.label}}</span>
            ${{isVerified ? '<span class="badge badge-yes"><span class="dot dot-green"></span>Verified Verbatim</span>' : '<span class="badge badge-neutral">Extracted Excerpt</span>'}}
          </div>
          <div class="evidence-quote">${{quote}}</div>
          ${{url ? `<div class="evidence-url">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
            <span>Source:</span> <a href="${{url}}" target="_blank" rel="noopener">${{url}}</a>
          </div>` : ''}}
        </div>
      `;
    }});

    if (item.blocker_note) {{
      htmlStr += `
        <div style="margin-top:12px;padding:12px 14px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);font-size:12.5px;color:var(--text-muted);">
          <strong style="color:var(--text);">Blocker Note:</strong> ${{item.blocker_note}}
        </div>
      `;
    }}

    $('modalContent').innerHTML = htmlStr;
    $('evidenceModal').style.display = 'flex';
  }};

  window.closeEvidenceModal = function(e) {{
    if (!e || e.target === $('evidenceModal')) {{
      $('evidenceModal').style.display = 'none';
    }}
  }};
</script>

</body>
</html>"""

(ROOT / "index.html").write_text(HTML.replace("__DATA__", blob), encoding="utf-8")
print("index.html successfully generated with zero emojis and high-standard UI")
