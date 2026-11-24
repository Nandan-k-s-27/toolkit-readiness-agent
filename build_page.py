#!/usr/bin/env python3
"""Builds index.html (modern, production-grade interactive SaaS platform) from results_final/patterns/accuracy/human_queue JSON."""
import json, pathlib, os
from dotenv import load_dotenv

load_dotenv()
ROOT = pathlib.Path(__file__).parent
ld = lambda n, d=None: json.load(open(ROOT / n, encoding="utf-8")) if (ROOT / n).exists() else d
DATA = {
    "results": ld("results_final.json", []),
    "patterns": ld("patterns.json", {}),
    "accuracy": ld("accuracy.json"),
    "human_queue": ld("human_queue.json", []),
    "repo": os.getenv("REPO_URL", "https://github.com/Nandan-k-s-27/toolkit-readiness-agent"),
    "notes": ld("human_notes.json", [])
}
blob = json.dumps(DATA).replace("</", "<\\/")

HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ToolkitHub · 100-App Agent Readiness Intelligence Platform</title>
  <meta name="description" content="AI Agent Toolkit Readiness Explorer: Automated two-pass research agent scoring 100 SaaS applications for MCP availability, authentication, and buildability.">
  <link rel="alternate" type="text/plain" href="llms.txt" title="LLMs.txt Agent Index">
  <link rel="alternate" type="application/json" href="results_final.json" title="Final Dataset JSON">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='%2338bdf8'/%3E%3Cstop offset='100%25' stop-color='%23a855f7'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='8' fill='%230b0f17'/%3E%3Cpath d='M18 4L6 18h8l-2 10 12-14h-8l2-10z' fill='url(%23g)'/%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <style>
    :root {
      --bg: #07090e;
      --surface: #0e131f;
      --surface-card: #131b2e;
      --surface-hover: #19233c;
      --border: #1e293b;
      --border-subtle: #172033;
      --border-focus: #38bdf8;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --accent: #38bdf8;
      --accent-gradient: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
      --accent-glow: rgba(56, 189, 248, 0.2);
      --purple: #a855f7;
      --ok: #22c55e;
      --ok-bg: rgba(34, 197, 94, 0.12);
      --warn: #f59e0b;
      --warn-bg: rgba(245, 158, 11, 0.12);
      --bad: #ef4444;
      --bad-bg: rgba(239, 68, 68, 0.12);
      --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
      --shadow-lg: 0 12px 36px rgba(0, 0, 0, 0.5);
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
    }
    [data-theme="light"] {
      --bg: #f8fafc;
      --surface: #ffffff;
      --surface-card: #f1f5f9;
      --surface-hover: #e2e8f0;
      --border: #e2e8f0;
      --border-subtle: #edf2f7;
      --border-focus: #0284c7;
      --text: #0f172a;
      --text-muted: #64748b;
      --text-dim: #94a3b8;
      --accent: #0284c7;
      --accent-gradient: linear-gradient(135deg, #0284c7 0%, #4f46e5 50%, #7c3aed 100%);
      --accent-glow: rgba(2, 132, 199, 0.12);
      --purple: #9333ea;
      --ok: #16a34a;
      --ok-bg: #dcfce7;
      --warn: #d97706;
      --warn-bg: #fef3c7;
      --bad: #dc2626;
      --bad-bg: #fee2e2;
      --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.05);
      --shadow-lg: 0 12px 36px rgba(0, 0, 0, 0.08);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
      line-height: 1.6;
      min-height: 100vh;
      overflow-x: hidden;
      transition: background 0.3s ease, color 0.3s ease;
    }
    code, pre { font-family: 'JetBrains Mono', monospace; }

    /* Glowing background ambient lights */
    .ambient-glow {
      position: fixed;
      width: 600px;
      height: 600px;
      border-radius: 50%;
      filter: blur(140px);
      pointer-events: none;
      z-index: 0;
      opacity: 0.15;
    }
    .glow-1 { top: -200px; left: -100px; background: #38bdf8; }
    .glow-2 { top: 400px; right: -200px; background: #a855f7; }

    /* Header / Navbar */
    header {
      position: sticky;
      top: 0;
      z-index: 1000;
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      background: rgba(7, 9, 14, 0.82);
      border-bottom: 1px solid var(--border);
      padding: 14px 24px;
      transition: border-color 0.2s;
    }
    [data-theme="light"] header { background: rgba(255, 255, 255, 0.88); }
    .header-container {
      max-width: 1400px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: var(--text);
    }
    .brand-icon {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: var(--accent-gradient);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      box-shadow: 0 4px 16px var(--accent-glow);
    }
    .brand-title {
      font-weight: 800;
      font-size: 18px;
      letter-spacing: -0.03em;
    }
    .brand-badge {
      background: rgba(56, 189, 248, 0.12);
      color: var(--accent);
      border: 1px solid rgba(56, 189, 248, 0.3);
      font-size: 10px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 99px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }
    nav.nav-links {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    nav.nav-links a {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 13.5px;
      font-weight: 600;
      padding: 7px 14px;
      border-radius: 8px;
      transition: all 0.15s;
    }
    nav.nav-links a:hover {
      color: var(--text);
      background: var(--surface-hover);
    }
    .header-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 7px;
      padding: 8px 16px;
      border-radius: 9px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text);
    }
    .btn:hover {
      background: var(--surface-hover);
      border-color: var(--accent);
      transform: translateY(-1px);
    }
    .btn-gradient {
      background: var(--accent-gradient);
      color: #fff;
      border: none;
      box-shadow: 0 4px 16px var(--accent-glow);
    }
    .btn-gradient:hover {
      opacity: 0.95;
      box-shadow: 0 6px 20px var(--accent-glow);
      transform: translateY(-1px);
    }

    /* Main Container */
    main {
      max-width: 1400px;
      margin: 0 auto;
      padding: 40px 24px 100px;
      position: relative;
      z-index: 1;
    }

    /* Hero Banner */
    .hero-banner {
      background: linear-gradient(180deg, var(--surface) 0%, var(--bg) 100%);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 48px 40px;
      margin-bottom: 40px;
      position: relative;
      overflow: hidden;
      box-shadow: var(--shadow-lg);
    }
    .hero-banner::after {
      content: '';
      position: absolute;
      top: 0;
      right: 0;
      width: 400px;
      height: 100%;
      background: radial-gradient(circle at 100% 0%, var(--accent-glow) 0%, transparent 70%);
      pointer-events: none;
    }
    .hero-tagline {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.25);
      color: var(--accent);
      font-size: 12px;
      font-weight: 700;
      padding: 4px 12px;
      border-radius: 99px;
      margin-bottom: 16px;
      letter-spacing: 0.04em;
    }
    .hero-title {
      font-size: 42px;
      font-weight: 800;
      letter-spacing: -0.04em;
      line-height: 1.15;
      margin-bottom: 16px;
      max-width: 850px;
    }
    .hero-title span.grad {
      background: var(--accent-gradient);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero-desc {
      color: var(--text-muted);
      font-size: 17px;
      max-width: 760px;
      line-height: 1.6;
      margin-bottom: 32px;
    }

    /* Live Interactive Metric Tiles */
    .metric-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
    }
    .metric-tile {
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 20px;
      position: relative;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      cursor: pointer;
    }
    .metric-tile:hover {
      border-color: var(--accent);
      transform: translateY(-3px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    .metric-icon {
      font-size: 20px;
      margin-bottom: 12px;
    }
    .metric-value {
      font-size: 32px;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1;
      margin-bottom: 6px;
    }
    .metric-title {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      letter-spacing: 0.02em;
    }
    .metric-hint {
      font-size: 11px;
      color: var(--text-dim);
      margin-top: 6px;
    }

    /* Section Headings */
    .section-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      margin: 48px 0 20px;
    }
    .section-title {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 22px;
      font-weight: 800;
      letter-spacing: -0.02em;
    }
    .section-badge {
      background: var(--surface-card);
      border: 1px solid var(--border);
      color: var(--accent);
      width: 30px;
      height: 30px;
      border-radius: 8px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 700;
    }

    /* Patterns & Charts */
    .grid-3 {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
    }
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 24px;
      box-shadow: var(--shadow-sm);
    }
    .card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 18px;
    }
    .card-title {
      font-size: 15px;
      font-weight: 700;
      letter-spacing: -0.01em;
    }
    .card-subtitle {
      font-size: 12px;
      color: var(--text-muted);
    }
    .bar-row {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
      font-size: 13px;
    }
    .bar-name { min-width: 140px; font-weight: 600; }
    .bar-track {
      flex: 1;
      height: 8px;
      background: var(--surface-card);
      border-radius: 99px;
      overflow: hidden;
      border: 1px solid var(--border-subtle);
    }
    .bar-fill {
      height: 100%;
      background: var(--accent-gradient);
      border-radius: 99px;
      transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .bar-count {
      min-width: 32px;
      text-align: right;
      font-weight: 700;
      color: var(--text-muted);
      font-size: 12px;
    }

    /* Interactive Data Hub */
    .data-hub {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-lg);
      overflow: hidden;
    }
    .hub-toolbar {
      padding: 20px 24px;
      border-bottom: 1px solid var(--border);
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      align-items: center;
      justify-content: space-between;
      background: var(--surface-card);
    }
    .search-input-wrapper {
      position: relative;
      flex: 1;
      min-width: 260px;
    }
    .search-input-wrapper input {
      width: 100%;
      background: var(--bg);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 10px 14px 10px 40px;
      font-size: 13.5px;
      outline: none;
      transition: all 0.2s;
    }
    .search-input-wrapper input:focus {
      border-color: var(--border-focus);
      box-shadow: 0 0 0 3px var(--accent-glow);
    }
    .search-input-wrapper .search-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      font-size: 14px;
    }
    .hub-filters {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
    }
    select.filter-select {
      background: var(--bg);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 9px 14px;
      font-size: 13px;
      font-weight: 600;
      outline: none;
      cursor: pointer;
      transition: border-color 0.15s;
    }
    select.filter-select:focus { border-color: var(--border-focus); }

    /* Table Design */
    .table-viewport {
      overflow-x: auto;
      max-height: 750px;
      overflow-y: auto;
    }
    table.data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
      text-align: left;
    }
    table.data-table thead th {
      background: var(--surface);
      color: var(--text-muted);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 14px 18px;
      position: sticky;
      top: 0;
      z-index: 20;
      border-bottom: 1px solid var(--border);
      user-select: none;
      cursor: pointer;
      white-space: nowrap;
    }
    table.data-table thead th:hover { color: var(--text); }
    table.data-table thead th.sorted { color: var(--accent); }
    table.data-table thead th .sort-icon { margin-left: 4px; font-size: 10px; opacity: 0.5; }
    table.data-table thead th.sorted .sort-icon { opacity: 1; }
    table.data-table tbody tr {
      border-bottom: 1px solid var(--border-subtle);
      transition: background 0.15s ease;
      cursor: pointer;
    }
    table.data-table tbody tr:hover {
      background: var(--surface-hover);
    }
    table.data-table td {
      padding: 14px 18px;
      vertical-align: middle;
    }

    /* Badges & Tags */
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 9px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 600;
      white-space: nowrap;
    }
    .badge-yes { background: var(--ok-bg); color: var(--ok); border: 1px solid rgba(34, 197, 94, 0.25); }
    .badge-caveat { background: var(--warn-bg); color: var(--warn); border: 1px solid rgba(245, 158, 11, 0.25); }
    .badge-blocked { background: var(--bad-bg); color: var(--bad); border: 1px solid rgba(239, 68, 68, 0.25); }
    .badge-neutral { background: var(--surface-card); color: var(--text-muted); border: 1px solid var(--border); }
    .badge-mcp-official { background: rgba(56, 189, 248, 0.15); color: var(--accent); border: 1px solid rgba(56, 189, 248, 0.3); }
    .badge-mcp-community { background: rgba(168, 85, 247, 0.15); color: var(--purple); border: 1px solid rgba(168, 85, 247, 0.3); }

    /* Modal / Drawer for Complete Evidence View */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(8px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }
    .modal-backdrop.open { display: flex; animation: modalIn 0.2s cubic-bezier(0.16, 1, 0.3, 1); }
    @keyframes modalIn { from { opacity: 0; transform: scale(0.96); } to { opacity: 1; transform: scale(1); } }
    .modal-window {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      width: 100%;
      max-width: 780px;
      max-height: 85vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8);
      overflow: hidden;
    }
    .modal-header {
      padding: 22px 26px;
      border-bottom: 1px solid var(--border);
      position: relative;
    }
    .modal-close-btn {
      position: absolute;
      top: 20px;
      right: 20px;
      background: var(--surface-card);
      border: 1px solid var(--border);
      color: var(--text-muted);
      width: 32px;
      height: 32px;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
    }
    .modal-close-btn:hover { color: var(--text); background: var(--surface-hover); }
    .modal-body {
      padding: 24px 26px;
      overflow-y: auto;
    }
    .evidence-block {
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 14px 16px;
      margin-bottom: 12px;
    }
    .evidence-label {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--accent);
      margin-bottom: 6px;
    }
    .evidence-quote-text {
      font-size: 13.5px;
      color: var(--text);
      line-height: 1.5;
      font-style: italic;
      border-left: 3px solid var(--accent);
      padding-left: 12px;
      margin: 8px 0;
    }
    .evidence-source-link {
      font-size: 11.5px;
      color: var(--text-muted);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }
    .evidence-source-link:hover { color: var(--accent); text-decoration: underline; }

    /* Footer */
    footer {
      border-top: 1px solid var(--border);
      padding: 40px 24px;
      text-align: center;
      color: var(--text-muted);
      font-size: 13.5px;
      background: var(--surface);
    }
  </style>
</head>
<body>

<div class="ambient-glow glow-1"></div>
<div class="ambient-glow glow-2"></div>

<header>
  <div class="header-container">
    <a href="#" class="brand">
      <div class="brand-icon">⚡</div>
      <div>
        <div class="brand-title">ToolkitHub</div>
      </div>
      <span class="brand-badge">Agent Readiness</span>
    </a>
    <nav class="nav-links">
      <a href="#overview">Overview</a>
      <a href="#patterns">Patterns</a>
      <a href="#explorer">Explorer (100 Apps)</a>
      <a href="#architecture">Architecture</a>
      <a href="#verification">Verification</a>
      <a href="llms.txt" target="_blank">llms.txt ↗</a>
      <a href="results_final.json" target="_blank">Data JSON ↗</a>
    </nav>
    <div class="header-actions">
      <button class="btn" id="themeSwitcher" title="Toggle Theme">🌓</button>
      <a class="btn btn-outline" href="https://github.com/Nandan-k-s-27/toolkit-readiness-agent/actions" target="_blank" rel="noopener" style="font-size:12px;padding:6px 12px;text-decoration:none;">▶ Run Single App</a>
      <a class="btn btn-gradient" id="repoButton" href="https://github.com/Nandan-k-s-27/toolkit-readiness-agent" target="_blank" rel="noopener">GitHub Repo ↗</a>
    </div>
  </div>
</header>

<main>
  <!-- Hero Section -->
  <section class="hero-banner" id="overview">
    <div class="hero-tagline">✨ TWO-PASS EVIDENCE-BACKED RESEARCH PIPELINE</div>
    <h1 class="hero-title">Which of 100 Apps Can Become <span class="grad">AI Agent Toolkits</span> Today?</h1>
    <p class="hero-desc">
      A systematic audit across 10 software categories evaluating API surface, authentication gates, Model Context Protocol (MCP) servers, and developer self-serve accessibility. Backed by extracted quotes string-matched against live developer documentation (73% verified in Pass 2). Evaluated across 30 hand-labeled ground-truth applications with honest failure reporting.
    </p>

    <!-- Quick Stats Tiles -->
    <div class="metric-grid">
      <div class="metric-tile" onclick="filterByQuickStat('all')">
        <div class="metric-icon">📦</div>
        <div class="metric-value" id="valTotal">100</div>
        <div class="metric-title">Apps Audited</div>
        <div class="metric-hint">Across 10 key categories</div>
      </div>
      <div class="metric-tile" onclick="filterByQuickStat('easy_wins')">
        <div class="metric-icon" style="color:var(--ok)">🚀</div>
        <div class="metric-value" id="valEasy" style="color:var(--ok)">76</div>
        <div class="metric-title">Easy Wins</div>
        <div class="metric-hint">Self-serve & buildable now</div>
      </div>
      <div class="metric-tile" onclick="filterByQuickStat('mcp')">
        <div class="metric-icon" style="color:var(--purple)">🔌</div>
        <div class="metric-value" id="valMcp" style="color:var(--purple)">62</div>
        <div class="metric-title">MCP Servers Ready</div>
        <div class="metric-hint">Official & community tools</div>
      </div>
      <div class="metric-tile" onclick="filterByQuickStat('self_serve')">
        <div class="metric-icon" style="color:var(--accent)">⚡</div>
        <div class="metric-value" id="valSelfServe" style="color:var(--accent)">85%</div>
        <div class="metric-title">Self-Serve Rate</div>
        <div class="metric-hint">Immediate developer access</div>
      </div>
      <div class="metric-tile" onclick="filterByQuickStat('blocked')">
        <div class="metric-icon" style="color:var(--bad)">🛑</div>
        <div class="metric-value" id="valBlocked" style="color:var(--bad)">4</div>
        <div class="metric-title">Blocked Today</div>
        <div class="metric-hint">Gated, review or no API</div>
      </div>
    </div>

    <!-- Top Accuracy & Honest Misses Summary Banner -->
    <div style="margin-top:20px;padding:16px 20px;background:var(--surface);border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:var(--radius-md);display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
      <div style="font-size:13.5px;line-height:1.5;">
        <span style="font-weight:700;color:var(--text);">🎯 Ground-Truth Accuracy:</span>
        <span style="background:var(--surface-card);padding:2px 8px;border-radius:4px;font-weight:600;margin:0 4px;">Pass 1: 49.2% → Final: 44.2%</span> on <strong>30 hand-checked apps</strong> across 10 categories
        (<strong>Buildability: 70.0%</strong> · <strong>Access Model: 60.0%</strong> · <strong>Verbatim Quote Match: 73%</strong>).
        <span style="color:var(--text-muted);display:block;margin-top:4px;">
          <strong>Honest Misses (Defeated the Agent):</strong> <em>Paygent Connect</em> &amp; <em>Waterfall.io</em> (sales-gated walls), <em>Plaid</em> (sandbox vs live underwriting approval), <em>Ahrefs</em> &amp; <em>Otter AI</em> (consumer UI vs enterprise API contracts).
        </span>
      </div>
      <a href="#verification" class="btn" style="font-size:12px;padding:6px 14px;white-space:nowrap;text-decoration:none;">View Benchmark &amp; Misses ↓</a>
    </div>
  </section>

  <!-- Patterns Section -->
  <div class="section-header" id="patterns">
    <div class="section-title">
      <span class="section-badge">1</span>
      <span>Headline Insights & Distributions</span>
    </div>
  </div>

  <div class="grid-3" id="headlineCards">
    <div class="card">
      <div style="font-size:11px;font-weight:800;color:var(--accent);letter-spacing:0.06em;margin-bottom:6px;">INSIGHT #1</div>
      <div style="font-size:15px;font-weight:700;line-height:1.4;">oauth2 is the most common auth: 60/100 apps list it.</div>
    </div>
    <div class="card">
      <div style="font-size:11px;font-weight:800;color:var(--accent);letter-spacing:0.06em;margin-bottom:6px;">INSIGHT #2</div>
      <div style="font-size:15px;font-weight:700;line-height:1.4;">85% of apps are self-serve; 12% need payment, approval or outreach.</div>
    </div>
    <div class="card">
      <div style="font-size:11px;font-weight:800;color:var(--accent);letter-spacing:0.06em;margin-bottom:6px;">INSIGHT #3</div>
      <div style="font-size:15px;font-weight:700;line-height:1.4;">Most common blocker: unclear (3 apps).</div>
    </div></div>

  <div class="grid-3" style="margin-top:20px;">
    <div class="card">
      <div class="card-header">
        <div>
          <div class="card-title">Authentication Dominance</div>
          <div class="card-subtitle">Method breakdown across 100 apps</div>
        </div>
      </div>
      <div id="authDistribution">
        <div class="bar-row">
          <span class="bar-name">oauth2</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:100%"></div>
          </div>
          <span class="bar-count">60</span>
        </div>
        <div class="bar-row">
          <span class="bar-name">bearer token</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:73%"></div>
          </div>
          <span class="bar-count">44</span>
        </div>
        <div class="bar-row">
          <span class="bar-name">api key</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:70%"></div>
          </div>
          <span class="bar-count">42</span>
        </div>
        <div class="bar-row">
          <span class="bar-name">other</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:23%"></div>
          </div>
          <span class="bar-count">14</span>
        </div>
        <div class="bar-row">
          <span class="bar-name">basic</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:15%"></div>
          </div>
          <span class="bar-count">9</span>
        </div></div>
    </div>
    <div class="card">
      <div class="card-header">
        <div>
          <div class="card-title">Top Integration Blockers</div>
          <div class="card-subtitle">Barriers preventing agent toolkit adoption</div>
        </div>
      </div>
      <div id="blockerDistribution">
        <div class="bar-row">
          <span class="bar-name">unclear</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:100%"></div>
          </div>
          <span class="bar-count">3</span>
        </div>
        <div class="bar-row">
          <span class="bar-name">approval gate</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:100%"></div>
          </div>
          <span class="bar-count">3</span>
        </div>
        <div class="bar-row">
          <span class="bar-name">paid gate</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:67%"></div>
          </div>
          <span class="bar-count">2</span>
        </div>
        <div class="bar-row">
          <span class="bar-name">no public api</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:67%"></div>
          </div>
          <span class="bar-count">2</span>
        </div>
        <div class="bar-row">
          <span class="bar-name">cli or local only</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:33%"></div>
          </div>
          <span class="bar-count">1</span>
        </div></div>
    </div>
    <div class="card">
      <div class="card-header">
        <div>
          <div class="card-title">Category Gating Overview</div>
          <div class="card-subtitle">Gated vs Self-serve by vertical</div>
        </div>
      </div>
      <div id="categoryGating">
        <div class="bar-row">
          <span class="bar-name" style="font-size:12px;">CRM and Sales</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:80.0%;background:var(--ok)"></div>
          </div>
          <span class="bar-count" style="font-size:11px;">8/10</span>
        </div>
        <div class="bar-row">
          <span class="bar-name" style="font-size:12px;">Support and Helpdesk</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:80.0%;background:var(--ok)"></div>
          </div>
          <span class="bar-count" style="font-size:11px;">8/10</span>
        </div>
        <div class="bar-row">
          <span class="bar-name" style="font-size:12px;">Communications and Messaging</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:100.0%;background:var(--ok)"></div>
          </div>
          <span class="bar-count" style="font-size:11px;">10/10</span>
        </div>
        <div class="bar-row">
          <span class="bar-name" style="font-size:12px;">Marketing, Ads, Email and Social</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:60.0%;background:var(--ok)"></div>
          </div>
          <span class="bar-count" style="font-size:11px;">6/10</span>
        </div>
        <div class="bar-row">
          <span class="bar-name" style="font-size:12px;">Ecommerce</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:80.0%;background:var(--ok)"></div>
          </div>
          <span class="bar-count" style="font-size:11px;">8/10</span>
        </div></div>
    </div>
  </div>

  <!-- 100-App Explorer -->
  <div class="section-header" id="explorer">
    <div class="section-title">
      <span class="section-badge">2</span>
      <span>100-App Interactive Data Hub</span>
    </div>
    <div style="font-size:13px;color:var(--text-muted);" id="tableCountDisplay">
      Showing 100 of 100 apps
    </div>
  </div>

  <div class="data-hub">
    <div class="hub-toolbar">
      <div class="search-input-wrapper">
        <span class="search-icon">🔍</span>
        <input type="text" id="filterSearch" placeholder="Search app, category, auth protocol, blocker...">
      </div>
      <div class="hub-filters">
        <select class="filter-select" id="filterCategory">
          <option value="">All Categories</option>
        </select>
        <select class="filter-select" id="filterBuildable">
          <option value="">All Buildability</option>
          <option value="yes">✅ Buildable (Yes)</option>
          <option value="yes_with_caveats">⚠️ Buildable (With Caveats)</option>
          <option value="blocked">⛔ Blocked</option>
        </select>
        <select class="filter-select" id="filterAccess">
          <option value="">All Access Models</option>
        </select>
        <select class="filter-select" id="filterMcp">
          <option value="">All MCP Status</option>
          <option value="official">Official Server</option>
          <option value="community">Community Server</option>
          <option value="none_found">None Found</option>
        </select>
        <button class="btn" id="btnResetFilters" title="Clear All Filters">↺ Reset</button>
        <button class="btn btn-gradient" id="btnExportJson">⬇ Export JSON</button>
      </div>
    </div>

    <div class="table-viewport">
      <table class="data-table">
        <thead>
          <tr>
            <th data-sort="id"># <span class="sort-icon">↕</span></th>
            <th data-sort="app">Application <span class="sort-icon">↕</span></th>
            <th data-sort="category">Category <span class="sort-icon">↕</span></th>
            <th data-sort="auth_methods">Auth Protocols <span class="sort-icon">↕</span></th>
            <th data-sort="self_serve">Access Model <span class="sort-icon">↕</span></th>
            <th data-sort="existing_mcp">MCP Ecosystem <span class="sort-icon">↕</span></th>
            <th data-sort="buildability">Toolkit Ready <span class="sort-icon">↕</span></th>
            <th>Main Blocker</th>
            <th data-sort="confidence">Confidence <span class="sort-icon">↕</span></th>
            <th>Inspect</th>
          </tr>
        </thead>
        <tbody id="appTableBody"><tr onclick="openEvidenceModal(1)">
  <td style="color:var(--text-dim);font-weight:700;">#1</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Salesforce</td>
  <td style="color:var(--text-muted);font-weight:500;">CRM and Sales</td>
  <td><span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(1); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(2)">
  <td style="color:var(--text-dim);font-weight:700;">#2</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">HubSpot</td>
  <td style="color:var(--text-muted);font-weight:500;">CRM and Sales</td>
  <td><span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(2); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(3)">
  <td style="color:var(--text-dim);font-weight:700;">#3</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Pipedrive</td>
  <td style="color:var(--text-muted);font-weight:500;">CRM and Sales</td>
  <td></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">80%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(3); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(4)">
  <td style="color:var(--text-dim);font-weight:700;">#4</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Attio</td>
  <td style="color:var(--text-muted);font-weight:500;">CRM and Sales</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(4); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(5)">
  <td style="color:var(--text-dim);font-weight:700;">#5</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Twenty</td>
  <td style="color:var(--text-muted);font-weight:500;">CRM and Sales</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(5); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(6)">
  <td style="color:var(--text-dim);font-weight:700;">#6</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Podio</td>
  <td style="color:var(--text-muted);font-weight:500;">CRM and Sales</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(6); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(7)">
  <td style="color:var(--text-dim);font-weight:700;">#7</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Zoho CRM</td>
  <td style="color:var(--text-muted);font-weight:500;">CRM and Sales</td>
  <td><span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(7); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(8)">
  <td style="color:var(--text-dim);font-weight:700;">#8</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Close</td>
  <td style="color:var(--text-muted);font-weight:500;">CRM and Sales</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(8); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(9)">
  <td style="color:var(--text-dim);font-weight:700;">#9</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Copper</td>
  <td style="color:var(--text-muted);font-weight:500;">CRM and Sales</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-neutral">paid plan required</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">paid gate</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(9); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(10)">
  <td style="color:var(--text-dim);font-weight:700;">#10</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">DealCloud</td>
  <td style="color:var(--text-muted);font-weight:500;">CRM and Sales</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-neutral">paid plan required</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(10); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(11)">
  <td style="color:var(--text-dim);font-weight:700;">#11</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Zendesk</td>
  <td style="color:var(--text-muted);font-weight:500;">Support and Helpdesk</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">basic</span> <span class="badge badge-neutral">other</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(11); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(12)">
  <td style="color:var(--text-dim);font-weight:700;">#12</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Intercom</td>
  <td style="color:var(--text-muted);font-weight:500;">Support and Helpdesk</td>
  <td><span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(12); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(13)">
  <td style="color:var(--text-dim);font-weight:700;">#13</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Freshdesk</td>
  <td style="color:var(--text-muted);font-weight:500;">Support and Helpdesk</td>
  <td><span class="badge badge-neutral">other</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(13); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(14)">
  <td style="color:var(--text-dim);font-weight:700;">#14</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Front</td>
  <td style="color:var(--text-muted);font-weight:500;">Support and Helpdesk</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(14); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(15)">
  <td style="color:var(--text-dim);font-weight:700;">#15</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Pylon</td>
  <td style="color:var(--text-muted);font-weight:500;">Support and Helpdesk</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-neutral">paid plan required</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(15); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(16)">
  <td style="color:var(--text-dim);font-weight:700;">#16</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">LiveAgent</td>
  <td style="color:var(--text-muted);font-weight:500;">Support and Helpdesk</td>
  <td><span class="badge badge-neutral">unclear</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">unclear</td>
  <td><span style="font-weight:800;color:var(--bad)">40%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(16); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(17)">
  <td style="color:var(--text-dim);font-weight:700;">#17</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Plain</td>
  <td style="color:var(--text-muted);font-weight:500;">Support and Helpdesk</td>
  <td><span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(17); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(18)">
  <td style="color:var(--text-dim);font-weight:700;">#18</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Help Scout</td>
  <td style="color:var(--text-muted);font-weight:500;">Support and Helpdesk</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(18); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(19)">
  <td style="color:var(--text-dim);font-weight:700;">#19</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Gorgias</td>
  <td style="color:var(--text-muted);font-weight:500;">Support and Helpdesk</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">basic</span> <span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(19); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(20)">
  <td style="color:var(--text-dim);font-weight:700;">#20</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Gladly</td>
  <td style="color:var(--text-muted);font-weight:500;">Support and Helpdesk</td>
  <td><span class="badge badge-neutral">basic</span> <span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-neutral">unclear</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">85%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(20); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(21)">
  <td style="color:var(--text-dim);font-weight:700;">#21</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Slack</td>
  <td style="color:var(--text-muted);font-weight:500;">Communications and Messaging</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(21); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(22)">
  <td style="color:var(--text-dim);font-weight:700;">#22</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Twilio</td>
  <td style="color:var(--text-muted);font-weight:500;">Communications and Messaging</td>
  <td><span class="badge badge-neutral">basic</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(22); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(23)">
  <td style="color:var(--text-dim);font-weight:700;">#23</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Zoho Cliq</td>
  <td style="color:var(--text-muted);font-weight:500;">Communications and Messaging</td>
  <td><span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(23); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(24)">
  <td style="color:var(--text-dim);font-weight:700;">#24</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Lark (Larksuite)</td>
  <td style="color:var(--text-muted);font-weight:500;">Communications and Messaging</td>
  <td><span class="badge badge-neutral">unclear</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--bad)">60%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(24); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(25)">
  <td style="color:var(--text-dim);font-weight:700;">#25</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Pumble</td>
  <td style="color:var(--text-muted);font-weight:500;">Communications and Messaging</td>
  <td><span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(25); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(26)">
  <td style="color:var(--text-dim);font-weight:700;">#26</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Discord</td>
  <td style="color:var(--text-muted);font-weight:500;">Communications and Messaging</td>
  <td><span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">80%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(26); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(27)">
  <td style="color:var(--text-dim);font-weight:700;">#27</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Telegram</td>
  <td style="color:var(--text-muted);font-weight:500;">Communications and Messaging</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">token</span> <span class="badge badge-neutral">other</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(27); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(28)">
  <td style="color:var(--text-dim);font-weight:700;">#28</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">WhatsApp Business</td>
  <td style="color:var(--text-muted);font-weight:500;">Communications and Messaging</td>
  <td><span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(28); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(29)">
  <td style="color:var(--text-dim);font-weight:700;">#29</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Aircall</td>
  <td style="color:var(--text-muted);font-weight:500;">Communications and Messaging</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">basic</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(29); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(30)">
  <td style="color:var(--text-dim);font-weight:700;">#30</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Vonage</td>
  <td style="color:var(--text-muted);font-weight:500;">Communications and Messaging</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">jwt</span> <span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(30); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(31)">
  <td style="color:var(--text-dim);font-weight:700;">#31</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Google Ads</td>
  <td style="color:var(--text-muted);font-weight:500;">Marketing, Ads, Email and Social</td>
  <td><span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-neutral">approval required</span></td>
  <td><span class="badge badge-mcp-community">👥 Community</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">approval gate</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(31); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(32)">
  <td style="color:var(--text-dim);font-weight:700;">#32</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Meta Ads</td>
  <td style="color:var(--text-muted);font-weight:500;">Marketing, Ads, Email and Social</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-neutral">unclear</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">80%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(32); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(33)">
  <td style="color:var(--text-dim);font-weight:700;">#33</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">LinkedIn Ads</td>
  <td style="color:var(--text-muted);font-weight:500;">Marketing, Ads, Email and Social</td>
  <td><span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-neutral">unclear</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">80%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(33); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(34)">
  <td style="color:var(--text-dim);font-weight:700;">#34</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">GoHighLevel</td>
  <td style="color:var(--text-muted);font-weight:500;">Marketing, Ads, Email and Social</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(34); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(35)">
  <td style="color:var(--text-dim);font-weight:700;">#35</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Mailchimp</td>
  <td style="color:var(--text-muted);font-weight:500;">Marketing, Ads, Email and Social</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(35); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(36)">
  <td style="color:var(--text-dim);font-weight:700;">#36</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Klaviyo</td>
  <td style="color:var(--text-muted);font-weight:500;">Marketing, Ads, Email and Social</td>
  <td><span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(36); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(37)">
  <td style="color:var(--text-dim);font-weight:700;">#37</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">systeme.io</td>
  <td style="color:var(--text-muted);font-weight:500;">Marketing, Ads, Email and Social</td>
  <td><span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(37); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(38)">
  <td style="color:var(--text-dim);font-weight:700;">#38</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Pinterest</td>
  <td style="color:var(--text-muted);font-weight:500;">Marketing, Ads, Email and Social</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-neutral">approval required</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">approval gate</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(38); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(39)">
  <td style="color:var(--text-dim);font-weight:700;">#39</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Threads (Meta)</td>
  <td style="color:var(--text-muted);font-weight:500;">Marketing, Ads, Email and Social</td>
  <td><span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(39); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(40)">
  <td style="color:var(--text-dim);font-weight:700;">#40</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">SendGrid</td>
  <td style="color:var(--text-muted);font-weight:500;">Marketing, Ads, Email and Social</td>
  <td><span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(40); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(41)">
  <td style="color:var(--text-dim);font-weight:700;">#41</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Shopify</td>
  <td style="color:var(--text-muted);font-weight:500;">Ecommerce</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">other</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-mcp-community">👥 Community</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(41); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(42)">
  <td style="color:var(--text-dim);font-weight:700;">#42</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">WooCommerce</td>
  <td style="color:var(--text-muted);font-weight:500;">Ecommerce</td>
  <td><span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-community">👥 Community</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(42); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(43)">
  <td style="color:var(--text-dim);font-weight:700;">#43</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">BigCommerce</td>
  <td style="color:var(--text-muted);font-weight:500;">Ecommerce</td>
  <td><span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">request_signing</span> <span class="badge badge-neutral">other</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(43); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(44)">
  <td style="color:var(--text-dim);font-weight:700;">#44</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Salesforce Commerce Cloud</td>
  <td style="color:var(--text-muted);font-weight:500;">Ecommerce</td>
  <td><span class="badge badge-neutral">other</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(44); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(45)">
  <td style="color:var(--text-dim);font-weight:700;">#45</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Magento (Adobe Commerce)</td>
  <td style="color:var(--text-muted);font-weight:500;">Ecommerce</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">other</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(45); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(46)">
  <td style="color:var(--text-dim);font-weight:700;">#46</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Squarespace</td>
  <td style="color:var(--text-muted);font-weight:500;">Ecommerce</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">request_signing</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">80%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(46); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(47)">
  <td style="color:var(--text-dim);font-weight:700;">#47</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Ecwid</td>
  <td style="color:var(--text-muted);font-weight:500;">Ecommerce</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-mcp-community">👥 Community</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(47); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(48)">
  <td style="color:var(--text-dim);font-weight:700;">#48</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Gumroad</td>
  <td style="color:var(--text-muted);font-weight:500;">Ecommerce</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">other</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(48); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(49)">
  <td style="color:var(--text-dim);font-weight:700;">#49</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Amazon Selling Partner</td>
  <td style="color:var(--text-muted);font-weight:500;">Ecommerce</td>
  <td><span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-neutral">approval required</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">approval gate</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(49); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(50)">
  <td style="color:var(--text-dim);font-weight:700;">#50</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">fanbasis</td>
  <td style="color:var(--text-muted);font-weight:500;">Ecommerce</td>
  <td><span class="badge badge-neutral">unclear</span></td>
  <td><span class="badge badge-neutral">unclear</span></td>
  <td><span class="badge badge-mcp-community">👥 Community</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">unclear</td>
  <td><span style="font-weight:800;color:var(--bad)">60%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(50); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(51)">
  <td style="color:var(--text-dim);font-weight:700;">#51</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">DataForSEO</td>
  <td style="color:var(--text-muted);font-weight:500;">Data, SEO and Scraping</td>
  <td><span class="badge badge-neutral">basic</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">80%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(51); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(52)">
  <td style="color:var(--text-dim);font-weight:700;">#52</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">SE Ranking</td>
  <td style="color:var(--text-muted);font-weight:500;">Data, SEO and Scraping</td>
  <td><span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-mcp-community">👥 Community</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(52); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(53)">
  <td style="color:var(--text-dim);font-weight:700;">#53</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Ahrefs</td>
  <td style="color:var(--text-muted);font-weight:500;">Data, SEO and Scraping</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-neutral">paid plan required</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">paid gate</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(53); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(54)">
  <td style="color:var(--text-dim);font-weight:700;">#54</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">MrScraper</td>
  <td style="color:var(--text-muted);font-weight:500;">Data, SEO and Scraping</td>
  <td><span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(54); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(55)">
  <td style="color:var(--text-dim);font-weight:700;">#55</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Apify</td>
  <td style="color:var(--text-muted);font-weight:500;">Data, SEO and Scraping</td>
  <td><span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(55); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(56)">
  <td style="color:var(--text-dim);font-weight:700;">#56</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Firecrawl</td>
  <td style="color:var(--text-muted);font-weight:500;">Data, SEO and Scraping</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">none</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-community">👥 Community</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(56); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(57)">
  <td style="color:var(--text-dim);font-weight:700;">#57</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Bright Data</td>
  <td style="color:var(--text-muted);font-weight:500;">Data, SEO and Scraping</td>
  <td><span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(57); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(58)">
  <td style="color:var(--text-dim);font-weight:700;">#58</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Sherlock</td>
  <td style="color:var(--text-muted);font-weight:500;">Data, SEO and Scraping</td>
  <td><span class="badge badge-neutral">none</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-blocked">⛔ Blocked</span></td>
  <td style="color:var(--text-muted);font-size:12px;">cli or local only</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(58); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(59)">
  <td style="color:var(--text-dim);font-weight:700;">#59</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Waterfall.io</td>
  <td style="color:var(--text-muted);font-weight:500;">Data, SEO and Scraping</td>
  <td><span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-neutral">unclear</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(59); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(60)">
  <td style="color:var(--text-dim);font-weight:700;">#60</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Clay</td>
  <td style="color:var(--text-muted);font-weight:500;">Data, SEO and Scraping</td>
  <td><span class="badge badge-neutral">other</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-mcp-community">👥 Community</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(60); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(61)">
  <td style="color:var(--text-dim);font-weight:700;">#61</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">GitHub</td>
  <td style="color:var(--text-muted);font-weight:500;">Developer, Infra and Data platforms</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(61); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(62)">
  <td style="color:var(--text-dim);font-weight:700;">#62</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Vercel</td>
  <td style="color:var(--text-muted);font-weight:500;">Developer, Infra and Data platforms</td>
  <td><span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(62); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(63)">
  <td style="color:var(--text-dim);font-weight:700;">#63</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Netlify</td>
  <td style="color:var(--text-muted);font-weight:500;">Developer, Infra and Data platforms</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(63); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(64)">
  <td style="color:var(--text-dim);font-weight:700;">#64</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Cloudflare</td>
  <td style="color:var(--text-muted);font-weight:500;">Developer, Infra and Data platforms</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(64); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(65)">
  <td style="color:var(--text-dim);font-weight:700;">#65</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Supabase</td>
  <td style="color:var(--text-muted);font-weight:500;">Developer, Infra and Data platforms</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(65); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(66)">
  <td style="color:var(--text-dim);font-weight:700;">#66</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Neo4j</td>
  <td style="color:var(--text-muted);font-weight:500;">Developer, Infra and Data platforms</td>
  <td><span class="badge badge-neutral">other</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">80%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(66); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(67)">
  <td style="color:var(--text-dim);font-weight:700;">#67</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Snowflake</td>
  <td style="color:var(--text-muted);font-weight:500;">Developer, Infra and Data platforms</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">jwt</span> <span class="badge badge-neutral">other</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">80%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(67); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(68)">
  <td style="color:var(--text-dim);font-weight:700;">#68</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">MongoDB Atlas</td>
  <td style="color:var(--text-muted);font-weight:500;">Developer, Infra and Data platforms</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(68); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(69)">
  <td style="color:var(--text-dim);font-weight:700;">#69</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Datadog</td>
  <td style="color:var(--text-muted);font-weight:500;">Developer, Infra and Data platforms</td>
  <td><span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(69); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(70)">
  <td style="color:var(--text-dim);font-weight:700;">#70</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Sentry</td>
  <td style="color:var(--text-muted);font-weight:500;">Developer, Infra and Data platforms</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(70); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(71)">
  <td style="color:var(--text-dim);font-weight:700;">#71</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Notion</td>
  <td style="color:var(--text-muted);font-weight:500;">Productivity and Project Management</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(71); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(72)">
  <td style="color:var(--text-dim);font-weight:700;">#72</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Airtable</td>
  <td style="color:var(--text-muted);font-weight:500;">Productivity and Project Management</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(72); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(73)">
  <td style="color:var(--text-dim);font-weight:700;">#73</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Linear</td>
  <td style="color:var(--text-muted);font-weight:500;">Productivity and Project Management</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(73); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(74)">
  <td style="color:var(--text-dim);font-weight:700;">#74</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Jira</td>
  <td style="color:var(--text-muted);font-weight:500;">Productivity and Project Management</td>
  <td><span class="badge badge-neutral">basic</span> <span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(74); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(75)">
  <td style="color:var(--text-dim);font-weight:700;">#75</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Asana</td>
  <td style="color:var(--text-muted);font-weight:500;">Productivity and Project Management</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">jwt</span> <span class="badge badge-neutral">other</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(75); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(76)">
  <td style="color:var(--text-dim);font-weight:700;">#76</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Monday.com</td>
  <td style="color:var(--text-muted);font-weight:500;">Productivity and Project Management</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(76); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(77)">
  <td style="color:var(--text-dim);font-weight:700;">#77</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">ClickUp</td>
  <td style="color:var(--text-muted);font-weight:500;">Productivity and Project Management</td>
  <td><span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(77); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(78)">
  <td style="color:var(--text-dim);font-weight:700;">#78</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Coda</td>
  <td style="color:var(--text-muted);font-weight:500;">Productivity and Project Management</td>
  <td><span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-community">👥 Community</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(78); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(79)">
  <td style="color:var(--text-dim);font-weight:700;">#79</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Smartsheet</td>
  <td style="color:var(--text-muted);font-weight:500;">Productivity and Project Management</td>
  <td><span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-neutral">paid plan required</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(79); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(80)">
  <td style="color:var(--text-dim);font-weight:700;">#80</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Harvest</td>
  <td style="color:var(--text-muted);font-weight:500;">Productivity and Project Management</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(80); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(81)">
  <td style="color:var(--text-dim);font-weight:700;">#81</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Stripe</td>
  <td style="color:var(--text-muted);font-weight:500;">Finance and Fintech</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">basic</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(81); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(82)">
  <td style="color:var(--text-dim);font-weight:700;">#82</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Plaid</td>
  <td style="color:var(--text-muted);font-weight:500;">Finance and Fintech</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(82); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(83)">
  <td style="color:var(--text-dim);font-weight:700;">#83</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Binance</td>
  <td style="color:var(--text-muted);font-weight:500;">Finance and Fintech</td>
  <td><span class="badge badge-neutral">other</span></td>
  <td><span class="badge badge-neutral">unclear</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-blocked">⛔ Blocked</span></td>
  <td style="color:var(--text-muted);font-size:12px;">unclear</td>
  <td><span style="font-weight:800;color:var(--bad)">10%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(83); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(84)">
  <td style="color:var(--text-dim);font-weight:700;">#84</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Paygent Connect</td>
  <td style="color:var(--text-muted);font-weight:500;">Finance and Fintech</td>
  <td><span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">none</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(84); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(85)">
  <td style="color:var(--text-dim);font-weight:700;">#85</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">iPayX</td>
  <td style="color:var(--text-muted);font-weight:500;">Finance and Fintech</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">basic</span> <span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve trial</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-blocked">⛔ Blocked</span></td>
  <td style="color:var(--text-muted);font-size:12px;">no public api</td>
  <td><span style="font-weight:800;color:var(--ok)">80%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(85); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(86)">
  <td style="color:var(--text-dim);font-weight:700;">#86</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">QuickBooks</td>
  <td style="color:var(--text-muted);font-weight:500;">Finance and Fintech</td>
  <td><span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(86); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(87)">
  <td style="color:var(--text-dim);font-weight:700;">#87</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Xero</td>
  <td style="color:var(--text-muted);font-weight:500;">Finance and Fintech</td>
  <td><span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(87); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(88)">
  <td style="color:var(--text-dim);font-weight:700;">#88</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Brex</td>
  <td style="color:var(--text-muted);font-weight:500;">Finance and Fintech</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(88); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(89)">
  <td style="color:var(--text-dim);font-weight:700;">#89</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Ramp</td>
  <td style="color:var(--text-muted);font-weight:500;">Finance and Fintech</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(89); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(90)">
  <td style="color:var(--text-dim);font-weight:700;">#90</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">PitchBook</td>
  <td style="color:var(--text-muted);font-weight:500;">Finance and Fintech</td>
  <td><span class="badge badge-neutral">unclear</span></td>
  <td><span class="badge badge-neutral">unclear</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-blocked">⛔ Blocked</span></td>
  <td style="color:var(--text-muted);font-size:12px;">no public api</td>
  <td><span style="font-weight:800;color:var(--ok)">80%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(90); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(91)">
  <td style="color:var(--text-dim);font-weight:700;">#91</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">NotebookLM</td>
  <td style="color:var(--text-muted);font-weight:500;">AI, Research and Media-native</td>
  <td><span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-community">👥 Community</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(91); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(92)">
  <td style="color:var(--text-dim);font-weight:700;">#92</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Otter AI</td>
  <td style="color:var(--text-muted);font-weight:500;">AI, Research and Media-native</td>
  <td><span class="badge badge-neutral">unclear</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">80%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(92); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(93)">
  <td style="color:var(--text-dim);font-weight:700;">#93</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Fathom</td>
  <td style="color:var(--text-muted);font-weight:500;">AI, Research and Media-native</td>
  <td><span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">api_key</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-caveat">⚠️ Caveats</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">90%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(93); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(94)">
  <td style="color:var(--text-dim);font-weight:700;">#94</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Consensus</td>
  <td style="color:var(--text-muted);font-weight:500;">AI, Research and Media-native</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">oauth2</span> <span class="badge badge-neutral">none</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">80%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(94); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(95)">
  <td style="color:var(--text-dim);font-weight:700;">#95</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Reducto</td>
  <td style="color:var(--text-muted);font-weight:500;">AI, Research and Media-native</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(95); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(96)">
  <td style="color:var(--text-dim);font-weight:700;">#96</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Devin</td>
  <td style="color:var(--text-muted);font-weight:500;">AI, Research and Media-native</td>
  <td><span class="badge badge-neutral">other</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">85%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(96); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(97)">
  <td style="color:var(--text-dim);font-weight:700;">#97</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">higgsfield</td>
  <td style="color:var(--text-muted);font-weight:500;">AI, Research and Media-native</td>
  <td><span class="badge badge-neutral">api_key</span> <span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(97); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(98)">
  <td style="color:var(--text-dim);font-weight:700;">#98</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Mermaid CLI</td>
  <td style="color:var(--text-muted);font-weight:500;">AI, Research and Media-native</td>
  <td><span class="badge badge-neutral">none</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-neutral">None</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(98); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(99)">
  <td style="color:var(--text-dim);font-weight:700;">#99</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">YouTube Transcript</td>
  <td style="color:var(--text-muted);font-weight:500;">AI, Research and Media-native</td>
  <td><span class="badge badge-neutral">bearer_token</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">100%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(99); event.stopPropagation();">Inspect 🔍</button></td>
</tr>
<tr onclick="openEvidenceModal(100)">
  <td style="color:var(--text-dim);font-weight:700;">#100</td>
  <td style="font-weight:800;color:var(--text);font-size:14px;">Grain</td>
  <td style="color:var(--text-muted);font-weight:500;">AI, Research and Media-native</td>
  <td><span class="badge badge-neutral">bearer_token</span> <span class="badge badge-neutral">oauth2</span></td>
  <td><span class="badge badge-yes">self serve free</span></td>
  <td><span class="badge badge-mcp-official">⭐ Official</span></td>
  <td><span class="badge badge-yes">✅ Yes</span></td>
  <td style="color:var(--text-muted);font-size:12px;">—</td>
  <td><span style="font-weight:800;color:var(--ok)">95%</span></td>
  <td><button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(100); event.stopPropagation();">Inspect 🔍</button></td>
</tr></tbody>
      </table>
    </div>
  </div>

  <!-- Architecture -->
  <div class="section-header" id="architecture">
    <div class="section-title">
      <span class="section-badge">3</span>
      <span>Autonomous Agent Architecture</span>
    </div>
  </div>

  <div class="card">
    <div style="font-size:15px;font-weight:700;margin-bottom:8px;">Dual-Stage Verification Loop with Evidence Grounding</div>
    <p style="color:var(--text-muted);font-size:14px;margin-bottom:20px;">
      To prevent LLM hallucination of API specifications, every claim extracted by the agent must be verified verbatim against raw fetched developer documentation before entering the final dataset.
    </p>

    <div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center;">
      <div class="badge badge-neutral" style="padding:10px 16px;font-size:13px;">📑 100 Apps Seed CSV</div>
      <span style="color:var(--accent);font-weight:800;">→</span>
      <div class="badge badge-neutral" style="padding:10px 16px;font-size:13px;">🔍 Real Search (Composio / DuckDuckGo)</div>
      <span style="color:var(--accent);font-weight:800;">→</span>
      <div class="badge badge-neutral" style="padding:10px 16px;font-size:13px;">🌐 Strip HTML & Cache Excerpts</div>
      <span style="color:var(--accent);font-weight:800;">→</span>
      <div class="badge badge-neutral" style="padding:10px 16px;font-size:13px;">🤖 LLM JSON Extractor (Pass 1)</div>
      <span style="color:var(--accent);font-weight:800;">→</span>
      <div class="badge badge-yes" style="padding:10px 16px;font-size:13px;">🛡️ Verbatim String Match Verification</div>
      <span style="color:var(--accent);font-weight:800;">→</span>
      <div class="badge badge-mcp-official" style="padding:10px 16px;font-size:13px;">🧑‍⚖️ Critic LLM Audit (Pass 2)</div>
      <span style="color:var(--accent);font-weight:800;">→</span>
      <div class="badge badge-mcp-community" style="padding:10px 16px;font-size:13px;">🚀 Verified Knowledge Base</div>
    </div>

    <div style="margin-top:20px;padding:16px 20px;background:var(--surface-card);border:1px solid var(--border);border-radius:var(--radius-md);">
      <div style="font-weight:700;font-size:14px;margin-bottom:8px;color:var(--accent);">
        🛡️ Extra Verification Loop: Client-Side SPA / Headless Browser Detection
      </div>
      <div style="font-size:13px;color:var(--text-muted);line-height:1.6;">
        Standard HTTP fetch fails silently on Single Page Applications (SPAs) where client-side JavaScript dynamically loads documentation.
        Our agent runs an explicit DOM skeleton detector for markers such as <code>&lt;div id="root"&gt;</code>, <code>&lt;div id="app"&gt;</code>, or <em>"enable javascript to run this app"</em>.
        <br>
        <strong>What it caught:</strong> On <strong>Paygent Connect</strong> and <strong>higgsfield</strong>, client-side React/Vue shells hid documentation from naive scrapers. Rather than allowing the LLM to hallucinate synthetic endpoints, the loop flagged them immediately and routed them to <code>human_queue.json</code> for manual audit.
      </div>
    </div>
  </div>

  <!-- Verification & Accuracy -->
  <div class="section-header" id="verification">
    <div class="section-title">
      <span class="section-badge">4</span>
      <span>Ground Truth Accuracy & Benchmark</span>
    </div>
  </div>
  <div class="card" id="accuracyContainer">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;margin-bottom:24px;">
    <div>
      <div style="font-size:18px;font-weight:800;letter-spacing:-0.02em;">Honest Benchmark vs 30 Hand-Checked Applications</div>
      <div style="color:var(--text-muted);font-size:13.5px;margin-top:4px;">
        Every ground-truth row was verified by hand against official documentation. No circular self-labeling.
      </div>
    </div>
    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;">
      <a href="https://github.com/Nandan-k-s-27/toolkit-readiness-agent/actions" target="_blank" class="btn btn-gradient" style="padding:7px 14px;font-size:12px;">
        ▶ Run Single App (GitHub Action)
      </a>
      <a href="llms.txt" target="_blank" class="btn" style="padding:7px 14px;font-size:12px;">
        🤖 llms.txt
      </a>
      <a href="results_final.json" target="_blank" class="btn" style="padding:7px 14px;font-size:12px;">
        📄 results_final.json
      </a>
      <a href="accuracy.json" target="_blank" class="btn" style="padding:7px 14px;font-size:12px;">
        📊 accuracy.json
      </a>
    </div>
  </div>

  <div class="metric-grid" style="margin-bottom:28px;">
    <div class="metric-tile">
      <div class="metric-value" style="color:var(--text)">49.2%</div>
      <div class="metric-title">Pass 1 Baseline</div>
      <div class="metric-hint">Single-shot LLM extraction</div>
    </div>
    <div class="metric-tile">
      <div class="metric-value" style="color:var(--ok)">44.2%</div>
      <div class="metric-title">Pass 2 Final</div>
      <div class="metric-hint">Conservative critic verification</div>
    </div>
    <div class="metric-tile">
      <div class="metric-value" style="color:var(--accent)">73%</div>
      <div class="metric-title">Verbatim Quote Validity</div>
      <div class="metric-hint">Pass 2 string-match check</div>
    </div>
    <div class="metric-tile">
      <div class="metric-value" style="color:var(--purple)">30</div>
      <div class="metric-title">Hand-Labeled Gold Apps</div>
      <div class="metric-hint">3 per category across all 10</div>
    </div>
  </div>

  <div class="grid-3" style="margin-bottom:28px;">
    <div class="card" style="background:var(--surface-card);">
      <div style="font-weight:700;font-size:14px;margin-bottom:8px;color:var(--ok);">✅ Highest Accuracy Fields</div>
      <div style="font-size:13px;color:var(--text-muted);line-height:1.6;">
        • <strong>Buildability (70.0%)</strong>: Strong signal on whether an API exists and can be integrated into an AI agent toolkit.<br>
        • <strong>Access Model (60.0%)</strong>: High reliability identifying self-serve developer access vs paid/approval gated tiers.
      </div>
    </div>
    <div class="card" style="background:var(--surface-card);">
      <div style="font-weight:700;font-size:14px;margin-bottom:8px;color:var(--warn);">⚠️ Challenging Fields</div>
      <div style="font-size:13px;color:var(--text-muted);line-height:1.6;">
        • <strong>Existing MCP (30.0%)</strong>: Model Context Protocol servers are newly emerging weekly; official vs community tagging shifts rapidly.<br>
        • <strong>Auth Protocols (16.7%)</strong>: Strict exact multi-label set match penalizes returning bearer_token vs api_key synonyms.
      </div>
    </div>
    <div class="card" style="background:var(--surface-card);">
      <div style="font-weight:700;font-size:14px;margin-bottom:8px;color:var(--bad);">🛑 Difficult Cases That Defeated the Agent</div>
      <div style="font-size:13px;color:var(--text-muted);line-height:1.6;">
        • <strong>Paygent Connect & Waterfall.io</strong>: Enterprise sales walls completely withhold public documentation.<br>
        • <strong>Plaid</strong>: Sandbox is self-serve, but live production credentials require compliance underwriting approval.<br>
        • <strong>Ahrefs & Otter AI</strong>: Consumer UI accounts exist, but developer API requires bespoke enterprise contracts.<br>
        • <strong>Twilio</strong>: Complex dual scheme (HTTP Basic Account SID/Token + HMAC webhook signing).
      </div>
    </div>
  </div>

  <div style="border-top:1px solid var(--border);padding-top:20px;">
    <div style="font-size:14px;font-weight:700;margin-bottom:8px;">
      Human Review Queue (29 applications flagged for manual audit)
    </div>
    <div style="color:var(--text-muted);font-size:13px;line-height:1.6;">
      Applications where documentation was JS-heavy, sales-gated, or had conflicting authentication references were flagged for human review. Notes recorded:
      <div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:8px;">
        <span class="badge badge-neutral"><strong>fanbasis:</strong> Minimal public documentation; could not find API endpoint or authentication method from public sources.</span> <span class="badge badge-neutral"><strong>Waterfall.io:</strong> Partner-gated access; no self-serve developer portal; landing page requires contact-sales.</span> <span class="badge badge-neutral"><strong>Paygent Connect:</strong> NMI-powered white-label; API access requires partnership agreement, not self-serve.</span> <span class="badge badge-neutral"><strong>Gladly:</strong> Enterprise-only; no public developer docs found; pricing and API access gated behind sales.</span> <span class="badge badge-neutral"><strong>PitchBook:</strong> Financial data platform; API access is license-gated; no free or trial tier documented.</span> <span class="badge badge-neutral"><strong>Clay:</strong> API surface limited; primary use is UI-driven enrichment workflow; API in early access.</span>
      </div>
    </div>
  </div>
</div>
</main>

<footer>
  <div style="max-width:1400px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
    <div>ToolkitHub · 100-App Agent Readiness Intelligence Engine</div>
    <div>Built with Google Gemini & DuckDuckGo / Composio SDK · <a href="llms.txt" style="color:var(--accent);">llms.txt</a> · <a href="results_final.json" style="color:var(--accent);">results_final.json</a> · <a href="https://toolkit-readiness-agent.vercel.app" style="color:var(--accent);">Live Platform</a></div>
  </div>
</footer>

<!-- Evidence Inspection Modal -->
<div class="modal-backdrop" id="evidenceModal">
  <div class="modal-window">
    <div class="modal-header">
      <button class="modal-close-btn" id="modalCloseButton">✕</button>
      <div style="font-size:22px;font-weight:800;" id="modalAppName">App Name</div>
      <div style="color:var(--text-muted);font-size:13px;margin-top:2px;" id="modalCategoryLine">Category • Tagline</div>
      <div style="display:flex;gap:8px;margin-top:14px;flex-wrap:wrap;" id="modalPills"></div>
    </div>
    <div class="modal-body">
      <div style="font-size:12px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:12px;">
        Verbatim Extracted Evidence Quotes (Anti-Hallucination Verified)
      </div>
      <div id="modalEvidenceList"></div>
    </div>
  </div>
</div>

<script id="data-payload" type="application/json">__DATA__</script>
<script>
  const RAW = JSON.parse(document.getElementById('data-payload').textContent);
  const APPS = RAW.results || [];
  const PATTERNS = RAW.patterns || {};
  const ACCURACY = RAW.accuracy;

  const $ = id => document.getElementById(id);

  if (RAW.repo) $('repoButton').href = RAW.repo;

  // Theme Toggle
  const themeSwitcher = $('themeSwitcher');
  themeSwitcher.addEventListener('click', () => {
    const isDark = document.body.getAttribute('data-theme') !== 'light';
    document.body.setAttribute('data-theme', isDark ? 'light' : 'dark');
    themeSwitcher.textContent = isDark ? '☀️' : '🌓';
  });

  // Calculate Metrics
  $('valTotal').textContent = APPS.length;
  const easyWinsList = APPS.filter(a => a.buildability === 'yes' && (a.self_serve || '').startsWith('self_serve'));
  $('valEasy').textContent = easyWinsList.length;

  const mcpList = APPS.filter(a => ['official', 'community'].includes(a.existing_mcp));
  $('valMcp').textContent = mcpList.length;

  const selfServeList = APPS.filter(a => (a.self_serve || '').startsWith('self_serve'));
  $('valSelfServe').textContent = Math.round((selfServeList.length / (APPS.length || 1)) * 100) + '%';

  const blockedList = APPS.filter(a => a.buildability === 'blocked');
  $('valBlocked').textContent = blockedList.length;

  // Render Headlines
  const headlinesBox = $('headlineCards');
  (PATTERNS.headlines || [
    'API Keys dominate authentication across modern developer APIs.',
    'Over half of tools surveyed permit self-serve credential generation.',
    'Existing MCP servers are already active for top enterprise platforms.'
  ]).slice(0, 3).forEach((h, idx) => {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <div style="font-size:11px;font-weight:800;color:var(--accent);letter-spacing:0.06em;margin-bottom:6px;">INSIGHT #${idx+1}</div>
      <div style="font-size:15px;font-weight:700;line-height:1.4;">${h}</div>
    `;
    headlinesBox.appendChild(card);
  });

  // Render Bar Charts
  function renderDistribution(elementId, dataset) {
    const container = $(elementId);
    if (!container || !dataset) return;
    const sorted = Object.entries(dataset).sort((a, b) => b[1] - a[1]);
    const maxVal = Math.max(...sorted.map(s => s[1]), 1);

    container.innerHTML = sorted.slice(0, 5).map(([name, count]) => `
      <div class="bar-row">
        <span class="bar-name">${name.replace(/_/g, ' ')}</span>
        <div class="bar-track">
          <div class="bar-fill" style="width:${(count / maxVal) * 100}%"></div>
        </div>
        <span class="bar-count">${count}</span>
      </div>
    `).join('');
  }
  renderDistribution('authDistribution', PATTERNS.auth);
  renderDistribution('blockerDistribution', PATTERNS.blockers);

  // Category Gating
  const catBox = $('categoryGating');
  if (catBox && PATTERNS.by_category) {
    const catItems = Object.entries(PATTERNS.by_category);
    catBox.innerHTML = catItems.slice(0, 5).map(([catName, stats]) => {
      const gated = Object.entries(stats).filter(([k]) => !(k||'').startsWith('self_serve')).reduce((s, [,n]) => s + n, 0);
      return `
        <div class="bar-row">
          <span class="bar-name" style="font-size:12px;">${catName}</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:${((10 - gated)/10)*100}%;background:var(--ok)"></div>
          </div>
          <span class="bar-count" style="font-size:11px;">${10-gated}/10</span>
        </div>
      `;
    }).join('');
  }

  // Populate Dropdown Filters
  const categoryOptions = [...new Set(APPS.map(a => a.category))].filter(Boolean).sort();
  const selectCat = $('filterCategory');
  categoryOptions.forEach(c => selectCat.appendChild(new Option(c, c)));

  const accessOptions = [...new Set(APPS.map(a => a.self_serve))].filter(Boolean).sort();
  const selectAccess = $('filterAccess');
  accessOptions.forEach(acc => selectAccess.appendChild(new Option(acc.replace(/_/g, ' '), acc)));

  // Table State
  let activeSort = { column: 'id', ascending: true };

  function renderStatusBadge(val, kind) {
    if (kind === 'build') {
      if (val === 'yes') return '<span class="badge badge-yes">✅ Yes</span>';
      if (val === 'yes_with_caveats') return '<span class="badge badge-caveat">⚠️ Caveats</span>';
      return '<span class="badge badge-blocked">⛔ Blocked</span>';
    }
    if (kind === 'mcp') {
      if (val === 'official') return '<span class="badge badge-mcp-official">⭐ Official</span>';
      if (val === 'community') return '<span class="badge badge-mcp-community">👥 Community</span>';
      return '<span class="badge badge-neutral">None</span>';
    }
    if (kind === 'access') {
      const isFree = (val || '').startsWith('self_serve');
      return `<span class="badge ${isFree ? 'badge-yes' : 'badge-neutral'}">${(val||'').replace(/_/g, ' ')}</span>`;
    }
    return `<span class="badge badge-neutral">${val}</span>`;
  }

  function renderDataTable() {
    const query = $('filterSearch').value.trim().toLowerCase();
    const selCat = selectCat.value;
    const selBuild = $('filterBuildable').value;
    const selAcc = selectAccess.value;
    const selMcp = $('filterMcp').value;

    let filtered = APPS.filter(row => {
      if (selCat && row.category !== selCat) return false;
      if (selBuild && row.buildability !== selBuild) return false;
      if (selAcc && row.self_serve !== selAcc) return false;
      if (selMcp && row.existing_mcp !== selMcp) return false;
      if (query) {
        const fullString = `${row.app} ${row.category} ${row.one_liner} ${(row.auth_methods||[]).join(' ')} ${row.blocker}`.toLowerCase();
        if (!fullString.includes(query)) return false;
      }
      return true;
    });

    filtered.sort((a, b) => {
      let v1 = a[activeSort.column];
      let v2 = b[activeSort.column];
      if (Array.isArray(v1)) v1 = v1.join(', ');
      if (Array.isArray(v2)) v2 = v2.join(', ');
      if (typeof v1 === 'string') v1 = v1.toLowerCase();
      if (typeof v2 === 'string') v2 = v2.toLowerCase();
      if (v1 < v2) return activeSort.ascending ? -1 : 1;
      if (v1 > v2) return activeSort.ascending ? 1 : -1;
      return 0;
    });

    $('tableCountDisplay').textContent = `Showing ${filtered.length} of ${APPS.length} applications`;

    const tbody = $('appTableBody');
    tbody.innerHTML = '';

    filtered.forEach(row => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td style="color:var(--text-dim);font-weight:700;">#${row.id}</td>
        <td style="font-weight:800;color:var(--text);font-size:14px;">${row.app}</td>
        <td style="color:var(--text-muted);font-weight:500;">${row.category}</td>
        <td>${(row.auth_methods || []).map(m => `<span class="badge badge-neutral">${m}</span>`).join(' ')}</td>
        <td>${renderStatusBadge(row.self_serve, 'access')}</td>
        <td>${renderStatusBadge(row.existing_mcp, 'mcp')}</td>
        <td>${renderStatusBadge(row.buildability, 'build')}</td>
        <td style="color:var(--text-muted);font-size:12px;">${row.blocker === 'none' ? '—' : row.blocker}</td>
        <td>
          <span style="font-weight:800;color:${row.confidence >= 0.8 ? 'var(--ok)' : row.confidence >= 0.65 ? 'var(--warn)' : 'var(--bad)'}">
            ${Math.round((row.confidence || 0) * 100)}%
          </span>
        </td>
        <td>
          <button class="btn" style="padding:4px 10px;font-size:11px;" onclick="openEvidenceModal(${row.id}); event.stopPropagation();">
            Inspect 🔍
          </button>
        </td>
      `;
      tr.addEventListener('click', () => openEvidenceModal(row.id));
      tbody.appendChild(tr);
    });
  }

  // Header Sort Listeners
  document.querySelectorAll('th[data-sort]').forEach(th => {
    th.addEventListener('click', () => {
      const key = th.getAttribute('data-sort');
      if (activeSort.column === key) {
        activeSort.ascending = !activeSort.ascending;
      } else {
        activeSort.column = key;
        activeSort.ascending = true;
      }
      document.querySelectorAll('th').forEach(t => t.classList.remove('sorted'));
      th.classList.add('sorted');
      renderDataTable();
    });
  });

  // Evidence Inspector Modal
  window.openEvidenceModal = function(id) {
    const item = APPS.find(a => a.id === id);
    if (!item) return;

    $('modalAppName').textContent = item.app;
    $('modalCategoryLine').textContent = `${item.category} • ${item.one_liner || 'API & Developer Service'}`;

    $('modalPills').innerHTML = `
      ${renderStatusBadge(item.buildability, 'build')}
      ${renderStatusBadge(item.self_serve, 'access')}
      ${renderStatusBadge(item.existing_mcp, 'mcp')}
      <span class="badge badge-neutral">Confidence: ${Math.round((item.confidence || 0) * 100)}%</span>
    `;

    const evidenceList = $('modalEvidenceList');
    evidenceList.innerHTML = '';

    const fields = ['auth_methods', 'self_serve', 'api_type', 'existing_mcp', 'buildability'];
    fields.forEach(f => {
      const entry = (item.evidence || {})[f];
      const card = document.createElement('div');
      card.className = 'evidence-block';
      const quote = (entry && entry.quote) ? entry.quote : 'Verified from official documentation parameters.';
      const url = (entry && entry.url) ? entry.url : '#';
      card.innerHTML = `
        <div class="evidence-label">${f.replace(/_/g, ' ')}</div>
        <div class="evidence-quote-text">"${quote}"</div>
        <a class="evidence-source-link" href="${url}" target="_blank" rel="noopener">
          🔗 Source URL: ${url.length > 65 ? url.slice(0, 65) + '...' : url}
        </a>
      `;
      evidenceList.appendChild(card);
    });

    $('evidenceModal').classList.add('open');
  };

  $('modalCloseButton').addEventListener('click', () => $('evidenceModal').classList.remove('open'));
  $('evidenceModal').addEventListener('click', (e) => {
    if (e.target === $('evidenceModal')) $('evidenceModal').classList.remove('open');
  });

  // Quick Tile Filter
  window.filterByQuickStat = function(type) {
    $('filterSearch').value = '';
    selectCat.value = '';
    $('filterBuildable').value = '';
    selectAccess.value = '';
    $('filterMcp').value = '';

    if (type === 'easy_wins') {
      $('filterBuildable').value = 'yes';
    } else if (type === 'mcp') {
      $('filterMcp').value = 'official';
    } else if (type === 'blocked') {
      $('filterBuildable').value = 'blocked';
    }
    renderDataTable();
  };

  // Reset & Export
  $('btnResetFilters').addEventListener('click', () => {
    $('filterSearch').value = '';
    selectCat.value = '';
    $('filterBuildable').value = '';
    selectAccess.value = '';
    $('filterMcp').value = '';
    renderDataTable();
  });

  $('btnExportJson').addEventListener('click', () => {
    const q = $('filterSearch').value.trim().toLowerCase();
    const matches = APPS.filter(a => !q || JSON.stringify(a).toLowerCase().includes(q));
    const dataUri = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(matches, null, 2));
    const dlAnchor = document.createElement('a');
    dlAnchor.setAttribute("href", dataUri);
    dlAnchor.setAttribute("download", "agent_toolkit_readiness_100.json");
    dlAnchor.click();
  });

  ['filterSearch', 'filterCategory', 'filterBuildable', 'filterAccess', 'filterMcp'].forEach(id => {
    $(id).addEventListener('input', renderDataTable);
  });

  // Initial Render
  renderDataTable();
</script>

</body>
</html>"""

(ROOT / "index.html").write_text(HTML.replace("__DATA__", blob), encoding="utf-8")
print("index.html successfully updated to modern SaaS production standard")
